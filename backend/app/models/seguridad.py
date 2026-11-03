from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Rol(Base):
    __tablename__ = "rol"

    id_rol: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    usuarios: Mapped[List["Usuario"]] = relationship(back_populates="rol")


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_rol: Mapped[int] = mapped_column(ForeignKey("rol.id_rol"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    rol: Mapped["Rol"] = relationship(back_populates="usuarios")
    docente: Mapped[Optional["Docente"]] = relationship(back_populates="usuario", uselist=False)


class Docente(Base):
    __tablename__ = "docente"

    id_docente: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"), unique=True, nullable=False)
    codigo_docente: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    departamento: Mapped[str] = mapped_column(String(100), nullable=False)

    usuario: Mapped["Usuario"] = relationship(back_populates="docente")
    grupos: Mapped[List["GrupoAcademico"]] = relationship(back_populates="docente")