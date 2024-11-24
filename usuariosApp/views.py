from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy
from django.contrib.auth import login, authenticate
from usuariosApp.models import Producto
from usuariosApp.forms import ProductoForm, ComentarioForm, CustomUserCreationForm 
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
import uuid
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.utils.timezone import now, timedelta
from django.db.models import Avg, F, Q
from django.http import JsonResponse



# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("verify_email")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # Guardar los datos del formulario en la sesión
        self.request.session['user_data'] = {
            'username': form.cleaned_data['username'],
            'password1': form.cleaned_data['password1'],
            'password2': form.cleaned_data['password2'],
            'email': form.cleaned_data['email'],
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
        }

        # Generar código de verificación
        verification_code = str(uuid.uuid4())[:6].strip()
        self.request.session['verification_code'] = verification_code.strip()

        # Enviar correo de verificación con el código
        send_mail(
            'Verifica tu correo - RexMarket',
            f'Hola {form.cleaned_data["first_name"]}, tu código de verificación es:{verification_code}\n\nPor favor ingresa este código para activar tu cuenta.',
            'rexmarket26@gmail.com',
            [form.cleaned_data['email']],
            fail_silently=False,
        )

        messages.success(self.request, 'Te hemos enviado un correo con el código de verificación.')
        return redirect(self.success_url)



@login_required
def publicar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()
            return redirect('home')
    else:
        form = ProductoForm()
    return render(request, 'publicar_producto.html', {'form': form})


def lista_productos(request):
    # Captura los parámetros de búsqueda y filtros
    query = request.GET.get('q', '').strip()
    categoria_seleccionada = request.GET.get('categoria', '')  # Captura la categoría seleccionada
    ordenar_por = request.GET.get('ordenar_por', '')  # Captura el orden seleccionado

    # Obtiene todos los productos
    productos = Producto.objects.annotate(
        destacado_valido=Q(destacado_hasta__gte=now())
    ).order_by(
        F('destacado_hasta').desc(nulls_last=True)
    )

    # Filtrar por búsqueda
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    # Filtrar por categoría
    if categoria_seleccionada:
        productos = productos.filter(categoria=categoria_seleccionada)

    # Ordenar productos
    if ordenar_por == 'precio_asc':
        productos = productos.order_by('precio')
    elif ordenar_por == 'precio_desc':
        productos = productos.order_by('-precio')
    elif ordenar_por == 'valoracion':
        productos = productos.annotate(
            valoracion_promedio=Avg('comentarios__valoracion')
        ).order_by('-valoracion_promedio')

    # Calcular promedio de valoraciones (si no está ordenado por ello)
    if ordenar_por != 'valoracion':
        for producto in productos:
            promedio = producto.comentarios.aggregate(promedio=Avg('valoracion'))['promedio']
            producto.valoracion_promedio = promedio if promedio is not None else 0

    # Paginación
    paginator = Paginator(productos, 21)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Obtener todas las categorías del modelo
    categorias = Producto.CATEGORIAS

    # Pasar los datos al contexto
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'query': query,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
        'ordenar_por': ordenar_por,
        'user': request.user
    })


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    # Verificar si el usuario tiene permiso para editar
    if producto.vendedor != request.user and not request.user.is_superuser:
        return redirect('home')  # Redirigir si no es el dueño o no es superusuario

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirigir después de guardar
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    # Verificar si el usuario tiene permiso para eliminar
    if producto.vendedor != request.user and not request.user.is_superuser:
        return redirect('home')  # Redirigir si no es el dueño o no es superusuario

    producto.delete()
    return redirect('home') 


def detalle_producto(request, producto_id):
    # Obtén el producto por ID
    producto = get_object_or_404(Producto, id=producto_id)

    # Formularios
    form_comentario = ComentarioForm()
    
    # Obtener los comentarios del producto
    comentarios = producto.comentarios.all()

    if request.method == 'POST' and 'comentario' in request.POST:
        if request.user.is_authenticated:
            form_comentario = ComentarioForm(request.POST)
            if form_comentario.is_valid():
                comentario = form_comentario.save(commit=False)
                comentario.usuario = request.user
                comentario.producto = producto
                comentario.save()
                messages.success(request, "Comentario añadido exitosamente")
                return redirect('detalle_producto', producto_id=producto.id)
        else:
            messages.error(request, "Debes iniciar sesión para dejar un comentario")

    context = {
        'producto': producto,
        'form_comentario': form_comentario,
        'comentarios': comentarios,
    }

    return render(request, 'detalle_producto.html', context)

def login_register_view(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()

    if request.method == "POST":
        if "login_submit" in request.POST:  # Formulario de inicio de sesión
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('home')  # Redirecciona al inicio
        elif "register_submit" in request.POST:  # Formulario de registro
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                user = authenticate(
                    username=register_form.cleaned_data['username'],
                    password=register_form.cleaned_data['password1']
                )
                if user:
                    login(request, user)
                    return redirect('home')

    return render(request, 'registration/login.html', {
        'login_form': login_form,
        'register_form': register_form
    })

class VerifyEmailView(View):
    def get(self, request):
        return render(request, 'registration/verify_email.html')

    def post(self, request):
        verification_code = request.POST.get('verification_code')
        session_code = request.session.get('verification_code')

        if verification_code == session_code:
            user_data = request.session.get('user_data')

            # Crear el usuario después de verificar el código
            user = User.objects.create_user(
                username=user_data['username'],
                password=user_data['password1'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            user.is_active = True  # Activar el usuario
            user.save()

            # Limpiar la sesión
            del request.session['user_data']
            del request.session['verification_code']

            messages.success(request, '¡Correo verificado exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')

        messages.error(request, 'El código de verificación no es válido. Intenta de nuevo.')
        return redirect('verify_email')
    
@login_required
def destacar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, vendedor=request.user)
    
    if request.method == 'POST':
        duracion = request.POST.get('duracion')  # 1, 7 o 14 días
        precios = {
            '1': 490,
            '7': 2990,
            '14': 4990
        }

        if duracion in precios:
            # Actualizar fecha de destacación
            dias = int(duracion)
            producto.destacado_hasta = now() + timedelta(days=dias)
            producto.save()
            messages.success(request, f'El producto {producto.nombre} ha sido destacado por {dias} días.')
        else:
            messages.error(request, 'Duración inválida.')

        return redirect('home')  # Redirige a la lista de productos

    return render(request, 'destacar.html', {'producto': producto})
