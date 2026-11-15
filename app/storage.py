import io
from typing import BinaryIO

from fastapi_storages.base import BaseStorage

from app.config import STATIC_DIR
from app.database import session
from app.models.stored_file import StoredFile


def read_file(name: str) -> bytes | None:
    """Содержимое файла: сначала из базы, затем с диска (фото из assets/ лежат в репозитории)."""
    with session() as db:
        row = db.get(StoredFile, name)
        if row is not None:
            return row.content

    path = (STATIC_DIR / name).resolve()
    if path.is_file() and STATIC_DIR.resolve() in path.parents:   # не выходим за пределы static/
        return path.read_bytes()
    return None


class DatabaseStorage(BaseStorage):
    """Хранилище для fastapi-storages: файлы лежат в таблице stored_files."""

    def get_name(self, name: str) -> str:
        return name

    def get_path(self, name: str) -> str:
        return name

    def get_size(self, name: str) -> int:
        data = read_file(name)
        return len(data) if data is not None else 0

    def open(self, name: str) -> BinaryIO:
        data = read_file(name)
        if data is None:
            raise FileNotFoundError(name)
        return io.BytesIO(data)

    def write(self, file: BinaryIO, name: str) -> str:
        file.seek(0, 0)
        content = file.read()
        with session() as db:
            db.merge(StoredFile(name=name, content=content))
            db.commit()
        return name

    def delete(self, name: str) -> None:
        with session() as db:
            row = db.get(StoredFile, name)
            if row is not None:
                db.delete(row)
                db.commit()

    def generate_new_filename(self, filename: str) -> str:
        return filename
