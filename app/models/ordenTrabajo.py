# app/models/orders.py

from mongoengine import Document, StringField, DateTimeField, BooleanField, ObjectIdField
from bson import ObjectId
    
class OrdenTrabajoModel(Document):
    
    estado = StringField(required=True) # en estado FINALIZADO
    codSeguimiento = StringField(required=True)
    fechaInicio = DateTimeField(required=True)
    fechaFin = DateTimeField(required=True)
    empresaId = StringField(required=True)  
    clienteId = StringField(required=True)  
    empleadoId = StringField(required=True)  
    servicioId = StringField(required=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "estado" : self.estado, 
            "codSeguimiento" : self.codSeguimiento,
            "fechaInicio" : self.fechaInicio.strftime("%d-%m-%Y"), 
            "fechaFin" : self.fechaFin.strftime("%d-%m-%Y"), 
            "empresaId" : self.empresaId,   
            "clienteId" : self.clienteId,  
            "empleadoId" : self.empleadoId, 
            "servicioId" : self.servicioId
        }