"""Buisness module."""
import os
from datetime import datetime

from annuaire.annuaire.query import get_form_page, search

from config import settings


def format_output_directory(barreau_code):
    """
    Format output directory.

    :param barreau_code:
    :return:
    """
    timestamp = datetime.strftime(datetime.now(), "%Y%m%d%H%I")
    path = os.path.join(settings.DATA_DIR, "annuaire", timestamp, barreau_code)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


__all__ = [format_output_directory, get_form_page, search]
