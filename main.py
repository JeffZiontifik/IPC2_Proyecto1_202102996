if __name__ == "__main__":

    while True:
        print("-----------------Menú Principal-----------------")
        print("|1. Cargar archivo                             |")
        print("|2. Procesar archivo                           |")
        print("|3. Escribir archivo salida                    |")
        print("|4. Mostrar datos del estudiante               |")
        print("|5. Generar gráfica                            |")
        print("|6. Salida                                     |")
        print("------------------------------------------------")

        try:
            opcion = int(input("Ingrese una opción: "))
        except ValueError:
            print("| Error: Debe ingresar un número               |")
            continue  # vuelve a mostrar el menú

        if opcion == 1:
            print(" ")
            print("|Opción 1: Cargar archivo                      |")
            print(" ")
            input("Presiona Enter para continuar...")

        elif opcion == 2:
            print(" ")
            print("|Opción 2: Procesar archivo                    |")
            print(" ")
            input("Presiona Enter para continuar...")

        elif opcion == 3:
            print(" ")
            print("|--------------Archivo de salida---------------|")
            print(" ")
            input("Presiona Enter para continuar...")

        elif opcion == 4:
            print(" ")
            print("|-------------Datos del estudiante-------------|")
            print("|Nombre: Anferny Jefferson Jolón Palencia      |")
            print("|Carné: 202102996                              |")
            print("|Introducción a la Programación y Computación 2|")
            print("|Sección: N                                    |")
            print("|Documentación:                                |")
            print(" ")
            input("Presiona Enter para continuar...")

        elif opcion == 5:
            print(" ")
            print("|Opción 5: Generar gráfica                     |")
            print(" ")
            input("Presiona Enter para continuar...")

        elif opcion == 6:
            print(" ")
            print("|-------------Saliendo del programa------------|")
            print(" ")
            break

        else:
            print(" ")
            print("|Opción inválida. No se reconoce.              |")
            print(" ")
            input("Presiona Enter para continuar...")


