from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import UserProfile, RefreshToken
from mysite.db.schema import UserProfileRegistrationSchema, UserProfileLoginSchema
from fastapi.security import OAuth2PasswordBearer,  OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta
from datetime import datetime
from typing import Optional
from mysite.config import ACCESS_EXPIRE_TOKEN, REFRESH_EXPIRE_TOKEN, SECRET_KEY, ALGORITHM
from jose import jwt

auth_router = APIRouter(prefix='/auth', tags=['Authorization'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = (datetime.utcnow()) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_EXPIRE_TOKEN))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data:dict):
    return create_access_token(data=data, expires_delta=timedelta(days=REFRESH_EXPIRE_TOKEN))


@auth_router.post('/register')
async def register(user: UserProfileRegistrationSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if user_db:
        raise HTTPException(status_code=400, detail='Mynday adam Registration bolgon')

    hash_password = get_password_hash(user.password)
    user_data = UserProfile(
    username=user.username,
    first_name=user.first_name,
    last_name=user.last_name,
    age=user.age,
    phone_number=user.phone_number,
    profile_image=user.profile_image,
    password=hash_password,
    created_at=user.created_at
    )

    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return {'status': 'Сен регистрация болдун'}

@auth_router.post('/login')
async def login(user:UserProfileLoginSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.username == user.username).first()
    if not user_db:
        raise HTTPException(status_code=401, detail='username туура эмес')
    if not verify_password(user.password, user_db.password):
        raise HTTPException(status_code=401, detail='password туура эмес')
    refresh_token = create_refresh_token({'sub': user_db.username})
    access_token = create_access_token({'sub': user_db.username})
    refresh_user = RefreshToken(user_id=user_db.id, token=refresh_token)
    db.add(refresh_user)
    db.commit()
    db.refresh(refresh_user)

    return {
        'access_token': access_token,
        'refresh_token0': refresh_token,
        'type': 'bearer'
    }

@auth_router.post('/logout')
async def logout(token: str, db: Session = Depends(get_db)):
    token_db = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not token_db:
        raise HTTPException(status_code=404, detail='Maalymat tuura emes')
    db.delete(token_db)
    db.commit()
    return {'message': 'Success 200 ok'}




