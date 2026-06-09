# app/routers/servicios.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.servicio import ServicioCreate, ServicioUpdate, ServicioResponse
from app.services import servicio_service
from app.services.auth_service import obtener_admin_actual

router = APIRouter(prefix="/api/servicios", tags=["Servicios"])

@router.get("/", response_model=list[ServicioResponse])
def listar_servicios(db: Session = Depends(get_db)):
    return servicio_service.obtener_servicios(db)

@router.get("/{servicio_id}", response_model=ServicioResponse)
def obtener_servicio(servicio_id: int, db: Session = Depends(get_db)):
    return servicio_service.obtener_servicio_por_id(db, servicio_id)

@router.post("/", response_model=ServicioResponse, status_code=201)
def crear_servicio(
    servicio_data: ServicioCreate,
    db: Session = Depends(get_db),
    _=Depends(obtener_admin_actual)
):
    return servicio_service.crear_servicio(db, servicio_data)

@router.put("/{servicio_id}", response_model=ServicioResponse)
def actualizar_servicio(
    servicio_id: int,
    servicio_data: ServicioUpdate,
    db: Session = Depends(get_db),
    _=Depends(obtener_admin_actual)
):
    return servicio_service.actualizar_servicio(db, servicio_id, servicio_data)

@router.delete("/{servicio_id}")
def eliminar_servicio(
    servicio_id: int,
    db: Session = Depends(get_db),
    _=Depends(obtener_admin_actual)
):
    return servicio_service.eliminar_servicio(db, servicio_id)