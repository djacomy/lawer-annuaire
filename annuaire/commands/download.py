"""Command module for references downloading."""
from annuaire.annuaire import get_form_page
from annuaire.annuaire.database import poplulate_references

from flask_script import Command


class DownloadReferencesCommand(Command):
    """Class DownloadReferencesCommand."""

    description = "Upload reference command"

    option_list = (
    )

    def run(self):
        """
        Execute the download references command.

        :return:
        """
        result = get_form_page()
        poplulate_references("barreau", result["raw"].xpath("//select[@name='barreau']/option"))
        poplulate_references("mentions", result["raw"].xpath("//select[@name='mentions']/option"))
        poplulate_references("langues", result["raw"].xpath("//select[@name='langues']/option"))
