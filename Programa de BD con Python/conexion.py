from pymongo import MongoClient

def obtener_base_datos():
    """
    Establece la conexión con MongoDB local y retorna la base de datos 'prueba3'.
    """
    try:
        
        cliente = MongoClient("mongodb://localhost:27017/")
        
        
        bd = cliente["ev3sumativa"]
        
        return bd
    except Exception as e:
        print(f"❌ Error crítico al conectar a MongoDB: {e}")
        return None