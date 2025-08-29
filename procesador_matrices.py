from estructura_datos.lista_enlazada import Lista
from modelos import DatosFrecuenciaSuelo, DatosFrecuenciaCultivo

class Matriz:
    def __init__(self, num_filas, num_columnas):
        self.num_filas = num_filas
        self.num_columnas = num_columnas
        self.matriz = Lista()

        # Crear matriz inicializada con ceros
        for i in range(num_filas):
            fila = Lista()
            for j in range(num_columnas):
                frecuencia = leer_frecuencias_suelo("", "0")
                fila.inserta(frecuencia)
            self.matriz.inserta(fila)
    
    def establecer(self, num_fila, num_columna, frecuencia):
        fila = self.matriz.obtener(num_fila)
        if fila:
            columna = fila.cabeza
            for i in range(num_columna):
                if columna:
                    columna = columna.siguiente
                if columna:
                    columna.dato = frecuencia

    def obtener(self, num_fila, num_columna):
        fila = self.matriz.obtener(num_fila)
        if fila:
            return fila.obtener(num_columna)
        else:
            return None
        
    def mostrar(self, titulo, headers_fila, headers_columna, id_sensor_suelo, id_estacion):
        print(f"\n{titulo}")
        print(" " * 49)

        # Headers de las columnas
        print("Estación\\Sensor", end = "\t")
        for j in range(self.num_columnas):
            print(f"{id_sensor_suelo}", end = "\t")

        # Filas con sus datos
        for i in range(self.num_filas):
            print(f"{id_estacion}", end = "\t")
            for j in range(self.num_columnas):
                frecuencia = self.obtener(i, j)
                print(f"{frecuencia}", end = "\t")
            print()


