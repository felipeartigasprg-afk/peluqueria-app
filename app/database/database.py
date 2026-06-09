# app/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Motor de conexión a PostgreSQL
# El engine es el punto de entrada de SQLAlchemy a la base de datos
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Muestra las queries SQL en consola durante desarrollo
    pool_pre_ping=True,   # Verifica que la conexión esté activa antes de usarla
    pool_size=10,         # Número de conexiones simultáneas en el pool
    max_overflow=20       # Conexiones extra permitidas si el pool está lleno
)

# Fábrica de sesiones
# Cada sesión es una unidad de trabajo con la base de datos
# autocommit=False significa que debemos confirmar los cambios manualmente
# autoflush=False significa que no envía cambios automáticamente
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Clase base para todos los modelos
# Todos los modelos van a heredar de esta clase
class Base(DeclarativeBase):
    pass

# Dependencia de FastAPI para inyectar la sesión en las rutas
# Esto garantiza que la sesión se cierre siempre, incluso si hay errores
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()