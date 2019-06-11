import os
import subprocess
import sys

from flask_script import Manager, Shell, Server, Command

from annuaire import create_app


server = Server(host="0.0.0.0", threaded=True)
app = create_app()
app.app_context().push()

def make_shell_context():
    return dict(app=app)


manager = Manager(app)


class CeleryWorker(Command):
    """Starts the celery worker."""
    name = 'celery'
    capture_all_args = True

    def run(self, argv):
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

    manager.run()
