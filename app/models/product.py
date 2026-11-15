import uuid
from pathlib import Path

from fastapi_storages import StorageFile
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.storage import DatabaseStorage

storage = DatabaseStorage()


def make_name(filename: str) -> str:
    """Имя для сохранения: случайное, чтобы файлы разных товаров не затирали друг друга."""
    if filename.startswith("uploads/"):
        return filename
    return f"uploads/{uuid.uuid4().hex}{Path(filename).suffix.lower()}"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]                                                     # «JAC T9»
    description: Mapped[str | None] = mapped_column(Text, default=None)
    features: Mapped[str | None] = mapped_column(Text, default=None)      # по одному свойству на строку
    image_1: Mapped[StorageFile | None] = mapped_column(FileType(storage=storage, upload_to=make_name), default=None)
    image_2: Mapped[StorageFile | None] = mapped_column(FileType(storage=storage, upload_to=make_name), default=None)
    position: Mapped[int] = mapped_column(default=0)                      # порядок на сайте
    is_active: Mapped[bool] = mapped_column(default=True)                 # показывать на сайте

    @property
    def features_list(self) -> list[str]:
        return [line.strip() for line in (self.features or "").splitlines() if line.strip()]

    def __str__(self) -> str:
        return self.name
