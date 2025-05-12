from pylogix import PLC

# Configurar la conexión con el PLC
plc = PLC()
plc.IPAddress = '192.168.1.16'  

# --------------Prueba con contadores-------------------------



counter_response = plc.Read('contador.acc')
timer_response = plc.Read('temporizador[0].acc')


if counter_response.Status == 'Success':
    print(f"Valor del contador: {counter_response.Value}")
else:
    print(f"Error al leer el contador: {counter_response.Status}")

if timer_response.Status == 'Success':
    print(f"Valor del temporizador (ms): {timer_response.Value}")
else:
    print(f"Error al leer el temporizador: {timer_response.Status}")

plc.Close()




# from pylogix import PLC

# # Conecta al PLC
# plc = PLC()
# plc.IPAddress = '192.168.1.16'  # Dirección IP del PLC

# # Lee un tag específico
# response = plc.Read('PROCS_Reference')  # Cambia 'TagName' por el nombre de tu variable en el PLC
# print(response.Value)

# # Cierra la conexión
# plc.Close()




# from pylogix import PLC

# plc = PLC()
# plc.IPAddress = '192.168.1.100'

# response = plc.Read('Python_Input')
# print(f"Valor recibido: {response.Value}")

# plc.Close()
