from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy
from django.contrib.auth import login
from usuariosApp.models import Producto
from usuariosApp.forms import ProductoForm, MessageForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Producto
from django.core.paginator import Paginator

# Create your views here.

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


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
    productos = Producto.objects.all()
    paginator = Paginator(productos, 21)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page_obj': page_obj,
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
    
    # Si el formulario es enviado para enviar un mensaje
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Obtén los datos del formulario
            mensaje = form.cleaned_data['mensaje']
            vendedor_email = producto.user.email  # Asumiendo que 'user' es el dueño del producto
            
            # Enviar el mensaje al vendedor
            send_mail(
                f'Mensaje sobre el producto {producto.nombre}',
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [vendedor_email]
            )
            # Redirigir o mostrar un mensaje de éxito
            return redirect('detalle_producto', producto_id=producto.id)
    else:
        form = MessageForm()

    return render(request, 'detalle_producto.html', {'producto': producto, 'form': form})

def mensajeria(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    return render(request, 'mensajeria.html', {'producto_id': producto.id, 'producto': producto})
