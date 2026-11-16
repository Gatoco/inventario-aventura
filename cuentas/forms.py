from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import ROLES, Perfil


class UsuarioCrearForm(UserCreationForm):
    rol = forms.ChoiceField(choices=ROLES, widget=forms.Select(attrs={'class': 'form-control'}))
    telefono = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs.setdefault('class', 'form-control')

    def save(self, commit=True):
        usuario = super().save(commit)
        if commit:
            Perfil.objects.filter(usuario=usuario).update(
                rol=self.cleaned_data['rol'], telefono=self.cleaned_data['telefono'])
        return usuario


class UsuarioEditarForm(forms.ModelForm):
    rol = forms.ChoiceField(choices=ROLES, widget=forms.Select(attrs={'class': 'form-control'}))
    telefono = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['rol'].initial = self.instance.perfil.rol
            self.fields['telefono'].initial = self.instance.perfil.telefono

    def save(self, commit=True):
        usuario = super().save(commit)
        if commit:
            Perfil.objects.filter(usuario=usuario).update(
                rol=self.cleaned_data['rol'], telefono=self.cleaned_data['telefono'])
        return usuario


class MiPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('telefono',)
        widgets = {'telefono': forms.TextInput(attrs={'class': 'form-control'})}
