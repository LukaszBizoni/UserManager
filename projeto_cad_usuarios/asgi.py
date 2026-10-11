"""ASGI config for projeto_cad_usuarios project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projeto_cad_usuarios.settings")

application = get_asgi_application()
