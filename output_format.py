from abc import abstractmethod
from typing import Protocol
import mimetypes


class OutputFormat(Protocol):
    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def write(self, _id: int, ext: str, content: bytes | str):
        """Добавляет файл в набор выходных ланных"""
        ...

    @abstractmethod
    def get_content(self) -> tuple[bytes, str]:
        """Возвращает контент ввиде байт и MIME-тип"""
        ...


# Базовый формат, частично реалзиющий протокол OutputFormat
class BaseOutputFormat():
    def __init__(self) -> None:
        self.items: dict[tuple[int, str], bytes] = {}

    def write(self, _id: int, ext: str, content: bytes | str):
        if isinstance(content, str):
            content = content.encode("utf8")

        self.items[(_id, ext)] = content


class Output7zArchive(BaseOutputFormat, OutputFormat):
    def get_content(self) -> tuple[bytes, str]:
        from py7zr import SevenZipFile
        from io import BytesIO

        with BytesIO() as io:
            # Создаём архив в памяти и записываем в
            # него все выходные файлы
            archive = SevenZipFile(io, mode="w")

            for (_id, ext), content in self.items.items():
                name = ".".join((str(_id), ext))
                archive.writestr(content, name)

            archive.close()
            return io.getvalue(), "application/x-7z-compressed"


class OutputPlain(BaseOutputFormat, OutputFormat):
    def write(self, _id: int, ext: str, content: bytes | str):
        if len(self.items) > 0:
            raise TypeError("Нельзя использовать несколько нод типа output, "
                            "если формат выходных данных равен plain")
        return super().write(_id, ext, content)

    def get_content(self) -> tuple[bytes, str]:
        (_id, ext), content = next(iter(self.items.items()))

        _type, _ = mimetypes.guess_type(".".join((str(_id), ext)))

        if not _type:
            raise Exception("Не удалось преобразовать выходные данные")

        return content, _type


# В целом, этот формат может пригодиться для использования
# в других приложениях
class OutputBase64Json(BaseOutputFormat, OutputFormat):
    def get_content(self) -> tuple[bytes, str]:
        import base64
        import ujson

        result = {}
        for (_id, ext), content in self.items.items():
            name = ".".join((str(_id), ext))
            result[name] = base64.encodebytes(content).decode("utf8")

        return ujson.dumps(result).encode("utf8"), "application/json"


formats: dict[str, type[OutputFormat]] = {
    "7z": Output7zArchive,
    "plain": OutputPlain,
    "base64json": OutputBase64Json
}
