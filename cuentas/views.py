from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from .decorators import rol_requerido
from .forms import MiPerfilForm, UsuarioCrearForm, UsuarioEditarForm


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@rol_requerido('admin')
def lista_usuarios(request):
    usuarios = User.objects.select_related('perfil').order_by('username')
    return render(request, 'cuentas/usuarios_lista.html', {'usuarios': usuarios})


@rol_requerido('admin')
def crear_usuario(request):
    form = UsuarioCrearForm()
    if request.method == 'POST':
        form = UsuarioCrearForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    return render(request, 'form.html', {'form': form, 'titulo': 'Nuevo usuario', 'volver': 'lista_usuarios'})


@rol_requerido('admin')
def editar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    form = UsuarioEditarForm(instance=usuario)
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    return render(request, 'form.html', {'form': form, 'titulo': 'Editar usuario', 'volver': 'lista_usuarios'})


@rol_requerido('admin')
@require_POST
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
    else:
        usuario.delete()
    return redirect('lista_usuarios')


@login_required
def mi_perfil(request):
    perfil = request.user.perfil
    form = MiPerfilForm(instance=perfil)
    if request.method == 'POST':
        form = MiPerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado.')
            return redirect('mi_perfil')
    return render(request, 'form.html', {'form': form, 'titulo': 'Mi perfil', 'volver': 'dashboard'})
