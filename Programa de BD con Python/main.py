import conexion  # Importa tu nuevo archivo independiente de conexión
import consultas # Importa tus funciones analíticas

def main():
    # Invocamos la conexión desde el archivo externo
    bd = conexion.obtain_base_datos() if hasattr(conexion, 'obtain_base_datos') else conexion.obtener_base_datos()
    
    if bd is None:
        print("No se pudo iniciar el programa debido a un error de conexión.")
        return
        
    # Mapeamos las colecciones directamente desde la base de datos recuperada
    coleccion_eventos = bd["eventos"]
    coleccion_invitados = bd["invitados"]
    
    while True:
        print("\n========================================")
        print("     SISTEMA DE GESTIÓN DE EVENTOS      ")
        print("========================================")
        print("1. Listar todos los eventos")
        print("2. Búsqueda específica (Evento o Invitado)") # Nueva opción para búsqueda específica
        print("3. Listar invitados activos")
        print("4. Validar acceso de un invitado a un evento")
        print("5. Top 3 eventos con más invitados")
        print("6. Ver detalle completo de asistencia ($lookup)") # Nueva opción para consulta avanzada con $lookup
        print("0. Salir")
        print("========================================")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            consultas.listar_eventos(coleccion_eventos)
        elif opcion == "2":
            consultas.buscar_especifico(bd) 
        elif opcion == "3":
            consultas.listar_invitados_activos(coleccion_invitados)
        elif opcion == "4":
            consultas.validar_acceso_evento(bd) # Enviamos la BD completa porque requiere leer ambas colecciones
        elif opcion == "5":
            consultas.obtener_top_eventos(coleccion_eventos)
        elif opcion == "6":
            consultas.consultar_detalles_invitados_lookup(bd)
        elif opcion == "0":
            print("Cerrando aplicación. ¡Mucho éxito en la evaluación de INACAP!")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()