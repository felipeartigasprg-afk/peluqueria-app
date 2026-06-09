# app/services/servicio_service.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.servicio import Servicio
from app.schemas.servicio import ServicioCreate, ServicioUpdate

def obtener_servicios(db: Session, solo_activos: bool = True) -> list[Servicio]:
    stmt = select(Servicio)
    if solo_activos:
        stmt = stmt.where(Servicio.activo == True)
    return list(db.execute(stmt).scalars().all())

def obtener_servicio_por_id(db: Session, servicio_id: int) -> Servicio:
    stmt = select(Servicio).where(Servicio.id == servicio_id)
    servicio = db.execute(stmt).scalar_one_or_none()
    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con id {servicio_id} no encontrado"
        )
    return servicio

def crear_servicio(db: Session, servicio_data: ServicioCreate) -> Servicio:
    servicio = Servicio(**servicio_data.model_dump())
    db.add(servicio)
    db.commit()
    db.refresh(servicio)
    return servicio

def actualizar_servicio(db: Session, servicio_id: int, servicio_data: ServicioUpdate) -> Servicio:
    servicio = obtener_servicio_por_id(db, servicio_id)
    datos = servicio_data.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(servicio, campo, valor)
    db.commit()
    db.refresh(servicio)
    return servicio

def eliminar_servicio(db: Session, servicio_id: int) -> dict:
    servicio = obtener_servicio_por_id(db, servicio_id)
    servicio.activo = False
    db.commit()
    return {"mensaje": "Servicio eliminado correctamente"}