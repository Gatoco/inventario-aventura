from django.contrib import admin
from .models import Categoria, Experiencia, Inscripcion


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado')
    search_fields = ('nombre',)


@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'creador', 'precio', 'cupo_maximo', 'fecha_hora', 'estado')
    list_filter = ('categoria', 'estado')
    search_fields = ('titulo',)


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'experiencia', 'fecha_inscripcion', 'estado_pago')
    list_filter = ('estado_pago',)
