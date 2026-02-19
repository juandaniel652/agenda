import os
from uuid import uuid4
from fastapi import UploadFile

BASE_URL = os.getenv("BASE_URL", "https://agenda-1-zomu.onrender.com")
if not BASE_URL:
    raise ValueError("BASE_URL no configurado")

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(file: UploadFile) -> str:

    ext = file.filename.split(".")[-1]

    filename = f"{uuid4()}.{ext}"

    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return f"{BASE_URL}/uploads/{filename}"
