"""Command module to import lawyers in database."""
import logging

from annuaire.annuaire.database import get_all_barreaux
from annuaire.tasks.add import scrap_one_barreau

from flask_script import Command, Option

log = logging.getLogger(__name__)


class ImportCommand(Command):
    """Class ImportCommand."""

    description = "Import lawyers"

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

        for code in codes:
            log.info(f"{code}: {barreaux.get(code)}")
            scrap_one_barreau.delay(code)
