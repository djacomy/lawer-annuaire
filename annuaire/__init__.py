"""Root package of the annuaire application."""
import logging
import sys
from logging.handlers import RotatingFileHandler

from config import settings

from flask import Flask


def register_logging(app):
    """
    Register app"s loggers and root"s loggers.

    :param app:
    :return:
    """
    app.logger.name = "app"

    # set own root logger
    root_logger = logging.getLogger(__name__)
    handler = RotatingFileHandler("annuaire.log", maxBytes=10000, backupCount=1)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    root_logger.addHandler(handler)

    handler2 = logging.StreamHandler(sys.stdout)
    handler2.setFormatter(formatter)
    handler2.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    root_logger.addHandler(handler2)
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)


def create_app():
    """
    Create an flask app and fill the context.

    :return:
    """
    app = Flask(__name__)
    app.config.from_object(settings)
    register_logging(app)

    from .tasks import celery
    celery.conf.update(app.config)

    TaskBase = celery.create_task_cls()

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    from .webapp import webapp_bp, route as webap_route
    from .api import api_bp, route as api_route

    app.register_blueprint(api_bp)
    app.register_blueprint(webapp_bp)

    return app
