"""Command module to import lawyers in database."""
import json
import os
from datetime import datetime

from annuaire.annuaire import get_form_page, search
from annuaire.annuaire.database import get_all_barreaux, populate_lawyers
from annuaire.annuaire.exception import AnnuaireException

from config import settings

from flask_script import Command, Option


class ImportCommand(Command):
    """Class ImportCommand."""

    description = "Upload reference command"

    option_list = (
        Option("--barreau-code",
               dest="barreau_code",
               default=None,
               help="Import lawyers in dattabse"),
    )

    def run(self, barreau_code=None):
        """
        Execute the command.

        :param barreau_code:
        :return:
        """
        barreaux = get_all_barreaux()
        codes = []
        if barreau_code:
            codes.append(barreau_code)
        else:
            codes = sorted(barreaux.keys())

        result = get_form_page()
        statistitics = {}
        for code in codes:
            print(code, barreaux.get(code))
            try:
                items = search(code, result["cookies"])
                statistitics[code] = len(items)
                populate_lawyers(items)
            except AnnuaireException:
                statistitics[code] = None

        with open(os.path.join(settings.DATA_DIR,
                               "stats_{0}.json".format(datetime.now().strftime("%Y%m%d%H%i%s"))), "w") as fp:
            json.dump(statistitics, fp)
