# app/schemas/administrador.py

from datetime import datetime
from pydantic import BaseModel, EmailStr

class AdministradorBase(BaseModel):
    nombre: str
    usuario: str
    email: EmailStr

class AdministradorCreate(AdministradorBase):
    contrasena: str  # Recibimos la contraseña en texto plano y la hasheamos en el servicio

class AdministradorResponse(AdministradorBase):
    id: int
    activo: bool
    fecha_creacion: datetime
    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    usuario: str
    contrasena: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    administrador: AdministradorResponse