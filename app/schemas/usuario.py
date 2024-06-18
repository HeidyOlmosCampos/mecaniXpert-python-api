from pydantic import BaseModel, Field

class UsuarioRequest(BaseModel):
    nombre : str
    correo : str
    password : str
    codigoEmpresa : str #este es del codigo en el ERP
    idERP : str