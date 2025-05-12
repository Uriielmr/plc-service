


from pylogix import PLC
import mysql.connector

# Configuración del PLC
PLC_IP = '192.168.1.100'  # Reemplaza con la IP real del PLC

# Configuración de MySQL
DB_CONFIG = {
    'host': 'localhost',  # Cambia si el servidor MySQL está en otro lugar
    'user': 'root',       # Usuario de MySQL
    'password': 'tu_contraseña',  # Reemplaza con tu contraseña
    'database': 'plc_data'  # Nombre de la base de datos
}

def leer_datos_plc():
    """Lee los valores del PLC."""
    plc = PLC()
    plc.IPAddress = PLC_IP

    contador = plc.Read('Counter_Accum')
    temporizador = plc.Read('Timer_Accum')

    plc.Close()

    if contador.Status == 'Success' and temporizador.Status == 'Success':
        return contador.Value, temporizador.Value
    else:
        print(f"Error en la lectura: Contador={contador.Status}, Temporizador={temporizador.Status}")
        return None, None

def guardar_en_mysql(contador, temporizador):
    """Guarda los datos en MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        sql = "INSERT INTO registros (contador, temporizador) VALUES (%s, %s)"
        valores = (contador, temporizador)

        cursor.execute(sql, valores)
        conn.commit()

        print(f"Datos guardados: Contador={contador}, Temporizador={temporizador}")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error en MySQL: {err}")

# Leer y guardar datos
contador, temporizador = leer_datos_plc()
if contador is not None and temporizador is not None:
    guardar_en_mysql(contador, temporizador)