# app/models/cliente.py

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from app.models.base import TimestampMixin

class Cliente(Base, TimestampMixin):
    """
    Representa la tabla 'clientes' en la base de datos.
    Hereda de Base (requerido por SQLAlchemy) y de TimestampMixin
    (agrega fecha_creacion y fecha_actualizacion automáticamente).
    """
    __tablename__ = "clientes"

    # Clave primaria — SQLAlchemy la autoincrementa automáticamente
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Mapped[str] significa que esta columna es obligatoria (NOT NULL)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)

    # unique=True significa que no puede haber dos clientes con el mismo email
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)

    # Mapped[bool] con default True — el cliente está activo al registrarse
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relación con turnos — un cliente puede tener muchos turnos
    # back_populates conecta esta relación con la del modelo Turno
    # lazy="select" significa que los turnos se cargan cuando se necesitan
    turnos: Mapped[list["Turno"]] = relationship(
        "Turno",
        back_populates="cliente",
        lazy="select"
    )

    def __repr__(self) -> str:
        return f"<Cliente(id={self.id}, nombre={self.nombre} {self.apellido})>"