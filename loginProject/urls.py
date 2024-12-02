"""
URL configuration for loginProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from tkinter.font import names

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from usuariosApp.views import publicar_producto, lista_productos,editar_producto, eliminar_producto, detalle_producto,VerifyEmailView, destacar_producto, toggle_favorito, eliminar_comentario, inbox, send_message, conversation_detail, start_conversation, conversations_list, get_conversation_messages, ProfileView
from usuariosApp.views import SignUpView
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # Todas las urls de autenticación
    path("", lista_productos, name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("publicar/", publicar_producto, name='publicar_producto'),
    path('editar/<int:pk>/', editar_producto, name='editar_producto'),  # Ruta para editar producto
    path('eliminar/<int:pk>/', eliminar_producto, name='eliminar_producto'),  # Ruta para eliminar producto
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('destacar/<int:producto_id>/', destacar_producto, name='destacar_producto'),
    path('toggle-favorito/', toggle_favorito, name='toggle_favorito'),
    path('comentarios/eliminar/<int:comentario_id>/', eliminar_comentario, name='eliminar_comentario'),
    path('inbox/', inbox, name='inbox'),
    path('conversations/<int:conversation_id>/', conversation_detail, name='conversation_detail'),
    path('start-conversation/<int:recipient_id>/', start_conversation, name='start_conversation'),
    path('conversations/<int:conversation_id>/messages/send/', send_message, name='send_message'),
    path('conversations/', conversations_list, name='conversations_list'),
    path('conversations/<int:conversation_id>/messages/', get_conversation_messages, name='get_conversation_messages'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
