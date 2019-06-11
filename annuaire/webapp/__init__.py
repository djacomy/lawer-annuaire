from flask import Blueprint

webapp_bp = Blueprint('app', __name__,
                      url_prefix='/',
                      template_folder='templates'  # templates folder
                    )

from . import route

