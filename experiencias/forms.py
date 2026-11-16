from django import forms
from django.utils import timezone

from .models import Categoria, Experiencia


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        # no me sirve tener la misma categoria dos veces, despues no se cual es cual
        repetida = Categoria.objects.filter(nombre__iexact=nombre).exclude(pk=self.instance.pk)
        if repetida.exists():
            raise forms.ValidationError('Ya existe una categoria con ese nombre.')
        return nombre


class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        exclude = ('creador',)  # el creador lo pone la vista, no el formulario
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'cupo_maximo': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_hora': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(estado=True)
        self.fields['fecha_hora'].input_formats = ['%Y-%m-%dT%H:%M']

    def clean_fecha_hora(self):
        fecha = self.cleaned_data['fecha_hora']
        # no tiene sentido ofrecer una salida que ya paso
        if fecha <= timezone.now():
            raise forms.ValidationError('La fecha y hora tienen que ser futuras.')
        return fecha

    def clean(self):
        datos = super().clean()
        precio, cupo = datos.get('precio'), datos.get('cupo_maximo')
        if precio is not None and precio < 1:
            self.add_error('precio', 'El precio tiene que ser mayor que cero.')
        # al editar, el cupo no puede quedar por debajo de la gente que ya se inscribio
        inscritos = self.instance.inscripciones.count() if self.instance.pk else 0
        if cupo is not None and cupo < inscritos:
            self.add_error('cupo_maximo', f'Ya hay {inscritos} inscritos, el cupo no puede ser menor.')
        return datos
