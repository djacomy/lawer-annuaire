import os
from celery import Celery


celery = Celery(__name__,
                broker=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379'),
                backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379'),
                include=["annuaire.tasks"])
celery.config_from_object('celeryconfig')

Task = celery.create_task_cls()


class BaseTask(Task):
    abstract = True


from . import add
