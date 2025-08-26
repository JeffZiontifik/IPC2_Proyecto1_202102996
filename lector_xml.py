import xml.etree.ElementTree as ET

def leer_archivo (ruta_del_archivo):
    tree = ET.parse(ruta_del_archivo)
    root = tree.getroot()
    
    #Leemos los datos del campo en el XML
    for campo in root.findall('campo'):
        id_campo = campo.get('id') #Usamos get porque es un atributo y no un elemento
        nombre_campo = campo.get('nombre')
        print(f"Cargando campo agrícola {id_campo}...")
        print(f"ID: {id_campo}, Nombre: {nombre_campo}")
        print("-" * 49)

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

        print("Sensores de Suelo:")
        sensores_suelo = campo.find('sensoresSuelo')
        if sensores_suelo is not None:
            for sensor_suelo in sensores_suelo.findall('sensorS'):
                id_sensor_suelo = sensor_suelo.get('id')
                nombre_sensor_suelo = sensor_suelo.get('nombre')
                print(f"Sensor de suelo: ID: {id_sensor_suelo}, Nombre: {nombre_sensor_suelo}")
        
                print(f"Frecuencias sensor de suelo {id_sensor_suelo}:")
                for frecuencia_sensorS in sensor_suelo.findall('frecuencia'):
                    id_frecuencia_sensorS = frecuencia_sensorS.get('idEstacion')
                    valor_frecuencia_sensorS = frecuencia_sensorS.text
                    print(f"  Estación: {id_frecuencia_sensorS}, Valor: {valor_frecuencia_sensorS}")
    
                print("-" * 49)

        print("Sensores de Cultivo:")
        sensores_cultivo = campo.find('sensoresCultivo')
        if sensores_cultivo is not None:
            for sensor_cultivo in sensores_cultivo.findall('sensorT'):
                id_sensor_cultivo = sensor_cultivo.get('id')
                nombre_sensor_cultivo = sensor_cultivo.get('nombre')
                print(f"Sensor de cultivo: ID: {id_sensor_cultivo}, Nombre: {nombre_sensor_cultivo}")
        
                print(f"Frecuencias sensor de suelo {id_sensor_cultivo}:")
                for frecuencia_sensorT in sensor_suelo.findall('frecuencia'):
                    id_frecuencia_sensorT = frecuencia_sensorT.get('idEstacion')
                    valor_frecuencia_sensorT = frecuencia_sensorT.text
                    print(f"  Estación: {id_frecuencia_sensorT}, Valor: {valor_frecuencia_sensorT}")
    
                print("-" * 49)


