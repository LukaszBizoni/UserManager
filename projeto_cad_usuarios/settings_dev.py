"""Local development settings used by manage.py."""

import os


os.environ.setdefault("DJANGO_DEBUG", "true")

from .settings import *  # noqa: E402,F403
