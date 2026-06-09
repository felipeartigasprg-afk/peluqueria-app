# app/models/turno.py

import enum
from datetime import date, time
from sqlalchemy import String, Date, Time, Text, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from app.models.base import TimestampMixin

# Enum para los estados posibles de un turno
# Usar un Enum evita errores de tipeo y valores inválidos
class EstadoTurno(str, enum.Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    CANCELADO = "cancelado"
    COMPLETADO = "completado"

class Turno(Base, TimestampMixin):
    """
    Representa la tabla 'turnos' en la base de datos.
    Es la tabla central del sistema — conecta clientes con servicios.
    """
    __tablename__ = "turnos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # ForeignKey vincula esta columna con el id de la tabla clientes
    # ondelete="RESTRICT" impide borrar un cliente si tiene turnos
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="RESTRICT"),
        nullable=False,
        index=True  # Índice porque vamos a filtrar turnos por cliente frecuentemente
    )

    servicio_id: Mapped[int] = mapped_column(
        ForeignKey("servicios.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    # Date guarda solo la fecha: 2024-12-25
    fecha: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # Time guarda solo la hora: 14:30:00
    hora: Mapped[time] = mapped_column(Time, nullable=False)

    # SAEnum usa el Enum de Python en PostgreSQL
    estado: Mapped[EstadoTurno] = mapped_column(
        SAEnum(EstadoTurno),
        default=EstadoTurno.PENDIENTE,
        nullable=False
    )

    notas: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relaciones — permiten acceder al cliente y servicio desde un turno
    # Ejemplo: turno.cliente.nombre
    cliente: Mapped["Cliente"] = relationship(
        "Cliente",
        back_populates="turnos"
    )
    servicio: Mapped["Servicio"] = relationship(
        "Servicio",
        back_populates="turnos"
    )

    def __repr__(self) -> str:
        return f"<Turno(id={self.id}, fecha={self.fecha}, hora={self.hora}, estado={self.estado})>"