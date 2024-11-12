from django.db import models
from django.contrib.auth.models import User


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
    
