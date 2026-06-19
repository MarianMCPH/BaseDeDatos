import conexion  
import consultas 

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
        print("1. Búsqueda específica (Evento o Invitado)") 
        print("2. Buscar invitado activo por correo")
        print("3. Top 3 eventos con más invitados")
        print("0. Salir")
        print("========================================")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            consultas.buscar_especifico(bd)
        elif opcion == "2":
            consultas.listar_eventos_po_invitado(bd) 
        elif opcion == "3":
            consultas.obtener_top_eventos(coleccion_eventos)
        elif opcion == "0":
            print("Cerrando aplicación.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()