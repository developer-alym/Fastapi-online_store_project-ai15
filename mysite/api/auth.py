from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from mysite.db.database import SessionLocal
from mysite.db.models import UserProfile
from mysite.db.schema import UserProfileRegistrationSchema, UserProfileLoginSchema
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

auth_router = APIRouter(prefix='/auth', tags=['Authorization'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="bearer")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


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
    if not user_db or verify_password(user.password, user_db.password):
        raise HTTPException(status_code=401, detail='username же password туура эмес')
    return {'status': 'Ийгиликтуу аккаунтка кирдин'}




