# app/services/cliente_service.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

def obtener_clientes(db: Session, skip: int = 0, limit: int = 100) -> list[Cliente]:
    """Retorna todos los clientes activos."""
    stmt = select(Cliente).where(Cliente.activo == True).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def obtener_cliente_por_id(db: Session, cliente_id: int) -> Cliente:
    """Retorna un cliente por su ID o lanza error 404."""
    stmt = select(Cliente).where(Cliente.id == cliente_id, Cliente.activo == True)
    cliente = db.execute(stmt).scalar_one_or_none()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con id {cliente_id} no encontrado"
        )
    return cliente

def obtener_cliente_por_email(db: Session, email: str) -> Cliente | None:
    """Retorna un cliente por email o None si no existe."""
    stmt = select(Cliente).where(Cliente.email == email)
    return db.execute(stmt).scalar_one_or_none()

def crear_cliente(db: Session, cliente_data: ClienteCreate) -> Cliente:
    """Crea un nuevo cliente verificando que el email no esté registrado."""
    # Verificar email duplicado
    if obtener_cliente_por_email(db, cliente_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente registrado con ese email"
        )
    cliente = Cliente(**cliente_data.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)  # Recarga el objeto con los datos generados por la BD (id, fecha)
    return cliente

def actualizar_cliente(db: Session, cliente_id: int, cliente_data: ClienteUpdate) -> Cliente:
    """Actualiza los datos de un cliente."""
    cliente = obtener_cliente_por_id(db, cliente_id)
    # model_dump(exclude_unset=True) solo incluye los campos que el usuario envió
    datos = cliente_data.model_dump(exclude_unset=True)
    for campo, valor in datos.items():
        setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente

def eliminar_cliente(db: Session, cliente_id: int) -> dict:
    """Soft delete — marca el cliente como inactivo en lugar de borrarlo."""
    cliente = obtener_cliente_por_id(db, cliente_id)
    cliente.activo = False
    db.commit()
    return {"mensaje": "Cliente eliminado correctamente"}