"""Одноразовый запуск: python3 seed_products.py — заносит в базу два товара, которые сейчас вручную прописаны на сайте."""
from sqlalchemy import select

from app.database import Base, engine, session
from app.models import product  # noqa: F401
from app.models.product import Product

Base.metadata.create_all(engine)

FEATURES = "AISI 304\nЧёрный металл + порошок\nБез сверления"

with session() as db:
    if db.scalars(select(Product)).first():
        print("В базе уже есть товары, ничего не добавлено.")
    else:
        db.add_all([
            Product(
                name="JAC T9",
                description="Готовый комплект защиты переднего и заднего бамперов для пикапа JAC T9. Устанавливается на штатные места без сверления.",
                features=FEATURES,
                image_1="assets/hero-jac-t9.png",
                image_2="assets/jac-t9-white.png",
                position=1,
            ),
            Product(
                name="Haval H3",
                description="Готовый комплект защиты переднего и заднего бамперов для внедорожника Haval H3. Устанавливается на штатные места без сверления.",
                features=FEATURES,
                image_1="assets/haval-front.png",
                image_2="assets/haval-rear.png",
                position=2,
            ),
        ])
        db.commit()
        print("Добавлено: JAC T9, Haval H3")