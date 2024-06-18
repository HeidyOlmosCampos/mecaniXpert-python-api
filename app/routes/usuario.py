
from fastapi import APIRouter, HTTPException
from mongoengine import DoesNotExist
from passlib.context import CryptContext
from datetime import datetime
from bson import ObjectId
from app.models.usuario import UsuarioModel
from app.models.empresa import EmpresaModel
from app.schemas.usuario import UsuarioRequest

router = APIRouter()


# Contexto de hashing de contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Obtener hash de la contraseña
def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/")
async def create_usuario(usuario_data: UsuarioRequest):
    try:
        empresa = EmpresaModel.objects.get(codigoEmpresa=usuario_data.codigoEmpresa)
        hashed_password = get_password_hash(usuario_data.password)  # Hashear la contraseña
        nueva_usuario = UsuarioModel(
            nombre = usuario_data.nombre,
            correo = usuario_data.correo,
            password = hashed_password,
            empresaId = str(empresa.id),
            idERP = usuario_data.idERP
        )
        nueva_usuario.save()
        return {"message": "Usuario creado con éxito", "usuario_id": str(nueva_usuario.id)}
    except ValueError:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")

@router.get("/")
async def get_usuarios():
    usuarios = UsuarioModel.objects().all()
    usuarios_serializable = [usuario.to_dict() for usuario in usuarios]
    return {"usuarios": usuarios_serializable}  

@router.get("/{usuario_id}")
async def get_usuario(usuario_id: str):
    if not ObjectId.is_valid(usuario_id):
        raise HTTPException(status_code=400, detail="Invalid order_id format. Must be a 24-character hexadecimal string.")
    try:
        usuario = UsuarioModel.objects.get(id=ObjectId(usuario_id))
        return {"usuario": usuario.to_dict()}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")
    
    
@router.get("/porEmpresa/{empresa_id}")
async def get_usuarios_empresa(empresa_id: str):
    try:
        clientes = UsuarioModel.objects.filter(empresaId=empresa_id)
        clientes_serializable = [cliente.to_dict() for cliente in clientes]
        return {"usuarios": clientes_serializable}
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")