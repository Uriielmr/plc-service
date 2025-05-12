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
        cursor1.execute("USE plc_data")  
        cursor1.execute("SELECT * FROM registros") 
        rows = cursor1.fetchall()  

        for row in rows: 
            print(row)

        conexion1.close()
        print(row)
        return rows  

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
