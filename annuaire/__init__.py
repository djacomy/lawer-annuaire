import logging
import os
import sys

from logging.handlers import RotatingFileHandler
from flask import Flask

from config import settings

from .tasks import celery


def register_logging(app):
    app.logger.name = 'app'

    # set own root logger
    rootLogger = logging.getLogger(__name__)
    handler = RotatingFileHandler('annuaire.log', maxBytes=10000, backupCount=1)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    handler.setLevel(logging.INFO)
    rootLogger.addHandler(handler)

    handler2 = logging.StreamHandler(sys.stdout)
    handler2.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    handler2.setLevel(logging.INFO)

    rootLogger.addHandler(handler2)
    rootLogger.setLevel(logging.DEBUG if os.environ.get('DEBUG', False) else logging.INFO)


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    register_logging(app)

    from .tasks import celery, add
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    from .webapp import webapp_bp
    from .api import api_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(webapp_bp)

    return app
