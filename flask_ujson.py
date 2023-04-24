import ujson
import typing as t
from flask import Flask, request
from flask.json.provider import DefaultJSONProvider


# Моё самописное расширение для Flask, заменяющее стандартный JSON
# на UltraJSON (ujson). Я думаю, это ускорит работу приложения.
# Часть кода скопирована из оригинального DefaultJSONProvider

class UltraJSONProvider(DefaultJSONProvider):
    def __init__(self, app: Flask) -> None:
        super().__init__(app)
        self.default_provider = app.json

    def dumps(self, obj: t.Any, **kwargs: t.Any) -> str:
        try:
            cls = self._app._json_encoder
            bp = self._app.blueprints.get(
                request.blueprint) if request else None

            if bp is not None and bp._json_encoder is not None:
                cls = bp._json_encoder

            if cls is None:
                kwargs.setdefault("default", self.default)

            ensure_ascii = self._app.config["JSON_AS_ASCII"]
            sort_keys = self._app.config["JSON_SORT_KEYS"]

            if ensure_ascii is None:
                ensure_ascii = self.ensure_ascii

            if sort_keys is None:
                sort_keys = self.sort_keys

            kwargs.setdefault("ensure_ascii", ensure_ascii)
            kwargs.setdefault("sort_keys", sort_keys)
            return ujson.dumps(obj, **kwargs)
        except Exception:
            print("Falling back to default dumper")
            return self.default_provider.dumps(obj, **kwargs)

    def loads(self, s: t.AnyStr, **kwargs: t.Any) -> t.Any:
        try:
            return ujson.loads(s)
        except Exception:
            print("Falling back to default loader")
            return self.default_provider.loads(s, **kwargs)


def init_app(app: Flask):
    app.json = UltraJSONProvider(app)
