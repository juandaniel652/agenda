from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload
from app.models.turno import Turno
from app.schemas.turno import TurnoCreate
from app.models.tecnico_disponibilidad import TecnicoDisponibilidad
from app.models.tecnico import Tecnico as TecnicoModel
from datetime import datetime, timezone, timedelta


class TurnoService:

    @staticmethod
    def obtener_todos(db: Session):
    
        turnos = db.query(Turno).options(
        
            joinedload(Turno.cliente),
            joinedload(Turno.tecnico)
    
        ).all()
    
        return turnos
    
    @staticmethod
    def obtener_sugerencias(db, tecnico_id, dias=3):

        hoy = datetime.now().date()
        resultados = []

        tecnico = db.query(TecnicoModel).filter(
            TecnicoModel.id == tecnico_id
        ).first()

        if not tecnico:
            return []

        for i in range(1, 30):

            fecha = hoy + timedelta(days=i)

            slots = TurnoService.obtener_disponibilidad(
                db,
                tecnico_id,
                fecha
            )

            if slots:
                resultados.append({
                    "fecha": fecha,
                    "slots": slots
                })

            if len(resultados) == dias:
                break

        return resultados


    @staticmethod
    def crear(db: Session, turno_data: TurnoCreate):

        conflicto = db.query(Turno).filter(

            Turno.tecnico_id == turno_data.tecnico_id,

            Turno.fecha == turno_data.fecha,

            Turno.estado != "Cancelado",

            Turno.hora_inicio < turno_data.hora_fin,

            Turno.hora_fin > turno_data.hora_inicio

        ).first()

        if conflicto:

            raise Exception(
                "El técnico ya tiene un turno en ese horario"
            )

        turno = Turno(**turno_data.dict())

        db.add(turno)

        db.commit()

        db.refresh(turno)

        return turno
    
    @staticmethod
    
    @staticmethod
    def obtener_disponibilidad(db, tecnico_id, fecha, t=1):
        """
        Devuelve solo los slots disponibles de t bloques consecutivos
        para un técnico en una fecha.
        """
        dia_semana = fecha.weekday()

        disponibilidades = db.query(TecnicoDisponibilidad).filter(
            TecnicoDisponibilidad.tecnico_id == tecnico_id,
            TecnicoDisponibilidad.dia_semana == dia_semana
        ).all()

        if not disponibilidades:
            return []

        tecnico = db.query(TecnicoModel).filter(
            TecnicoModel.id == tecnico_id
        ).first()

        duracion = tecnico.duracion_turno_min  # duración de cada bloque

        # 1. Turnos ocupados
        turnos_ocupados = db.query(Turno).filter(
            Turno.tecnico_id == tecnico_id,
            Turno.fecha == fecha,
            Turno.estado != "Cancelado"
        ).all()

        # 2. Generar slots posibles
        slots = []
        for disp in disponibilidades:
            inicio = datetime.combine(fecha, disp.hora_inicio)
            fin = datetime.combine(fecha, disp.hora_fin)

            while inicio + timedelta(minutes=duracion) <= fin:
                slot_inicio = inicio.time()
                slot_fin = (inicio + timedelta(minutes=duracion)).time()

                conflicto = any(
                    t.hora_inicio < slot_fin and t.hora_fin > slot_inicio
                    for t in turnos_ocupados
                )

                if not conflicto:
                    slots.append(slot_inicio.strftime("%H:%M"))

                inicio += timedelta(minutes=duracion)

        # 3. Buscar secuencias de t bloques consecutivos
        slots_consecutivos = []
        for i in range(len(slots) - t + 1):
            secuencia = slots[i:i+t]
            # Chequear si son consecutivos
            consecutivos = True
            for j in range(1, t):
                h1, m1 = map(int, secuencia[j-1].split(":"))
                h2, m2 = map(int, secuencia[j].split(":"))
                dt1 = h1*60 + m1
                dt2 = h2*60 + m2
                if dt2 - dt1 != duracion:
                    consecutivos = False
                    break
            if consecutivos:
                slots_consecutivos.append(secuencia[0])  # solo el inicio de la secuencia

        return slots_consecutivos

    @staticmethod
    def obtener_sugerencias(db, tecnico_id, dias=3, t=1):
        """
        Devuelve hasta `dias` fechas con slots de `t` bloques consecutivos.
        Solo la primera fecha con slots suficientes.
        """
        hoy = datetime.now().date()
        tecnico = db.query(TecnicoModel).filter(
            TecnicoModel.id == tecnico_id
        ).first()

        if not tecnico:
            return []

        resultados = []

        for i in range(1, 30):
            fecha = hoy + timedelta(days=i)
            slots = TurnoService.obtener_disponibilidad(db, tecnico_id, fecha, t)

            if slots:
                resultados.append({
                    "fecha": fecha,
                    "slots": slots
                })

            if len(resultados) == dias:
                break

        return resultados
    
    
    @staticmethod
    def eliminar(db: Session, turno_id):
    
        turno = db.query(Turno).filter(
            Turno.id == turno_id
        ).first()
    
        if not turno:
            raise Exception("Turno no encontrado")
    
        turno.estado = "Cancelado"
        turno.cancelado_en = datetime.now(timezone.utc)
    
        db.commit()
        db.refresh(turno)
    
        return turno