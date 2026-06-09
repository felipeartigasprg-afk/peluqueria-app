# app/models/base.py

from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base

class TimestampMixin:
    """
    Mixin que agrega columnas de auditoría a todos los modelos.
    Un Mixin es una clase que agrega funcionalidad sin ser un modelo completo.
    """
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # PostgreSQL pone la fecha automáticamente
        nullable=False
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),  # Se actualiza automáticamente al modificar el registro
        nullable=False
    )