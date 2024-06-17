from mongoengine import Document, StringField, FloatField

class ServicioModel(Document):
    nombre = StringField(required=True)
    tarifaBase = FloatField(required=True)
    tipo = StringField(required=True) #Taller - Chaperio
    empresaId = StringField(required=True)  
    idERP = StringField(required=True)# el del ERP

    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "tarifaBase": self.tarifaBase,
            "tipo": self.tipo,
            "empresaId": self.empresaId,
            "idERP": self.idERP
        }
        

