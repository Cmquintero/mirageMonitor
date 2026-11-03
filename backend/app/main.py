from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.session import get_db, engine
from app.database.base import Base
import app.models
from app.routers import dashboard

# Crear las tablas en PostgreSQL si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mirage Monitor API",
    description="Sistema de gestión de asistencia y seguimiento académico - UFPSO",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar Routers de la API
app.include_router(dashboard.router)


@app.get("/", tags=["General"])
def read_root():
    return {
        "sistema": "Mirage Monitor API",
        "estado": "Operativo",
        "institucion": "UFPSO",
    }


@app.get("/health", tags=["General"])
def health_check():
    return {"status": "ok"}


@app.get("/health/db", tags=["General"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT version();")).scalar()
        return {
            "status": "Conexión a PostgreSQL exitosa",
            "version_pg": result,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al conectar con la base de datos: {str(e)}",
        )