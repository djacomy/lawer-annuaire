"""Package which define api module of the flask application."""
from flask import Blueprint

from flask_restful import Api

from flask_restful_swagger import swagger


api_bp = Blueprint("api", __name__, url_prefix="/api")

api = Api()
api.init_app(api_bp)
###################################
# Wrap the Api with swagger.docs. It is a thin wrapper around the Api class that adds some swagger smarts
api_manager = swagger.docs(api, apiVersion="0.1", api_spec_url="/docs")
###################################
