from mongoengine import connect
from dotenv import load_dotenv

# load_csv_to_db.py
import pandas as pd
from datetime import datetime
import os
from models.empresa import EmpresaModel
from models.cliente import ClienteModel
from models.empleado import EmpleadoModel
from models.servicio import ServicioModel
from models.ordenTrabajo import OrdenTrabajoModel


def load_csv_to_db(csv_file):
    
    #Cargar variables de entorno desde el archivo .env
    load_dotenv()

    # Obtener la URI de MongoDB desde las variables de entorno
    mongodb_uri = os.getenv("MONGODB_URI")

    # Conectar a MongoDB usando mongoengine
    connect(host=mongodb_uri)
    

    # Leer el archivo CSV
    df = pd.read_csv(csv_file, delimiter=';')
    
    #imprimir cabecera de columnas
    print(df.columns)
    
    codERPEmpresa = 1
    codERPCliente = 1
    codERPServicio = 1
    codERPEmpleado = 1
    
    # Iterar sobre cada fila en el DataFrame
    for index, row in df.iterrows():
        #--------------------------------EMPRESAS--------------------------------
        nombreEmpresa = row['nombreEmpresa']
        empresaGet = EmpresaModel.objects(nombre=nombreEmpresa).first()
        empresaActual = None
        if empresaGet is None:
            # Si la empresa no existe, la creamos y la guardamos
            nuevo = EmpresaModel(
                nombre = nombreEmpresa,
                fechaInicioSusc = datetime.strptime(row['fechaInicioEmpresa'], "%d/%m/%Y"),
                fechaFinSuc = datetime.strptime(row['fechaFinEmpresa'], "%d/%m/%Y"),
                codigoEmpresa="MIGEMP" + str(codERPEmpresa)
            )
            codERPEmpresa += 1
            nuevo.save()
            empresaActual = nuevo
        else:
            empresaActual = empresaGet 
            
            
        #--------------------------------EMPLEADOS--------------------------------    
        nombreEmpleado = row['nombreEmpleado']
        empleadoGet = EmpleadoModel.objects(nombre=nombreEmpleado).first()
        empleadoActual = None
        if empleadoGet is None:
            # Si la empresa no existe, la creamos y la guardamos
            nuevo = EmpleadoModel(
                nombre = nombreEmpleado,   
                empresaId = str(empresaActual.id),
                idERP = "MIGPER" + str(codERPEmpleado)
            )
            codERPEmpleado += 1
            nuevo.save()
            empleadoActual = nuevo
        else:
            empleadoActual = empleadoGet 
            
            
        #--------------------------------CLIENTES--------------------------------    
        nombreCliente = row['nombreCliente']
        clienteGet = EmpleadoModel.objects(nombre=nombreCliente).first()
        clienteActual = None
        if clienteGet is None:
            # Si la empresa no existe, la creamos y la guardamos
            nuevo = ClienteModel(
                nombre = nombreCliente,  
                empresaId = str(empresaActual.id),
                idERP = "MIGCLI" + str(codERPCliente)
            )
            codERPCliente += 1
            nuevo.save()
            clienteActual = nuevo
        else:
            clienteActual = clienteGet
     
     
        #--------------------------------SERVICIOS--------------------------------    
        nombreServicio = row['nombreServicio']
        servicioGet = ServicioModel.objects(nombre=nombreServicio).first()
        servicioActual = None
        if servicioGet is None:
            # Si la empresa no existe, la creamos y la guardamos
            nuevo = ServicioModel(
                nombre = nombreServicio,  
                tipo = row['tipoServicio'],
                tarifaBase = float(row['tarifaBaseServicio']),
                empresaId = str(empresaActual.id),
                idERP = "MIGSER" + str(codERPServicio)
            )
            codERPServicio += 1
            nuevo.save()
            servicioActual = nuevo
        else:
            servicioActual = servicioGet
            
            
        #--------------------------------ORDENES--------------------------------    
        nuevaOrden = OrdenTrabajoModel(
            estado = row['estadoOrden'],   
            codSeguimiento = row['codSeguimientoOrden'],  
            fechaInicio = datetime.strptime(row['fechaInicioOrden'], "%d/%m/%Y"),
            fechaFin = datetime.strptime(row['fechaFinOrden'], "%d/%m/%Y"),
            empresaId = str(empresaActual.id),
            clienteId = str(clienteActual.id),
            empleadoId = str(empleadoActual.id),
            servicioId = str(servicioActual.id)
        )
        nuevaOrden.save()

      
    print("datos cargados exitosamente")

if __name__ == "__main__":
    # Ruta al archivo CSV
    csv_file = 'datos.csv'
    load_csv_to_db(csv_file)
