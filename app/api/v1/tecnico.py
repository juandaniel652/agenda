from fastapi import APIRouter, Depends
from app.api.deps import require_roles
from app.schemas.tecnico import TecnicoCreate
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
