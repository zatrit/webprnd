from io import BytesIO
from typing import Protocol
from py7zr import SevenZipFile


class OutputFormat(Protocol):
    def __init__(self) -> None:
        ...

    def write(self, id: int, ext: str, content: bytes | str):
        """Добавляет файл в набор выходных ланных"""
        ...

    def get_content(self) -> tuple[bytes, str]:
        """Возвращает контент ввиде байт и MIME-тип"""
        ...


class Output7zArchive(OutputFormat):
    def __init__(self) -> None:
        self.items: dict[tuple[int, str], bytes] = {}

    def write(self, _id: int, ext: str, content: bytes | str):
        if isinstance(content, str):
            content = content.encode("utf8")

        self.items[(_id, ext)] = content

    def get_content(self) -> tuple[bytes, str]:
        with BytesIO() as io:
            archive = SevenZipFile(io, mode="w")

            for (_id, ext), content in self.items.items():
                name = ".".join((str(_id), ext))
                archive.writestr(content, name)

            archive.close()
            return io.getvalue(), "application/x-7z-compressed"


formats: dict[str, type[OutputFormat]] = {
    "7z": Output7zArchive
}
