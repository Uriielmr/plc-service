# pienso leer algunos tags de un plc, leer el timpo y un contador, pero
# esto no es solo de una maquina, es de varias ¿como puedo hacer para que esta funcion 
# funcione para todas las maquinas que quiera leer y no solo para 1 sola?
# puedes ser con una clase o como?
# esta es mi funcion actual y solo lee esos tags


from db import guardar_en_mysql
from pylogix import PLC

def leer_datos_plc():
    plc = PLC()
    plc.IPAddress = '192.168.1.16'  

    counter_response = plc.Read('contador.acc')
    timer_response = plc.Read('temporizador[0].acc')
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
    print(datoContador, "--------", datoTemporizador, "<<<<<<<<<<<")

    plc.Close()
    print(datos)  # Para verificar los datos antes de guardar
    guardarDatos = guardar_en_mysql(datos['contador'], datos['temporizador'])
    return datos








Para que esta función funcione para varias máquinas en lugar de solo una, puedes adaptarla utilizando una clase que gestione diferentes PLCs con diferentes direcciones IP. Con este enfoque, podrías instanciar un objeto para cada máquina y luego leer sus valores, lo que lo haría mucho más flexible.

A continuación te muestro cómo podrías hacerlo utilizando una clase para gestionar múltiples PLCs:

python
Copiar código
from db import guardar_en_mysql
from pylogix import PLC

class PLCReader:
    def __init__(self, ip_address):
        self.plc = PLC()
        self.plc.IPAddress = ip_address

    def leer_datos(self):
        counter_response = self.plc.Read('contador.acc')
        timer_response = self.plc.Read('temporizador[0].acc')
        datos = {}

        if counter_response.Status == 'Success':
            datos['contador'] = counter_response.Value
        else:
            print(f"Error al leer el contador: {counter_response.Status}")
            datos['contador'] = None

        if timer_response.Status == 'Success':
            datos['temporizador'] = timer_response.Value
        else:
            print(f"Error al leer el temporizador: {timer_response.Status}")
            datos['temporizador'] = None

        self.plc.Close()

        print(datos)  # Para verificar los datos antes de guardar
        guardar_en_mysql(datos['contador'], datos['temporizador'])
        return datos


def leer_datos_de_varios_plcs():
    # Lista de IPs de las máquinas
    ips_maquinas = ['192.168.1.16', '192.168.1.17', '192.168.1.18']  # Ejemplo de varias IPs de PLCs

    for ip in ips_maquinas:
        plc_reader = PLCReader(ip)
        print(f"Leyendo datos del PLC con IP {ip}...")
        plc_reader.leer_datos()
Explicación de la solución:
Clase PLCReader:

La clase se inicializa con la dirección IP de un PLC y tiene el método leer_datos para leer los valores de los tags (contador y temporizador).
De esta manera, puedes crear una instancia de PLCReader para cada PLC que quieras leer.
Función leer_datos_de_varios_plcs:

Tienes una lista de direcciones IP de las máquinas. Para cada IP, se crea una instancia de PLCReader, se leen los datos y se guardan.
Flexibilidad:

Si tienes más PLCs en el futuro, simplemente añades más IPs a la lista ips_maquinas.
Uso:
Para leer los datos de todas las máquinas, simplemente llama a la función leer_datos_de_varios_plcs(), y automáticamente se leerán los datos de todos los PLCs en la lista.
Ventajas de este enfoque:
Escalabilidad: Puedes añadir tantas máquinas como quieras sin tener que modificar mucho el código.
Mantenibilidad: Cada PLC se maneja independientemente, por lo que es más fácil mantener y modificar el código de manera modular.
Flexibilidad: Puedes modificar la clase PLCReader para incluir otros métodos o manejar otros tags si es necesario.
Si necesitas realizar otras operaciones, como obtener diferentes tags o procesar datos adicionales, puedes expandir la clase PLCReader de acuerdo a tus necesidades.





Adjuntar

Buscar

Ana




puedes hacer lo mismo pero ahora no solo para un timer y un temporizador, 
ahora quisiera añadir una clase para el timer y el temporizador para que no
solo sea 1 si no varios o los que quiera, ya que la maquina tiene varias estaciones
y quiero que 1 solo plc lea varios





¡Claro! Para manejar múltiples temporizadores (timers) y contadores (counters) en un PLC, podemos crear una estructura más flexible. La idea es tener clases separadas para cada tipo de tag (Timer y Counter), y que cada estación de la máquina pueda tener su propio conjunto de temporizadores y contadores.

Aquí te dejo una propuesta para manejar esto de forma modular:

1. Clase Timer y Counter:
Estas clases se encargan de leer los valores de los temporizadores y contadores, respectivamente.

2. Clase PLCReader:
Esta clase gestionará las instancias de los temporizadores y contadores para cada máquina. Además, puedes añadir tantas estaciones como quieras (con sus respectivos tags) y leer los valores correspondientes.

3. Estructura general:
Te muestro cómo estructurarlo para soportar múltiples estaciones (con varios timers y counters):

python
Copiar código
from db import guardar_en_mysql
from pylogix import PLC

class Timer:
    def __init__(self, nombre_tag):
        self.nombre_tag = nombre_tag
        self.valor = None

    def leer(self, plc):
        response = plc.Read(self.nombre_tag)
        if response.Status == 'Success':
            self.valor = response.Value
        else:
            print(f"Error al leer el timer {self.nombre_tag}: {response.Status}")
            self.valor = None
        return self.valor

class Counter:
    def __init__(self, nombre_tag):
        self.nombre_tag = nombre_tag
        self.valor = None

    def leer(self, plc):
        response = plc.Read(self.nombre_tag)
        if response.Status == 'Success':
            self.valor = response.Value
        else:
            print(f"Error al leer el contador {self.nombre_tag}: {response.Status}")
            self.valor = None
        return self.valor

class Estacion:
    def __init__(self, nombre_estacion):
        self.nombre_estacion = nombre_estacion
        self.timers = []  # Lista de instancias de Timer
        self.counters = []  # Lista de instancias de Counter

    def agregar_timer(self, nombre_tag):
        self.timers.append(Timer(nombre_tag))

    def agregar_counter(self, nombre_tag):
        self.counters.append(Counter(nombre_tag))

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
            guardar_en_mysql(datos_estacion)

Explicación:
Clases Timer y Counter:

Cada clase tiene un método leer que lee un tag específico de un PLC.
Al crear instancias de estas clases, puedes asignarles diferentes tags (por ejemplo, temporizador[0].acc, contador.acc, etc.).
Las clases encapsulan la lógica para leer esos valores y manejar los errores.
Clase Estacion:

Representa una estación de la máquina. Una estación puede tener varios timers y contadores.
Puedes agregar múltiples timers y contadores mediante los métodos agregar_timer y agregar_counter.
Clase PLCReader:

Gestiona las estaciones de un PLC específico.
La función leer_datos recorre todas las estaciones y lee sus datos.
Cada PLC puede tener múltiples estaciones, y cada estación puede tener múltiples timers y contadores.