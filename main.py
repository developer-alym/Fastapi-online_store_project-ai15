from fastapi import FastAPI
from mysite.api import category, sub_category, user, auth

hotel_app = FastAPI(title='Wildberies FastApi Project')
hotel_app.include_router(category.category_router)
hotel_app.include_router(user.user_router)
hotel_app.include_router(sub_category.sub_category_router)
hotel_app.include_router(auth.auth_router)



