from pydantic import BaseModel
from mysite.db.models import UserStatus
from datetime import date

class UserProfileSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    age: int | None
    phone_number: str | None
    profile_image: str | None
    status: UserStatus
    created_at: date

class UserProfileRegistrationSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    age: int | None
    phone_number: str | None
    profile_image: str | None
    status: UserStatus
    created_at: date
    password: str

class UserProfileLoginSchema(BaseModel):
    username: str
    password: str


class CategorySchema(BaseModel):
    category_name: str

class SubCategorySchema(BaseModel):
    sub_category_name: str
    category_id: int


class ProductSchema(BaseModel):
    product_name: str
    description: str
    price: int
    product_image: str
    category_id: int
    subcategory_id: int


class ImageProductSchema(BaseModel):
    image: str
    product_id: int

class ReviewSchema(BaseModel):
    user_id: int
    product_id: int
    comment: str
    stars: int
    image: str
    video: str

class CartSchema(BaseModel):
    user_id: int

class CartItemSchema(BaseModel):
    cart_id: int
    product_id: int

class FavoriteSchema(BaseModel):
    user_id: int

class FavoriteItemSchema(BaseModel):
    favorite_id: int
    product_id: int
    like: bool
