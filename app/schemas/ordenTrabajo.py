from pydantic import BaseModel, Field

class OrdenTrabajoRequest(BaseModel):
    estado : str 
    codSeguimiento : str
    fechaInicio : str 
    fechaFin : str 
    codigoEmpresa : str  #este es del codigo en el ERP
    codigoCliente : str  #este es del codigo en el ERP
    codigoEmpleado : str #este es del codigo en el ERP
    codigoServicio : str #este es del codigo en el ERP