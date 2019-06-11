import csv
from io import StringIO

from flask import make_response

from annuaire.annuaire.database import export_lawyers

from . import webapp_bp


@webapp_bp.route("/")
def download():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(export_lawyers())
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
