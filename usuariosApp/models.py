from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return self.nombre

class Mensaje(models.Model):
    remitente = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensajes_enviados")
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mensajes_recibidos")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)  # Campo para marcar si el mensaje ha sido leído

    def __str__(self):
        return f"Mensaje de {self.remitente.username} para {self.receptor.username} sobre {self.producto.nombre}"