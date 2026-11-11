from security import verify_password
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from starlette.requests import Request

from app.database import session
from app.models.users import User


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # 1. Проверка на строки
        if not isinstance(username, str) or not isinstance(password, str):
            return False

        # 2. Достаем пользователя из бд
        with session() as db:
            query = select(User).where(User.username == username)
            user = db.execute(query).scalar_one_or_none()

        # 3. Проверка наличие юзера, совпадение пароля и права супер-админа
        if user and verify_password(password, user.hashed_password) and user.is_superuser:
            request.session.update({"token": str(user.id)})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        return bool(token)
