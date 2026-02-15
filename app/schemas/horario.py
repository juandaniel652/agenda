from pydantic import BaseModel
from typing import Optional

class HorarioBase(BaseModel):
    dia_semana: int  # 0-6
    hora_inicio: str  # "09:00"
    hora_fin: str     # "13:00"
