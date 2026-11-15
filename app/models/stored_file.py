from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class StoredFile(Base):
    __tablename__ = "stored_files"

    name: Mapped[str] = mapped_column(primary_key=True)   
    content: Mapped[bytes] = mapped_column(LargeBinary)
