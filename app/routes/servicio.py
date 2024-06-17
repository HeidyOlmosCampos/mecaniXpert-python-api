
from fastapi import APIRouter, HTTPException
from mongoengine import DoesNotExist
from datetime import datetime
from bson import ObjectId
from app.models.servicio import ServicioModel
from app.models.empresa import EmpresaModel
from app.schemas.servicio import ServicioRequest

router = APIRouter()

@router.post("/")
async def create_servicio(servicio_data: ServicioRequest):
    try:
        empresa = EmpresaModel.objects.get(codigoEmpresa=servicio_data.codigoEmpresa)
        nuevo_servicio = ServicioModel(
            nombre = servicio_data.nombre,
            tarifaBase = servicio_data.tarifaBase,
            tipo = servicio_data.tipo,
            empresaId = str(empresa.id),
            idERP = servicio_data.idERP
        )
        nuevo_servicio.save()
        return {"message": "Servicio creado con éxito", "servicio_id": str(nuevo_servicio.id)}
    except ValueError:
        raise HTTPException(status_code=400, detail="No se pudo crear el servicio")

@router.get("/")
async def get_servicios():
    servicios = ServicioModel.objects().all()
    servicio_serializable = [servicio.to_dict() for servicio in servicios]
    return {"servicios": servicio_serializable}  

@router.get("/{servicio_id}")
async def get_servicio(servicio_id: str):
    if not ObjectId.is_valid(servicio_id):
        raise HTTPException(status_code=400, detail="Invalid order_id format. Must be a 24-character hexadecimal string.")
    try:
        servicio = ServicioModel.objects.get(id=ObjectId(servicio_id))
        return {"servicio": servicio.to_dict()}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")
    
    