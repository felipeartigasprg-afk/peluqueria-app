# app/models/servicio.py

from decimal import Decimal
from sqlalchemy import String, Text, Integer, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from app.models.base import TimestampMixin

class Servicio(Base, TimestampMixin):
    """
    Representa la tabla 'servicios' en la base de datos.
    Contiene los servicios que ofrece la peluquería.
    """
    __tablename__ = "servicios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)

    # Mapped[str | None] significa que puede ser NULL en la base de datos
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Duración en minutos
    duracion: Mapped[int] = mapped_column(Integer, nullable=False)

    # Numeric(10, 2) → hasta 10 dígitos en total, 2 decimales
    # Es el tipo correcto para dinero — nunca uses Float para precios
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relación con turnos
    turnos: Mapped[list["Turno"]] = relationship(
        "Turno",
        back_populates="servicio",
        lazy="select"
    )

    def __repr__(self) -> str:
        return f"<Servicio(id={self.id}, nombre={self.nombre}, precio={self.precio})>"