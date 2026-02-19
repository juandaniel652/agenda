import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "uploads"

def save_image(file: UploadFile) -> str:

    if not file:
        return None

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    path = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    with open(path, "wb") as buffer:
        buffer.write(file.file.read())

    return f"/uploads/{filename}"
