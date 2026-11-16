from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from experiencias.models import Categoria, Experiencia, Inscripcion

PASSWORD = 'Aventura2026!'


def usuario(username, rol, **extra):
    u, creado = User.objects.get_or_create(username=username, defaults=extra)
    if creado:
        u.set_password(PASSWORD)
        u.save()
    u.perfil.rol = rol
    u.perfil.save()
    return u


class Command(BaseCommand):
    help = 'carga los datos de prueba, se puede correr las veces que quieras sin duplicar nada'

    def handle(self, *args, **options):
        admin = usuario('admin', 'admin', is_staff=True, is_superuser=True, email='admin@aventuras.cl')
        guias = [usuario(f'guia{i}', 'guia', first_name=f'Guía{i}', email=f'guia{i}@aventuras.cl') for i in (1, 2)]
        turistas = [usuario(f'turista{i}', 'turista', first_name=f'Turista{i}', email=f'turista{i}@aventuras.cl')
                    for i in (1, 2)]
        cats = {n: Categoria.objects.get_or_create(nombre=n, defaults={'descripcion': d})[0] for n, d in [
            ('Trekking', 'Caminatas guiadas por senderos del parque'),
            ('Canopy', 'Tirolesa entre árboles nativos'),
            ('Kayak', 'Navegación en kayak por el lago'),
            ('Arriendo de equipos', 'Arriendo de equipo outdoor'),
        ]}
        base = timezone.now() + timedelta(days=7)
        experiencias = []
        for gi, guia in enumerate(guias):
            for n, (cat, titulo, precio) in enumerate([
                ('Trekking', 'Sendero Bosque Valdiviano', 15000),
                ('Canopy', 'Circuito Canopy Alto', 28000),
                ('Kayak', 'Kayak al Atardecer', 22000),
                ('Arriendo de equipos', 'Pack Camping 2 Días', 18000),
            ]):
                e, _ = Experiencia.objects.get_or_create(
                    titulo=f'{titulo} ({guia.username})', creador=guia,
                    defaults={'descripcion': f'{titulo}, a cargo de {guia.username}.', 'precio': precio,
                              'cupo_maximo': 10, 'fecha_hora': base + timedelta(days=gi * 4 + n),
                              'categoria': cats[cat]})
                experiencias.append(e)
        for ti, turista in enumerate(turistas):
            for n in range(3):
                Inscripcion.objects.get_or_create(
                    usuario=turista, experiencia=experiencias[ti * 3 + n],
                    defaults={'estado_pago': 'confirmado' if n % 2 == 0 else 'pendiente'})
        self.stdout.write(self.style.SUCCESS(f'Seed OK. Usuarios: admin, guia1-2, turista1-2 · clave: {PASSWORD}'))
