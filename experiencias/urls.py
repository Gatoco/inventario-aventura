from django.urls import path

from . import views

urlpatterns = [
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('experiencias/', views.lista_experiencias, name='lista_experiencias'),
    path('experiencias/nueva/', views.crear_experiencia, name='crear_experiencia'),
    path('experiencias/editar/<int:id>/', views.editar_experiencia, name='editar_experiencia'),
    path('experiencias/eliminar/<int:id>/', views.eliminar_experiencia, name='eliminar_experiencia'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('inscribirse/<int:id>/', views.inscribirse, name='inscribirse'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('reservas/', views.reservas, name='reservas'),
    path('reservas/confirmar/<int:id>/', views.confirmar_pago, name='confirmar_pago'),
]
