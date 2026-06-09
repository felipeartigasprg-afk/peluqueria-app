# app/models/administrador.py

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base
from app.models.base import TimestampMixin

class Administrador(Base, TimestampMixin):
    """
    Representa la tabla 'administradores' en la base de datos.
    Nunca guardamos la contraseña en texto plano, siempre el hash.
    """
    __tablename__ = "administradores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    usuario: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    # Guardamos el hash, nunca la contraseña original
    contrasena_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Administrador(id={self.id}, usuario={self.usuario})>"