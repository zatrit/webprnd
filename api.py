from functools import lru_cache
from flask import Blueprint, jsonify, request
from api_error import ApiError, ApiMessage
import auth
from generation import Project, generate_project
import nodes

blueprint = Blueprint(
    "api",
    __name__
)

# Тут и api и user для того, чтобы через
# API подгружать нужные данные в редактор
requires_auth = auth.requires_auth(["api", "user"])


@blueprint.route("/api/v1/random", methods=["POST"])
@requires_auth
def random():
    try:
        if request.json:
            project = Project.from_json(request.json)
            generate_project(project)
            return []
    except ApiError as error:
        return error.json(), 400
    except TypeError as error:
        return ApiError(ApiMessage.WRONG_TYPE, {"details": str(error)}).json(), 400
    return ApiError(ApiMessage.NO_DATA).json(), 400


# POST тут нужен для обращения к API без лишней боли
@blueprint.route("/api/v1/types", methods=["GET", "POST"])
@requires_auth
# Использование кэширования тут имеет смысл, т.к.
# функция всегда возвращает один результат во время
# работы программы, и динамического добавления
# типов нод я не собираюсь реализовывать
# (если вдруг соберусь, то уберу)
@lru_cache(1)
def node_types():
    result = []
    for key, (params, _) in nodes.registry.items():
        node_params = {}

        for name, param in params.items():
            node_params[name] = param.serialize()

        # Прописано в nodes.schema.json
        result.append({
            "type": key._type.value,
            "name": key.name,
            "params": node_params
        })
    return jsonify(result)
