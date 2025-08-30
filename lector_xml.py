# >Lector XML

import xml.etree.ElementTree as ET
from estructura_datos.lista_enlazada import Lista
from modelos import DatosCampo, DatosEstaciones, DatosSensorSuelo, DatosSensorCultivo, DatosFrecuenciaSuelo, DatosFrecuenciaCultivo

# Lista global para almacenar todos los campos agricolas
campos_agricolas = Lista()

def leer_archivo(ruta_del_archivo):
    # funcion principal que lee todo el XML y almacena los datos
    global campos_agricolas
    campos_agricolas = Lista()  # reiniciamos la lista
    
    tree = ET.parse(ruta_del_archivo)
    root = tree.getroot()
    
    for campo in root.findall('campo'):
        datos_campo = leer_datos_campo(campo)
        leer_estaciones_base(campo, datos_campo)
        leer_sensores_suelo(campo, datos_campo)
        leer_sensores_cultivo(campo, datos_campo)
        
        # agregamos el campo completo a nuestra lista global
        campos_agricolas.insertar_al_final(datos_campo)
    
    return campos_agricolas

def leer_datos_campo(campo):
    # leemos los datos del campo en el XML y creamos el objeto
    id_campo = campo.get('id')
    nombre_campo = campo.get('nombre')
    print(f"Cargando campo agrícola {id_campo}...")
    print(f"ID: {id_campo}, Nombre: {nombre_campo}")
    print("-" * 49)
    
    # creamos el objeto campo con listas para sus componentes
    datos_campo = DatosCampo(id_campo, nombre_campo)
    datos_campo.estaciones_base = Lista()
    datos_campo.sensores_suelo = Lista()
    datos_campo.sensores_cultivo = Lista()
    
    return datos_campo

def leer_estaciones_base(campo, datos_campo):
    # leemos las estaciones base y las almacenamos en la lista del campo
    print("Estaciones Base:")
    estaciones_base = campo.find('estacionesBase')
    if estaciones_base is not None:
        for estacion in estaciones_base.findall('estacion'):
            id_estacion = estacion.get('id')
            nombre_estacion = estacion.get('nombre')
            print(f"Creando estacion base {id_estacion}...")
            print(f"ID: {id_estacion}, Nombre: {nombre_estacion}")
            print("-" * 49)
            
            # creamos el objeto estacion y lo agregamos a la lista
            datos_estacion = DatosEstaciones(id_estacion, nombre_estacion)
            datos_campo.estaciones_base.insertar_al_final(datos_estacion)

def leer_sensores_suelo(campo, datos_campo):
    print("Sensores de Suelo:")
    sensores_suelo = campo.find('sensoresSuelo')
    if sensores_suelo is not None:
        for sensor_suelo in sensores_suelo.findall('sensorS'):
            id_sensor_suelo = sensor_suelo.get('id')
            nombre_sensor_suelo = sensor_suelo.get('nombre')
            print(f"Sensor de suelo: ID: {id_sensor_suelo}, Nombre: {nombre_sensor_suelo}")
            
            # creamos el objeto sensor con su lista de frecuencias
            datos_sensor = DatosSensorSuelo(id_sensor_suelo, nombre_sensor_suelo)
            datos_sensor.frecuencias = Lista()
            
            leer_frecuencias_suelo(sensor_suelo, id_sensor_suelo, datos_sensor)
            datos_campo.sensores_suelo.insertar_al_final(datos_sensor)
            print("-" * 49)

def leer_frecuencias_suelo(sensor_suelo, id_sensor_suelo, datos_sensor):           
    print(f"Frecuencias sensor de suelo {id_sensor_suelo}:")
    for frecuencia_sensorS in sensor_suelo.findall('frecuencia'):
        id_frecuencia_sensorS = frecuencia_sensorS.get('idEstacion')
        texto_frecuencia_sensorS = frecuencia_sensorS.text.strip()
        valor_frecuencia_sensorS = int(texto_frecuencia_sensorS) if texto_frecuencia_sensorS.isdigit() else texto_frecuencia_sensorS
        print(f"  Estación: {id_frecuencia_sensorS}, Valor: {valor_frecuencia_sensorS}")
        
        # creamos el objeto frecuencia y lo agregamos a la lista del sensor
        datos_frecuencia = DatosFrecuenciaSuelo(id_frecuencia_sensorS, valor_frecuencia_sensorS)
        datos_sensor.frecuencias.insertar_al_final(datos_frecuencia)

def leer_sensores_cultivo(campo, datos_campo):    
    print("Sensores de Cultivo:")
    sensores_cultivo = campo.find('sensoresCultivo')
    if sensores_cultivo is not None:
        for sensor_cultivo in sensores_cultivo.findall('sensorT'):
            id_sensor_cultivo = sensor_cultivo.get('id')
            nombre_sensor_cultivo = sensor_cultivo.get('nombre')
            print(f"Sensor de cultivo: ID: {id_sensor_cultivo}, Nombre: {nombre_sensor_cultivo}")

            # creamos el objeto sensor con su lista de frecuencias
            datos_sensor = DatosSensorCultivo(id_sensor_cultivo, nombre_sensor_cultivo)
            datos_sensor.frecuencias = Lista()
            
            leer_frecuencias_cultivo(sensor_cultivo, id_sensor_cultivo, datos_sensor)
            datos_campo.sensores_cultivo.insertar_al_final(datos_sensor)
            print("-" * 49)
        
def leer_frecuencias_cultivo(sensor_cultivo, id_sensor_cultivo, datos_sensor):
    print(f"Frecuencias sensor de cultivo {id_sensor_cultivo}:")
    for frecuencia_sensorT in sensor_cultivo.findall('frecuencia'):
        id_frecuencia_sensorT = frecuencia_sensorT.get('idEstacion')
        texto_frecuencia_sensorT = frecuencia_sensorT.text.strip()
        valor_frecuencia_sensorT = int(texto_frecuencia_sensorT) if texto_frecuencia_sensorT.isdigit() else texto_frecuencia_sensorT
        print(f"  Estación: {id_frecuencia_sensorT}, Valor: {valor_frecuencia_sensorT}")
        
        # creamos el objeto frecuencia y lo agregamos a la lista del sensor
        datos_frecuencia = DatosFrecuenciaCultivo(id_frecuencia_sensorT, valor_frecuencia_sensorT)
        datos_sensor.frecuencias.insertar_al_final(datos_frecuencia)

def obtener_campos_agricolas():
    # funcion helper para obtener la lista de campos desde otros modulos
    global campos_agricolas
    return campos_agricolas