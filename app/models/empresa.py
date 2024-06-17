from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class EmpresaModel(Document):
    nombre = StringField(required=True)
    fechaInicioSusc = DateTimeField(required=True)
    fechaFinSuc = DateTimeField(required=True)
    codigoEmpresa = StringField(required=True)  # el que viene del ERP

    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "fechaInicioSusc": self.fechaInicioSusc.strftime("%d-%m-%Y"),
            "fechaFinSuc": self.fechaFinSuc.strftime("%d-%m-%Y"),
            "codigoEmpresa": self.codigoEmpresa
        }
        

