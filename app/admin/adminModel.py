from models.users import User
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = (User.id, User.username, User.email)

    column_exclude_list = (User.hashed_password,)