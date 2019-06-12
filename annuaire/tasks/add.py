"""Example module of celery tasks."""
import time

from annuaire.tasks import celery


@celery.task(bind=True, track_started=True)
def add(self, x: int, y: int) -> int:
    """
    Compute an addition.

    :param self:
    :param x:
    :param y:
    :return:
    """
    time.sleep(5)
    return x + y
