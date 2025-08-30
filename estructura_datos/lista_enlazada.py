# Clase Lista

from .nodo import Nodo

class Lista:
    def __init__(self):
        # inicializamos con cabeza vacia
        self.cabeza = None
        self.tamaño = 0
    
    def esta_vacia(self):
        # verifica si la lista no tiene elementos
        return self.cabeza is None
    
    def obtener_tamaño(self):
        # retorna el numero de elementos en la lista
        return self.tamaño
    
    def insertar_al_inicio(self, dato):
        # inserta un nuevo nodo al inicio de la lista
        nuevo_nodo = Nodo(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        self.tamaño = self.tamaño + 1
    
    def insertar_al_final(self, dato):
        # inserta un nuevo nodo al final de la lista
        nuevo_nodo = Nodo(dato)
        
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            # recorremos hasta el ultimo nodo
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        
        self.tamaño = self.tamaño + 1
    
    def obtener_por_indice(self, indice):
        # obtiene el elemento en la posicion especificada
        if indice < 0 or indice >= self.tamaño:
            return None
        
        actual = self.cabeza
        contador = 0
        
        while actual is not None:
            if contador == indice:
                return actual.dato
            actual = actual.siguiente
            contador = contador + 1
        
        return None
    
    def buscar(self, dato_buscado):
        # busca un elemento en la lista y retorna su posicion
        actual = self.cabeza
        posicion = 0
        
        while actual is not None:
            if actual.dato == dato_buscado:
                return posicion
            actual = actual.siguiente
            posicion = posicion + 1
        
        return -1  # no encontrado
    
    def eliminar_por_indice(self, indice):
        # elimina el elemento en la posicion especificada
        if indice < 0 or indice >= self.tamaño or self.esta_vacia():
            return False
        
        if indice == 0:
            # eliminar el primer elemento
            self.cabeza = self.cabeza.siguiente
            self.tamaño = self.tamaño - 1
            return True
        
        actual = self.cabeza
        contador = 0
        
        # encontrar el nodo anterior al que queremos eliminar
        while contador < indice - 1:
            actual = actual.siguiente
            contador = contador + 1
        
        # saltamos el nodo a eliminar
        if actual.siguiente is not None:
            actual.siguiente = actual.siguiente.siguiente
            self.tamaño = self.tamaño - 1
            return True
        
        return False
    
    def mostrar_lista(self):
        # imprime todos los elementos de la lista
        if self.esta_vacia():
            print("Lista vacia")
            return
        
        actual = self.cabeza
        elementos = ""
        
        while actual is not None:
            elementos = elementos + str(actual.dato)
            if actual.siguiente is not None:
                elementos = elementos + " -> "
            actual = actual.siguiente
        
        print(elementos)
    
    def iterar(self):
        # permite recorrer la lista elemento por elemento
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente