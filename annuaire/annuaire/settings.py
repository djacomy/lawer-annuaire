import os


DATA_DIR = os.environ.get('DATA_DIR', os.path.join(".", "data"))

BASE_URL = 'https://annuaire.avocat.fr'

DB_PATH = os.environ.get('DB_PATH', os.path.join(DATA_DIR, 'annuaire.json'))


