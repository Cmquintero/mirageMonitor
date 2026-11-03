from datetime import date, datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Date, DateTime, Boolean, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ProgramaAcademico(Base):
    __tablename__ = "programa_academico"

    id_programa: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, default=True)

    estudiantes: Mapped[List["Estudiante"]] = relationship(back_populates="programa")


class Estudiante(Base):
    __tablename__ = "estudiante"

    id_estudiante: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    documento: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    id_programa: Mapped[int] = mapped_column(ForeignKey("programa_academico.id_programa"), nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, default=True)

    programa: Mapped["ProgramaAcademico"] = relationship(back_populates="estudiantes")
    matriculas: Mapped[List["Matricula"]] = relationship(back_populates="estudiante")
    credenciales: Mapped[List["CredencialMifare"]] = relationship(back_populates="estudiante")
    asistencias: Mapped[List["Asistencia"]] = relationship(back_populates="estudiante")


class Asignatura(Base):
    __tablename__ = "asignatura"

    id_asignatura: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    creditos: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("creditos > 0", name="chk_creditos_positivos"),
    )

    grupos: Mapped[List["GrupoAcademico"]] = relationship(back_populates="asignatura")


class PeriodoAcademico(Base):
    __tablename__ = "periodo_academico"

    id_periodo: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date] = mapped_column(Date, nullable=False)
    estado: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint("fecha_fin > fecha_inicio", name="chk_fechas_periodo"),
    )

    grupos: Mapped[List["GrupoAcademico"]] = relationship(back_populates="periodo")


class GrupoAcademico(Base):
    __tablename__ = "grupo_academico"

    id_grupo: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_asignatura: Mapped[int] = mapped_column(ForeignKey("asignatura.id_asignatura"), nullable=False)
    id_docente: Mapped[int] = mapped_column(ForeignKey("docente.id_docente"), nullable=False)
    id_periodo: Mapped[int] = mapped_column(ForeignKey("periodo_academico.id_periodo"), nullable=False)
    codigo_grupo: Mapped[str] = mapped_column(String(10), nullable=False)
    cupo: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("cupo > 0", name="chk_cupo_positivo"),
        UniqueConstraint("id_asignatura", "id_periodo", "codigo_grupo", name="uq_grupo_periodo"),
    )

    asignatura: Mapped["Asignatura"] = relationship(back_populates="grupos")
    docente: Mapped["Docente"] = relationship(back_populates="grupos")
    periodo: Mapped["PeriodoAcademico"] = relationship(back_populates="grupos")
    matriculas: Mapped[List["Matricula"]] = relationship(back_populates="grupo")
    horarios: Mapped[List["Horario"]] = relationship(back_populates="grupo")
    sesiones: Mapped[List["SesionClase"]] = relationship(back_populates="grupo")


class Matricula(Base):
    __tablename__ = "matricula"

    id_matricula: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_estudiante: Mapped[int] = mapped_column(ForeignKey("estudiante.id_estudiante"), nullable=False)
    id_grupo: Mapped[int] = mapped_column(ForeignKey("grupo_academico.id_grupo"), nullable=False)
    fecha_matricula: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    estado: Mapped[str] = mapped_column(String(20), default="ACTIVA")

    __table_args__ = (
        UniqueConstraint("id_estudiante", "id_grupo", name="uq_estudiante_grupo"),
    )

    estudiante: Mapped["Estudiante"] = relationship(back_populates="matriculas")
    grupo: Mapped["GrupoAcademico"] = relationship(back_populates="matriculas")