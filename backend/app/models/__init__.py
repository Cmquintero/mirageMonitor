from app.models.seguridad import Rol, Usuario, Docente
from app.models.academico import (
    ProgramaAcademico,
    Estudiante,
    Asignatura,
    PeriodoAcademico,
    GrupoAcademico,
    Matricula,
)
from app.models.clases import Aula, Horario, SesionClase, Asistencia
from app.models.rfid import CredencialMifare, DispositivoLector, LecturaRFID

__all__ = [
    "Rol",
    "Usuario",
    "Docente",
    "ProgramaAcademico",
    "Estudiante",
    "Asignatura",
    "PeriodoAcademico",
    "GrupoAcademico",
    "Matricula",
    "Aula",
    "Horario",
    "SesionClase",
    "Asistencia",
    "CredencialMifare",
    "DispositivoLector",
    "LecturaRFID",
]