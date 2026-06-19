
def buscar_especifico(base_datos):
    print("\n--- BÚSQUEDA ESPECÍFICA ---")
   
    try:
        opcion = input("¿Desea buscar un (1) Evento o un (2) Invitado?: ").strip()
        
        if opcion == "1":
            termino = input("Ingrese el término de búsqueda para el Evento (código, nombre, lugar, etc): ").strip()
            
            filtro = {
                "$or": [
                    {"codigo": {"$regex": termino, "$options": "i"}},
                    {"nombre": {"$regex": termino, "$options": "i"}},
                    {"fecha": {"$regex": termino, "$options": "i"}},
                    {"lugar": {"$regex": termino, "$options": "i"}},
                    {"categoria": {"$regex": termino, "$options": "i"}}
                ]
            }
            resultados = list(base_datos["eventos"].find(filtro))
            
            if not resultados:
                print(f"No se encontraron eventos que coincidan con: '{termino}'")
            else:
                print(f"\nSe encontraron {len(resultados)} eventos:")
                for ev in resultados:
                    print(f"\n[{ev.get('codigo')}] {ev.get('nombre')} | Lugar: {ev.get('lugar')} | Categoría: {ev.get('categoria')} | Fecha: {ev.get('fecha')}")

        elif opcion == "2":
            termino = input("Ingrese el término de búsqueda para el Invitado (nombre, RUT o correo): ").strip()

            filtro = {
                "$or": [
                    {"nombre": {"$regex": termino, "$options": "i"}},
                    {"rut": {"$regex": termino, "$options": "i"}},
                    {"correo": {"$regex": termino, "$options": "i"}}
                ]
            }
            resultados = list(base_datos["invitados"].find(filtro))
            
            if not resultados:
                print(f"No se encontraron invitados que coincidan con: '{termino}'")
            else:
                print(f"\nSe encontraron {len(resultados)} invitados:")
                for inv in resultados:
                    print(f"\nRUT: {inv.get('rut')} | Nombre: {inv.get('nombre')} | Correo: {inv.get('correo')}")
        
        else:
            print("Opción no válida. Por favor, elija 1 o 2.")
            
    except Exception as e:
        print(f"Error crítico durante la búsqueda: {e}")

    input("Presione enter para continuar...") #Para que no muestre el menú principal de inmediato


def listar_invitados_activos(coleccion_invitados):
    print("\n--- LISTADO DE INVITADOS ACTIVOS ---")

    filtro = {"estado": {"$regex": "activo", "$options": "i"}}
    
    resultados = coleccion_invitados.find(filtro)
    lista_resultados = list(resultados)
    
    if len(lista_resultados) == 0:
        print("No hay invitados activos registrados.")
    else:
        for inv in lista_resultados:
            print(f"\nRUT: {inv.get('rut')} | Nombre: {inv.get('nombre')} | Empresa: {inv.get('empresa')}")

    input("Presione enter para continuar...") #Para que no muestre el menú principal de inmediato
    

def validar_acceso_evento(base_datos):
    print("\n--- VALIDACIÓN DE ACCESO A EVENTO ---")
    codigo_evento = input("Ingrese el CÓDIGO del evento (ej. EVT-2025-001): ")
    correo_invitado = input("Ingrese el CORREO del invitado: ")
    
    invitado = base_datos["invitados"].find_one({"correo": correo_invitado})
    if not invitado:
        print("El invitado con ese correo no existe en el sistema.")
        return
        
    rut_invitado = invitado["rut"]
    
    filtro = {
        "codigo": codigo_evento,
        "invitados": {
            "$elemMatch": {
                "rut": rut_invitado,
                "estado": "confirmado"
            }
        }
    }
    
    evento = base_datos["eventos"].find_one(filtro)
    
    if evento:
        print(f"\nACCESO PERMITIDO. {invitado.get('nombre')} está CONFIRMADO para el evento: {evento.get('nombre')}")
        input("Presione enter para continuar...") #Para que no muestre el menú principal de inmediato
    else:
        print("\nACCESO DENEGADO: El invitado no está confirmado o el evento/código no existe.")
        input("Presione enter para continuar...") #Para que no muestre el menú principal de inmediato


def obtener_top_eventos(coleccion_eventos):
    print("\n--- TOP 3 EVENTOS CON MAYOR NÚMERO DE INVITADOS ---")

    pipeline = [
        {
            "$project": {
                "nombre": 1,
                "fecha": 1,
                "total_asistentes": {"$size": "$invitados"}
            }
        },
        {"$sort": {"total_asistentes": -1}}, # Ordena de mayor a menor
        {"$limit": 3} # Trae solo los 3 primeros
    ]
    
    resultados = list(coleccion_eventos.aggregate(pipeline)) 
    
    if len(resultados) == 0:
        print("No hay eventos registrados.")
    else:
        for puesto, res in enumerate(resultados, 1):
            print(f"Top {puesto}: {res.get('nombre')} | Fecha: {res.get('fecha')} -> ({res.get('total_asistentes')} invitados asignados)")
    input("Presione enter para continuar...") #Para que no muestre el menú principal de inmediato