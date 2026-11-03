from datetime import date, datetime, time
from app.database.session import SessionLocal
from app.models import (
    Rol,
    Usuario,
    Docente,
    ProgramaAcademico,
    Estudiante,
    Asignatura,
    PeriodoAcademico,
    GrupoAcademico,
    Matricula,
    Aula,
    Horario,
    SesionClase,
    Asistencia,
    CredencialMifare,
    DispositivoLector,
    LecturaRFID,
)


def seed_database():
    db = SessionLocal()
    try:
        # Verificar si ya existen datos
        if db.query(Rol).first():
            print(
                "La base de datos ya contiene información. Omitiendo sembrado."
            )
            return

        print("Poblando la base de datos con datos de la UFPSO...")

        # 1. Roles
        rol_admin = Rol(
            nombre="Administrador",
            descripcion="Administrador del sistema Mirage Monitor",
        )
        rol_docente = Rol(
            nombre="Docente", descripcion="Docente universitario UFPSO"
        )
        db.add_all([rol_admin, rol_docente])
        db.flush()

        # 2. Usuarios y Docentes
        user_admin = Usuario(
            id_rol=rol_admin.id_rol,
            nombre="Administrador UFPSO",
            correo="admin@ufpso.edu.co",
            password_hash="pbkdf2:sha256:dummyhash123",
            activo=True,
        )
        user_docente1 = Usuario(
            id_rol=rol_docente.id_rol,
            nombre="Carlos Mario Quintero",
            correo="cmquinteroo@ufpso.edu.co",
            password_hash="pbkdf2:sha256:dummyhash123",
            activo=True,
        )
        user_docente2 = Usuario(
            id_rol=rol_docente.id_rol,
            nombre="Ingrid Patricia Arévalo",
            correo="iparevalof@ufpso.edu.co",
            password_hash="pbkdf2:sha256:dummyhash123",
            activo=True,
        )
        db.add_all([user_admin, user_docente1, user_docente2])
        db.flush()

        docente1 = Docente(
            id_usuario=user_docente1.id_usuario,
            codigo_docente="DOC-101",
            departamento="Ingeniería de Sistemas",
        )
        docente2 = Docente(
            id_usuario=user_docente2.id_usuario,
            codigo_docente="DOC-102",
            departamento="Ingeniería de Sistemas",
        )
        db.add_all([docente1, docente2])
        db.flush()

        # 3. Programas Académicos
        prog_sistemas = ProgramaAcademico(
            codigo="115", nombre="Ingeniería de Sistemas", estado=True
        )
        prog_mecanica = ProgramaAcademico(
            codigo="118", nombre="Ingeniería Mecánica", estado=True
        )
        db.add_all([prog_sistemas, prog_mecanica])
        db.flush()

        # 4. Estudiantes
        estudiantes_data = [
            (
                "1091234567",
                "Juan Diego",
                "Pérez Gómez",
                "jdperezg@ufpso.edu.co",
                prog_sistemas.id_programa,
            ),
            (
                "1097654321",
                "Maria Fernanda",
                "López Rueda",
                "mflopezr@ufpso.edu.co",
                prog_sistemas.id_programa,
            ),
            (
                "1098887766",
                "Andrés Felipe",
                "Torres Mora",
                "aftorresm@ufpso.edu.co",
                prog_sistemas.id_programa,
            ),
            (
                "1095554433",
                "Laura Camila",
                "Sánchez Vega",
                "lcsanchezv@ufpso.edu.co",
                prog_mecanica.id_programa,
            ),
            (
                "1092221100",
                "Kevin Alexis",
                "Ramírez Guerrero",
                "karamirezg@ufpso.edu.co",
                prog_sistemas.id_programa,
            ),
        ]
        estudiantes_objs = []
        for doc, nom, ape, corr, prog_id in estudiantes_data:
            est = Estudiante(
                documento=doc,
                nombres=nom,
                apellidos=ape,
                correo=corr,
                id_programa=prog_id,
                estado=True,
            )
            estudiantes_objs.append(est)
            db.add(est)
        db.flush()

        # 5. Credenciales RFID MIFARE
        uids = [
            "A3:B4:C5:D6",
            "E1:F2:12:34",
            "88:99:AA:BB",
            "11:22:33:44",
            "55:66:77:88",
        ]
        credenciales_objs = []
        for i, est in enumerate(estudiantes_objs):
            cred = CredencialMifare(
                id_estudiante=est.id_estudiante, uid=uids[i], estado="ACTIVA"
            )
            credenciales_objs.append(cred)
            db.add(cred)
        db.flush()

        # 6. Asignaturas
        asig_poo = Asignatura(
            codigo="SIS-201",
            nombre="Programación Orientada a Objetos",
            creditos=4,
        )
        asig_bd = Asignatura(
            codigo="SIS-302", nombre="Bases de Datos", creditos=3
        )
        asig_redes = Asignatura(
            codigo="SIS-401", nombre="Redes de Computadores", creditos=3
        )
        db.add_all([asig_poo, asig_bd, asig_redes])
        db.flush()

        # 7. Periodo Académico
        periodo_actual = PeriodoAcademico(
            nombre="2026-1",
            fecha_inicio=date(2026, 2, 1),
            fecha_fin=date(2026, 6, 30),
            estado=True,
        )
        db.add(periodo_actual)
        db.flush()

        # 8. Grupos Académicos
        grupo_bd_a = GrupoAcademico(
            id_asignatura=asig_bd.id_asignatura,
            id_docente=docente1.id_docente,
            id_periodo=periodo_actual.id_periodo,
            codigo_grupo="A",
            cupo=30,
        )
        grupo_poo_a = GrupoAcademico(
            id_asignatura=asig_poo.id_asignatura,
            id_docente=docente2.id_docente,
            id_periodo=periodo_actual.id_periodo,
            codigo_grupo="A",
            cupo=25,
        )
        db.add_all([grupo_bd_a, grupo_poo_a])
        db.flush()

        # 9. Matrículas
        for est in estudiantes_objs:
            mat = Matricula(
                id_estudiante=est.id_estudiante,
                id_grupo=grupo_bd_a.id_grupo,
                estado="ACTIVA",
            )
            db.add(mat)
        db.flush()

        # 10. Aula y Lectores (ubicacion sin tilde)
        aula_lab1 = Aula(
            nombre="Laboratorio Redes y BD",
            ubicacion="Edificio de Ingenierías - Lab 201",
            capacidad=35,
        )
        db.add(aula_lab1)
        db.flush()

        lector1 = DispositivoLector(
            id_aula=aula_lab1.id_aula,
            nombre="Lector Entrada Lab 201",
            numero_serie="ESP32-RFID-001",
            tipo="ESP32_RC522",
            estado="ACTIVO",
        )
        db.add(lector1)
        db.flush()

        # 11. Horario
        horario_bd = Horario(
            id_grupo=grupo_bd_a.id_grupo,
            id_aula=aula_lab1.id_aula,
            dia_semana="Martes",
            hora_inicio=time(8, 0),
            hora_fin=time(10, 0),
        )
        db.add(horario_bd)
        db.flush()

        # 12. Sesión de Clase de prueba
        ahora = datetime.now()
        sesion_hoy = SesionClase(
            id_grupo=grupo_bd_a.id_grupo,
            id_horario=horario_bd.id_horario,
            inicio_programado=ahora.replace(hour=8, minute=0, second=0, microsecond=0),
            fin_programado=ahora.replace(hour=10, minute=0, second=0, microsecond=0),
            estado="FINALIZADA",
        )
        db.add(sesion_hoy)
        db.flush()

        # 13. Lecturas RFID y Asistencias de prueba
        asist1 = Asistencia(
            id_sesion=sesion_hoy.id_sesion,
            id_estudiante=estudiantes_objs[0].id_estudiante,
            estado="Presente",
            hora_ingreso=ahora.replace(hour=8, minute=2, second=0, microsecond=0),
            registrado_por="RFID",
        )
        db.add(asist1)
        db.flush()
        lec1 = LecturaRFID(
            id_dispositivo=lector1.id_dispositivo,
            id_credencial=credenciales_objs[0].id_credencial,
            id_sesion=sesion_hoy.id_sesion,
            id_asistencia=asist1.id_asistencia,
            resultado="ACEPTADA",
        )
        db.add(lec1)

        asist2 = Asistencia(
            id_sesion=sesion_hoy.id_sesion,
            id_estudiante=estudiantes_objs[1].id_estudiante,
            estado="Tarde",
            hora_ingreso=ahora.replace(hour=8, minute=22, second=0, microsecond=0),
            registrado_por="RFID",
        )
        db.add(asist2)
        db.flush()
        lec2 = LecturaRFID(
            id_dispositivo=lector1.id_dispositivo,
            id_credencial=credenciales_objs[1].id_credencial,
            id_sesion=sesion_hoy.id_sesion,
            id_asistencia=asist2.id_asistencia,
            resultado="ACEPTADA",
        )
        db.add(lec2)

        asist3 = Asistencia(
            id_sesion=sesion_hoy.id_sesion,
            id_estudiante=estudiantes_objs[2].id_estudiante,
            estado="Ausente",
            registrado_por="MANUAL",
        )
        db.add(asist3)

        lec_rechazada = LecturaRFID(
            id_dispositivo=lector1.id_dispositivo,
            id_credencial=None,
            id_sesion=sesion_hoy.id_sesion,
            resultado="RECHAZADA",
            motivo_rechazo="Credencial desconocida",
        )
        db.add(lec_rechazada)

        db.commit()
        print("¡Base de datos sembrada con éxito!")

    except Exception as e:
        db.rollback()
        print(f"Error al sembrar la base de datos: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()