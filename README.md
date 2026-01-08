<img width="275" height="138" alt="DOLY_LOGO-bg_white-font_black-Corporative2" src="https://github.com/user-attachments/assets/491c22c5-f3ff-4623-96fd-4bb56cce10ba" />

# DOLY — Documentación del Proyecto

Última actualización: 2026-01-06

---

## Resumen ejecutivo

DOLY es una plataforma web para gestión de asistencia vial y administración de servicios relacionados con clientes, empresas y recursos (vehículos, equipos y operadores). Está construida como una aplicación monolítica en Flask con SQLAlchemy (PostgreSQL) y una capa de frontend basada en plantillas Jinja2, SCSS y JavaScript estático.

Este README ofrece una visión completa y accionable para desarrolladores, administradores y equipos de operaciones: arquitectura, guía de instalación y ejecución, estructura de carpetas, flujos principales, seguridad, despliegue y resolución de problemas.

---

## Contenido

- Resumen ejecutivo
- Arquitectura
- Componentes principales
- Requisitos
- Configuración local (desarrollo)
- Ejecución y pruebas
- Despliegue
- Estructura del proyecto (resumen)
- Base de datos y ERD
- Seguridad y buenas prácticas
- Logs, monitoreo y troubleshooting
- Contribución y estilo de código
- Contacto y licencia

---

## Arquitectura (alto nivel)

- Frontend: plantillas Jinja2 + CSS (SCSS compilado) + JS estático. El navegador consume recursos estáticos y las páginas renderizadas por Flask.
- Backend: Flask (factory pattern) con Blueprints (`views`, `auth`, etc.). Lógica de negocio en controladores y modelos SQLAlchemy.
- Persistencia: PostgreSQL (esquema definido en `app/utilities/Documentation/Database/ServiceDDL.sql`).
- Utilidades/Docs: `app/utilities/Documentation/` contiene DDL, DML y diagramas ERD.
- Infraestructura: despliegue por Heroku (Procfile presente) o similar; variables sensibles vía `.env`.

---

## Componentes principales

- `app/__init__.py`: fábrica de la app y registro de blueprints.
- `app/auth.py`: registro, login, logout y control de sesiones.
- `app/views.py` / `app/views_client.py`: rutas públicas y paneles.
- `app/database.py`: inicialización de `SQLAlchemy` y utilidades de conexión.
- `app/models/`: modelos por entidad (cada archivo define una entidad, todos con `db.Model` y `@dataclass`).
- `app/templates/`: plantillas Jinja2 agrupadas por sección (auth, landpage, client, admin).
- `app/static/`: assets compilados y JS.
- `app/utilities/Documentation/Database/`: DDL, DML y ERD (Mermaid) para referencia y migraciones manuales.

---

## Requisitos

- Python 3.10+ (entorno virtual recomendado)
- PostgreSQL (o servicio compatible: Neon, ElephantSQL, etc.)
- Node.js/npm (solo si vas a compilar SCSS o usar herramientas front-end)
- Dependencias Python: ver `requirements.txt`

Instalación rápida en Bash (Windows WSL o Linux/macOS):

```bash
# crear y activar venv
python -m venv venv
source venv/Scripts/activate   # Windows bash (adapta según shell)

# instalar dependencias
pip install -r requirements.txt
```

Asegúrate de definir variables de entorno en `.env` (ejemplo en `.env.example` si existe):

- `SECRET_KEY` — clave secreta Flask
- `DATABASE_URL` — URL SQLAlchemy (p.ej. postgresql+psycopg2://user:pass@host/dbname)

---

## Configuración local (desarrollo)

1. Configura tu `.env` con `SECRET_KEY` y `DATABASE_URL`.
2. Crea la base de datos o usa la existente.
3. Ejecuta el DDL para crear tablas (opcionalmente con una herramienta de migraciones):

```bash
# desde la carpeta raíz del proyecto
psql "$DATABASE_URL" -f app/utilities/Documentation/Database/ServiceDDL.sql
```

4. Para cargar datos de ejemplo (DML):

```bash
psql "$DATABASE_URL" -f app/utilities/Documentation/Database/ServiceDML.sql
```

5. Inicia la app en modo desarrollo:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

O usando el runner incluido:

```bash
python run.py
```

---

## Ejecución y pruebas

- Tests unitarios: existen pruebas de conexión y entorno en `app/test/`. Ejecuta con `pytest` si lo tienes configurado:

```bash
pytest -q
```

- Revisión rápida de imports de modelos (útil tras cambios en modelos):

```bash
python -c "import importlib, pkgutil, sys; sys.path.append('c:/workspace/DOLY'); pkg='app.models'; m=importlib.import_module(pkg); mods=[name for _,name,_ in pkgutil.iter_modules(m.__path__)]; print(mods)"
```

---

## Despliegue

- Heroku: `Procfile` presente. Asegúrate de configurar variables de entorno en el dashboard y habilitar la conexión a la base de datos.
- Contenedores: crea un Dockerfile si prefieres contenedores; asegúrate de usar un entrypoint que ejecute `gunicorn`.

Recomendación de producción:
- Servir estáticos desde CDN o bucket (S3)
- Usar `gunicorn` detrás de un proxy (NGINX)
- Habilitar TLS/HTTPS

---

## Estructura del proyecto (resumen)

```
DOLY/
├─ app/
│  ├─ __init__.py
│  ├─ auth.py
│  ├─ database.py
│  ├─ models/ (entidades SQLAlchemy)
│  ├─ templates/
│  ├─ static/
│  └─ utilities/
└─ run.py
```

(Ver árbol completo en la raíz del repo si lo necesitas en `tree.txt`)

---

## Base de datos y ERD

- Los scripts DDL/DML están en `app/utilities/Documentation/Database/`.
- El ERD está en `app/utilities/Documentation/Database/utils/ERD.md` en formato Mermaid. Puedes pegar ese contenido en https://mermaid.live para visualizarlo.

---

## Seguridad y buenas prácticas

- Nunca subas credenciales al repositorio (.env debe estar en `.gitignore`).
- Hashea contraseñas con `werkzeug.security.generate_password_hash` (ya usado en la app).
- Valida y sanea entradas del usuario tanto en cliente como en servidor (tu app ya aplica checks y constraints en la DB).
- Usa HTTPS y HSTS en producción.
- Revisa `server_default` y `CHECK` constraints en modelos para evitar inconsistencias.

---

## Logs, monitoreo y troubleshooting

- Logs se escriben en `app/utilities/logs/data.log` y mediante `app/log_control.py`.
- Para investigar errores comunes:
  - Revisa la salida de Flask y el archivo de logs
  - Verifica que `DATABASE_URL` esté accesible desde la red donde corre la app
  - Comprueba integridad del esquema: `psql "$DATABASE_URL" -c "\d+"` para revisar tablas

---

## Contribuir

- Sigue el estilo de código del repositorio: usa `black`/`isort` si están configurados.
- Cada modelo debe vivir en su propio archivo dentro de `app/models/` con `@dataclass` y `db.Model`.
- Abre Pull Requests descriptivos y referencia issues.

---

## Contacto

- Mantenedor: equipo DOLY (repositorio: `jr-devel/doly`)
- Para incidencias: abrir issue en el repositorio o escribir a dolylogistic@gmail.com

---

## Licencia

- Este proyecto está licenciado bajo la **MIT License**. El archivo `LICENSE` se encuentra en la raíz del repositorio.
- Copyright (c) 2026 jr-devel.

---

Si quieres, genero también:
- Un `README` en inglés.
- Un `CONTRIBUTING.md` con normas de commits y PRs.
- Un `tree.txt` automático con el árbol completo del proyecto.

---

## Árbol completo del proyecto (estado actual)

```
DOLY/
├─ .gitignore
├─ Procfile
├─ run.py
├─ requirements.txt
└─ app/
  ├─ __init__.py
  ├─ auth.py
  ├─ database.py
  ├─ log_control.py
  ├─ views.py
  ├─ views_client.py
  ├─ test/
  │  ├─ test_env.py
  │  └─ test_conn.py
  ├─ models/
  │  ├─ AuditLog.py
  │  ├─ Assistance.py
  │  ├─ Client.py
  │  ├─ ClientType.py
  │  ├─ Client_Vehicle.py
  │  ├─ Communication.py
  │  ├─ Company.py
  │  ├─ Company_Employee.py
  │  ├─ Discount.py
  │  ├─ Employee.py
  │  ├─ EmployeeType.py
  │  ├─ Evidence.py
  │  ├─ Invoice.py
  │  ├─ MaintenanceLog.py
  │  ├─ Notification.py
  │  ├─ Payment.py
  │  ├─ Persona.py
  │  ├─ Resource.py
  │  ├─ Resource_Company.py
  │  ├─ ResourceType.py
  │  ├─ Review.py
  │  ├─ Service.py
  │  ├─ ServiceType.py
  │  ├─ Service_Discount.py
  │  ├─ Session.py
  │  ├─ Settings.py
  │  ├─ Status.py
  │  ├─ SubResourceType.py
  │  ├─ Tracking.py
  │  ├─ UserAccount.py
  │  ├─ Vehicle.py
  │  └─ VehicleType.py
  ├─ templates/
  │  ├─ base.html
  │  ├─ header.html
  │  ├─ footer.html
  ├─ templates/admin/
  │  └─ index.html
  ├─ templates/auth/
  │  ├─ login.html
  │  └─ signup.html
  ├─ templates/client/
  │  └─ dashboard.html
  ├─ templates/landpage/
  │  ├─ index.html
  │  ├─ about.html
  │  ├─ contact.html
  │  ├─ help.html
  │  └─ services.html
  ├─ static/
  │  ├─ manifest.json
  │  ├─ css/
  │  │  └─ style.min.css
  │  ├─ js/
  │  │  ├─ app.js
  │  │  ├─ modernizr.js
  │  │  └─ sw.js
  │  └─ img/
  │     └─ logos/
  │        ├─ DOLY_LOGO-extended.png
  │        ├─ DOLY_LOGO-bg_white-font_orange.png
  │        ├─ DOLY_LOGO-bg_white-font_orange_square.png
  │        ├─ DOLY_LOGO-bg_orange-font_black.png
  │        ├─ DOLY_LOGO-bg_orange-font_black_square.png
  │        ├─ DOLY_LOGO-bg_black-font_orange.png
  │        ├─ DOLY_LOGO-bg_black-font_orange_square.png
  │        ├─ DOLY_LOGO-bg_aqua-font_orange.png
  │        ├─ DOLY_LOGO-bg_aqua-font_orange_square.png
  │        └─ ico/
  │           ├─ DOLY_LOGO-extended.ico
  │           ├─ DOLY_LOGO-bg_white-font_orange.ico
  │           ├─ DOLY_LOGO-bg_orange-font_black.ico
  │           ├─ DOLY_LOGO-bg_black-font_orange.ico
  │           └─ DOLY_LOGO-bg_aqua-font_orange.ico
  └─ utilities/
    └─ logs/
      └─ data.log
```

