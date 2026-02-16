from pydantic import BaseModel
from datetime import time

class HorarioBase(BaseModel):
    dia_semana: int
    hora_inicio: time
    hora_fin: time
