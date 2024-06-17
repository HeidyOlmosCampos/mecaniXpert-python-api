from mongoengine import Document, StringField

class ClienteModel(Document):
    nombre = StringField(required=True)    
    empresaId = StringField(required=True)  
    idERP = StringField(required=True)# el que le de en el ERP

    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "empresaId": self.empresaId,
            "idERP": self.idERP
        }
        

