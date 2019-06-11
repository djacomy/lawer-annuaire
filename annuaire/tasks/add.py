import time
from annuaire.tasks import celery


@celery.task(bind=True, track_started=True)
def add(self, x: int, y: int) -> int:
    time.sleep(5)
    return x + y

