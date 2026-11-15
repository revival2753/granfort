import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Render сам выставляет переменную RENDER, у вас на компьютере её нет
ON_RENDER = bool(os.getenv("RENDER"))

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    if ON_RENDER:
        raise RuntimeError("Не задана переменная окружения SECRET_KEY")
    SECRET_KEY = "ключ-только-для-запуска-на-своём-компьютере"

# Первый администратор: создаётся при запуске, если такого пользователя ещё нет
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# SEED_DEMO=1 — при пустой базе добавить два стартовых товара (JAC T9 и Haval H3)
SEED_DEMO = os.getenv("SEED_DEMO") == "1"


def _database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        return f"sqlite:///{BASE_DIR / 'app.db'}"   # локально: файл app.db в корне проекта
    # Render отдаёт адрес вида postgresql://..., а SQLAlchemy с драйвером psycopg нужен postgresql+psycopg://
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


DATABASE_URL = _database_url()
