from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:ts123@localhost:5432/sekolah_db")
JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-key-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 1440
