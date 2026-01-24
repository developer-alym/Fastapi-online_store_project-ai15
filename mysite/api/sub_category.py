from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import SubCategory
from mysite.db.schema import SubCategorySchema

sub_category_router = APIRouter(prefix='/sub_category', tags=['SubCategory'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@sub_category_router.post('/create')
async def create_sub_category(sub_data: SubCategorySchema, db: Session = Depends(get_db)):
    sub_db = SubCategory(**sub_data.dict())
    db.add(sub_db)
    db.commit()
    db.refresh(sub_db)
    return sub_db


@sub_category_router.get('/get')
async def get_sub(db: Session = Depends(get_db)):
    sub_db = db.query(SubCategory).all()
    return sub_db




