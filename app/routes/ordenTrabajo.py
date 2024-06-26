
from fastapi import APIRouter, HTTPException
from mongoengine import DoesNotExist
from datetime import datetime
from bson import ObjectId
from app.models.ordenTrabajo import OrdenTrabajoModel
from app.models.empresa import EmpresaModel
from app.models.cliente import ClienteModel
from app.models.empleado import EmpleadoModel
from app.models.servicio import ServicioModel
from app.schemas.ordenTrabajo import OrdenTrabajoRequest

router = APIRouter()

@router.post("/")
async def create_orden(orden_data: OrdenTrabajoRequest):
    try:
        #recuperar los ID's correctos
        empresa = EmpresaModel.objects.get(codigoEmpresa=orden_data.codigoEmpresa)
        cliente = ClienteModel.objects.get(idERP=orden_data.codigoCliente)
        empleado = EmpleadoModel.objects.get(idERP=orden_data.codigoEmpleado)
        servicio = ServicioModel.objects.get(idERP=orden_data.codigoServicio)
        
        # Convertir las cadenas de texto a objetos datetime
        fecha_inicio = datetime.strptime(orden_data.fechaInicio, "%d/%m/%Y")
        fecha_fin = datetime.strptime(orden_data.fechaFin, "%d/%m/%Y")
        
        nueva_orden = OrdenTrabajoModel(         
            estado = orden_data.estado,
            codSeguimiento = orden_data.codSeguimiento,
            fechaInicio = fecha_inicio,
            fechaFin = fecha_fin,
            empresaId = str(empresa.id),
            clienteId = str(cliente.id),
            empleadoId = str(empleado.id), 
            servicioId = str(servicio.id)
        )
        nueva_orden.save()
        return {"message": "Orden de trabajo creado con éxito", "orden_id": str(nueva_orden.id)}
    except ValueError:
        raise HTTPException(status_code=400, detail="No se pudo crear la orden de trabajo")

@router.get("/")
async def get_ordenes():
    ordenes = OrdenTrabajoModel.objects().all()
    ordenes_serializable = [orden.to_dict() for orden in ordenes]
    return {"ordenes": ordenes_serializable}  

@router.get("/{orden_id}")
async def get_orden(orden_id: str):
    if not ObjectId.is_valid(orden_id):
        raise HTTPException(status_code=400, detail="Invalid order_id format. Must be a 24-character hexadecimal string.")
    try:
        orden = OrdenTrabajoModel.objects.get(id=ObjectId(orden_id))
        return {"orden": orden.to_dict()}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")
    
    
@router.get("/porEmpresa/{empresa_id}")
async def get_ordenes_empresa(empresa_id: str):
    try:
        clientes = OrdenTrabajoModel.objects.filter(empresaId=empresa_id)
        clientes_serializable = [cliente.to_dict() for cliente in clientes]
        return {"ordenes": clientes_serializable}
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")
    
@router.get("/porEmpresaText/{empresa_id}")
async def get_ordenes_empresa(empresa_id: str):
    try:
        empresa = EmpresaModel.objects.get(id=ObjectId(empresa_id))
        ordenes = OrdenTrabajoModel.objects.filter(empresaId=empresa_id)
        
    
        ordenes_serializable = []
        for orden in ordenes:
            orden_dict = orden.to_dict()
            
            # Obtener el nombre del servicio
            try:
                servicio = ServicioModel.objects.get(id=ObjectId(orden_dict['servicioId']))
                orden_dict['servicio'] = servicio.nombre
            except ServicioModel.DoesNotExist:
                orden_dict['servicio'] = None  # O manejarlo de otra manera
            
            # Obtener el nombre del empleado
            try:
                empleado = EmpleadoModel.objects.get(id=ObjectId(orden_dict['empleadoId']))
                orden_dict['empleado'] = empleado.nombre
            except EmpleadoModel.DoesNotExist:
                orden_dict['empleado'] = None  # O manejarlo de otra manera
            
            # Agregar el nombre de la empresa
            orden_dict['empresa'] = empresa.nombre
            
            # Eliminar los campos clienteId, servicioId, empleadoId y empresaId
            orden_dict.pop('empresaId', None)  
            orden_dict.pop('clienteId', None)
            orden_dict.pop('empleadoId', None)
            orden_dict.pop('servicioId', None) 
            orden_dict.pop('id', None)           
            
            ordenes_serializable.append(orden_dict)
        
        return {"ordenes": ordenes_serializable}
    
    
    
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")
    