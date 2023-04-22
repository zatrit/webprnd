from .types import ParamDict, ParamTypes


def fill_defaults(params: ParamDict, accepts_params: ParamTypes, only_allowed: bool = True):
    forward_params = {}

    if only_allowed:
        for key, _ in (params or {}).items():
            if key not in accepts_params:
                raise ValueError("Неизвестный параметр " + key)

    for key, param in accepts_params.items():
        value = params.get(key, param.default)
        if not param.validate(value):
            raise ValueError("Неверный тип или значение " + key)
        forward_params[key] = value

    return forward_params
