import os
from lector_xml import leer_archivo, leer_datos_campo, leer_estaciones_base, leer_sensores_suelo, leer_frecuencias_suelo, leer_sensores_cultivo
from procesador_matrices import procesar_campo_agricola
from xml.etree import ElementTree as ET

#Creamos nuestro menu principal
class Menu:
    def __init__(self):
        self.ruta_del_archivo = None
        self.ejecutando = True
        self.campos_cargados = None

    #Método o función que muestra las opciones del menú
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

    #Método o función para ejecutar el menú interactivo
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

    #Método o función para cargar el archivo .xml
    def cargar_archivo(self):
        print("\nOpción 1: Cargar archivo")
        # Aquí va tu lógica para cargar archivo
        ruta_carpeta = input("Ingrese la ruta del archivo XML: ")
        nombre_archivo = input("Ingrese el nombre del archivo XML: ")
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

        self.ruta_del_archivo = ruta_completa
        # resultado = leer_archivo(ruta_completa)
        print(f"Archivo cargado desde: {ruta_completa}")

        # return resultado
        self.pausar()

    #Método o función para procesar el archivo .xml
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

    #Método o función para generar el archivo de salida .xml
    def escribir_salida(self):
        print("\nOpción 3: Escribir archivo salida")
        # Aquí va tu lógica para escribir
        self.pausar()

    #Método o función para mostrar los datos del estudiante
    def mostrar_datos_estudiante(self):
        print("\n" + "-" * 49)
        print("           Datos del estudiante")
        print("-" * 49)
        print("Nombre: Anferny Jefferson Jolón Palencia")
        print("Carné: 202102996")
        print("Curso: Introducción a la Programación y Computación 2")
        print("Sección: N")
        print("Documentación: [Link o descripción]")
        print("-" * 49)
        self.pausar()

    #Método o función para generar la gráfica
    def generar_grafica(self):
        print("\nOpción 5: Generar gráfica")
        # Aquí va tu lógica para generar gráfica
        self.pausar()

    #Método o función para salir del programa
    def salir(self):
        print("\nSaliendo del programa...")
        self.ejecutando = False

    #Método o función para pausar la ejecución
    def pausar(self):
        input("\nPresiona Enter para continuar...")