
from fastapi import APIRouter, HTTPException
from mongoengine import DoesNotExist
from bson import ObjectId
from app.models.cliente import ClienteModel
from app.models.empresa import EmpresaModel
from app.schemas.cliente import ClienteRequest

router = APIRouter()

@router.post("/")
async def create_cliente(cliente_data: ClienteRequest):
    try:
        empresa = EmpresaModel.objects.get(idERP=cliente_data.codigoEmpresa)
        nuevo_cliente = ClienteModel(
            nombre = cliente_data.nombre,
            empresaId = str(empresa.id),
            idERP = cliente_data.idERP
        )
        nuevo_cliente.save()
        return {"message": "Cliente creado con éxito", "cliente_id": str(nuevo_cliente.id)}
    except ValueError:
        raise HTTPException(status_code=400, detail="No se pudo crear el cliente")

@router.get("/")
async def get_clientes():
    usuarios = ClienteModel.objects().all()
    clientes_serializable = [cliente.to_dict() for cliente in usuarios]
    return {"usuarios": clientes_serializable}  

@router.get("/{cliente_id}")
async def get_cliente(cliente_id: str):
    if not ObjectId.is_valid(cliente_id):
        raise HTTPException(status_code=400, detail="Invalid order_id format. Must be a 24-character hexadecimal string.")
    try:
        cliente = ClienteModel.objects.get(id=ObjectId(cliente_id))
        return {"cliente": cliente.to_dict()}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")
    
    