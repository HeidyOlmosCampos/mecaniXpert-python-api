from pydantic import BaseModel, Field

class EmpresaRequest(BaseModel):
    nombre: str = Field(..., example="Mi Empresa")
    fechaInicioSusc: str = Field(..., example="12/05/2024")
    fechaFinSuc: str = Field(..., example="12/05/2024")
    codigoEmpresa: str = Field(..., example="ERP12345") #el que viene del erp
