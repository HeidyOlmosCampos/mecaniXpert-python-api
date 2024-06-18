# app/main.py

from fastapi import FastAPI
from mongoengine import connect
from dotenv import load_dotenv
import os
from app.routes import *


# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URI de MongoDB desde las variables de entorno
mongodb_uri = os.getenv("MONGODB_URI")

# Conectar a MongoDB usando mongoengine
connect(host=mongodb_uri)

# Crear instancia de FastAPI
app = FastAPI()

# Importar y usar las rutas definidas en el archivo routes/__init__.py

app.include_router(empresa_router, tags=["Empresas"], prefix="/empresas")
app.include_router(usuario_router, tags=["Usuarios"], prefix="/usuarios")
app.include_router(cliente_router, tags=["Clientes"], prefix="/clientes")
app.include_router(servicio_router, tags=["Servicios"], prefix="/servicios")
app.include_router(empleado_router, tags=["Empleados"], prefix="/empleados")
app.include_router(orden_trabajo_router, tags=["Ordenes"], prefix="/ordenes")
app.include_router(kpis_router, tags=["Kpis"], prefix="/kpis")
app.include_router(auth_router, tags=["auth"], prefix="/auth")

