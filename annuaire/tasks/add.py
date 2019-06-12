"""Example module of celery tasks."""
import logging
import time

from annuaire.annuaire.database import populate_lawyers
from annuaire.annuaire.exception import AnnuaireException
from annuaire.annuaire.query import get_form_page, search
from annuaire.tasks import celery

log = logging.getLogger(__name__)


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


@celery.task(bind=True, track_started=True)
def scrap_one_barreau(self, barreau_code):
    """

    :param self:
    :param barreau_code:
    :return:
    """
    result = get_form_page()
    try:
        items = search(barreau_code, result["cookies"])
        populate_lawyers(items)
    except AnnuaireException as e:
        log.warning(e.message)
        self.retry(max_retries=3, countdown=60)
