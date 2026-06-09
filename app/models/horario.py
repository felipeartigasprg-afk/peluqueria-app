# app/models/horario.py

from datetime import time
from sqlalchemy import Integer, Time, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base
from app.models.base import TimestampMixin

class Horario(Base, TimestampMixin):
    """
    Representa los horarios de atención de la peluquería.
    dia_semana: 0=Lunes, 1=Martes, ..., 6=Domingo
    """
    __tablename__ = "horarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    dia_semana: Mapped[int] = mapped_column(Integer, nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Horario(dia={self.dia_semana}, inicio={self.hora_inicio}, fin={self.hora_fin})>"