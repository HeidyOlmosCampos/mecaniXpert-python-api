from pydantic import BaseModel, Field

class EmpleadoRequest(BaseModel):
    nombre : str
    codigoEmpresa : str #este es del codigo en el ERP
    idERP : str