# app/schemas/cliente.py

from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
import re

class ClienteBase(BaseModel):
    """Campos compartidos entre creación y respuesta."""
    nombre: str
    apellido: str
    telefono: str
    email: EmailStr  # Pydantic valida que sea un email válido automáticamente

    @field_validator("nombre", "apellido")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError("Debe tener al menos 2 caracteres")
        return v.strip().title()  # Capitaliza correctamente: "juan" → "Juan"

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, v: str) -> str:
        # Solo permite números, espacios, guiones y el signo +
        if not re.match(r'^[\d\s\-\+]{7,20}$', v):
            raise ValueError("Teléfono inválido")
        return v.strip()

class ClienteCreate(ClienteBase):
    """Esquema para crear un cliente — solo recibe estos campos."""
    pass

class ClienteUpdate(BaseModel):
    """Esquema para actualizar — todos los campos son opcionales."""
    nombre: str | None = None
    apellido: str | None = None
    telefono: str | None = None
    email: EmailStr | None = None

class ClienteResponse(ClienteBase):
    """Esquema de respuesta — incluye campos generados por el sistema."""
    id: int
    activo: bool
    fecha_creacion: datetime

    model_config = {"from_attributes": True}  # Permite convertir modelos SQLAlchemy a Pydantic