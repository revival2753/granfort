from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from app.admin.adminModel import ProductAdmin, UserAdmin
from app.admin.adminVerify import AdminAuth
from app.bootstrap import init_db
from app.config import SECRET_KEY, STATIC_DIR
from app.database import engine
from app.routers import auth, site

init_db()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

admin = Admin(app, engine, authentication_backend=AdminAuth(secret_key=SECRET_KEY))
admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)

app.include_router(auth.router)
app.include_router(site.router)

app.mount("/", StaticFiles(directory=STATIC_DIR), name="site")  # последней!
