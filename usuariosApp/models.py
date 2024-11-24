from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings




class Producto(models.Model):
    CATEGORIAS = [
    ('Comida y Bebidas', 'Comida y Bebidas'),      
    ('POSTRES', 'Postres y Dulces'),            
    ('TECNOLOGIA', 'Tecnología y accesorios'),    
    ('ROPA', 'Ropa y Moda'),                     
    ('ACCESORIOS', 'Accesorios'),                
    ('LIBROS_PAPELERIA', 'Libros y Papelería'),  
    ('MANUALIDADES', 'Manualidades'),           
    ('SERVICIOS', 'Servicios'),                  
    ('HOGAR', 'Hogar y Decoración'),           
    ('ENTRETENIMIENTO', 'Juegos y Entretenimiento'),  
    ('DEPORTES', 'Deportes y Fitness'),          
    ('OTROS', 'Otros'),                          
]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.CharField(max_length=20) 
    imagen = models.ImageField(upload_to='productos/')
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos')
    categoria = models.CharField(max_length=30, choices=CATEGORIAS, default='OTROS')
    destacado_hasta = models.DateTimeField(null=True, blank=True)  

    def __str__(self):
        return self.nombre
    
    def es_destacado(self):
        return self.destacado_hasta and self.destacado_hasta > now()

    

class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=36, default=uuid.uuid4)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Verificado' if self.is_verified else 'No verificado'}"
    


class Comentario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    valoracion = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.producto.nombre}'
    