from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.api.deps import require_roles
from app.schemas.tecnico import TecnicoUpdate
from app.services.tecnico_service import TecnicoService
from app.utils.cloudinary_upload import upload_image
from typing import Optional
import json

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
        imagen_url = upload_image(imagen)

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
    nombre: str = Form(...),
    apellido: str = Form(...),
    telefono: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    duracion_turno_min: int = Form(...),
    imagen: UploadFile = File(None),
    horarios: str = Form(None),  # JSON string
    user=Depends(require_roles(["admin"]))
):

    imagen_url = None

    if imagen:
        imagen_url = upload_image(imagen)


    horarios_list = None

    if horarios:
        horarios_list = json.loads(horarios)

    data_dict = {
        "nombre": nombre,
        "apellido": apellido,
        "telefono": telefono,
        "email": email,
        "duracion_turno_min": duracion_turno_min,
    }

    if imagen_url:
        data_dict["imagen_url"] = imagen_url

    if horarios_list is not None:
        data_dict["horarios"] = horarios_list

    data = TecnicoUpdate(**data_dict)

    return TecnicoService.actualizar(id, data)

@router.delete("/{id}")
def eliminar_tecnico(
    id: str,
    user=Depends(require_roles(["admin"]))
):
    return TecnicoService.eliminar(id)
