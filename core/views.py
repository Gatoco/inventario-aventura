from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from experiencias.models import Categoria, Experiencia, Inscripcion


def landing(request):
    experiencias = Experiencia.objects.filter(estado=True, categoria__estado=True).select_related('categoria')
    return render(request, 'core/landing.html', {'experiencias': experiencias})


@login_required
def dashboard(request):
    rol = request.user.perfil.rol
    if rol == 'admin':
        datos = {'Categorías': Categoria.objects.count(), 'Experiencias': Experiencia.objects.count(),
                 'Reservas': Inscripcion.objects.count()}
    elif rol == 'guia':
        datos = {'Mis experiencias': Experiencia.objects.filter(creador=request.user).count(),
                 'Inscritos en mis rutas': Inscripcion.objects.filter(experiencia__creador=request.user).count()}
    else:
        datos = {'Mis reservas': request.user.inscripciones.count()}
    return render(request, 'core/dashboard.html', {'datos': datos})
