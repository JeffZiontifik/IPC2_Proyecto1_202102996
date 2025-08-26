import os
from lector_xml import leer_archivo
#Creamos nuestro menu principal
class Menu:
    def __init__(self):

        self.ruta_del_archivo = None
        #Método o función constructor que genera el menú
        #Usamos un diccionario para almacenar las opciones del menú
        self.opciones = {
            1: self.cargar_archivo,
            2: self.procesar_archivo,
            3: self.escribir_salida,
            4: self.mostrar_datos_estudiante,
            5: self.generar_grafica,
            6: self.salir
        }
        self.ejecutando = True

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
                if opcion in self.opciones:
                    self.opciones[opcion]()
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
        if self.ruta_del_archivo is None:
            print("Debe de cargar un archivo primero.")
            return
        try:
            leer_archivo(self.ruta_del_archivo)
            print("El archivo ha sido procesado correctamente.")
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
        # Aquí va tu lógica para procesar
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