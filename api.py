from flask import Blueprint, jsonify
from flask_restful import Api, Resource
import auth
import nodes

blueprint = Blueprint(
    "api",
    __name__
)

requires_auth = auth.requires_auth(["api", "user"])
api = Api(blueprint)


class Random(Resource):
    @requires_auth
    def post(self):
        pass


@blueprint.route("/api/v1/types", methods=["GET"])
@requires_auth
def node_types():
    result = {}
    for key in nodes.registry.keys():
        _type = key.node_type.value
        if _type not in result:
            result[_type] = []
        result[_type].append(key.name)
    return jsonify(result)


api.add_resource(Random, "/api/v1/random")
