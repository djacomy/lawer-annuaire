import os

from datetime import datetime

from annuaire.annuaire import settings
from .parser import parse_detail, parse_result
from .query import search, get_form_page


def format_output_directory(barreau_code):
    timestamp = datetime.strftime(datetime.now(), '%Y%m%d%H%I')
    path = os.path.join(settings.DATA_DIR, 'annuaire', timestamp, barreau_code)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


__all__ = [search, format_output_directory, get_form_page]
