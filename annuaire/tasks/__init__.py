"""Task module."""
from celery import Celery


celery = Celery(__name__,
                include=["annuaire.tasks"])
celery.config_from_object("celeryconfig")

from . import add
