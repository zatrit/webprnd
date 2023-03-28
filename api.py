from flask import Blueprint, request
from flask_restful import Api, Resource

blueprint = Blueprint(
    "api",
    __name__
)

api = Api(blueprint)


class Random(Resource):
    def post(self):
        pass


api.add_resource(Random, "/api/v1/random")
