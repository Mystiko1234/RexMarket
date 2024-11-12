from django import forms
from usuariosApp.models import Producto, Mensaje
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'categoria']

    imagen = forms.ImageField(required=True)
    categoria = forms.ChoiceField(
        choices=Producto.CATEGORIAS,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    precio = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio en CLP'}),
        validators=[
            RegexValidator(r'^\d{1,3}(?:[.,]\d{3})*(?:,\d+)?$', 'El precio debe ser un número válido.')
        ]
    )


class MessageForm(forms.Form):
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu mensaje...'}))


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'