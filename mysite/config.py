from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

ACCESS_EXPIRE_TOKEN = 60
REFRESH_EXPIRE_TOKEN = 3
ALGORITHM = 'HS256'

