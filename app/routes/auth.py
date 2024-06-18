from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from mongoengine import DoesNotExist
from app.models.usuario import UsuarioModel
from app.utils.jwt_utils import create_jwt_token, decode_jwt_token

router = APIRouter()

# Contexto de hashing de contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Verificar contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Obtener hash de la contraseña
def get_password_hash(password):
    return pwd_context.hash(password)

# Autenticar usuario
def authenticate_user(correo: str, password: str):
    try:
        user = UsuarioModel.objects.get(correo=correo)
        if user and verify_password(password, user.password):
            return user
    except DoesNotExist:
        return None
    return None

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Correo o contraseña incorrectos"
        )
    # Generar token JWT
    access_token = create_jwt_token(user.id)
    return {"access_token": access_token,"correo": user.correo, "empresaId":user.empresaId}

@router.get("/me")
async def read_users_me(current_user: UsuarioModel = Depends(oauth2_scheme)):
    try:
        user = UsuarioModel.objects.get(id=current_user.id)
        return {"nombre": user.nombre, "correo": user.correo}
    except DoesNotExist:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )


