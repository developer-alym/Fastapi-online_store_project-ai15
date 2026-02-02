from fastapi import FastAPI
from mysite.api import category, sub_category, user, auth
from mysite.admin.setup import  setup_admin

store_app = FastAPI(title='Wildberies FastApi Project')
store_app.include_router(category.category_router)
store_app.include_router(user.user_router)
store_app.include_router(sub_category.sub_category_router)
store_app.include_router(auth.auth_router)
setup_admin(store_app)


