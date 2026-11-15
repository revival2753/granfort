import mimetypes
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import TEMPLATES_DIR
from app.database import get_db
from app.models.product import Product
from app.storage import read_file

router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/")
def index(request: Request, db: Annotated[Session, Depends(get_db)]):
    products = db.scalars(
        select(Product).where(Product.is_active.is_(True)).order_by(Product.position, Product.id)
    ).all()
    return templates.TemplateResponse(request, "index.html", {"products": products})


@router.get("/uploads/{filename}")
def uploaded_file(filename: str):
    """Отдаёт фото, загруженные через админку (они лежат в базе)."""
    data = read_file(f"uploads/{filename}")
    if data is None:
        raise HTTPException(status_code=404)

    return Response(
        data,
        media_type=mimetypes.guess_type(filename)[0] or "application/octet-stream",
        headers={
            "Cache-Control": "public, max-age=31536000, immutable",   # имя файла случайное и не повторяется
            "X-Content-Type-Options": "nosniff",
        },
    )
