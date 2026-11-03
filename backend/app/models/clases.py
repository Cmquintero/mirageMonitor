from datetime import time, datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Time, DateTime, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Aula(Base):
    __tablename__ = "aula"

    id_aula: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)  # Ej: "Sistemas 1"
    ubicacion: Mapped[str] = mapped_column(String(100), nullable=False)
    capacidad: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("capacidad > 0", name="chk_capacidad_aula_positiva"),
    )

    horarios: Mapped[List["Horario"]] = relationship(back_populates="aula")
    dispositivos: Mapped[List["DispositivoLector"]] = relationship(back_populates="aula")


class Horario(Base):
    __tablename__ = "horario"

    id_horario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_grupo: Mapped[int] = mapped_column(ForeignKey("grupo_academico.id_grupo"), nullable=False)
    id_aula: Mapped[int] = mapped_column(ForeignKey("aula.id_aula"), nullable=False)
    dia_semana: Mapped[str] = mapped_column(String(15), nullable=False)  # Lunes, Martes...
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)

    __table_args__ = (
        CheckConstraint("hora_fin > hora_inicio", name="chk_rango_horario"),
    )

    grupo: Mapped["GrupoAcademico"] = relationship(back_populates="horarios")
    aula: Mapped["Aula"] = relationship(back_populates="horarios")
    sesiones: Mapped[List["SesionClase"]] = relationship(back_populates="horario")


class SesionClase(Base):
    __tablename__ = "sesion_clase"

    id_sesion: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_grupo: Mapped[int] = mapped_column(ForeignKey("grupo_academico.id_grupo"), nullable=False)
    id_horario: Mapped[Optional[int]] = mapped_column(ForeignKey("horario.id_horario"), nullable=True)
    inicio_programado: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fin_programado: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="PROGRAMADA")  # PROGRAMADA, EN_CURSO, FINALIZADA, CANCELADA

    grupo: Mapped["GrupoAcademico"] = relationship(back_populates="sesiones")
    horario: Mapped[Optional["Horario"]] = relationship(back_populates="sesiones")
    asistencias: Mapped[List["Asistencia"]] = relationship(back_populates="sesion")
    lecturas: Mapped[List["LecturaRFID"]] = relationship(back_populates="sesion")


class Asistencia(Base):
    __tablename__ = "asistencia"

    id_asistencia: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_sesion: Mapped[int] = mapped_column(ForeignKey("sesion_clase.id_sesion"), nullable=False)
    id_estudiante: Mapped[int] = mapped_column(ForeignKey("estudiante.id_estudiante"), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)  # Presente, Tarde, Ausente, Justificado
    hora_ingreso: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    registrado_por: Mapped[str] = mapped_column(String(20), default="RFID")  # RFID o MANUAL

    __table_args__ = (
        UniqueConstraint("id_sesion", "id_estudiante", name="uq_asistencia_estudiante_sesion"),
        CheckConstraint("estado IN ('Presente', 'Tarde', 'Ausente', 'Justificado')", name="chk_estado_asistencia"),
    )

    sesion: Mapped["SesionClase"] = relationship(back_populates="asistencias")
    estudiante: Mapped["Estudiante"] = relationship(back_populates="asistencias")
    lecturas: Mapped[List["LecturaRFID"]] = relationship(back_populates="asistencia")