import os
from lector_xml import leer_archivo, obtener_campos_agricolas
from procesador_matrices import procesar_campo_agricola
from generador_graficas import GeneradorGraficas
from xml.etree import ElementTree as ET
from estructura_datos.lista_enlazada import Lista

# Creamos nuestro menu principal
class Menu:
    def __init__(self):
        self.ruta_del_archivo = None
        self.ejecutando = True
        self.campos_cargados = None  # aqui almacenamos los campos procesados

    # Método o función que muestra las opciones del menú
    def mostrar_menu(self):
        print("-" * 49)
        print("              Menú Principal")
        print("-" * 49)
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar gráfica")
        print("6. Salir")
        print("-" * 49)

    # Método o función para ejecutar el menú interactivo
    def ejecutar(self):
        while self.ejecutando:
            self.mostrar_menu()
            
            try:
                opcion = int(input("Ingrese una opción: "))
                
                if opcion == 1:
                    self.cargar_archivo()
                elif opcion == 2:
                    self.procesar_archivo()
                elif opcion == 3:
                    self.escribir_salida()
                elif opcion == 4:
                    self.mostrar_datos_estudiante()
                elif opcion == 5:
                    self.generar_grafica()
                elif opcion == 6:
                    self.salir()
                else:
                    print("Opción inválida. Intente de nuevo.")
                    self.pausar()
                    
            except ValueError:
                print("Error: Debe ingresar un número.")
                self.pausar()

    # Método o función para cargar el archivo .xml
    def cargar_archivo(self):
        print("\nOpción 1: Cargar archivo")
        ruta_carpeta = input("Ingrese la ruta del archivo XML: ")
        nombre_archivo = input("Ingrese el nombre del archivo XML: ")
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

        try:
            self.ruta_del_archivo = ruta_completa
            # aqui llamamos a la funcion mejorada que almacena los datos
            self.campos_cargados = leer_archivo(ruta_completa)
            print(f"Archivo cargado exitosamente desde: {ruta_completa}")
            print(f"Se cargaron {self.campos_cargados.obtener_tamaño()} campos agrícolas")
            
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo en la ruta: {ruta_completa}")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
        
        self.pausar()

    # Método o función para procesar el archivo .xml
    def procesar_archivo(self):
        print("\nOpción 2: Procesar archivo")
        if self.ruta_del_archivo is None or self.campos_cargados is None:
            print("Error: Debe cargar un archivo primero.")
            self.pausar()
            return
        
        try:
            print("Iniciando procesamiento de matrices y patrones...")
            print("=" * 60)
            
            # procesamos cada campo agricola cargado
            for campo in self.campos_cargados.iterar():
                print(f"\n>>> Procesando campo: {campo.nombre}")
                procesador, grupos = procesar_campo_agricola(campo)
                
                # guardamos el procesador en el campo para usarlo despues
                campo.procesador = procesador
                campo.grupos_estaciones = grupos
                
                print(f"Campo {campo.id} procesado exitosamente!")
                print("=" * 60)
            
            print("\nTodos los campos han sido procesados correctamente.")
            
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
        
        self.pausar()

    # Método o función para generar el archivo de salida .xml
    def escribir_salida(self):
        print("\nOpción 3: Escribir archivo salida")
        
        if self.campos_cargados is None:
            print("Error: Debe cargar un archivo primero.")
            self.pausar()
            return
        
        # Verificar que los campos hayan sido procesados
        campos_procesados = 0
        for campo in self.campos_cargados.iterar():
            if hasattr(campo, 'procesador') and hasattr(campo, 'grupos_estaciones'):
                campos_procesados += 1
                print(f"Campo procesado encontrado: {campo.nombre}")
                print(f"  - Grupos de estaciones: {campo.grupos_estaciones.obtener_tamaño()}")
                print(f"  - Sensores de suelo: {campo.sensores_suelo.obtener_tamaño()}")
                print(f"  - Sensores de cultivo: {campo.sensores_cultivo.obtener_tamaño()}")
        
        if campos_procesados == 0:
            print("Error: Debe procesar el archivo primero (opción 2).")
            self.pausar()
            return
        
        print(f"Se encontraron {campos_procesados} campos procesados.")
        
        ruta_salida = input("Ingrese la ruta donde guardar el archivo: ")
        nombre_salida = input("Ingrese el nombre del archivo de salida: ")
        
        # Agregar extensión .xml si no la tiene
        if not nombre_salida.endswith('.xml'):
            nombre_salida += '.xml'
        
        ruta_completa_salida = os.path.join(ruta_salida, nombre_salida)
        
        try:
            self._generar_xml_salida(ruta_completa_salida)
            print(f"Archivo de salida generado exitosamente: {ruta_completa_salida}")
        except Exception as e:
            print(f"Error al generar archivo de salida: {e}")
            import traceback
            traceback.print_exc()
        
        self.pausar()

    def _concatenar_nombres(self, lista_nombres):
        """Concatena nombres de una Lista TDA con comas"""
        if lista_nombres.obtener_tamaño() == 0:
            return ""
        
        resultado = ""
        for i in range(lista_nombres.obtener_tamaño()):
            nombre = lista_nombres.obtener_por_indice(i)
            if i == 0:
                resultado = nombre
            else:
                resultado = resultado + ", " + nombre
        
        return resultado

    def _generar_xml_salida(self, ruta_archivo):
        """Genera el XML de salida con las estaciones agrupadas y frecuencias sumadas"""
        from xml.etree.ElementTree import Element, SubElement, ElementTree
        
        # Elemento raíz
        root = Element("camposAgricolas")
        
        for campo in self.campos_cargados.iterar():
            # Verificar que el campo haya sido procesado
            if not (hasattr(campo, 'procesador') and hasattr(campo, 'grupos_estaciones')):
                print(f"Saltando campo {campo.nombre} - no procesado")
                continue
            
            print(f"Generando XML para campo: {campo.nombre}")
            
            # Elemento campo
            elemento_campo = SubElement(root, "campo", id=str(campo.id), nombre=campo.nombre)
            
            # Estaciones base reducidas  
            estaciones_reducidas = SubElement(elemento_campo, "estacionesBaseReducidas")
            
            # Debug: verificar grupos
            print(f"Número de grupos: {campo.grupos_estaciones.obtener_tamaño()}")
            
            # Crear las estaciones agrupadas
            for i in range(campo.grupos_estaciones.obtener_tamaño()):
                grupo = campo.grupos_estaciones.obtener_por_indice(i)
                
                if grupo.obtener_tamaño() == 0:
                    continue
                
                # Obtener el primer ID del grupo y concatenar nombres usando TDA
                primer_indice = grupo.obtener_por_indice(0)
                primera_estacion = campo.estaciones_base.obtener_por_indice(primer_indice)
                primer_id = primera_estacion.id
                
                # Usar Lista TDA en lugar de lista nativa
                nombres_agrupadas = Lista()
                for j in range(grupo.obtener_tamaño()):
                    indice_estacion = grupo.obtener_por_indice(j)
                    estacion = campo.estaciones_base.obtener_por_indice(indice_estacion)
                    nombres_agrupadas.insertar_al_final(estacion.nombre)
                
                nombre_concatenado = self._concatenar_nombres(nombres_agrupadas)
                
                print(f"Grupo {i+1}: ID={primer_id}, Nombres={nombre_concatenado}")
                
                SubElement(estaciones_reducidas, "estacion", 
                          id=str(primer_id), 
                          nombre=nombre_concatenado)
            
            # Sensores de suelo con frecuencias reducidas
            sensores_suelo_elem = SubElement(elemento_campo, "sensoresSuelo")
            self._agregar_sensores_reducidos_suelo(sensores_suelo_elem, campo)
            
            # Sensores de cultivo con frecuencias reducidas
            sensores_cultivo_elem = SubElement(elemento_campo, "sensoresCultivo")
            self._agregar_sensores_reducidos_cultivo(sensores_cultivo_elem, campo)
        
        # Formatear el XML con indentación antes de guardar
        self._formatear_xml_bonito(root)
        
        # Guardar el archivo
        tree = ElementTree(root)
        tree.write(ruta_archivo, encoding='utf-8', xml_declaration=True)
        print(f"XML generado correctamente en: {ruta_archivo}")
    
    def _agregar_sensores_reducidos_suelo(self, parent_elem, campo):
        """Agrega los sensores de suelo con frecuencias sumadas por grupos"""
        from xml.etree.ElementTree import SubElement
        
        print(f"Procesando {campo.sensores_suelo.obtener_tamaño()} sensores de suelo")
        
        for i in range(campo.sensores_suelo.obtener_tamaño()):
            sensor = campo.sensores_suelo.obtener_por_indice(i)
            sensor_elem = SubElement(parent_elem, "sensorS", 
                                    id=str(sensor.id), 
                                    nombre=sensor.nombre)
            
            print(f"  Sensor: {sensor.nombre} (ID: {sensor.id})")
            
            # Calcular frecuencias agrupadas
            for j in range(campo.grupos_estaciones.obtener_tamaño()):
                grupo = campo.grupos_estaciones.obtener_por_indice(j)
                
                if grupo.obtener_tamaño() == 0:
                    continue
                
                # Sumar las frecuencias de todas las estaciones del grupo
                suma_frecuencias = 0
                primer_indice = grupo.obtener_por_indice(0)
                primera_estacion = campo.estaciones_base.obtener_por_indice(primer_indice)
                primer_id_grupo = primera_estacion.id
                
                for k in range(grupo.obtener_tamaño()):
                    indice_estacion = grupo.obtener_por_indice(k)
                    estacion = campo.estaciones_base.obtener_por_indice(indice_estacion)
                    
                    # Buscar la frecuencia de este sensor para esta estación
                    for l in range(sensor.frecuencias.obtener_tamaño()):
                        frecuencia = sensor.frecuencias.obtener_por_indice(l)
                        if frecuencia.id == estacion.id:
                            suma_frecuencias += frecuencia.valor
                            print(f"    Estación {estacion.id}: +{frecuencia.valor}")
                            break
                
                # Solo agregar si hay frecuencia > 0
                if suma_frecuencias > 0:
                    freq_elem = SubElement(sensor_elem, "frecuencia", 
                                         idEstacion=str(primer_id_grupo))
                    freq_elem.text = str(suma_frecuencias)
                    print(f"    Grupo {j+1}: Total={suma_frecuencias}")
    
    def _agregar_sensores_reducidos_cultivo(self, parent_elem, campo):
        """Agrega los sensores de cultivo con frecuencias sumadas por grupos"""
        from xml.etree.ElementTree import SubElement
        
        print(f"Procesando {campo.sensores_cultivo.obtener_tamaño()} sensores de cultivo")
        
        for i in range(campo.sensores_cultivo.obtener_tamaño()):
            sensor = campo.sensores_cultivo.obtener_por_indice(i)
            sensor_elem = SubElement(parent_elem, "sensorT", 
                                    id=str(sensor.id), 
                                    nombre=sensor.nombre)
            
            print(f"  Sensor: {sensor.nombre} (ID: {sensor.id})")
            
            # Calcular frecuencias agrupadas
            for j in range(campo.grupos_estaciones.obtener_tamaño()):
                grupo = campo.grupos_estaciones.obtener_por_indice(j)
                
                if grupo.obtener_tamaño() == 0:
                    continue
                
                # Sumar las frecuencias de todas las estaciones del grupo
                suma_frecuencias = 0
                primer_indice = grupo.obtener_por_indice(0)
                primera_estacion = campo.estaciones_base.obtener_por_indice(primer_indice)
                primer_id_grupo = primera_estacion.id
                
                for k in range(grupo.obtener_tamaño()):
                    indice_estacion = grupo.obtener_por_indice(k)
                    estacion = campo.estaciones_base.obtener_por_indice(indice_estacion)
                    
                    # Buscar la frecuencia de este sensor para esta estación
                    for l in range(sensor.frecuencias.obtener_tamaño()):
                        frecuencia = sensor.frecuencias.obtener_por_indice(l)
                        if frecuencia.id == estacion.id:
                            suma_frecuencias += frecuencia.valor
                            print(f"    Estación {estacion.id}: +{frecuencia.valor}")
                            break
                
                # Solo agregar si hay frecuencia > 0
                if suma_frecuencias > 0:
                    freq_elem = SubElement(sensor_elem, "frecuencia", 
                                         idEstacion=str(primer_id_grupo))
                    freq_elem.text = str(suma_frecuencias)
                    print(f"    Grupo {j+1}: Total={suma_frecuencias}")

    # Método o función para mostrar los datos del estudiante
    def mostrar_datos_estudiante(self):
        print("\n" + "-" * 49)
        print("           Datos del estudiante")
        print("-" * 49)
        print("Nombre: Anferny Jefferson Jolón Palencia")
        print("Carné: 202102996")
        print("Curso: Introducción a la Programación y Computación 2")
        print("Sección: N")
        print("Documentación: https://github.com/tu-usuario/IPC2_Proyecto1_202102996")
        print("-" * 49)
        self.pausar()

    # Método o función para generar gráfica
    def generar_grafica(self):
        print("\nOpción 5: Generar gráfica")
        
        if self.campos_cargados is None:
            print("Error: Debe cargar un archivo primero.")
            self.pausar()
            return
        
        # mostramos los campos disponibles
        print("Campos disponibles:")
        contador = 1
        for campo in self.campos_cargados.iterar():
            print(f"{contador}. {campo.nombre} (ID: {campo.id})")
            contador = contador + 1
        
        try:
            opcion_campo = int(input("Seleccione el número del campo: "))
            if opcion_campo < 1 or opcion_campo > self.campos_cargados.obtener_tamaño():
                print("Opción inválida.")
                self.pausar()
                return
            
            campo_seleccionado = self.campos_cargados.obtener_por_indice(opcion_campo - 1)
            
            print("\nTipo de gráfica:")
            print("1. Gráfica de matriz de frecuencias")
            print("2. Gráfica de matriz de patrones")
            print("3. Gráfica de matriz reducida")
            print("4. Generar todas las gráficas")
            
            tipo_grafica = int(input("Seleccione el tipo: "))
            
            print(f"Generando gráfica para campo {campo_seleccionado.nombre}...")
            
            # verificamos que el campo este procesado
            if not (hasattr(campo_seleccionado, 'procesador') and hasattr(campo_seleccionado, 'grupos_estaciones')):
                print("Error: El campo debe ser procesado primero (opción 2)")
                self.pausar()
                return
            
            generador = GeneradorGraficas()
            
            if tipo_grafica == 1:  # matriz de frecuencias
                print("Seleccione tipo de sensor:")
                print("1. Sensores de suelo")
                print("2. Sensores de cultivo")
                tipo = int(input("Opción: "))
                if tipo == 1:
                    exito = generador.generar_tabla_matriz_frecuencias(campo_seleccionado, "suelo")
                elif tipo == 2:
                    exito = generador.generar_tabla_matriz_frecuencias(campo_seleccionado, "cultivo")
                else:
                    print("Opción inválida")
                    self.pausar()
                    return
                    
            elif tipo_grafica == 2:  # matriz de patrones
                print("Seleccione tipo de sensor:")
                print("1. Sensores de suelo")
                print("2. Sensores de cultivo")
                tipo = int(input("Opción: "))
                if tipo == 1:
                    exito = generador.generar_tabla_matriz_patrones(campo_seleccionado, "suelo")
                elif tipo == 2:
                    exito = generador.generar_tabla_matriz_patrones(campo_seleccionado, "cultivo")
                else:
                    print("Opción inválida")
                    self.pausar()
                    return
                    
            elif tipo_grafica == 3:  # matriz reducida
                exito = generador.generar_tabla_matriz_reducida(campo_seleccionado)
                
            elif tipo_grafica == 4:  # todas las gráficas
                exito = generador.generar_todas_tablas_pdf(campo_seleccionado)
                
            else:
                print("Tipo de gráfica inválido")
                self.pausar()
                return
            
            if exito:
                print("¡Gráfica(s) generada(s) exitosamente!")
            else:
                print("Error al generar la(s) gráfica(s).")
                
        except ValueError:
            print("Error: Debe ingresar un número válido.")
        except Exception as e:
            print(f"Error al generar gráfica: {e}")
        
        self.pausar()

    # Método o función para salir del programa
    def salir(self):
        print("\nGracias por usar el sistema de agricultura de precisión!")
        print("Saliendo del programa...")
        self.ejecutando = False

    # Método o función para pausar la ejecución
    def pausar(self):
        input("\nPresiona Enter para continuar...")

    def _formatear_xml_bonito(self, elem, nivel=0):
        """Función para agregar indentación y formato lindo al XML"""
        espacios = "\n" + "  " * nivel  # 2 espacios por cada nivel
        
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = espacios + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = espacios
            
            for hijo in elem:
                self._formatear_xml_bonito(hijo, nivel + 1)
            
            if not hijo.tail or not hijo.tail.strip():
                hijo.tail = espacios
        else:
            if nivel and (not elem.tail or not elem.tail.strip()):
                elem.tail = espacios