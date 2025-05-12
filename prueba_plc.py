from db import guardar_en_mysql
from pylogix import PLC


class PLCReader:
    def __init__(self, ip_address='192.168.1.16'):
        self.plc = PLC()
        self.plc.IPAddress = ip_address
    
    def leer_tag(self, tag):
        response = self.plc.Read(tag)
        return response

    def cerrar_conexion(self):
        self.plc.Close()

class Timer:
    def __init__(self, temporizador):
        # self.temporizador = temporizador
        self.valor = 0

    def leer(self, temporizador):
        plc_reader = PLCReader()
        response = plc_reader.leer_tag(self.temporizador)
        if response.Status == 'Success':
            self.valor = response.Value
        else:
            print(f"Error al leer el timer {self.temporizador}: {response.Status}")
            self.valor = 0 
        return self.valor

class Counter:
    def __init__(self, contador):
        self.contador = contador
        self.valor = None

    def leer(self, plc):
        response = plc.Read(self.contador.acc)
        if response.Status == 'Success':
            self.valor = response.Value
        else:
            print(f"Error al leer el contador {self.contador}: {response.Status}")
            self.valor = None
        return self.valor

        
def leer_datos_plc():
    plc_reader = PLCReader()

    counter_response = plc_reader.leer_tag('contador.acc')
    timer_response = plc_reader.leer_tag('temporizador[0].acc')

    datos = {}

    if counter_response.Status == 'Success':
        datos['contador'] = counter_response.Value
        datoContador = datos['contador']
    else:
        print(f"Error al leer el contador: {counter_response.Status}")
        # datos['contador'] = None

    if timer_response.Status == 'Success':
        datos['temporizador'] = timer_response.Value
        datoTemporizador = datos['temporizador']
    else:
        print(f"Error al leer el temporizador: {timer_response.Status}")
        # datos['temporizador'] = None

    print(datoContador, "--------", datoTemporizador, "<<<<<<<<<<<")

    plc_reader.cerrar_conexion()
    print(datos)  # Para verificar los datos antes de guardar
    
    return datos

leer = leer_datos_plc()
print(leer)

