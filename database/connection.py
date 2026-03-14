import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Try to get DATABASE_URL from environment, fallback to .env
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:zzIQdiQoTkiRQPKYmwAGBaoXWqNuJjHq@autorack.proxy.rlwy.net:19017/railway"
)

# Ensure the connection uses proper settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connection before using
    pool_recycle=3600,   # Recycle connections every hour
    echo=False           # Set to True for debugging
)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)