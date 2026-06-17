# =============================================================================
# OPCIÓN 1: Listar todos los eventos (Campos específicos exigidos por la guía)
# =============================================================================
def listar_eventos(coleccion_eventos):
    print("\n--- LISTADO GENERAL DE EVENTOS ---")
    
    # Consulta comentada para la profesora:
    # db.eventos.find({}, { "codigo": 1, "nombre": 1, "fecha": 1, "lugar": 1, "categoria": 1, "_id": 0 })
    
    proyeccion = {
        "codigo": 1, 
        "nombre": 1, 
        "fecha": 1, 
        "lugar": 1, 
        "categoria": 1, 
        "_id": 0
    }
    
    eventos = coleccion_eventos.find({}, proyeccion)
    
    for ev in eventos:
        print(f"Código: {ev.get('codigo')} | Nombre: {ev.get('nombre')}")
        print(f"Fecha: {ev.get('fecha')} | Lugar: {ev.get('lugar')} | Categoría: {ev.get('categoria')}")
        print("-" * 60)


# =============================================================================
# OPCIÓN 2: Buscar invitados por Expresiones Regulares (Nombre o Correo)
# =============================================================================
def buscar_invitados_regex(coleccion_invitados):
    print("\n--- BÚSQUEDA DINÁMICA DE INVITADOS (REGEX) ---")
    termino = input("Ingrese el nombre parcial o correo a buscar: ")
    
    # Consulta comentada para la profesora:
    # db.invitados.find({ $or: [ { "nombre": { $regex: "termino", $options: "i" } }, { "correo": { $regex: "termino", $options: "i" } } ] })
    
    filtro = {
        "$or": [
            {"nombre": {"$regex": termino, "$options": "i"}},
            {"correo": {"$regex": termino, "$options": "i"}}
        ]
    }
    
    resultados = coleccion_invitados.find(filtro)
    lista_resultados = list(resultados)
    
    if len(lista_resultados) == 0:
        print("❌ No se encontraron invitados con ese criterio.")
    else:
        print(f"\nSe encontraron {len(lista_resultados)} invitados:")
        for inv in lista_resultados:
            print(f"RUT: {inv.get('rut')} | Nombre: {inv.get('nombre')} | Correo: {inv.get('correo')}")


# =============================================================================
# OPCIÓN 3: Listar invitados activos (Filtro básico de estado)
# =============================================================================
def listar_invitados_activos(coleccion_invitados):
    print("\n--- LISTADO DE INVITADOS ACTIVOS ---")
    
    # Consulta comentada para la profesora:
    # db.invitados.find({ "activo": true })
    
    filtro = {"activo": True}
    resultados = coleccion_invitados.find(filtro)
    lista_resultados = list(resultados)
    
    if len(lista_resultados) == 0:
        print("No hay invitados activos registrados.")
    else:
        for inv in lista_resultados:
            print(f"RUT: {inv.get('rut')} | Nombre: {inv.get('nombre')} | Empresa: {inv.get('empresa')}")


# =============================================================================
# OPCIÓN 4: Validación de Acceso (Búsqueda cruzada usando el RUT)
# =============================================================================
def validar_acceso_evento(base_datos):
    print("\n--- VALIDACIÓN DE ACCESO A EVENTO ---")
    codigo_evento = input("Ingrese el CÓDIGO del evento (ej. EVT-2025-001): ")
    correo_invitado = input("Ingrese el CORREO del invitado: ")
    
    # 1. Buscamos primero el RUT del invitado mediante su correo
    invitado = base_datos["invitados"].find_one({"correo": correo_invitado})
    if not invitado:
        print("❌ El invitado con ese correo no existe en el sistema.")
        return
        
    rut_invitado = invitado["rut"]

    # 2. Buscamos si en el evento existe ese RUT con estado 'confirmado'
    # Consulta comentada para la profesora:
    # db.eventos.find({ "codigo": "codigo_evento", "invitados": { $elemMatch: { "rut": "rut_invitado", "estado": "confirmado" } } })
    
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
        print(f"\n✅ ACCESO PERMITIDO. {invitado.get('nombre')} está CONFIRMADO para el evento: {evento.get('nombre')}")
    else:
        print("\n❌ ACCESO DENEGADO: El invitado no está confirmado o el evento/código no existe.")


# =============================================================================
# OPCIÓN 5: Top 3 Eventos con más Invitados (Framework de Agregación con $size)
# =============================================================================
def obtener_top_eventos(coleccion_eventos):
    print("\n--- TOP 3 EVENTOS CON MAYOR NÚMERO DE INVITADOS ---")
    
    # Consulta comentada para la profesora:
    # db.eventos.aggregate([ { $project: { nombre: 1, total: { $size: "$invitados" } } }, { $sort: { total: -1 } }, { $limit: 3 } ])
    
    pipeline = [
        {
            "$project": {
                "nombre": 1,
                "total_asistentes": {"$size": "$invitados"} # Mide el largo del arreglo 'invitados'
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
            print(f"Top {puesto}: {res.get('nombre')} -> ({res.get('total_asistentes')} invitados asignados)")