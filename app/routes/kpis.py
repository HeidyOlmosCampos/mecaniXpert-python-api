
from fastapi import APIRouter, HTTPException, Query
from mongoengine import DoesNotExist
from datetime import datetime
from bson import ObjectId
from typing import Dict, Any
from collections import defaultdict, Counter

from app.models.ordenTrabajo import OrdenTrabajoModel
from app.models.empresa import EmpresaModel
from app.models.cliente import ClienteModel
from app.models.empleado import EmpleadoModel
from app.models.servicio import ServicioModel
from app.schemas.ordenTrabajo import OrdenTrabajoRequest

router = APIRouter()

    
@router.get("/ordenes-trabajo")
async def obtener_total_ordenes_trabajo(
    inicio: str = Query(..., description="Fecha de inicio del rango en formato DD/MM/YYYY"),
    fin: str = Query(..., description="Fecha de fin del rango en formato DD/MM/YYYY"),
    empresa: str = Query(..., description="ID de la empresa")
):
    try:
        # Convertir los parámetros de fecha a objetos datetime
        fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fin, "%d/%m/%Y")

        # Filtrar las órdenes de trabajo en el rango de fechas y por empresa
        ordenes_trabajo = OrdenTrabajoModel.objects(
            fechaFin__gte=fecha_inicio,
            fechaFin__lte=fecha_fin,
            empresaId=empresa,
            estado="FINALIZADO"
        ).count()

        return {"total_ordenes_trabajo": ordenes_trabajo}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use DD/MM/YYYY.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@router.get("/tasa-retencion-clientes")
async def obtener_tasa_retencion_clientes(
    inicio: str = Query(..., description="Fecha de inicio del rango en formato DD/MM/YYYY"),
    fin: str = Query(..., description="Fecha de fin del rango en formato DD/MM/YYYY"),
    empresa: str = Query(..., description="ID de la empresa")
):
    try:

        # Convertir los parámetros de fecha a objetos datetime
        fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fin, "%d/%m/%Y")

        # Filtrar las órdenes de trabajo en el rango de fechas y por empresa
        ordenes_trabajo = OrdenTrabajoModel.objects(
            fechaFin__gte=fecha_inicio,
            fechaFin__lte=fecha_fin,
            empresaId=empresa,
            estado="FINALIZADO"
        )
        
        # Diccionario para contar las ocurrencias de codSeguimiento
        seguimiento_count = {}

        # Contar las ocurrencias de codSeguimiento
        for orden in ordenes_trabajo:
            if orden.codSeguimiento in seguimiento_count:
                seguimiento_count[orden.codSeguimiento] += 1
            else:
                seguimiento_count[orden.codSeguimiento] = 1

        total_ventas = len(seguimiento_count)
        
        # Inicializar un diccionario para contar las órdenes por cliente
        cliente_ordenes_count = defaultdict(set)

        # Iterar sobre las órdenes de trabajo y agregar cada codSeguimiento al conjunto correspondiente al cliente
        for orden in ordenes_trabajo:
            cliente_ordenes_count[orden.clienteId].add(orden.codSeguimiento)


        # Inicializar una lista para las ocurrencias de los clientes
        clientes_mas_9_ordenes = []
        clientes_6_9_ordenes = []
        clientes_2_5_ordenes = []

        # Iterar sobre cliente_ordenes_count y contar/eliminar aquellos con más de 10 órdenes
        for cliente_id, seguimientos in list(cliente_ordenes_count.items()):
            if len(seguimientos) > 9:
                clientes_mas_9_ordenes.append(cliente_id)
                del cliente_ordenes_count[cliente_id]
                
        # Iterar sobre cliente_ordenes_count y contar/eliminar aquellos con más de 5 órdenes
        for cliente_id, seguimientos in list(cliente_ordenes_count.items()):
            if len(seguimientos) > 5:
                clientes_6_9_ordenes.append(cliente_id)
                del cliente_ordenes_count[cliente_id]
                
        # Iterar sobre cliente_ordenes_count y contar/eliminar aquellos con más de 1 órdenes
        for cliente_id, seguimientos in list(cliente_ordenes_count.items()):
            if len(seguimientos) > 1:
                clientes_2_5_ordenes.append(cliente_id)
                del cliente_ordenes_count[cliente_id]
                
        compras_1 = len(cliente_ordenes_count) #los que solo tienen una compra
        compras_2_5 = len(clientes_2_5_ordenes) # los que tienen de 2 a 5 compras
        compras_6_9 = len(clientes_6_9_ordenes) #los que tienen de 6 a 9 compras
        compras_mas_9 = len(clientes_mas_9_ordenes) # los que tienen 10 compras o mas
        total = compras_1 + compras_2_5 + compras_6_9 + compras_mas_9
        
        porcentaje = ((compras_1 * 100) / total )
        
        return {
            "compras_1": {
                "rango": "Una compra",
                "porcentaje": round((compras_1 * 100) / total, 2) if total > 0 else 0
            },
            "compras_2_5": {
                "rango": "Dos a cinco compras",
                "porcentaje": round((compras_2_5 * 100) / total, 2) if total > 0 else 0
            },
            "compras_6_9": {
                "rango": "Seis a nueve compras",
                "porcentaje": round((compras_6_9 * 100) / total, 2) if total > 0 else 0
            },
            "compras_mas_9": {
                "rango": "Mas de nueve compras",
                "porcentaje": round((compras_mas_9 * 100) / total, 2) if total > 0 else 0
            }
        }
     
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use DD/MM/YYYY.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
@router.get("/top-empleados-ordenes-trabajo")
async def obtener_top_empleados_ordenes_trabajo(
    inicio: str = Query(..., description="Fecha de inicio del rango en formato DD/MM/YYYY"),
    fin: str = Query(..., description="Fecha de fin del rango en formato DD/MM/YYYY"),
    empresa: str = Query(..., description="ID de la empresa")
):
    try:
        # Convertir los parámetros de fecha a objetos datetime
        fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fin, "%d/%m/%Y")

        # Filtrar las órdenes de trabajo en el rango de fechas y por empresa
        ordenes_trabajo = OrdenTrabajoModel.objects(
            fechaFin__gte=fecha_inicio,
            fechaFin__lte=fecha_fin,
            empresaId=empresa,
            estado="FINALIZADO"
        )

        # Contar las órdenes de trabajo finalizadas por cada empleado
        empleado_count = Counter(orden.empleadoId for orden in ordenes_trabajo)

        # Obtener los top 5 empleados con más órdenes finalizadas
        top_6_empleados = empleado_count.most_common(6)

        # Obtener nombres de empleados y crear la respuesta
        resultado = []
        for empleado_id, ordenes in top_6_empleados:
            empleado = EmpleadoModel.objects.get(id=ObjectId(empleado_id))
            resultado.append({
                "nombre": empleado.nombre,
                "ordenes": ordenes
            })

        return {"top_6_empleados": resultado}

    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use DD/MM/YYYY.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/top-servicios-vendidos-finalizados")
async def obtener_top_empleados_ordenes_trabajo(
    inicio: str = Query(..., description="Fecha de inicio del rango en formato DD/MM/YYYY"),
    fin: str = Query(..., description="Fecha de fin del rango en formato DD/MM/YYYY"),
    empresa: str = Query(..., description="ID de la empresa")
):
    try:
        # Convertir los parámetros de fecha a objetos datetime
        fecha_inicio = datetime.strptime(inicio, "%d/%m/%Y")
        fecha_fin = datetime.strptime(fin, "%d/%m/%Y")

        # Filtrar las órdenes de trabajo en el rango de fechas y por empresa
        ordenes_trabajo = OrdenTrabajoModel.objects(
            fechaFin__gte=fecha_inicio,
            fechaFin__lte=fecha_fin,
            empresaId=empresa,
            estado="FINALIZADO"
        )

        # Contar las órdenes de trabajo finalizadas por cada empleado
        servicio_count = Counter(orden.servicioId for orden in ordenes_trabajo)

        # Obtener los top 6 servicios finalizados mas vendidos
        top_6_servicios = servicio_count.most_common(6)

        # Obtener nombres de servicios y crear la respuesta
        resultado = []
        for servicio_id, ordenes in top_6_servicios:
            servicio = ServicioModel.objects.get(id=ObjectId(servicio_id))
            resultado.append({
                "servicio": servicio.nombre,
                "ventas": ordenes
            })

        return {"top_6_servicios": resultado}

    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use DD/MM/YYYY.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
