from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cuentas.decorators import rol_requerido

from .forms import CategoriaForm, ExperienciaForm
from .models import Categoria, Experiencia, Inscripcion


# categorias: esto es solo del admin
@rol_requerido('admin')
def lista_categorias(request):
    return render(request, 'experiencias/categorias_lista.html', {'categorias': Categoria.objects.all()})


@rol_requerido('admin')
def crear_categoria(request):
    form = CategoriaForm()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    return render(request, 'form.html', {'form': form, 'titulo': 'Nueva categoría', 'volver': 'lista_categorias'})


@rol_requerido('admin')
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(instance=categoria)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    return render(request, 'form.html', {'form': form, 'titulo': 'Editar categoría', 'volver': 'lista_categorias'})


@rol_requerido('admin')
@require_POST
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    try:
        categoria.delete()
    except ProtectedError:
        messages.error(request, 'No se puede eliminar: la categoría tiene experiencias asociadas.')
    return redirect('lista_categorias')


# experiencias: el admin ve todas, el guia solo las que creo el
def _experiencia_propia(request, id):
    """el admin entra a cualquiera, el guia solo a las suyas. si no es suya, 404 y listo"""
    if request.user.perfil.rol == 'admin':
        return get_object_or_404(Experiencia, id=id)
    return get_object_or_404(Experiencia, id=id, creador=request.user)


@rol_requerido('admin', 'guia')
def lista_experiencias(request):
    experiencias = Experiencia.objects.select_related('categoria', 'creador')
    if request.user.perfil.rol == 'guia':
        experiencias = experiencias.filter(creador=request.user)
    return render(request, 'experiencias/experiencias_lista.html', {'experiencias': experiencias})


@rol_requerido('admin', 'guia')
def crear_experiencia(request):
    form = ExperienciaForm()
    if request.method == 'POST':
        form = ExperienciaForm(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.creador = request.user
            experiencia.save()
            return redirect('lista_experiencias')
    return render(request, 'form.html', {'form': form, 'titulo': 'Nueva experiencia', 'volver': 'lista_experiencias'})


@rol_requerido('admin', 'guia')
def editar_experiencia(request, id):
    experiencia = _experiencia_propia(request, id)
    form = ExperienciaForm(instance=experiencia)
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            return redirect('lista_experiencias')
    return render(request, 'form.html', {'form': form, 'titulo': 'Editar experiencia', 'volver': 'lista_experiencias'})


@rol_requerido('admin')
@require_POST
def eliminar_experiencia(request, id):
    get_object_or_404(Experiencia, id=id).delete()
    return redirect('lista_experiencias')


# reservas
@rol_requerido('turista')
def catalogo(request):
    experiencias = Experiencia.objects.filter(estado=True, categoria__estado=True).select_related('categoria')
    mias = set(request.user.inscripciones.values_list('experiencia_id', flat=True))
    return render(request, 'experiencias/catalogo.html', {'experiencias': experiencias, 'mias': mias})


@rol_requerido('turista')
@require_POST
def inscribirse(request, id):
    experiencia = get_object_or_404(Experiencia, id=id, estado=True, categoria__estado=True)
    if experiencia.cupos_disponibles() <= 0:
        messages.error(request, 'No quedan cupos disponibles.')
    else:
        try:
            Inscripcion.objects.create(usuario=request.user, experiencia=experiencia)
            messages.success(request, f'Te inscribiste en «{experiencia.titulo}».')
        except IntegrityError:
            messages.warning(request, 'Ya estás inscrito en esta experiencia.')
    return redirect('mis_reservas')


@rol_requerido('turista')
def mis_reservas(request):
    reservas = request.user.inscripciones.select_related('experiencia')
    return render(request, 'experiencias/mis_reservas.html', {'reservas': reservas})


@rol_requerido('admin', 'guia')
def reservas(request):
    reservas = Inscripcion.objects.select_related('experiencia', 'usuario')
    if request.user.perfil.rol == 'guia':
        reservas = reservas.filter(experiencia__creador=request.user)
    return render(request, 'experiencias/reservas_lista.html', {'reservas': reservas})


@login_required
@require_POST
def confirmar_pago(request, id):
    reserva = get_object_or_404(Inscripcion, id=id)
    if request.user.perfil.rol != 'admin' and reserva.usuario != request.user:
        messages.error(request, 'No puedes modificar esta reserva.')
        return redirect('dashboard')
    reserva.estado_pago = 'confirmado'
    reserva.save()
    messages.success(request, 'Pago confirmado.')
    return redirect('reservas' if request.user.perfil.rol == 'admin' else 'mis_reservas')
