from flask import Blueprint
from flask_restful import Api, Resource
import auth

blueprint = Blueprint(
    "api",
    __name__
)
requires_auth = auth.requires_auth("api")

api = Api(blueprint)


class Random(Resource):
    @requires_auth
    def post(self):
        pass


api.add_resource(Random, "/api/v1/random")
