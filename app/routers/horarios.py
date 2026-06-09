# app/routers/horarios.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.database import get_db
from app.models.horario import Horario
from app.schemas.horario import HorarioCreate, HorarioResponse, DIAS_SEMANA
from app.services.auth_service import obtener_admin_actual

router = APIRouter(prefix="/api/horarios", tags=["Horarios"])

@router.get("/", response_model=list[HorarioResponse])
def listar_horarios(db: Session = Depends(get_db)):
    stmt = select(Horario).where(Horario.activo == True).order_by(Horario.dia_semana)
    horarios = list(db.execute(stmt).scalars().all())
    for h in horarios:
        h.dia_nombre = DIAS_SEMANA.get(h.dia_semana)
    return horarios

@router.post("/", response_model=HorarioResponse, status_code=201)
def crear_horario(
    horario_data: HorarioCreate,
    db: Session = Depends(get_db),
    _=Depends(obtener_admin_actual)
):
    horario = Horario(**horario_data.model_dump())
    db.add(horario)
    db.commit()
    db.refresh(horario)
    return horario

@router.delete("/{horario_id}")
def eliminar_horario(
    horario_id: int,
    db: Session = Depends(get_db),
    _=Depends(obtener_admin_actual)
):
    stmt = select(Horario).where(Horario.id == horario_id)
    horario = db.execute(stmt).scalar_one_or_none()
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    horario.activo = False
    db.commit()
    return {"mensaje": "Horario eliminado correctamente"}