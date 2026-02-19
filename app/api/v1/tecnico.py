from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.api.deps import require_roles
from app.schemas.tecnico import TecnicoUpdate
from app.services.tecnico_service import TecnicoService
from app.utils.file_upload import save_image

router = APIRouter(
    prefix="/tecnicos",
    tags=["Tecnicos"]
)

@router.post("/")
def crear_tecnico(
    nombre: str = Form(...),
    apellido: str = Form(...),
    telefono: str = Form(None),
    email: str = Form(None),
    duracion_turno_min: int = Form(...),
    imagen: UploadFile = File(None),
    user=Depends(require_roles(["admin"]))
):

    imagen_url = None

    if imagen:
        imagen_url = save_image(imagen)

    return TecnicoService.crear_tecnico({
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "email": email,
        "duracion_turno_min": duracion_turno_min,
        "imagen_url": imagen_url
    })

@router.get("/")
def listar_tecnicos(
    user=Depends(require_roles(["admin"]))
):
    return TecnicoService.listar()

@router.put("/{id}")
def actualizar_tecnico(
    id: str,
    data: TecnicoUpdate,
    user=Depends(require_roles(["admin"]))
):
    print("USANDO TecnicoUpdate")
    print(data)
    return TecnicoService.actualizar(id, data)

@router.delete("/{id}")
def eliminar_tecnico(
    id: str,
    user=Depends(require_roles(["admin"]))
):
    return TecnicoService.eliminar(id)
