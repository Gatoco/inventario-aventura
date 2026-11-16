# inventarioAventura — Ecoparque «Aventuras del Sur»

Django + MySQL (PyMySQL) + SB Admin 2. Apps: `core`, `cuentas`, `experiencias`.

## Credenciales de prueba (clave de todos: `Aventura2026!`)
| Rol | Usuario |
|---|---|
| Administrador | `admin` |
| Guía / Operador | `guia1`, `guia2` (4 experiencias c/u) |
| Turista | `turista1`, `turista2` (3 inscripciones c/u) |

## Arranque
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# MySQL/MariaDB en localhost:3306, usuario root sin clave (ver settings.py)
mysql -uroot < backup_inventarioAventura.sql      # restaura BD con datos
python manage.py runserver
```
Alternativa sin el `.sql`: crear la BD `inventario_aventura_db`, luego `python manage.py migrate && python manage.py seed_demo`.

Pruebas: `python manage.py test`.
