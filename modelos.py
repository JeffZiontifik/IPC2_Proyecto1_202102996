
# Métodos que nos sirven para almacenar los datos que leemos del XML

class DatosCampo:
    def __init__(self, id_campo, nombre_campo):
        self.id = id_campo
        self.nombre = nombre_campo

class DatosEstaciones:
    def __init__(self, id_estacion, nombre_estacion):
        self.id = id_estacion
        self.nombre = nombre_estacion

class DatosSensorSuelo:
    def __init__(self, id_sensor_suelo, nombre_sensor_suelo):
        self.id = id_sensor_suelo
        self.nombre = nombre_sensor_suelo

class DatosSensorCultivo:
    def __init__(self, id_sensor_cultivo, nombre_sensor_cultivo):
        self.id = id_sensor_cultivo
        self.nombre = nombre_sensor_cultivo

class DatosFrecuenciaSuelo:
    def __init__(self, id_frecuencia_sensorS, valor_frecuencia_sensorS):
        self.id = id_frecuencia_sensorS
        self.valor = valor_frecuencia_sensorS

class DatosFrecuenciaCultivo:
    def __init__(self, id_frecuencia_sensorT, valor_frecuencia_sensorT):
        self.id = id_frecuencia_sensorT
        self.valor = valor_frecuencia_sensorT