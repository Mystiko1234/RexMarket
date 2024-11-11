from django import forms
from usuariosApp.models import Producto
from usuariosApp.models import Mensaje

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen']

        imagen = forms.ImageField(required=True)

class MessageForm(forms.Form):
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escribe tu mensaje...'}))


class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']