import xml.etree.ElementTree as ET

def leer_archivo (ruta_del_archivo):
    tree = ET.parse(ruta_del_archivo)
    root = tree.getroot()
    
    for campo in root.findall('campo'):
        leer_datos_campo(campo)
        leer_estaciones_base(campo)
        leer_sensores_suelo(campo)
        leer_sensores_cultivo(campo)

def leer_datos_campo(campo):
    #Leemos los datos del campo en el XML
    id_campo = campo.get('id') #Usamos get porque es un atributo y no un elemento
    nombre_campo = campo.get('nombre')
    print(f"Cargando campo agrícola {id_campo}...")
    print(f"ID: {id_campo}, Nombre: {nombre_campo}")
    print("-" * 49)

def leer_estaciones_base(campo):
    #Leemos los datos de las estaciones base para cada campo
    print("Estaciones Base:")
    estaciones_base = campo.find('estacionesBase')
    if estaciones_base is not None:
        for estacion in estaciones_base.findall('estacion'):
            id_estacion = estacion.get('id')
            nombre_estacion = estacion.get('nombre')
            print(f"Cargando estacion base {id_estacion}...")
            print(f"ID: {id_estacion}, Nombre: {nombre_estacion}")
            print("-" * 49)

def leer_sensores_suelo(campo):
    print("Sensores de Suelo:")
    sensores_suelo = campo.find('sensoresSuelo')
    if sensores_suelo is not None:
        for sensor_suelo in sensores_suelo.findall('sensorS'):
            id_sensor_suelo = sensor_suelo.get('id')
            nombre_sensor_suelo = sensor_suelo.get('nombre')
            print(f"Sensor de suelo: ID: {id_sensor_suelo}, Nombre: {nombre_sensor_suelo}")
            
            leer_frecuencias_suelo(sensor_suelo, id_sensor_suelo)
            print("-" * 49)

def leer_frecuencias_suelo(sensor_suelo, id_sensor_suelo):           
    print(f"Frecuencias sensor de suelo {id_sensor_suelo}:")
    for frecuencia_sensorS in sensor_suelo.findall('frecuencia'):
        id_frecuencia_sensorS = frecuencia_sensorS.get('idEstacion')
        texto_frecuencia_sensorS = frecuencia_sensorS.text.strip()
        valor_frecuencia_sensorS = int(texto_frecuencia_sensorS) if texto_frecuencia_sensorS.isdigit() else texto_frecuencia_sensorS
        print(f"  Estación: {id_frecuencia_sensorS}, Valor: {valor_frecuencia_sensorS}")

def leer_sensores_cultivo(campo):    
    print("Sensores de Cultivo:")
    sensores_cultivo = campo.find('sensoresCultivo')
    if sensores_cultivo is not None:
        for sensor_cultivo in sensores_cultivo.findall('sensorT'):
            id_sensor_cultivo = sensor_cultivo.get('id')
            nombre_sensor_cultivo = sensor_cultivo.get('nombre')
            print(f"Sensor de cultivo: ID: {id_sensor_cultivo}, Nombre: {nombre_sensor_cultivo}")

            leer_frecuencias_cultivo(sensor_cultivo, id_sensor_cultivo)
            print("-" * 49)
        
def leer_frecuencias_cultivo(sensor_cultivo, id_sensor_cultivo):
    print(f"Frecuencias sensor de cultivo {id_sensor_cultivo}:")
    for frecuencia_sensorT in sensor_cultivo.findall('frecuencia'):
        id_frecuencia_sensorT = frecuencia_sensorT.get('idEstacion')
        texto_frecuencia_sensorT = frecuencia_sensorT.text.strip()
        valor_frecuencia_sensorT = int(texto_frecuencia_sensorT) if texto_frecuencia_sensorT.isdigit() else texto_frecuencia_sensorT
        print(f"  Estación: {id_frecuencia_sensorT}, Valor: {valor_frecuencia_sensorT}")
    



