
from fastapi import APIRouter, HTTPException
from mongoengine import DoesNotExist
from bson import ObjectId
from app.models.empleado import EmpleadoModel
from app.models.empresa import EmpresaModel
from app.schemas.empleado import EmpleadoRequest

router = APIRouter()

@router.post("/")
async def create_empleado(empleado_data: EmpleadoRequest):
    try:
        empresa = EmpresaModel.objects.get(codigoEmpresa=empleado_data.codigoEmpresa)
        nuevo_empleado = EmpleadoModel(
            nombre = empleado_data.nombre,
            empresaId = str(empresa.id),
            idERP = empleado_data.idERP
        )
        nuevo_empleado.save()
        return {"message": "Empleado creado con éxito", "empleado_id": str(nuevo_empleado.id)}
    except ValueError:
        raise HTTPException(status_code=400, detail="No se pudo crear el empleado")

@router.get("/")
async def get_empleados():
    empleados = EmpleadoModel.objects().all()
    empleados_serializable = [empleado.to_dict() for empleado in empleados]
    return {"empleados": empleados_serializable}  

@router.get("/{empleado_id}")
async def get_empleado(empleado_id: str):
    if not ObjectId.is_valid(empleado_id):
        raise HTTPException(status_code=400, detail="Invalid order_id format. Must be a 24-character hexadecimal string.")
    try:
        empleado = EmpleadoModel.objects.get(id=ObjectId(empleado_id))
        return {"empleado": empleado.to_dict()}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")
    
    