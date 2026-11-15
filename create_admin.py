from app.database import Base, engine, session
from app.models.users import User
from app.security import get_password_hash

Base.metadata.create_all(engine)

with session() as db:
    db.add(User(
        username="admin",
        hashed_password=get_password_hash("admin"),
        is_superuser=True,
    ))
    db.commit()