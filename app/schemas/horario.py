# app/schemas/horario.py

from datetime import time
from pydantic import BaseModel, field_validator

DIAS_SEMANA = {
    0: "Lunes", 1: "Martes", 2: "Miércoles",
    3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"
}

class HorarioBase(BaseModel):
    dia_semana: int
    hora_inicio: time
    hora_fin: time

    @field_validator("dia_semana")
    @classmethod
    def validar_dia(cls, v: int) -> int:
        if v < 0 or v > 6:
            raise ValueError("El día debe ser entre 0 (Lunes) y 6 (Domingo)")
        return v

    @field_validator("hora_fin")
    @classmethod
    def validar_horas(cls, v: time, info) -> time:
        if "hora_inicio" in info.data and v <= info.data["hora_inicio"]:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")
        return v

class HorarioCreate(HorarioBase):
    pass

class HorarioResponse(HorarioBase):
    id: int
    activo: bool
    dia_nombre: str | None = None
    model_config = {"from_attributes": True}