import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CELERY_CONFIG = {}
    DATA_DIR = os.environ.get('DATA_DIR', os.path.join(basedir, "data"))
    BASE_URL = 'https://annuaire.avocat.fr'
    DB_PATH = os.environ.get('DB_PATH', os.path.join(DATA_DIR, 'annuaire.json'))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    CELERY_CONFIG = {'CELERY_ALWAYS_EAGER': True}


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

settings = config[os.environ.get('ENV', 'default')]
