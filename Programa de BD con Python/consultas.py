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
# OPCIÓN 2: Búsqueda específica (Evento o Invitado) 
# Cumple con: Punto 1 (Camila), Punto 3 (Excepciones/Case Insensitive) y Punto 4 (Búsqueda parcial)
# =============================================================================
def buscar_especifico(base_datos):
    print("\n--- BÚSQUEDA ESPECÍFICA ---")
    # Punto 3: El uso de try-except permite capturar errores de ejecución y evitar que el programa se cierre
    try:
        opcion = input("¿Desea buscar un (1) Evento o un (2) Invitado?: ").strip()
        
        if opcion == "1":
            termino = input("Ingrese el término de búsqueda para el Evento (código, nombre, lugar, etc): ").strip()
            
            # Punto 4: El uso de $regex permite la búsqueda parcial (coincidencia de fragmentos)
            # Punto 3: $options: 'i' hace que la búsqueda ignore mayúsculas y minúsculas
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
                print(f"❌ No se encontraron eventos que coincidan con: '{termino}'")
            else:
                print(f"\n✅ Se encontraron {len(resultados)} eventos:")
                for ev in resultados:
                    print(f"[{ev.get('codigo')}] {ev.get('nombre')} | Lugar: {ev.get('lugar')} | Categoría: {ev.get('categoria')}")

        elif opcion == "2":
            termino = input("Ingrese el término de búsqueda para el Invitado (nombre, RUT o correo): ").strip()
            
            # Punto 4: Búsqueda parcial por nombre, rut o correo
            # Punto 3: Insensible a la capitalización de letras
            filtro = {
                "$or": [
                    {"nombre": {"$regex": termino, "$options": "i"}},
                    {"rut": {"$regex": termino, "$options": "i"}},
                    {"correo": {"$regex": termino, "$options": "i"}}
                ]
            }
            resultados = list(base_datos["invitados"].find(filtro))
            
            if not resultados:
                print(f"❌ No se encontraron invitados que coincidan con: '{termino}'")
            else:
                print(f"\n✅ Se encontraron {len(resultados)} invitados:")
                for inv in resultados:
                    print(f"RUT: {inv.get('rut')} | Nombre: {inv.get('nombre')} | Correo: {inv.get('correo')}")
        
        else:
            print("❌ Opción no válida. Por favor, elija 1 o 2.")
            
    except Exception as e:
        # Punto 3: Manejo genérico de excepciones para informar errores de base de datos
        print(f"❌ Error crítico durante la búsqueda: {e}")


# =============================================================================
# NUEVA OPCIÓN: Consulta con $lookup (Punto 2 Camila)
# Une la información de eventos con la información detallada de invitados
# =============================================================================
def consultar_detalles_invitados_lookup(base_datos):
    print("\n--- DETALLE DE INVITADOS POR EVENTO (USANDO $LOOKUP) ---")
    try:
        pipeline = [
            # 1. Descomponemos el array de invitados que existe dentro de cada evento
            {"$unwind": "$invitados"},
            # 2. Realizamos el "Join" con la colección de invitados usando el RUT como llave
            {
                "$lookup": {
                    "from": "invitados",
                    "localField": "invitados.rut",
                    "foreignField": "rut",
                    "as": "detalle_persona"
                }
            },
            # 3. Al obtener un array del lookup, lo aplanamos
            {"$unwind": "$detalle_persona"},
            # 4. Seleccionamos solo los campos necesarios para mostrar
            {
                "$project": {
                    "_id": 0,
                    "evento": "$nombre",
                    "invitado": "$detalle_persona.nombre",
                    "empresa": "$detalle_persona.empresa",
                    "estado_asistencia": "$invitados.estado"
                }
            }
        ]
        
        resultados = list(base_datos["eventos"].aggregate(pipeline))
        
        if not resultados:
            print("No se encontraron registros vinculados.")
        else:
            for res in resultados:
                print(f"Evento: {res['evento']} | Invitado: {res['invitado']} | Empresa: {res['empresa']} | Estado: {res['estado_asistencia']}")
    except Exception as e:
        print(f"❌ Error al realizar la consulta $lookup: {e}")


# =============================================================================
# OPCIÓN 3: Listar invitados activos (Filtro básico de estado)
# Cumple con: Punto 5 (Corrección de búsqueda de invitados activos)
# =============================================================================
def listar_invitados_activos(coleccion_invitados):
    print("\n--- LISTADO DE INVITADOS ACTIVOS ---")
    
    # Punto 5: Se corrige la búsqueda ya que a veces el campo 'activo' puede venir como booleano o string
    # Usamos $in para buscar cualquiera de las representaciones de "Verdadero"
    filtro = {"activo": {"$in": [True, "true", "True", 1]}}
    
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
    # Consulta comentada por el profesor:
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
    
    # Consulta comentada por el profesor:
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