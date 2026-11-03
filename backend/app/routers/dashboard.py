from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.session import get_db
from app.models import (
    Estudiante,
    Docente,
    GrupoAcademico,
    ProgramaAcademico,
    Asistencia,
    LecturaRFID,
    DispositivoLector,
    Aula,
    CredencialMifare,
)
from app.schemas.dashboard import (
    DashboardResponse,
    ResumenTotales,
    EstadisticasAsistencia,
    LecturaRFIDResumen,
    DispositivoEstado,
)

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=DashboardResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):
    # 1. Conteo global de entidades académicas
    total_estudiantes = db.query(func.count(Estudiante.id_estudiante)).scalar() or 0
    total_docentes = db.query(func.count(Docente.id_docente)).scalar() or 0
    total_grupos = db.query(func.count(GrupoAcademico.id_grupo)).scalar() or 0
    total_programas = db.query(func.count(ProgramaAcademico.id_programa)).scalar() or 0

    # 2. Conteo de asistencias registradas en el sistema
    presentes = db.query(func.count(Asistencia.id_asistencia)).filter(Asistencia.estado == "Presente").scalar() or 0
    tarde = db.query(func.count(Asistencia.id_asistencia)).filter(Asistencia.estado == "Tarde").scalar() or 0
    ausentes = db.query(func.count(Asistencia.id_asistencia)).filter(Asistencia.estado == "Ausente").scalar() or 0
    justificados = db.query(func.count(Asistencia.id_asistencia)).filter(Asistencia.estado == "Justificado").scalar() or 0

    total_registros = presentes + tarde + ausentes + justificados

    # Cálculo del porcentaje de asistencia efectiva (Presentes + Tarde)
    if total_registros > 0:
        porcentaje_asistencia = round(((presentes + tarde) / total_registros) * 100, 2)
    else:
        porcentaje_asistencia = 0.0

    # 3. Consultar las últimas 10 lecturas RFID registradas
    lecturas_query = (
        db.query(LecturaRFID, DispositivoLector, Aula, Estudiante)
        .join(DispositivoLector, LecturaRFID.id_dispositivo == DispositivoLector.id_dispositivo)
        .join(Aula, DispositivoLector.id_aula == Aula.id_aula)
        .outerjoin(CredencialMifare, LecturaRFID.id_credencial == CredencialMifare.id_credencial)
        .outerjoin(Estudiante, CredencialMifare.id_estudiante == Estudiante.id_estudiante)
        .order_by(LecturaRFID.fecha_hora.desc())
        .limit(10)
        .all()
    )

    ultimas_lecturas = []
    for lec, disp, aula, est in lecturas_query:
        nombre_estudiante = f"{est.nombres} {est.apellidos}" if est else "Desconocido"
        uid_tarjeta = lec.credencial.uid if lec.credencial else "N/A"
        ultimas_lecturas.append(
            LecturaRFIDResumen(
                id_lectura=lec.id_lectura,
                dispositivo=disp.nombre,
                aula=aula.nombre,
                estudiante=nombre_estudiante,
                uid=uid_tarjeta,
                resultado=lec.resultado,
                motivo_rechazo=lec.motivo_rechazo,
                fecha_hora=lec.fecha_hora,
            )
        )

    # 4. Estado actual de los dispositivos lectores RFID
    dispositivos_query = (
        db.query(DispositivoLector, Aula)
        .join(Aula, DispositivoLector.id_aula == Aula.id_aula)
        .all()
    )

    dispositivos_estado = [
        DispositivoEstado(
            id_dispositivo=d.id_dispositivo,
            nombre=d.nombre,
            aula=a.nombre,
            estado=d.estado,
        )
        for d, a in dispositivos_query
    ]

    return DashboardResponse(
        totales=ResumenTotales(
            total_estudiantes=total_estudiantes,
            total_docentes=total_docentes,
            total_grupos=total_grupos,
            total_programas=total_programas,
        ),
        asistencia=EstadisticasAsistencia(
            presentes=presentes,
            tarde=tarde,
            ausentes=ausentes,
            justificados=justificados,
            total_registros=total_registros,
            porcentaje_asistencia=porcentaje_asistencia,
        ),
        ultimas_lecturas_rfid=ultimas_lecturas,
        dispositivos_rfid=dispositivos_estado,
    )