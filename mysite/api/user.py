from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import UserProfile
from mysite.db.schema import UserProfileSchema

user_router = APIRouter(prefix='/user', tags=['UserProfile'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@user_router.get('/get')
async def get_users(db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).all()
    return user_db

@user_router.get('/get/{user_id}')
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday Adam jok')
    return user_db


@user_router.put('/put/{user_id}')
async def update_user(user_id: int, user_data: UserProfileSchema,  db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday Adam jok')
    for user_key, user_value in user_data.dict().items():
        setattr(user_db, user_key, user_value)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.delete('/delete')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Mynday Adam jok')
    db.delete(user_db)
    db.commit()
    return {'status': 'Success deleted User'}


