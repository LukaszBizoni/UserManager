# UserManager

Current version: **v1.2**

UserManager is a simple Django application for managing user records. It was built as a personal learning project and provides a complete CRUD flow for names and ages.

## What's new in v1.2

This release focuses on security hardening and safer deployment:

- Login and logout flow using Django authentication
- Permission-based access for viewing, creating, editing, and deleting records
- Secure production settings for secrets, allowed hosts, HTTPS, cookies, and HSTS
- Content Security Policy and additional browser security headers
- Separate development and production configurations
- Expanded automated tests for authentication, authorization, CSRF, and CSP

## Technologies

- Python
- Django 6.1.2
- Bootstrap 5.3.2
- HTML, CSS, and JavaScript
- SQLite

## Features

- Create and validate user records
- List registered users
- Edit existing users
- Delete users with a confirmation page
- Authentication and per-operation permissions
- Production security settings loaded from environment variables
- Content Security Policy and HTTPS hardening
- Success and error messages
- Responsive Bootstrap interface
- Dark and light themes with saved preferences
- Smooth transitions with reduced-motion support

## Running locally

1. Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

2. Activate the environment on Windows:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Apply the database migrations:

   ```powershell
   python manage.py migrate
   ```

5. Create an administrator account:

   ```powershell
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```powershell
   python manage.py runserver
   ```

Open `http://127.0.0.1:8000/` in your browser.

`manage.py` uses `projeto_cad_usuarios.settings_dev` so local development can
run over HTTP with a disposable secret. WSGI and ASGI use the secure production
settings, which refuse to start without the required environment variables.

The CRUD pages require authentication and Django's `view_usuario`,
`add_usuario`, `change_usuario`, and `delete_usuario` permissions. A
superuser has all of them; permissions for other accounts can be assigned in
`/admin/`.

## Production configuration

Copy the variable names from `.env.example` into the environment provided by
your hosting platform. The project does not load `.env` files automatically.
At minimum, production requires:

```text
DJANGO_DEBUG=false
DJANGO_SECRET_KEY=<a long random secret>
DJANGO_ALLOWED_HOSTS=example.com,www.example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
```

Generate a secret without committing it:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

If a trusted reverse proxy terminates HTTPS and sends
`X-Forwarded-Proto: https`, set `DJANGO_BEHIND_HTTPS_PROXY=true`. Keep it false
otherwise. Before deployment, run:

```powershell
python manage.py check --deploy
python manage.py test
python manage.py collectstatic --noinput
```

Use a production WSGI/ASGI server rather than Django's development server.
