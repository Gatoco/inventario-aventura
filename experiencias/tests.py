from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import CategoriaForm, ExperienciaForm
from .models import Categoria, Experiencia, Inscripcion


def crear(username, rol):
    u = User.objects.create_user(username, password='x')
    u.perfil.rol = rol
    u.perfil.save()
    return u


class PermisosTest(TestCase):
    def setUp(self):
        self.admin = crear('admin1', 'admin')
        self.g1, self.g2 = crear('g1', 'guia'), crear('g2', 'guia')
        self.t1, self.t2 = crear('t1', 'turista'), crear('t2', 'turista')
        self.cat = Categoria.objects.create(nombre='Trekking')
        kw = dict(descripcion='d', precio=1000, cupo_maximo=1, fecha_hora=timezone.now() + timedelta(days=1),
                  categoria=self.cat)
        self.e1 = Experiencia.objects.create(titulo='E1', creador=self.g1, **kw)
        self.e2 = Experiencia.objects.create(titulo='E2', creador=self.g2, **kw)

    def test_signup_crea_turista(self):
        self.client.post(reverse('signup'), {'username': 'nuevo', 'password1': 'Clave-Segura-99',
                                             'password2': 'Clave-Segura-99'})
        self.assertEqual(User.objects.get(username='nuevo').perfil.rol, 'turista')

    def test_guia_solo_ve_y_edita_lo_suyo(self):
        self.client.login(username='g1', password='x')
        r = self.client.get(reverse('lista_experiencias'))
        self.assertContains(r, 'E1'); self.assertNotContains(r, 'E2')
        self.assertEqual(self.client.get(reverse('editar_experiencia', args=[self.e2.id])).status_code, 404)

    def test_guia_no_elimina_ni_ve_categorias(self):
        self.client.login(username='g1', password='x')
        self.client.post(reverse('eliminar_experiencia', args=[self.e1.id]))
        self.assertTrue(Experiencia.objects.filter(id=self.e1.id).exists())
        self.assertRedirects(self.client.get(reverse('lista_categorias')), reverse('dashboard'))

    def test_turista_no_entra_a_crud(self):
        self.client.login(username='t1', password='x')
        self.assertRedirects(self.client.get(reverse('lista_experiencias')), reverse('dashboard'))

    def test_admin_elimina(self):
        self.client.login(username='admin1', password='x')
        self.client.post(reverse('eliminar_experiencia', args=[self.e1.id]))
        self.assertFalse(Experiencia.objects.filter(id=self.e1.id).exists())

    def test_borrado_requiere_post(self):
        self.client.login(username='admin1', password='x')
        r = self.client.get(reverse('eliminar_experiencia', args=[self.e1.id]))
        self.assertEqual(r.status_code, 405)
        self.assertTrue(Experiencia.objects.filter(id=self.e1.id).exists())

    def test_inscripcion_cupo_y_duplicado(self):
        self.client.login(username='t1', password='x')
        self.client.post(reverse('inscribirse', args=[self.e1.id]))
        self.client.post(reverse('inscribirse', args=[self.e1.id]))  # se inscribe dos veces, no deberia crear otra
        self.assertEqual(Inscripcion.objects.count(), 1)
        self.client.logout(); self.client.login(username='t2', password='x')
        self.client.post(reverse('inscribirse', args=[self.e1.id]))  # el cupo es 1 y ya esta lleno
        self.assertEqual(Inscripcion.objects.count(), 1)

    def test_confirmar_pago_ajeno_denegado(self):
        ins = Inscripcion.objects.create(usuario=self.t1, experiencia=self.e1)
        self.client.login(username='t2', password='x')
        self.client.post(reverse('confirmar_pago', args=[ins.id]))
        ins.refresh_from_db(); self.assertEqual(ins.estado_pago, 'pendiente')
        self.client.logout(); self.client.login(username='t1', password='x')
        self.client.post(reverse('confirmar_pago', args=[ins.id]))
        ins.refresh_from_db(); self.assertEqual(ins.estado_pago, 'confirmado')


class FormulariosTest(TestCase):
    """lo que no deberia poder guardarse desde los formularios del panel"""

    def setUp(self):
        self.cat = Categoria.objects.create(nombre='Trekking')
        self.datos = dict(titulo='E1', descripcion='d', precio=1000, cupo_maximo=2,
                          fecha_hora=(timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
                          categoria=self.cat.id, estado=True)

    def test_fecha_en_el_pasado_no_pasa(self):
        self.datos['fecha_hora'] = (timezone.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        self.assertFalse(ExperienciaForm(self.datos).is_valid())

    def test_precio_en_cero_no_pasa(self):
        self.datos['precio'] = 0
        self.assertFalse(ExperienciaForm(self.datos).is_valid())

    def test_cupo_menor_a_los_ya_inscritos_no_pasa(self):
        e = ExperienciaForm(self.datos).save(commit=False)
        e.creador = crear('g9', 'guia')
        e.save()
        Inscripcion.objects.create(usuario=crear('t9', 'turista'), experiencia=e)
        self.datos['cupo_maximo'] = 0
        self.assertFalse(ExperienciaForm(self.datos, instance=e).is_valid())

    def test_categoria_repetida_no_pasa(self):
        self.assertFalse(CategoriaForm({'nombre': 'trekking', 'estado': True}).is_valid())
        self.assertTrue(CategoriaForm({'nombre': 'Kayak', 'estado': True}).is_valid())
