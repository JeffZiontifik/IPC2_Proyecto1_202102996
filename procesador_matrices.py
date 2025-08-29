# Modulo que nos ayuda a procesar las matrices

from estructura_datos.lista_enlazada import Lista

class MatrizFrecuencias:
    def __init__(self, num_estaciones, num_sensores):
        # creamos una matriz usando listas enlazadas
        self.num_estaciones = num_estaciones
        self.num_sensores = num_sensores
        self.filas = Lista()  # cada fila es una lista de frecuencias
        
        # inicializamos la matriz con ceros
        for i in range(num_estaciones):
            fila = Lista()
            for j in range(num_sensores):
                fila.insertar_al_final(0)
            self.filas.insertar_al_final(fila)
    
    def establecer_valor(self, fila, columna, valor):
        # establece un valor en la posicion [fila][columna]
        if fila >= 0 and fila < self.num_estaciones and columna >= 0 and columna < self.num_sensores:
            fila_datos = self.filas.obtener_por_indice(fila)
            if fila_datos is not None:
                # tenemos que recorrer manualmente hasta la columna deseada
                actual = fila_datos.cabeza
                for i in range(columna):
                    if actual is not None:
                        actual = actual.siguiente
                if actual is not None:
                    actual.dato = valor
    
    def obtener_valor(self, fila, columna):
        # obtiene el valor en la posicion [fila][columna]
        if fila >= 0 and fila < self.num_estaciones and columna >= 0 and columna < self.num_sensores:
            fila_datos = self.filas.obtener_por_indice(fila)
            if fila_datos is not None:
                return fila_datos.obtener_por_indice(columna)
        return 0
    
    def obtener_fila_como_lista(self, num_fila):
        # retorna una fila completa como lista enlazada
        if num_fila >= 0 and num_fila < self.num_estaciones:
            return self.filas.obtener_por_indice(num_fila)
        return None
    
    def mostrar_matriz(self, titulo, ids_estaciones, ids_sensores):
        # imprime la matriz de forma legible
        print(f"\n{titulo}")
        print("=" * 50)
        
        # encabezados de columnas (sensores)
        print("Estacion\\Sensor", end="")
        for sensor in ids_sensores.iterar():
            print(f"\t{sensor}", end="")
        print()
        
        # filas con datos
        contador_fila = 0
        for estacion in ids_estaciones.iterar():
            print(f"{estacion}", end="")
            for j in range(self.num_sensores):
                valor = self.obtener_valor(contador_fila, j)
                print(f"\t{valor}", end="")
            print()
            contador_fila = contador_fila + 1

class ProcesadorMatrices:
    def __init__(self, datos_campo):
        self.campo = datos_campo
        self.matriz_suelo = None
        self.matriz_cultivo = None
        self.matriz_patrones_suelo = None
        self.matriz_patrones_cultivo = None
    
    def crear_matrices_frecuencias(self):
        # crea las matrices F[n,s] y F[n,t] del enunciado
        print(f"\nProcesando campo: {self.campo.id}")
        print("Creando matrices de frecuencias...")
        
        num_estaciones = self.campo.estaciones_base.obtener_tamaño()
        num_sensores_suelo = self.campo.sensores_suelo.obtener_tamaño()
        num_sensores_cultivo = self.campo.sensores_cultivo.obtener_tamaño()
        
        self.matriz_suelo = MatrizFrecuencias(num_estaciones, num_sensores_suelo)
        self.matriz_cultivo = MatrizFrecuencias(num_estaciones, num_sensores_cultivo)
        
        # llenamos la matriz de suelo
        self._llenar_matriz_suelo()
        
        # llenamos la matriz de cultivo
        self._llenar_matriz_cultivo()
        
        print("Matrices de frecuencias creadas!")
    
    def _llenar_matriz_suelo(self):
        # llena la matriz de frecuencias de sensores de suelo
        contador_sensor = 0
        for sensor_suelo in self.campo.sensores_suelo.iterar():
            # para cada sensor, buscamos sus frecuencias por estacion
            for frecuencia in sensor_suelo.frecuencias.iterar():
                # encontramos el indice de la estacion
                indice_estacion = self._buscar_indice_estacion(frecuencia.id)
                if indice_estacion != -1:
                    self.matriz_suelo.establecer_valor(indice_estacion, contador_sensor, frecuencia.valor)
            contador_sensor = contador_sensor + 1
    
    def _llenar_matriz_cultivo(self):
        # llena la matriz de frecuencias de sensores de cultivo
        contador_sensor = 0
        for sensor_cultivo in self.campo.sensores_cultivo.iterar():
            # para cada sensor, buscamos sus frecuencias por estacion
            for frecuencia in sensor_cultivo.frecuencias.iterar():
                # encontramos el indice de la estacion
                indice_estacion = self._buscar_indice_estacion(frecuencia.id)
                if indice_estacion != -1:
                    self.matriz_cultivo.establecer_valor(indice_estacion, contador_sensor, frecuencia.valor)
            contador_sensor = contador_sensor + 1
    
    def _buscar_indice_estacion(self, id_estacion):
        # busca el indice de una estacion por su id
        contador = 0
        for estacion in self.campo.estaciones_base.iterar():
            if estacion.id == id_estacion:
                return contador
            contador = contador + 1
        return -1
    
    def crear_matrices_patrones(self):
        # convierte las matrices de frecuencias a matrices de patrones (0s y 1s)
        if self.matriz_suelo is None or self.matriz_cultivo is None:
            print("Error: Primero debe crear las matrices de frecuencias")
            return
        
        print("Creando matrices de patrones...")
        
        # creamos matrices del mismo tamaño
        self.matriz_patrones_suelo = MatrizFrecuencias(self.matriz_suelo.num_estaciones, self.matriz_suelo.num_sensores)
        self.matriz_patrones_cultivo = MatrizFrecuencias(self.matriz_cultivo.num_estaciones, self.matriz_cultivo.num_sensores)
        
        # convertimos frecuencias a patrones (0 si frecuencia=0, 1 si frecuencia>0)
        for i in range(self.matriz_suelo.num_estaciones):
            for j in range(self.matriz_suelo.num_sensores):
                valor_original = self.matriz_suelo.obtener_valor(i, j)
                patron = 1 if valor_original > 0 else 0
                self.matriz_patrones_suelo.establecer_valor(i, j, patron)
        
        for i in range(self.matriz_cultivo.num_estaciones):
            for j in range(self.matriz_cultivo.num_sensores):
                valor_original = self.matriz_cultivo.obtener_valor(i, j)
                patron = 1 if valor_original > 0 else 0
                self.matriz_patrones_cultivo.establecer_valor(i, j, patron)
        
        print("Matrices de patrones creadas!")
    
    def agrupar_estaciones_similares(self):
        # encuentra estaciones con patrones identicos y las agrupa
        if self.matriz_patrones_suelo is None or self.matriz_patrones_cultivo is None:
            print("Error: Primero debe crear las matrices de patrones")
            return
        
        print("Analizando patrones para agrupar estaciones...")
        
        grupos = Lista()  # lista de grupos de estaciones similares
        estaciones_procesadas = Lista()  # para no procesar la misma estacion dos veces
        
        # comparamos cada estacion con las demas
        for i in range(self.matriz_patrones_suelo.num_estaciones):
            if self._estacion_ya_procesada(i, estaciones_procesadas):
                continue
            
            grupo_actual = Lista()
            grupo_actual.insertar_al_final(i)  # agregamos la estacion actual al grupo
            
            # buscamos otras estaciones con el mismo patron
            for j in range(i + 1, self.matriz_patrones_suelo.num_estaciones):
                if self._estacion_ya_procesada(j, estaciones_procesadas):
                    continue
                
                if self._patrones_son_iguales(i, j):
                    grupo_actual.insertar_al_final(j)
                    estaciones_procesadas.insertar_al_final(j)
            
            grupos.insertar_al_final(grupo_actual)
            estaciones_procesadas.insertar_al_final(i)
        
        print(f"Se encontraron {grupos.obtener_tamaño()} grupos de estaciones")
        self._mostrar_grupos(grupos)
        
        return grupos
    
    def _estacion_ya_procesada(self, indice_estacion, lista_procesadas):
        # verifica si una estacion ya fue procesada
        for procesada in lista_procesadas.iterar():
            if procesada == indice_estacion:
                return True
        return False
    
    def _patrones_son_iguales(self, estacion1, estacion2):
        # compara si dos estaciones tienen patrones identicos en ambas matrices
        # primero comparamos patrones de suelo
        for j in range(self.matriz_patrones_suelo.num_sensores):
            patron1 = self.matriz_patrones_suelo.obtener_valor(estacion1, j)
            patron2 = self.matriz_patrones_suelo.obtener_valor(estacion2, j)
            if patron1 != patron2:
                return False
        
        # luego comparamos patrones de cultivo
        for j in range(self.matriz_patrones_cultivo.num_sensores):
            patron1 = self.matriz_patrones_cultivo.obtener_valor(estacion1, j)
            patron2 = self.matriz_patrones_cultivo.obtener_valor(estacion2, j)
            if patron1 != patron2:
                return False
        
        return True
    
    def _mostrar_grupos(self, grupos):
        # muestra los grupos de estaciones encontrados
        contador_grupo = 1
        for grupo in grupos.iterar():
            print(f"Grupo {contador_grupo}: ", end="")
            nombres_estaciones = ""
            for indice_estacion in grupo.iterar():
                estacion = self.campo.estaciones_base.obtener_por_indice(indice_estacion)
                nombres_estaciones = nombres_estaciones + estacion.id
                if grupo.obtener_por_indice(grupo.obtener_tamaño() - 1) != indice_estacion:
                    nombres_estaciones = nombres_estaciones + ", "
            print(nombres_estaciones)
            contador_grupo = contador_grupo + 1
    
    def mostrar_matrices(self):
        # muestra todas las matrices creadas
        if self.matriz_suelo is not None and self.matriz_cultivo is not None:
            # creamos listas de IDs para los headers
            ids_estaciones = Lista()
            for estacion in self.campo.estaciones_base.iterar():
                ids_estaciones.insertar_al_final(estacion.id)
            
            ids_sensores_suelo = Lista()
            for sensor in self.campo.sensores_suelo.iterar():
                ids_sensores_suelo.insertar_al_final(sensor.id)
            
            ids_sensores_cultivo = Lista()
            for sensor in self.campo.sensores_cultivo.iterar():
                ids_sensores_cultivo.insertar_al_final(sensor.id)
            
            # mostramos las matrices
            self.matriz_suelo.mostrar_matriz("MATRIZ DE FRECUENCIAS - SENSORES DE SUELO", ids_estaciones, ids_sensores_suelo)
            self.matriz_cultivo.mostrar_matriz("MATRIZ DE FRECUENCIAS - SENSORES DE CULTIVO", ids_estaciones, ids_sensores_cultivo)
            
            if self.matriz_patrones_suelo is not None and self.matriz_patrones_cultivo is not None:
                self.matriz_patrones_suelo.mostrar_matriz("MATRIZ DE PATRONES - SENSORES DE SUELO", ids_estaciones, ids_sensores_suelo)
                self.matriz_patrones_cultivo.mostrar_matriz("MATRIZ DE PATRONES - SENSORES DE CULTIVO", ids_estaciones, ids_sensores_cultivo)

def procesar_campo_agricola(datos_campo):
    # funcion principal que ejecuta todo el algoritmo para un campo
    procesador = ProcesadorMatrices(datos_campo)
    
    print(f"Iniciando procesamiento del campo {datos_campo.id}...")
    procesador.crear_matrices_frecuencias()
    procesador.crear_matrices_patrones()
    grupos = procesador.agrupar_estaciones_similares()
    
    # mostramos las matrices si el usuario quiere verlas
    procesador.mostrar_matrices()
    
    return procesador, grupos