from mysite.db.models import UserProfile, Category,  SubCategory, Product
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.id, UserProfile.username]

class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.id, Category.category_name]

class SubCategoryAdmin(ModelView, model=SubCategory):
    column_list = [SubCategory.id, SubCategory.sub_category_name]

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.product_name]

