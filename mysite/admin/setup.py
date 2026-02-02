from .view import CategoryAdmin, UserProfileAdmin, SubCategoryAdmin, ProductAdmin
from sqladmin import Admin
from fastapi import FastAPI
from mysite.db.database import engine

def setup_admin(app:FastAPI):
    admin = Admin(app, engine)
    admin.add_view(CategoryAdmin)
    admin.add_view(UserProfileAdmin)
    admin.add_view(SubCategoryAdmin)
    admin.add_view(ProductAdmin)


