# inventarioAventura

Sistema de administración y reservas para el ecoparque "Aventuras del Sur", hecho en
Django con MySQL para el ramo de Programación Back End.

Maneja el catálogo de experiencias (trekking, canopy, kayak, arriendo de equipos), las
inscripciones de los turistas y el acceso según el rol de cada uno.

El repositorio está en https://github.com/Gatoco/inventario-aventura

## Instalación

Hace falta Django 5.2 y PyMySQL, los dos están en requirements.txt:

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Después hay que tener MySQL o MariaDB corriendo en localhost:3306 y cargar el respaldo:

    mysql -u root < backup_inventarioAventura.sql

Si prefieres partir de cero, crea la base inventario_aventura_db a mano y corre:

    python manage.py migrate
    python manage.py seed_demo

Ese comando deja los usuarios y los datos de prueba listos, y se puede correr las veces
que quieras sin que se duplique nada.

Para levantar el sitio:

    python manage.py runserver

## Usuarios de prueba

La clave es la misma para todos, Aventura2026!

- admin es el administrador, el único que entra a usuarios y categorías
- guia1 y guia2 son guías, cada uno tiene sus 4 experiencias y solo ve esas
- turista1 y turista2 son turistas, cada uno con 3 reservas hechas

## Cómo está armado

El proyecto se llama inventarioAventura y adentro hay tres apps. core tiene la landing
pública y las vistas generales. cuentas se encarga de los usuarios, los perfiles con rol
y las sesiones. experiencias tiene las categorías, las experiencias, las inscripciones y
el comando seed_demo.

Los modelos son Perfil, que extiende el User de Django con el rol, Categoria, Experiencia
e Inscripcion. Todos están registrados en el admin y las migraciones van incluidas en el
repositorio.

## Un par de cosas que hace

Las categorías las maneja solo el administrador. Si intenta borrar una que todavía tiene
experiencias asociadas, el sistema no lo deja y le avisa.

Si un guía escribe a mano la URL de una experiencia que no es suya, le sale un 404,
porque el queryset está filtrado por creador=request.user.

Un administrador tampoco se puede eliminar a sí mismo, y la fecha de una experiencia
tiene que ser futura para poder guardarla.

## Pruebas

    python manage.py test
