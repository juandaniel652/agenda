from typing import Annotated
from pydantic import BaseModel, StringConstraints

HoraStr = Annotated[str, StringConstraints(pattern=r"^\d{2}:\d{2}:\d{2}$")]

class HorarioBase(BaseModel):
    dia_semana: int
    hora_inicio: HoraStr
    hora_fin: HoraStr
