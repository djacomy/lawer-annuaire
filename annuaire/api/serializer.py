from flask_restful import fields
from flask_restful_swagger import swagger


@swagger.model
class Reference:
  resource_fields = {
      'code': fields.String,
      'name': fields.String,
  }


@swagger.model
@swagger.nested(items=Reference.__name__)
class ReferencesList:
  resource_fields = {
      'items': fields.List(fields.Nested(Reference.resource_fields))
  }
