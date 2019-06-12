"""Route module attached to the webapp module of the flask application."""
import csv
from io import StringIO

from annuaire.annuaire.database import export_lawyers
from annuaire.webapp import webapp_bp

from flask import make_response


@webapp_bp.route("/")
def download():
    """
    Export the database in csv file.

    :return:
    """
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(export_lawyers())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
