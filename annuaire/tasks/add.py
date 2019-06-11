import time
from annuaire.tasks import celery, BaseTask


@celery.task(base=BaseTask)
def add(x: int, y: int) -> int:
    time.sleep(5)
    return x + y


celery.tasks.register(add)
