import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

async def guardar_imagen(imagen: UploadFile | None):

    if not imagen:
        return None

    extension = imagen.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"

    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        buffer.write(await imagen.read())

    return f"/uploads/{filename}"
