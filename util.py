from collections.abc import Mapping, MutableMapping


# https://stackoverflow.com/a/3233356/12245612
def update(d: MutableMapping, u: Mapping):
    for k, v in u.items():
        if isinstance(v, Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
