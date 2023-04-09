from flask import Blueprint
from flask_restful import Api, Resource
from auth import requires_auth_api

blueprint = Blueprint(
    "api",
    __name__
)

api = Api(blueprint)


class Random(Resource):
    @requires_auth_api
    def post(self):
        pass


api.add_resource(Random, "/api/v1/random")
