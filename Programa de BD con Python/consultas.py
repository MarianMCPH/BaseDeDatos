
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


def listar_eventos_po_invitado(base_datos):
    try:
        correo_invitado = input("Ingrese el correo del invitado: ").strip()

        #Buscar el invitado por correo
        invitado = base_datos["invitados"].find_one({"correo": correo_invitado})

        if not invitado:
            print(f"No se encontro el invitado con el correo ingresado: '{correo_invitado}'")
            input("\nPresione enter para continuar...")

            return
        
        rut_invitado = invitado["rut"]
        nombre_invitado = invitado["nombre"]

# Consulta: db.eventos.find({ "invitados": { $elemMatch: { "rut": "rut_invitado" } } })
        filtro = {
            "invitados": {
                "$elemMatch": {
                    "rut": rut_invitado
                }
            }
        }
        
        eventos = list(base_datos["eventos"].find(filtro, {"codigo": 1, "nombre": 1, "fecha": 1, "_id": 0}))
        
        if not eventos:
            print(f"\n El invitado '{nombre_invitado}' no está registrado en ningún evento.")
        else:
            print(f"\n El invitado '{nombre_invitado}' participa en {len(eventos)} evento(s):")
            print("="*70)
            for i, ev in enumerate(eventos, 1):
                print(f"{i}. Código: {ev.get('codigo')} | Nombre: {ev.get('nombre')}")
                print(f"   Fecha: {ev.get('fecha')}")
                print("-"*70)
    
    except Exception as e:
        print(f"❌ Error al realizar la búsqueda: {e}")
    
    input("Presione enter para continuar...")


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