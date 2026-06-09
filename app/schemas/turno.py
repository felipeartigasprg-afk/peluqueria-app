# app/schemas/turno.py

from datetime import date, time, datetime
from decimal import Decimal
from pydantic import BaseModel, field_validator
from app.models.turno import EstadoTurno

class TurnoBase(BaseModel):
    cliente_id: int
    servicio_id: int
    fecha: date
    hora: time
    notas: str | None = None

    @field_validator("fecha")
    @classmethod
    def validar_fecha(cls, v: date) -> date:
        from datetime import date as date_type
        if v < date_type.today():
            raise ValueError("No se pueden reservar turnos en fechas pasadas")
        return v

class TurnoCreate(TurnoBase):
    pass

class TurnoUpdate(BaseModel):
    fecha: date | None = None
    hora: time | None = None
    estado: EstadoTurno | None = None
    notas: str | None = None

class TurnoResponse(TurnoBase):
    id: int
    estado: EstadoTurno
    fecha_creacion: datetime
    cliente: "ClienteResumen | None" = None
    servicio: "ServicioResumen | None" = None

    model_config = {"from_attributes": True}

class ClienteResumen(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str
    telefono: str
    model_config = {"from_attributes": True}

class ServicioResumen(BaseModel):
    id: int
    nombre: str
    duracion: int
    precio: "Decimal"
    model_config = {"from_attributes": True}

TurnoResponse.model_rebuild()

