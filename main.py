from fastapi import FastAPI, HTTPException
from db import guardar_en_mysql, consultar_datos_mysql
from plc import leer_datos_plc

app = FastAPI()

@app.get("/")
async def root():
    return {"mensaje": "API lectura de tags en OK Funcionandooooooooo"}

@app.get("/plc-leer/")
async def leer_plc():
    datos = leer_datos_plc()
    if datos['contador'] is None or datos['temporizador'] is None:
        raise HTTPException(status_code=500, detail="Error al leer datos del PLC")
    guardar_en_mysql(datos['contador'], datos['temporizador'])
    # guardar_en_mysql_corregir(datos['contador'], datos['temporizador'])
    return {"mensaje": "Estos son los datos leidos", "datos": datos}

@app.get("/registros/")
async def obtener_registros():
    registros = consultar_datos_mysql()
    print(registros)
    if not registros:
        raise HTTPException(status_code=404, detail="No se encontraron registros")
    return registros

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)