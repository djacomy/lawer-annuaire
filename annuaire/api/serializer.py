"""Module serializer used by swagger to describe params and response."""
from flask_restful import fields

from flask_restful_swagger import swagger


@swagger.model
class Reference:
    """Reference model."""

    resource_fields = {
        "code": fields.String,
        "name": fields.String,
    }


@swagger.model
@swagger.nested(items=Reference.__name__)
class ReferencesList:
    """List or Reference model."""

    resource_fields = {
        "items": fields.List(fields.Nested(Reference.resource_fields))
    }
