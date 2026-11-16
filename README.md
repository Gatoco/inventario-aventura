# inventarioAventura — Ecoparque «Aventuras del Sur»

Sistema de administración y reservas de experiencias al aire libre, hecho en Django
con MySQL. Permite gestionar el catálogo de actividades, las inscripciones de los
visitantes y el acceso según el rol de cada usuario.

**Repositorio:** https://github.com/Gatoco/inventario-aventura

## Qué hay que instalar

```
Django>=5.2,<5.3
PyMySQL>=1.1
```

## Cómo levantarlo

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# La base de datos tiene que estar corriendo en localhost:3306
mysql -u root < backup_inventarioAventura.sql

python manage.py runserver
```

Si prefieres no usar el respaldo `.sql`, crea la base `inventario_aventura_db` a mano
y después corre:

```bash
python manage.py migrate
python manage.py seed_demo
```

## Credenciales de prueba

La clave es la misma para todos: `Aventura2026!`

| Rol | Usuario | Qué puede hacer |
|---|---|---|
| Administrador | `admin` | Todo: usuarios, categorías, experiencias y todas las reservas |
| Guía / Operador | `guia1` | Solo sus 4 experiencias. Puede crear, ver y editar. No elimina |
| Guía / Operador | `guia2` | Solo sus 4 experiencias. Mismo alcance |
| Turista | `turista1` | Ve el catálogo activo y tiene 3 inscripciones |
| Turista | `turista2` | Ve el catálogo activo y tiene 3 inscripciones |

## Estructura

El proyecto principal es `inventarioAventura`. Adentro hay tres apps:

- `core` — la landing pública y las vistas generales
- `cuentas` — usuarios, perfiles con rol, autenticación y sesiones
- `experiencias` — categorías, experiencias, inscripciones y el comando `seed_demo`

Los modelos son cuatro: `Perfil` (extiende el User de Django con el rol),
`Categoria`, `Experiencia` e `Inscripcion`. Todos están registrados en el admin y las
migraciones están incluidas en el repositorio.

## Un par de detalles de comportamiento

Las categorías solo las maneja el administrador. Si se intenta borrar una que todavía
tiene experiencias asociadas, el sistema lo impide y avisa.

Un guía que escribe a mano la URL de una experiencia que no es suya recibe un 404,
porque el queryset está filtrado por `creador=request.user`.

Un administrador tampoco puede eliminarse a sí mismo.

## Pruebas

```bash
python manage.py test
```
