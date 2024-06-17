from pydantic import BaseModel, Field

class ClienteRequest(BaseModel):
    nombre : str
    codigoEmpresa : str #este es del codigo en el ERP
    idERP : str