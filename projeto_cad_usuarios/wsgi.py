"""WSGI config for projeto_cad_usuarios project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projeto_cad_usuarios.settings")

application = get_wsgi_application()
