
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
    
    
@router.get("/porEmpresa/{empresa_id}")
async def get_servicios_empresa(empresa_id: str):
    try:
        clientes = ServicioModel.objects.filter(empresaId=empresa_id)
        clientes_serializable = [cliente.to_dict() for cliente in clientes]
        return {"servicios": clientes_serializable}
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")
    
    
@router.get("/porEmpresaText/{empresa_id}")
async def get_servicios_empresa(empresa_id: str):
    try:
        empresa = EmpresaModel.objects.get(id=ObjectId(empresa_id))
        clientes = ServicioModel.objects.filter(empresaId=empresa_id)

        # Serializar la respuesta con el nombre de la empresa en lugar del ID y sin empresaId en los clientes
        clientes_serializable = []
        for cliente in clientes:
            cliente_dict = cliente.to_dict()
            cliente_dict.pop('idERP', None)  # Eliminar empresaId del diccionario del cliente
            cliente_dict.pop('empresaId', None)  # Eliminar empresaId del diccionario del cliente
            cliente_dict['empresa'] = empresa.nombre  # Agregar el nombre de la empresa
            clientes_serializable.append(cliente_dict)

        return {"servicios": clientes_serializable}
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")