"""Package defined the webapp module of the flask application."""
from flask import Blueprint

webapp_bp = Blueprint("app", __name__,
                      url_prefix="/",
                      template_folder="templates"  # templates folder
                      )
