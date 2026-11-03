from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ResumenTotales(BaseModel):
    total_estudiantes: int
    total_docentes: int
    total_grupos: int
    total_programas: int


class EstadisticasAsistencia(BaseModel):
    presentes: int
    tarde: int
    ausentes: int
    justificados: int
    total_registros: int
    porcentaje_asistencia: float


class LecturaRFIDResumen(BaseModel):
    id_lectura: int
    dispositivo: str
    aula: str
    estudiante: Optional[str] = "Desconocido"
    uid: Optional[str] = "N/A"
    resultado: str
    motivo_rechazo: Optional[str] = None
    fecha_hora: datetime

    class Config:
        from_attributes = True


class DispositivoEstado(BaseModel):
    id_dispositivo: int
    nombre: str
    aula: str
    estado: str


class DashboardResponse(BaseModel):
    totales: ResumenTotales
    asistencia: EstadisticasAsistencia
    ultimas_lecturas_rfid: List[LecturaRFIDResumen]
    dispositivos_rfid: List[DispositivoEstado]