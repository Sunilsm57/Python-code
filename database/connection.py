import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Try to get DATABASE_URL from environment, fallback to .env
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:zzIQdiQoTkiRQPKYmwAGBaoXWqNuJjHq@postgres.railway.internal:5432/railway"
)

# Log database connection info (masked password)
if "@" in DATABASE_URL:
    masked_url = DATABASE_URL.split("@")[0].rsplit(":", 1)[0] + ":***@" + DATABASE_URL.split("@")[1]
else:
    masked_url = DATABASE_URL

logger.info(f"Connecting to database: {masked_url}")

# Check for problematic hostname
if "postgres.railway.internal" in DATABASE_URL:
    logger.warning("⚠️  WARNING: Using internal Railway hostname (postgres.railway.internal)")
    logger.warning("   This will NOT work. Use the PUBLIC DATABASE_URL instead!")
    logger.warning("   Check Railway dashboard for DATABASE_PUBLIC_URL")

try:
    # Ensure the connection uses proper settings
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,      # Verify connection before using
        pool_recycle=3600,       # Recycle connections every hour
        pool_size=5,             # Number of connections to keep in pool
        max_overflow=10,         # Maximum overflow connections
        echo=False,              # Set to True for debugging SQL queries
        connect_args={
            "connect_timeout": 10,  # 10 second timeout for connections
            "keepalives": 1,        # Enable TCP keepalive
            "keepalives_idle": 30,  # Start keepalive after 30 seconds idle
        }
    )
    
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    logger.info("✅ Database engine created successfully")
    
except Exception as e:
    logger.error(f"❌ Failed to create database engine: {e}")
    raise