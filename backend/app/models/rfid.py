from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class CredencialMifare(Base):
    __tablename__ = "credencial_mifare"

    id_credencial: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_estudiante: Mapped[int] = mapped_column(ForeignKey("estudiante.id_estudiante"), nullable=False)
    uid: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), default="ACTIVA")  # ACTIVA, INACTIVA, EXTRAVIADA
    fecha_asignacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_baja: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    estudiante: Mapped["Estudiante"] = relationship(back_populates="credenciales")
    lecturas: Mapped[List["LecturaRFID"]] = relationship(back_populates="credencial")


class DispositivoLector(Base):
    __tablename__ = "dispositivo_lector"

    id_dispositivo: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_aula: Mapped[int] = mapped_column(ForeignKey("aula.id_aula"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    numero_serie: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), default="ESP32_RC522")
    estado: Mapped[str] = mapped_column(String(20), default="ACTIVO")  # ACTIVO, INACTIVO, MANTENIMIENTO

    aula: Mapped["Aula"] = relationship(back_populates="dispositivos")
    lecturas: Mapped[List["LecturaRFID"]] = relationship(back_populates="dispositivo")


class LecturaRFID(Base):
    __tablename__ = "lectura_rfid"

    id_lectura: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_dispositivo: Mapped[int] = mapped_column(ForeignKey("dispositivo_lector.id_dispositivo"), nullable=False)
    id_credencial: Mapped[Optional[int]] = mapped_column(ForeignKey("credencial_mifare.id_credencial"), nullable=True)
    id_sesion: Mapped[Optional[int]] = mapped_column(ForeignKey("sesion_clase.id_sesion"), nullable=True)
    id_asistencia: Mapped[Optional[int]] = mapped_column(ForeignKey("asistencia.id_asistencia"), nullable=True)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    resultado: Mapped[str] = mapped_column(String(20), nullable=False)  # ACEPTADA, RECHAZADA
    motivo_rechazo: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    dispositivo: Mapped["DispositivoLector"] = relationship(back_populates="lecturas")
    credencial: Mapped[Optional["CredencialMifare"]] = relationship(back_populates="lecturas")
    sesion: Mapped[Optional["SesionClase"]] = relationship(back_populates="lecturas")
    asistencia: Mapped[Optional["Asistencia"]] = relationship(back_populates="lecturas")