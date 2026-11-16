from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def rol_requerido(*roles):
    """deja pasar solo al que tenga uno de esos roles en su perfil, el resto vuelve al panel"""
    def decorador(vista):
        @login_required
        @wraps(vista)
        def envoltura(request, *args, **kwargs):
            if request.user.perfil.rol in roles:
                return vista(request, *args, **kwargs)
            messages.error(request, 'No tienes permiso para acceder a esa sección.')
            return redirect('dashboard')
        return envoltura
    return decorador
