
from fastapi import APIRouter, HTTPException
from mongoengine import DoesNotExist
from datetime import datetime
from bson import ObjectId
from app.models.empresa import EmpresaModel 
from app.schemas.empresa import EmpresaRequest

router = APIRouter()

@router.post("/")
async def create_empresa(empresa_data: EmpresaRequest):
    try:
        # Convertir las cadenas de texto a objetos datetime
        fecha_inicio_susc = datetime.strptime(empresa_data.fechaInicioSusc, "%d/%m/%Y")
        fecha_fin_suc = datetime.strptime(empresa_data.fechaFinSuc, "%d/%m/%Y")
        
        # Crear y guardar un nuevo documento
        nueva_empresa = EmpresaModel(
            nombre=empresa_data.nombre,
            fechaInicioSusc=fecha_inicio_susc,
            fechaFinSuc=fecha_fin_suc,
            codigoEmpresa=empresa_data.codigoEmpresa
        )
        nueva_empresa.save()
        return {"message": "Empresa creada con éxito", "empresa_id": str(nueva_empresa.id)}
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use dd/mm/yyyy.")

@router.get("/")
async def get_empresas():
    empresas = EmpresaModel.objects().all()
    empresas_serializable = [empresa.to_dict() for empresa in empresas]
    return {"empresas": empresas_serializable}  

@router.get("/{empresa_id}")
async def get_empresa(empresa_id: str):
    if not ObjectId.is_valid(empresa_id):
        raise HTTPException(status_code=400, detail="Invalid order_id format. Must be a 24-character hexadecimal string.")
    try:
        empresa = EmpresaModel.objects.get(id=ObjectId(empresa_id))
        return {"empresa": empresa.to_dict()}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")
    
    