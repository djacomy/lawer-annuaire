from flask_script import Command

from annuaire.annuaire import get_form_page

from annuaire.annuaire.database import poplulate_references


class DownloadReferencesCommand(Command):

    help = description = 'Upload reference command'

    option_list = (
    )

    def run(self):
        result = get_form_page()
        poplulate_references('barreau', result['raw'].xpath("//select[@name='barreau']/option"))
        poplulate_references('mentions', result['raw'].xpath("//select[@name='mentions']/option"))
        poplulate_references('langues', result['raw'].xpath("//select[@name='langues']/option"))


