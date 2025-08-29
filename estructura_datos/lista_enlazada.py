from nodo import Nodo

class Lista:
    def __init__(self):
        self.cabeza = None
        self.longitud = 0

    def inserta(self, dato):
        nodo = Nodo(dato)
        if self.cabeza is None:
            self.cabeza = nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nodo
        self.longitud += 1

    def obtener(self, indice):
        if indice < 0 or indice >= self.longitud:
            return None
        actual = self.cabeza
        for i in range(indice):
            actual = actual.siguiente
        return actual.dato
    
    def buscar_indice(self, id_buscar):
        actual = self.cabeza
        indice = 0
        while actual:
            if hasattr(actual.dato, 'id') and actual.dato.id == id_buscar:
                return indice
            actual = actual.siguiente
            indice += 1
        return -1