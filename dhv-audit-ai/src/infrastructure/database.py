import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/dhv_audit"
)

# Configura o engine de conex?o. Em ambientes de alta al?ada e produ??o, exige-se conex?es SSL.
connect_args = {}
if "postgresql" in DATABASE_URL and os.getenv("DB_REQUIRE_SSL", "false").lower() == "true":
    connect_args = {"sslmode": "require"}

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency generator para sess?es do FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
