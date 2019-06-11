import os

from flask_script import Manager, Shell, Server

from annuaire import create_app


server = Server(host="0.0.0.0", threaded=True)
app = create_app(os.environ.get('ENV', 'dev'))
app.app_context().push()


def make_shell_context():
    return dict(app=app)


manager = Manager(app)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", server)

import annuaire.commands
manager.add_command('download', annuaire.commands.download.DownloadReferencesCommand())
manager.add_command('import', annuaire.commands.import_lawyers.ImportCommand())

if __name__ == '__main__':

    manager.run()