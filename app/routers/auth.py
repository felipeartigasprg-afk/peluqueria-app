# app/routers/auth.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.administrador import AdministradorCreate, AdministradorResponse, LoginRequest, TokenResponse
from app.services import auth_service
from app.services.auth_service import obtener_admin_actual
from app.models.administrador import Administrador

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, login_data)

@router.post("/registro", response_model=AdministradorResponse, status_code=201)
def registrar_admin(
    admin_data: AdministradorCreate,
    db: Session = Depends(get_db)
):
    return auth_service.crear_administrador(db, admin_data)

@router.get("/me", response_model=AdministradorResponse)
def obtener_perfil(admin: Administrador = Depends(obtener_admin_actual)):
    return admin