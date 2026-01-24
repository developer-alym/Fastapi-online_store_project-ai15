from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.models import Category
from mysite.db.schema import CategorySchema
from mysite.db.database import SessionLocal



category_router = APIRouter(prefix='/category', tags=['Category'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@category_router.post('/create')
async def category_create(category_data: CategorySchema, db: Session = Depends(get_db)):
      category_db = Category(category_name=category_data.category_name)
      db.add(category_db)
      db.commit()
      db.refresh(category_db)
      return category_db


@category_router.get('/get')
async def category_get(db: Session = Depends(get_db)):
    category_db = db.query(Category).all()
    return category_db

@category_router.get('/get/{category_id}')
async def category_get_detail(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday Category jok')
    return category_db


@category_router.put('/update/{id}')
async def category_update(category_data: CategorySchema, category_id: int,  db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday Category jok')
    category_db.category_name = category_data.category_name
    db.commit()
    db.refresh(category_db)
    return category_db

@category_router.delete('/delete/{category_id}')
async def category_delete(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if category_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday Category jok')
    db.delete(category_db)
    db.commit()
    return {'status': '200 success deleted'}








