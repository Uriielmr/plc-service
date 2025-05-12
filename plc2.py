from db import guardar_en_mysql
from pylogix import PLC

class Timer:
    def __init__(self, temporizador):
        self.temporizador = temporizador
        self.valor = None

    def leer(self, plc):
        response = plc.Read(self.temporizador[0].acc)
        if response.Status == 'Success':
            self.valor = response.Value
        else:
            print(f"Error al leer el timer {self.temporizador}: {response.Status}")
            self.valor = None
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

class Estacion:
    def __init__(self, nombre_estacion):
        self.nombre_estacion = nombre_estacion
        self.timers = []  # Lista de instancias de Timer
        self.counters = []  # Lista de instancias de Counter

    def agregar_timer(self, timer):
        self.timers.append(Timer(timer))

    def agregar_counter(self, counter):
        self.counters.append(Counter(counter))

    def leer_estacion(self, plc):
        datos = {}
        for timer in self.timers:
            datos[f'timer_{timer.nombre_tag}'] = timer.leer(plc)
        for counter in self.counters:
            datos[f'counter_{counter.nombre_tag}'] = counter.leer(plc)
        return datos

class PLCReader:
    def __init__(self, ip_address):
        self.plc = PLC()
        self.plc.IPAddress = ip_address
        self.estaciones = []  # Lista de estaciones (de cada máquina)

    def agregar_estacion(self, estacion):
        self.estaciones.append(estacion)

    def leer_datos(self):
        datos_totales = {}
        for estacion in self.estaciones:
            print(f"Leyendo datos de la estación {estacion.nombre_estacion}...")
            datos_totales[estacion.nombre_estacion] = estacion.leer_estacion(self.plc)
        self.plc.Close()
        return datos_totales

def leer_datos_de_varios_plcs():
    # Ejemplo de varias IPs de PLCs
    ips_maquinas = ['192.168.1.16', '192.168.1.17']

    for ip in ips_maquinas:
        plc_reader = PLCReader(ip)

        # Creación de estaciones y asignación de timers y counters
        estacion_1 = Estacion("Estacion_1")
        estacion_1.agregar_timer('temporizador[0].acc')
        estacion_1.agregar_counter('contador.acc')

        estacion_2 = Estacion("Estacion_2")
        estacion_2.agregar_timer('temporizador[1].acc')
        estacion_2.agregar_counter('contador[1].acc')

        # Agregar estaciones al PLCReader
        plc_reader.agregar_estacion(estacion_1)
        plc_reader.agregar_estacion(estacion_2)

        # Leer los datos
        datos = plc_reader.leer_datos()

        # Mostrar los datos
        print(f"Datos leídos del PLC {ip}: {datos}")

        # Guardar los datos en la base de datos
        for estacion_nombre, datos_estacion in datos.items():
            print(f"Guardando datos de {estacion_nombre}...")
            # guardar_en_mysql(datos_estacion)
            print(datos_estacion)

leer_datos_de_varios_plcs()
