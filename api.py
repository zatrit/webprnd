from flask import Blueprint, jsonify
import auth
import nodes

blueprint = Blueprint(
    "api",
    __name__
)

requires_auth = auth.requires_auth(["api", "user"])


@blueprint.route("/api/v1/random", methods=["POST"])
@requires_auth
def random():
    return []


@blueprint.route("/api/v1/types", methods=["GET"])
@requires_auth
def node_types():
    result = []
    for key, (params, _) in nodes.registry.items():
        node_params = {}

        for name, (_type, default) in params.items():
            node_params[name] = {
                "type": _type.__name__,
                "default": default
            }

        result.append({
            "type": key.node_type.value,
            "name": key.name,
            "props": node_params
        })
    return jsonify(result)
