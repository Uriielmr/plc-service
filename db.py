import mysql.connector


conexion1=mysql.connector.connect(host="localhost", 
                                  user="root", 
                                  passwd="contrasena",
                                  database = "plc")

def consultar_datos_mysql():
    try:
        conexion1=mysql.connector.connect(host="localhost", 
                                  user="root", 
                                  passwd="contrasena",
                                  database = "plc")
        cursor1 = conexion1.cursor(dictionary=True)
        cursor1.execute("USE plc_data")  # Aqui vamos a seleccionar la base de datos que se va a usar
        cursor1.execute("SELECT * FROM registros")  # Aqui es la tabla
        rows = cursor1.fetchall()  # aqui se va a traer todo lo que hay en la tabla de registros

        for row in rows:  # aqui para imprimir con un for para que imprima linea por linea 
            print(row)

        conexion1.close()
        print(row)
        return rows  # Aquí agregamos el return para devolver los datos

    except mysql.connector.Error as err:
        print(f"Error en MySQL: {err}")
        return None 

def guardar_en_mysql(contador,temporizador):
    """Guarda los datos en MySQL"""
    try:
        conexion1=mysql.connector.connect(host="localhost", 
                                  user="root", 
                                  passwd="contrasena",
                                  database = "plc")
        cursor1 = conexion1.cursor(dictionary=True)
        cursor1.execute("USE plc_data")
        cursor1.execute("SHOW TABLES")
        print(cursor1, "<<<<-----")
        tablas = cursor1.fetchall()

        print("Tablas en la base de datos:")
        for tabla in tablas:
            print(tabla)

        sql = "INSERT INTO registros (contador, temporizador) VALUES (%s, %s)"
        valores = (contador, temporizador)

        cursor1.execute(sql, valores)
        conexion1.commit()
        cursor1.close()
        conexion1.close()
        return valores
    except mysql.connector.Error as err:
        print(f"Error en MySQL: {err}")
        return None



# def guardar_en_mysql_corregir(contador, temporizador):
#     """Guarda los datos en MySQL."""
#     try:
#         # conexion1=mysql.connector.connect(host="localhost", 
#         #                           user="root", 
#         #                           passwd="contrasena",
#         #                           database = "plc")

#         cursor1=conexion1.cursor(dictionary=True)
#         cursor1.execute("USE plc_data")
#         cursor1.execute("show databases")
#         print(cursor1)

#         sql = "INSERT INTO registros (contador, temporizador) VALUES (%s, %s)"
#         valores = (contador, temporizador)

#         cursor1.execute(sql, valores)
#         conexion1.commit()

#         print(f"Datos guardados: Contador={contador}, Temporizador={temporizador}")

#         cursor1.close()
#         conexion1.close()
#     except mysql.connector.Error as err:
#         print(f"Error en MySQL: {err}")

# def leer_datos_plc():
#     plc = PLC()
#     plc.IPAddress = '192.168.1.16' 

#     counter_response = plc.Read('contador.acc')
#     timer_response = plc.Read('temporizador[0].acc')

#     datos = {}
#     if counter_response.Status == 'Success':
#         datos['contador'] = counter_response.Value
#         print(f"Valor del contador: {counter_response.Value}")
#     else:
#         print(f"Error al leer el contador: {counter_response.Status}")

#     if timer_response.Status == 'Success':
#         datos['temporizador'] = timer_response.Value
#         print(f"Valor del temporizador (ms): {timer_response.Value}")
#     else:
#         print(f"Error al leer el temporizador: {timer_response.Status}")

#     plc.Close()

#     #  Si no se obtuvieron datos válidos
#     if not datos:
#         print(" No se obtuvieron datos del PLC.")
    
#     return datos


# lecturaDatos = leer_datos_plc()
# print(lecturaDatos)
# consulta = consultar_datos_mysql()
# print(consulta)









# cursor1=conexion1.cursor(dictionary=True)

# cursor1.execute("show databases")
# for base in cursor1:
#     print(base)

# cursor1.execute("USE plc_data")  # Aqui vamos a seleccionar la base de datos que se va a usar
# cursor1.execute("SELECT * FROM registros") #Aqui es la tabla
# rows = cursor1.fetchall() #aqui se va a a atraer todo lo que hay en la tabla de registros

# for row in rows:    #aqui para imprimir con un for para que imprima linea por linea 
#     print(row)

# conexion1.close()

# def consultar_datos_mysql():
#     try:

#         cursor1=conexion1.cursor(dictionary=True)

#         cursor1.execute("USE plc_data")  # Aqui vamos a seleccionar la base de datos que se va a usar
#         cursor1.execute("SELECT * FROM registros") #Aqui es la tabla
#         rows = cursor1.fetchall() #aqui se va a a atraer todo lo que hay en la tabla de registros

#         for row in rows:    #aqui para imprimir con un for para que imprima linea por linea 
#             print(row)

#         conexion1.close()

#     except mysql.connector.Error as err:
#         print(f"Error en MySQL: {err}")



