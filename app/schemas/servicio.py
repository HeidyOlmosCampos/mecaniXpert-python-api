from pydantic import BaseModel, Field

class ServicioRequest(BaseModel):
    nombre : str
    tarifaBase : float
    tipo: str
    codigoEmpresa : str #este es del codigo en el ERP
    idERP : str