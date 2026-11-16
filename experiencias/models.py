from django.contrib.auth.models import User
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)  # apagada no sale en el catalogo ni se puede reservar

    def __str__(self):
        return self.nombre


class Experiencia(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    cupo_maximo = models.PositiveIntegerField()
    fecha_hora = models.DateTimeField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='experiencias')
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiencias_creadas')
    estado = models.BooleanField(default=True)  # si la apago desaparece del catalogo publico

    def cupos_disponibles(self):
        return self.cupo_maximo - self.inscripciones.count()

    def __str__(self):
        return self.titulo


class Inscripcion(models.Model):
    ESTADOS_PAGO = [('pendiente', 'Pendiente'), ('confirmado', 'Confirmado')]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')

    class Meta:
        unique_together = ('usuario', 'experiencia')

    def __str__(self):
        return f"{self.usuario.username} → {self.experiencia}"
