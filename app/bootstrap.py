"""Подготовка базы при каждом запуске: таблицы, первый администратор, стартовые товары."""
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.config import ADMIN_PASSWORD, ADMIN_USERNAME, SEED_DEMO
from app.database import Base, engine, session
from app.models import product, stored_file, users  # noqa: F401  (чтобы все таблицы создались)
from app.models.product import Product
from app.models.users import User
from app.security import get_password_hash

FEATURES = "AISI 304\nЧёрный металл + порошок\nБез сверления"


def init_db() -> None:
    Base.metadata.create_all(engine)

    with session() as db:
        if ADMIN_USERNAME and ADMIN_PASSWORD:
            exists = db.scalar(select(User).where(User.username == ADMIN_USERNAME))
            if exists is None:
                db.add(User(
                    username=ADMIN_USERNAME,
                    hashed_password=get_password_hash(ADMIN_PASSWORD),
                    is_superuser=True,
                ))
                try:
                    db.commit()
                except IntegrityError:
                    db.rollback()   # при обновлении сервиса другой экземпляр приложения мог создать админа раньше

        if SEED_DEMO and db.scalars(select(Product)).first() is None:
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
