"""Manage module is the entrypoint of the app."""
import os
import subprocess
import sys

from flask_script import Command, Manager, Server, Shell

from annuaire import create_app

from config import settings

server = Server(host="0.0.0.0", threaded=True)
app = create_app()
app.app_context().push()
manager = Manager(app)


def make_shell_context():
    """Create shell context."""
    return {'app':app}


@manager.command
def test():
    """
    Run unit tests.

    :return:
    """
    tests = subprocess.call(["python", "-c", "import tests; tests.run()"])
    sys.exit(tests)


@manager.command
def lint():
    """
    Run code to show pep violations.

    :return:
    """
    res = subprocess.call(["flake8", "--config=flake8.ini", "--ignore=E402", "annuaire/",
                           "manage.py", "tests/"]) == 0
    if res:
        print("OK")
    sys.exit(res)


class CeleryWorker(Command):
    """Starts the celery worker."""

    name = 'celery'
    capture_all_args = True

    def run(self, argv):
        """
        Execute celery commands.

        :param argv:
        :return:
        """
        ret = subprocess.call(
            ['celery', 'worker', '-A', 'annuaire.tasks.celery'] + argv)
        sys.exit(ret)


manager.add_command("celery", CeleryWorker())
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", server)

import annuaire.commands
manager.add_command('download', annuaire.commands.download.DownloadReferencesCommand())
manager.add_command('import', annuaire.commands.import_lawyers.ImportCommand())

if __name__ == '__main__':

    if sys.argv[1] == "test":
        # small hack, to ensure that Flask-Script uses the testing
        # configuration if we are going to run the tests
        os.environ["ENV"] = "testing"

    if not os.path.isdir(settings.DATA_DIR):
        os.makedirs(settings.DATA_DIR)

    manager.run()
