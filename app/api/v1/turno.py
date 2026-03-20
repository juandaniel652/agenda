from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID
from datetime import date
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
    
    
@router.get("/disponibilidad")
def obtener_disponibilidad(
    tecnico_id: UUID,
    fecha: date,
    db: Session = Depends(get_db),

):
    tecnico = db.query(TecnicoModel).filter(TecnicoModel.id == tecnico_id).first()
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico no encontrado")
    if not tecnico.activo:
        raise HTTPException(status_code=400, detail="El técnico no está activo")

    slots = TurnoService.obtener_disponibilidad(db, tecnico_id, fecha)

    return {
        "tecnico_id": str(tecnico_id),
        "tecnico_nombre": tecnico.nombre,
        "fecha": fecha,
        "slots_disponibles": slots,
        "total_slots": len(slots),
        "siguiente_paso": {
            "accion": "Elegí un slot y usá el endpoint de creación",
            "endpoint": "POST /api/v1/turnos/",
            "body_ejemplo": {
                "numero_ticket": "TK-00001",
                "cliente_id": "uuid-del-cliente",
                "tecnico_id": str(tecnico_id),
                "tipo_turno": 1,
                "rango_horario": "M",
                "fecha": str(fecha),
                "hora_inicio": slots[0] if slots else "09:00",
                "hora_fin": "09:15",
                "estado": "Abierto"
            }
        }
    }


@router.get("/sugerencias")
def obtener_sugerencias(
    tecnico_id: UUID,
    db: Session = Depends(get_db)
):
    sugerencias = TurnoService.obtener_sugerencias(db, tecnico_id)

    return {
        "tecnico_id": tecnico_id,
        "sugerencias": sugerencias
    }


@router.get("/menu")
def obtener_menu(
    db: Session = Depends(get_db),
    user=Depends(require_roles(["admin"]))
):
    from datetime import date, timedelta

    # Técnicos activos
    tecnicos = db.query(TecnicoModel).filter(TecnicoModel.activo == True).all()

    tecnicos_con_slots = []
    for tecnico in tecnicos:
        # Próximos 3 días con disponibilidad
        sugerencias = TurnoService.obtener_sugerencias(db, tecnico.id, dias=3)
        tecnicos_con_slots.append({
            "tecnico_id": str(tecnico.id),
            "tecnico_nombre": tecnico.nombre,
            "proximas_disponibilidades": sugerencias
        })

    return {
        "opciones": [
            {
                "id": 1,
                "accion": "verificar_horario",
                "descripcion": "Verificar disponibilidad de un técnico en una fecha puntual",
                "endpoint": "GET /api/v1/turnos/disponibilidad?tecnico_id=...&fecha=YYYY-MM-DD"
            },
            {
                "id": 2,
                "accion": "ver_sugerencias",
                "descripcion": "Ver próximas fechas disponibles por técnico",
                "endpoint": "GET /api/v1/turnos/sugerencias?tecnico_id=..."
            },
            {
                "id": 3,
                "accion": "crear_turno",
                "descripcion": "Grabar una visita ya verificada",
                "endpoint": "POST /api/v1/turnos/"
            }
        ],
        "tecnicos_activos": tecnicos_con_slots
    }