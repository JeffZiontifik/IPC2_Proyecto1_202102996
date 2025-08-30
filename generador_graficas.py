# Modulo que nos permite generar nuestras gráficas usando Graphviz

try:
    import graphviz
    GRAPHVIZ_DISPONIBLE = True
except ImportError:
    GRAPHVIZ_DISPONIBLE = False
    print("Advertencia: Graphviz no está instalado. Use: pip install graphviz")

from estructura_datos.lista_enlazada import Lista

class GeneradorGraficas:
    def __init__(self):
        self.disponible = GRAPHVIZ_DISPONIBLE
    
    def _crear_tabla_html(self, matriz, etiquetas_filas, etiquetas_columnas, titulo):
        """Crea una tabla HTML para usar en Graphviz"""
        html = '<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
        
        # Título de la tabla
        num_columnas = etiquetas_columnas.obtener_tamaño() + 1
        html = html + '<TR><TD COLSPAN="' + str(num_columnas) + '" BGCOLOR="lightgray"><B>' + titulo + '</B></TD></TR>'
        
        # Encabezados de columnas
        html = html + '<TR><TD BGCOLOR="lightblue"><B> </B></TD>'
        for col in etiquetas_columnas.iterar():
            html = html + '<TD BGCOLOR="lightblue"><B>' + str(col) + '</B></TD>'
        html = html + '</TR>'
        
        # Filas con datos
        contador_fila = 0
        for fila_label in etiquetas_filas.iterar():
            html = html + '<TR><TD BGCOLOR="lightgreen"><B>' + str(fila_label) + '</B></TD>'
            for j in range(etiquetas_columnas.obtener_tamaño()):
                valor = matriz.obtener_valor(contador_fila, j)
                # Colorear las celdas según el valor
                if valor == 0:
                    color = "white"
                elif valor == 1:
                    color = "lightcyan"
                else:
                    color = "lightyellow"
                html = html + '<TD BGCOLOR="' + color + '">' + str(valor) + '</TD>'
            html = html + '</TR>'
            contador_fila = contador_fila + 1
        
        html = html + '</TABLE>>'
        return html
    
    def generar_tabla_matriz_frecuencias(self, campo, tipo_sensor="suelo"):
        """Genera la tabla de la matriz de frecuencias F[n,s] o F[n,t] como gráfica"""
        if not self.disponible:
            print("Error: Graphviz no está disponible")
            return False
        
        if not hasattr(campo, 'procesador'):
            print("Error: El campo no ha sido procesado")
            return False
        
        # Creamos el grafo
        dot = graphviz.Digraph(comment='Tabla Matriz Frecuencias - ' + campo.nombre)
        dot.attr(rankdir='TB')
        dot.attr(dpi='300')  # Alta resolución para gráfica
        
        # Obtenemos datos según el tipo de sensor
        if tipo_sensor == "suelo":
            sensores = campo.sensores_suelo
            matriz = campo.procesador.matriz_suelo
            titulo = "Matriz de Frecuencias - Sensores de Suelo - " + campo.nombre
        else:
            sensores = campo.sensores_cultivo
            matriz = campo.procesador.matriz_cultivo
            titulo = "Matriz de Frecuencias - Sensores de Cultivo - " + campo.nombre
        
        # Crear etiquetas usando listas enlazadas
        etiquetas_filas = Lista()
        for estacion in campo.estaciones_base.iterar():
            etiquetas_filas.insertar_al_final("Ee" + str(estacion.id).zfill(2))
        
        etiquetas_columnas = Lista()
        for sensor in sensores.iterar():
            etiquetas_columnas.insertar_al_final("Ss" + str(sensor.id).zfill(2))
        
        # Crear la tabla HTML
        tabla_html = self._crear_tabla_html(matriz, etiquetas_filas, etiquetas_columnas, titulo)
        
        # Agregar el nodo con la tabla
        dot.node('tabla', tabla_html, shape='none')
        
        # Guardar como gráfica
        nombre_archivo = "tabla_frecuencias_" + tipo_sensor + "_" + str(campo.id)
        try:
            dot.render(nombre_archivo, format='pdf', cleanup=True)
            print("Gráfica generada: " + nombre_archivo + ".pdf")
            return True
        except Exception as e:
            print("Error al generar gráfica: " + str(e))
            return False
    
    def generar_tabla_matriz_patrones(self, campo, tipo_sensor="suelo"):
        """Genera la tabla de la matriz de patrones Fp[n,s] o Fp[n,t] como gráfica"""
        if not self.disponible:
            print("Error: Graphviz no está disponible")
            return False
        
        if not hasattr(campo, 'procesador'):
            print("Error: El campo no ha sido procesado")
            return False
        
        # Creamos el grafo
        dot = graphviz.Digraph(comment='Tabla Matriz Patrones - ' + campo.nombre)
        dot.attr(rankdir='TB')
        dot.attr(dpi='300')
        
        # Obtenemos datos según el tipo de sensor
        if tipo_sensor == "suelo":
            sensores = campo.sensores_suelo
            matriz = campo.procesador.matriz_patrones_suelo
            titulo = "Matriz de Patrones - Sensores de Suelo - " + campo.nombre
        else:
            sensores = campo.sensores_cultivo
            matriz = campo.procesador.matriz_patrones_cultivo
            titulo = "Matriz de Patrones - Sensores de Cultivo - " + campo.nombre
        
        # Crear etiquetas usando listas enlazadas
        etiquetas_filas = Lista()
        for estacion in campo.estaciones_base.iterar():
            etiquetas_filas.insertar_al_final("Ee" + str(estacion.id).zfill(2))
        
        etiquetas_columnas = Lista()
        for sensor in sensores.iterar():
            if tipo_sensor == "suelo":
                etiquetas_columnas.insertar_al_final("Ss" + str(sensor.id).zfill(2))
            else:
                etiquetas_columnas.insertar_al_final("Tt" + str(sensor.id).zfill(2))
        
        # Crear la tabla HTML
        tabla_html = self._crear_tabla_html(matriz, etiquetas_filas, etiquetas_columnas, titulo)
        
        # Agregar el nodo con la tabla
        dot.node('tabla', tabla_html, shape='none')
        
        # Guardar como gráfica
        nombre_archivo = "tabla_patrones_" + tipo_sensor + "_" + str(campo.id)
        try:
            dot.render(nombre_archivo, format='pdf', cleanup=True)
            print("Gráfica generada: " + nombre_archivo + ".pdf")
            return True
        except Exception as e:
            print("Error al generar gráfica: " + str(e))
            return False
    
    def generar_tabla_matriz_reducida(self, campo):
        """Genera la tabla de la matriz reducida como gráfica"""
        if not self.disponible:
            print("Error: Graphviz no está disponible")
            return False
        
        if not hasattr(campo, 'grupos_estaciones'):
            print("Error: El campo no ha sido procesado")
            return False
        
        # Creamos el grafo
        dot = graphviz.Digraph(comment='Tabla Matriz Reducida - ' + campo.nombre)
        dot.attr(rankdir='TB')
        dot.attr(dpi='300')
        
        # Crear etiquetas para grupos de estaciones usando listas enlazadas
        etiquetas_grupos = Lista()
        grupos_validos = Lista()
        
        for i in range(campo.grupos_estaciones.obtener_tamaño()):
            grupo = campo.grupos_estaciones.obtener_por_indice(i)
            if grupo.obtener_tamaño() > 0:
                primer_indice = grupo.obtener_por_indice(0)
                primera_estacion = campo.estaciones_base.obtener_por_indice(primer_indice)
                etiqueta = "G" + str(i + 1) + "(Ee" + str(primera_estacion.id).zfill(2) + ")"
                etiquetas_grupos.insertar_al_final(etiqueta)
                grupos_validos.insertar_al_final(grupo)
        
        if etiquetas_grupos.obtener_tamaño() == 0:
            print("Error: No se encontraron grupos válidos")
            return False
        
        # Crear todas las listas de sensores
        todos_sensores = Lista()
        etiquetas_sensores = Lista()
        tipos_sensores = Lista()
        
        # Agregar sensores de suelo
        for sensor in campo.sensores_suelo.iterar():
            todos_sensores.insertar_al_final(sensor)
            etiquetas_sensores.insertar_al_final("Ss" + str(sensor.id).zfill(2))
            tipos_sensores.insertar_al_final("suelo")
        
        # Agregar sensores de cultivo
        for sensor in campo.sensores_cultivo.iterar():
            todos_sensores.insertar_al_final(sensor)
            etiquetas_sensores.insertar_al_final("Tt" + str(sensor.id).zfill(2))
            tipos_sensores.insertar_al_final("cultivo")
        
        # Crear tabla con GRUPOS como FILAS y SENSORES como COLUMNAS
        html = '<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
        
        # Título principal
        num_columnas_total = todos_sensores.obtener_tamaño() + 1
        html = html + '<TR><TD COLSPAN="' + str(num_columnas_total) + '" BGCOLOR="darkgray"><B>Matriz Reducida - Campo agricola ' + str(campo.id).zfill(2) + '</B></TD></TR>'
        
        # Subtítulo con separación de sensores
        html = html + '<TR><TD BGCOLOR="lightgray"><B>Grupo</B></TD>'
        
        # Encabezado de sensores de suelo
        for i in range(etiquetas_sensores.obtener_tamaño()):
            etiqueta = etiquetas_sensores.obtener_por_indice(i)
            tipo = tipos_sensores.obtener_por_indice(i)
            if tipo == "suelo":
                html = html + '<TD BGCOLOR="lightgreen"><B>' + str(etiqueta) + '</B></TD>'
            else:
                html = html + '<TD BGCOLOR="lightcoral"><B>' + str(etiqueta) + '</B></TD>'
        html = html + '</TR>'
        
        # Filas de datos: cada grupo como FILA
        for i in range(grupos_validos.obtener_tamaño()):
            grupo = grupos_validos.obtener_por_indice(i)
            etiqueta_grupo = etiquetas_grupos.obtener_por_indice(i)
            
            html = html + '<TR><TD BGCOLOR="lightblue"><B>' + str(etiqueta_grupo) + '</B></TD>'
            
            # Para cada sensor, calcular la suma de frecuencias de este grupo
            for j in range(todos_sensores.obtener_tamaño()):
                sensor = todos_sensores.obtener_por_indice(j)
                tipo_sensor = tipos_sensores.obtener_por_indice(j)
                
                suma_freq = 0
                for k in range(grupo.obtener_tamaño()):
                    indice_estacion = grupo.obtener_por_indice(k)
                    estacion = campo.estaciones_base.obtener_por_indice(indice_estacion)
                    
                    # Buscar frecuencia para esta estación
                    for freq in sensor.frecuencias.iterar():
                        if freq.id == estacion.id:
                            suma_freq = suma_freq + freq.valor
                            break
                
                # Colorear según el tipo de sensor y valor
                if suma_freq == 0:
                    color = "white"
                elif tipo_sensor == "suelo":
                    color = "lightyellow"
                else:
                    color = "lightcyan"
                
                html = html + '<TD BGCOLOR="' + color + '">' + str(suma_freq) + '</TD>'
            
            html = html + '</TR>'
        
        html = html + '</TABLE>>'
        
        # Agregar el nodo con la tabla
        dot.node('tabla', html, shape='none')
        
        # Guardar como gráfica
        nombre_archivo = "tabla_matriz_reducida_" + str(campo.id)
        try:
            dot.render(nombre_archivo, format='pdf', cleanup=True)
            print("Gráfica generada: " + nombre_archivo + ".pdf")
            return True
        except Exception as e:
            print("Error al generar gráfica: " + str(e))
            return False
    
    def generar_todas_tablas_pdf(self, campo):
        """Genera todas las tablas disponibles para un campo como gráficas"""
        if not self.disponible:
            print("Error: Graphviz no está disponible")
            return False
        
        print("Generando todas las gráficas para " + campo.nombre + "...")
        
        exito = True
        
        # Tabla de matriz de frecuencias para suelo
        print("- Generando gráfica matriz de frecuencias (suelo)...")
        if not self.generar_tabla_matriz_frecuencias(campo, "suelo"):
            exito = False
        
        # Tabla de matriz de frecuencias para cultivo
        print("- Generando gráfica matriz de frecuencias (cultivo)...")
        if not self.generar_tabla_matriz_frecuencias(campo, "cultivo"):
            exito = False
        
        # Tabla de matriz de patrones para suelo
        print("- Generando gráfica matriz de patrones (suelo)...")
        if not self.generar_tabla_matriz_patrones(campo, "suelo"):
            exito = False
        
        # Tabla de matriz de patrones para cultivo
        print("- Generando gráfica matriz de patrones (cultivo)...")
        if not self.generar_tabla_matriz_patrones(campo, "cultivo"):
            exito = False
        
        # Tabla de matriz reducida
        print("- Generando gráfica matriz reducida...")
        if not self.generar_tabla_matriz_reducida(campo):
            exito = False
        
        if exito:
            print("¡Todas las gráficas generadas exitosamente!")
        else:
            print("Algunas gráficas no pudieron generarse.")
        
        return exito

# funciones helper para usar desde el menu
def generar_grafica_campo(campo, tipo_grafica=1):
    generador = GeneradorGraficas()
    
    if not generador.disponible:
        print("Para usar esta función debe instalar Graphviz:")
        print("1. Instalar Python: pip install graphviz")
        print("2. Instalar Graphviz sistema: https://graphviz.org/download/")
        return False
    
    if tipo_grafica == 1:  # gráfica de matriz de frecuencias
        print("Seleccione tipo de sensor:")
        print("1. Sensores de suelo")
        print("2. Sensores de cultivo")
        try:
            tipo = int(input("Opción: "))
            if tipo == 1:
                return generador.generar_tabla_matriz_frecuencias(campo, "suelo")
            elif tipo == 2:
                return generador.generar_tabla_matriz_frecuencias(campo, "cultivo")
            else:
                print("Opción inválida")
                return False
        except ValueError:
            print("Entrada inválida")
            return False
    
    elif tipo_grafica == 2:  # gráfica de matriz de patrones
        print("Seleccione tipo de sensor:")
        print("1. Sensores de suelo")
        print("2. Sensores de cultivo")
        try:
            tipo = int(input("Opción: "))
            if tipo == 1:
                return generador.generar_tabla_matriz_patrones(campo, "suelo")
            elif tipo == 2:
                return generador.generar_tabla_matriz_patrones(campo, "cultivo")
            else:
                print("Opción inválida")
                return False
        except ValueError:
            print("Entrada inválida")
            return False
    
    elif tipo_grafica == 3:  # gráfica de matriz reducida
        return generador.generar_tabla_matriz_reducida(campo)
    
    elif tipo_grafica == 4:  # todas las gráficas
        return generador.generar_todas_tablas_pdf(campo)
    
    else:
        print("Tipo de gráfica inválido")
        return False