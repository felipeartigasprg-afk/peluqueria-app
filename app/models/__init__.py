# app/models/__init__.py

# Importamos todos los modelos para que Alembic los detecte automáticamente
# Cada vez que creemos un modelo nuevo lo agregamos aquí
from app.models.cliente import Cliente
from app.models.servicio import Servicio
from app.models.turno import Turno, EstadoTurno
from app.models.administrador import Administrador
from app.models.horario import Horario