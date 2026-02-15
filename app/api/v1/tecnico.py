from fastapi import APIRouter, Depends
from uuid import UUID
from app.api.deps import require_roles
from app.schemas.tecnico import TecnicoCreate, TecnicoUpdate
from app.services.tecnico_service import TecnicoService

router = APIRouter(
    prefix="/tecnicos",
    tags=["Tecnicos"]
)

@router.post("/")
def crear_tecnico(
    data: TecnicoCreate,
    user = Depends(require_roles(["admin"]))
):
    return TecnicoService.crear_tecnico(data)

@router.get("/")
def listar_tecnicos(
    user = Depends(require_roles(["admin"]))
):
    return TecnicoService.listar()

@router.put("/{id}")
def actualizar_tecnico(
    id: UUID,
    data: TecnicoUpdate,
    user = Depends(require_roles(["admin"]))
):
    return TecnicoService.actualizar(id, data)

@router.delete("/{id}")
def eliminar_tecnico(
    id: UUID,
    user = Depends(require_roles(["admin"]))
):
    return TecnicoService.eliminar(id)
