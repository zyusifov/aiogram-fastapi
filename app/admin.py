from sqladmin import Admin, ModelView
from fastapi import FastAPI
from app.db import engine
from app.models.users import User
from app.models.locations import Location


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.full_name, User.created_at]
    column_searchable_list = [User.username, User.full_name]


class LocationAdmin(ModelView, model=Location):
    column_list = [Location.user_id, Location.latitude, Location.longitude, Location.created_at]
    column_searchable_list = [Location.user_id]


def init_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(LocationAdmin)
