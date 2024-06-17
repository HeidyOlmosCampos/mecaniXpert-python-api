from mongoengine import Document, StringField

class UsuarioModel(Document):
    nombre = StringField(required=True)
    correo = StringField(required=True)
    contraseña = StringField(required=True)
    empresaId = StringField(required=True)  
    idERP = StringField(required=True)# el que le de en el ERP

    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "correo": self.correo,
            "contraseña": self.contraseña,
            "empresaId": self.empresaId,
            "idERP": self.idERP
        }
        

