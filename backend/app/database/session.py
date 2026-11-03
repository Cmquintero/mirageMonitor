from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Muestra en consola las consultas SQL generadas (ideal para desarrollo)
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """Inyección de dependencia para obtener la sesión de base de datos en los endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()