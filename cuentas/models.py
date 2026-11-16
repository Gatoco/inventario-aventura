from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

ROLES = [
    ('admin', 'Administrador'),
    ('guia', 'Guía / Operador'),
    ('turista', 'Turista / Cliente'),
]


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='turista')
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.usuario.username} ({self.get_rol_display()})"


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    # todo usuario nuevo entra como turista, salvo el superusuario que ya nace admin
    if created:
        Perfil.objects.create(usuario=instance, rol='admin' if instance.is_superuser else 'turista')
