"""Module which defined routes of the api."""
import logging

from annuaire.annuaire.database import get_references
from annuaire.api import api_manager
from annuaire.api.serializer import ReferencesList


from flask_restful import Resource, abort

from flask_restful_swagger import swagger

logger = logging.getLogger(__name__)


class Reference(Resource):
    """Give data by reference."""

    @swagger.operation(
        notes="Get data by reference",
        responseClass=ReferencesList,
        nickname="search",
        parameters=[
            {
                "name": "reference",
                "description": "Name of reference: barreau, mentions, langues",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Success !"
            },
            {
                "code": 400,
                "message": "Error !!"
            }
        ]
    )
    def get(self, reference):
        """GET method."""
        if reference not in ["barreau", "mentions", "langues"]:
            abort(400, message="{0} unknown".format(reference))

        return {"items": get_references(reference)}, 200


api_manager.add_resource(Reference, "/ref/<string:reference>/")
