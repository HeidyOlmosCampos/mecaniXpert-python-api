# app/routes/__init__.py

from .empresa import router as empresa_router
from .usuario import router as usuario_router
from .cliente import router as cliente_router
from .servicio import router as servicio_router
from .empleado import router as empleado_router
from .ordenTrabajo import router as orden_trabajo_router
from .kpis import router as kpis_router
from .auth import router as auth_router

# Importa aquí otras rutas si las tienes

__all__ = [
    "empresa_router",
    "usuario_router",
    "cliente_router",
    "servicio_router",
    "empleado_router",
    "orden_trabajo_router",
    "kpis_router",
    "auth_router"
    
]
