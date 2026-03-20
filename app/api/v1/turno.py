from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from datetime import date, datetime, timedelta
from app.models.turno import Turno
from typing import Optional
from pydantic import BaseModel
from app.models.tecnico import Tecnico as TecnicoModel
from app.db.session import get_db
from app.schemas.turno import TurnoCreate, TurnoResponse, EstadoTurnoEnum
from app.services.turno_service import TurnoService
from app.models.turno import Turno
from app.api.deps import get_db, require_roles
from app.models.tecnico_disponibilidad import TecnicoDisponibilidad
from fastapi import Query

router = APIRouter(prefix="/turnos", tags=["Turnos"])


class PatchEstadoSchema(BaseModel):
    estado: EstadoTurnoEnum


@router.get("/", response_model=list[TurnoResponse])
def obtener_turnos(
    fecha: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    query = (
        select(Turno)
        .join(TecnicoModel, Turno.tecnico_id == TecnicoModel.id)
        .where(TecnicoModel.activo == True)  # ← excluir técnicos inactivos
    )
    if fecha:
        query = query.where(Turno.fecha == fecha)

    turnos = db.execute(query).scalars().all()
    return [t for t in turnos if t.estado != "Cancelado"]


@router.post("/", response_model=TurnoResponse)
def crear_turno(
    turno: TurnoCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin"]))
):
    # Verificar que el técnico existe y está activo
    tecnico = db.query(TecnicoModel).filter(TecnicoModel.id == turno.tecnico_id).first()
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")
    if not tecnico.activo:
        raise HTTPException(status_code=400, detail="El técnico no está activo")

    try:
        nuevo_turno = TurnoService.crear(db, turno)
        return nuevo_turno
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{turno_id}/estado", response_model=TurnoResponse)
def actualizar_estado_turno(
    turno_id: UUID,
    body: PatchEstadoSchema,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin"])),  # ← agregar esto
):
    turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    turno.estado = body.estado.value
    db.commit()
    db.refresh(turno)
    return turno


@router.patch("/{turno_id}/cancelar")
def cancelar_turno(
    turno_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin"])),  # ← agregar esto
):
    try:
        TurnoService.eliminar(db, turno_id)
        return {"message": "Turno cancelado"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    
@staticmethod
def obtener_disponibilidad(db, tecnico_id, fecha, t=1):
    # Python weekday(): 0=lun, 1=mar, 2=mie, 3=jue, 4=vie, 5=sab, 6=dom
    # Front JS:         0=dom, 1=lun, 2=mar, 3=mie, 4=jue, 5=vie, 6=sab
    dia_python = fecha.weekday()
    dia_front = (dia_python + 1) % 7  # lun→1, mar→2, ... dom→0

    disponibilidades = db.query(TecnicoDisponibilidad).filter(
        TecnicoDisponibilidad.tecnico_id == tecnico_id,
        TecnicoDisponibilidad.dia_semana == dia_front
    ).all()

    if not disponibilidades:
        return []

    tecnico = db.query(TecnicoModel).filter(
        TecnicoModel.id == tecnico_id
    ).first()

    duracion = tecnico.duracion_turno_min

    turnos_ocupados = db.query(Turno).filter(
        Turno.tecnico_id == tecnico_id,
        Turno.fecha == fecha,
        Turno.estado != "Cancelado"
    ).all()

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

    # Buscar secuencias de t bloques consecutivos
    slots_consecutivos = []
    for i in range(len(slots) - t + 1):
        secuencia = slots[i:i+t]
        consecutivos = True
        for j in range(1, t):
            h1, m1 = map(int, secuencia[j-1].split(":"))
            h2, m2 = map(int, secuencia[j].split(":"))
            if (h2*60 + m2) - (h1*60 + m1) != duracion:
                consecutivos = False
                break
        if consecutivos:
            slots_consecutivos.append(secuencia[0])

    return slots_consecutivos



@staticmethod
def obtener_sugerencias(db, tecnico_id, dias=3, t=1):
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

@router.get("/menu")
def obtener_menu(db: Session = Depends(get_db)):
    tecnicos = db.query(TecnicoModel).filter(TecnicoModel.activo == True).all()

    tecnicos_con_slots = []
    for tecnico in tecnicos:
        sugerencias = TurnoService.obtener_sugerencias(db, tecnico.id, dias=3)
        tecnicos_con_slots.append({
            "tecnico_id": str(tecnico.id),
            "tecnico_nombre": tecnico.nombre,
            "tecnico_apellido": tecnico.apellido,
            "proximas_disponibilidades": sugerencias,
            "link_disponibilidad": f"https://agenda-1-zomu.onrender.com/api/v1/turnos/disponibilidad?tecnico_id={tecnico.id}&fecha=HOY",
            "link_sugerencias": f"https://agenda-1-zomu.onrender.com/api/v1/turnos/sugerencias?tecnico_id={tecnico.id}"
        })

    return {
        "opciones": [
            {
                "id": 1,
                "accion": "verificar_horario",
                "descripcion": "Verificar disponibilidad en una fecha puntual",
                "ejemplo": f"https://agenda-1-zomu.onrender.com/api/v1/turnos/disponibilidad?tecnico_id=8cd6183e-9069-4f0a-9654-4aae20ca21ef&fecha=2026-03-25"
            },
            {
                "id": 2,
                "accion": "ver_sugerencias",
                "descripcion": "Ver próximas fechas disponibles automáticamente",
                "ejemplo": f"https://agenda-1-zomu.onrender.com/api/v1/turnos/sugerencias?tecnico_id=8cd6183e-9069-4f0a-9654-4aae20ca21ef"
            },
            {
                "id": 3,
                "accion": "crear_turno",
                "descripcion": "Grabar una visita (requiere token de admin)",
                "endpoint": "POST https://agenda-1-zomu.onrender.com/api/v1/turnos/",
                "body_ejemplo": {
                    "numero_ticket": "TK-00001",
                    "cliente_id": "uuid-del-cliente",
                    "tecnico_id": "uuid-del-tecnico",
                    "tipo_turno": 1,
                    "rango_horario": "M",
                    "fecha": "2026-03-25",
                    "hora_inicio": "09:00",
                    "hora_fin": "09:15",
                    "estado": "Abierto"
                }
            }
        ],
        "tecnicos_activos": tecnicos_con_slots
    }