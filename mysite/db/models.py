from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
from sqlalchemy import Integer, String, Enum, Date, ForeignKey, Text, Boolean
from mysite.db.database import Base
from enum import Enum as PyEnum
from datetime import date
import bcrypt

class UserStatus(str, PyEnum):
    gold = 'gold'
    silver = 'silver'
    bronze = 'bronze'
    simple = 'simple'


class UserProfile(Base):
    __tablename__ = 'user_profile'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    age: Mapped[Optional[int]] = mapped_column(Integer, default=0, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    profile_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.simple)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[date] = mapped_column(Date, autoincrement=True)

    review_user: Mapped[List['Review']] = relationship('Review', back_populates='user',
                                                       cascade='all, delete-orphan')
    refresh_user: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                              cascade='all, delete-orphan')

class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)
    user: Mapped[UserProfile] = relationship('UserProfile', back_populates='refresh_user')
    token: Mapped[str] = mapped_column(String)
    

class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(32), unique=True)

    sub_category: Mapped[List['SubCategory']] = relationship('SubCategory',
                                                             back_populates='category',
                                                             cascade='all, delete-orphan')
    category_product: Mapped[List['Product']] = relationship('Product', back_populates='category',
                                                             cascade='all, delete-orphan')

    def __str__(self):
        return self.category_name


class SubCategory(Base):
    __tablename__ = 'sub_category'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    sub_category_name: Mapped[str] = mapped_column(String(32), unique=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    category: Mapped['Category'] = relationship('Category', back_populates='sub_category')

    sub_category_product: Mapped[List['Product']] = relationship('Product', back_populates='sub_category',
                                                                 cascade='all, delete-orphan')

    def __repr__(self):
        return self.sub_category_name



class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(32))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    product_image: Mapped[str] = mapped_column(String)

    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    subcategory_id: Mapped[int] = mapped_column(ForeignKey('sub_category.id'))

    category: Mapped['Category'] = relationship('Category', back_populates='category_product')
    sub_category: Mapped['SubCategory'] = relationship('SubCategory', back_populates='sub_category_product')

    images_product: Mapped[List['ImageProduct']] = relationship('ImageProduct', back_populates='product',
                                                                cascade='all, delete-orphan')
    review_product: Mapped[List['Review']] = relationship('Review', back_populates='product',
                                                          cascade='all, delete-orphan')
    items_products: Mapped[List['CartItem']] = relationship('CartItem', back_populates='product',
                                                            cascade='all, delete-orphan')
    favorite_products: Mapped[List['FavoriteItem']] = relationship('FavoriteItem', back_populates='product',
                                                                   cascade='all, delete-orphan')


class ImageProduct(Base):
    __tablename__ = 'image_product'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    image: Mapped[str] = mapped_column(String)

    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    product: Mapped['Product'] = relationship('Product', back_populates='images_product')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    video: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stars: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))

    user: Mapped['UserProfile'] = relationship('UserProfile', back_populates='review_user')
    product: Mapped['Product'] = relationship('Product', back_populates='review_product')


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)

    items: Mapped[List['CartItem']] = relationship('CartItem', back_populates='cart',
                                                   cascade='all, delete-orphan')

class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))

    cart: Mapped['Cart'] = relationship('Cart', back_populates='items')
    product: Mapped['Product'] = relationship('Product', back_populates='items_products')


class Favorite(Base):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'), unique=True)

    favorite_items: Mapped[List['FavoriteItem']] = relationship('FavoriteItem', back_populates='favorite',
                                                   cascade='all, delete-orphan')

class FavoriteItem(Base):
    __tablename__ = 'favorite_item'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    like: Mapped[bool] = mapped_column(Boolean, default=False)

    favorite_id: Mapped[int] = mapped_column(ForeignKey('favorite.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))

    favorite: Mapped['Favorite'] = relationship('Favorite', back_populates='favorite_items')
    product: Mapped['Product'] = relationship('Product', back_populates='favorite_products')
