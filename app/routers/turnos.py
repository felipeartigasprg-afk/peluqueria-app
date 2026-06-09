# app/routers/turnos.py

from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.turno import TurnoCreate, TurnoUpdate, TurnoResponse
from app.services import turno_service
from app.services.auth_service import obtener_admin_actual

router = APIRouter(prefix="/api/turnos", tags=["Turnos"])

@router.get("/", response_model=list[TurnoResponse])
def listar_turnos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _=Depends(obtener_admin_actual)
):
    return turno_service.obtener_turnos(db, skip, limit)

@router.get("/disponibles/{fecha}/{servicio_id}")
def horarios_disponibles(
    fecha: date,
    servicio_id: int,
    db: Session = Depends(get_db)
):
    slots = turno_service.obtener_horarios_disponibles(db, fecha, servicio_id)
    return {"fecha": str(fecha), "horarios_disponibles": slots}

@router.get("/{turno_id}", response_model=TurnoResponse)
def obtener_turno(turno_id: int, db: Session = Depends(get_db)):
    return turno_service.obtener_turno_por_id(db, turno_id)

@router.post("/", response_model=TurnoResponse, status_code=201)
def crear_turno(turno_data: TurnoCreate, db: Session = Depends(get_db)):
    return turno_service.crear_turno(db, turno_data)

@router.put("/{turno_id}", response_model=TurnoResponse)
def actualizar_turno(
    turno_id: int,
    turno_data: TurnoUpdate,
    db: Session = Depends(get_db),
    _=Depends(obtener_admin_actual)
):
    return turno_service.actualizar_turno(db, turno_id, turno_data)

@router.delete("/{turno_id}/cancelar", response_model=TurnoResponse)
def cancelar_turno(turno_id: int, db: Session = Depends(get_db)):
    return turno_service.cancelar_turno(db, turno_id)