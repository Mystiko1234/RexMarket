import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Mensaje, Producto
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtenemos el producto que se usa para la conversación
        self.producto_id = self.scope['url_route']['kwargs']['producto_id']
        self.room_name = f'chat_{self.producto_id}'
        self.room_group_name = f'chat_{self.producto_id}'

        # Unirse al grupo de chat
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Aceptar la conexión WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de chat
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
    # Parsear el mensaje recibido
        text_data_json = json.loads(text_data)
        contenido = text_data_json['contenido']
        remitente_username = text_data_json['remitente']
    
    # Obtener el remitente y receptor
        remitente = await self.get_user_by_username(remitente_username)
        producto = await self.get_producto_by_id(self.producto_id)
    
    # Crear el mensaje en la base de datos
        receptor = producto.vendedor if remitente != producto.vendedor else producto.vendedor  # Aquí podrías tener un error, ya que debes asegurarte de obtener al "otro" usuario
        mensaje = await self.create_message(remitente, receptor, producto, contenido)

    # Enviar el mensaje a todos los usuarios conectados al grupo de chat
        await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'chat_message',
            'contenido': mensaje.contenido,
            'remitente': remitente.username,
            'fecha_envio': str(mensaje.fecha_envio),
        }
    )


    async def chat_message(self, event):
        # Recibir el mensaje del grupo y enviarlo a WebSocket
        contenido = event['contenido']
        remitente = event['remitente']
        fecha_envio = event['fecha_envio']

        # Enviar mensaje a WebSocket
        await self.send(text_data=json.dumps({
            'contenido': contenido,
            'remitente': remitente,
            'fecha_envio': fecha_envio,
        }))

    # Métodos auxiliares para obtener objetos de la base de datos
    @sync_to_async
    def get_user_by_username(self, username):
        return User.objects.get(username=username)

    @sync_to_async
    def get_producto_by_id(self, producto_id):
        return Producto.objects.get(id=producto_id)

    @sync_to_async
    def create_message(self, remitente, receptor, producto, contenido):
        return Mensaje.objects.create(remitente=remitente, receptor=receptor, producto=producto, contenido=contenido)

