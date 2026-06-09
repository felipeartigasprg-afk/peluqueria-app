# app/services/auth_service.py

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.models.administrador import Administrador
from app.schemas.administrador import AdministradorCreate, LoginRequest, TokenResponse
from app.core.config import settings
from app.database.database import get_db

# Contexto para hashear contraseñas con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hashear_contrasena(contrasena: str) -> str:
    """Convierte una contraseña en texto plano a un hash seguro."""
    return pwd_context.hash(contrasena)

def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    """Verifica si una contraseña coincide con su hash."""
    return pwd_context.verify(contrasena_plana, contrasena_hash)

def crear_token(data: dict) -> str:
    """Genera un token JWT con expiración."""
    datos = data.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    datos.update({"exp": expiracion})
    return jwt.encode(datos, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def crear_administrador(db: Session, admin_data: AdministradorCreate) -> Administrador:
    """Crea un administrador hasheando su contraseña."""
    stmt = select(Administrador).where(Administrador.usuario == admin_data.usuario)
    if db.execute(stmt).scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )
    admin = Administrador(
        nombre=admin_data.nombre,
        usuario=admin_data.usuario,
        email=admin_data.email,
        contrasena_hash=hashear_contrasena(admin_data.contrasena)
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

def login(db: Session, login_data: LoginRequest) -> TokenResponse:
    """Verifica las credenciales y retorna un token JWT."""
    stmt = select(Administrador).where(
        Administrador.usuario == login_data.usuario,
        Administrador.activo == True
    )
    admin = db.execute(stmt).scalar_one_or_none()
    if not admin or not verificar_contrasena(login_data.contrasena, admin.contrasena_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    token = crear_token({"sub": str(admin.id), "usuario": admin.usuario})
    from app.schemas.administrador import AdministradorResponse
    return TokenResponse(
        access_token=token,
        administrador=AdministradorResponse.model_validate(admin)
    )

def obtener_admin_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Administrador:
    """Dependencia de FastAPI que verifica el token y retorna el admin autenticado."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        admin_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    stmt = select(Administrador).where(
        Administrador.id == admin_id,
        Administrador.activo == True
    )
    admin = db.execute(stmt).scalar_one_or_none()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Administrador no encontrado"
        )
    return admin