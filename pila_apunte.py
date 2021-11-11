class Pila:
    '''
    Representa una pila con operaciones de apilar, desapilar y
    verificar si está vacía.
    '''

    def __init__(self):
        '''
        Crea una pila vacía.
        '''
        self.items = []

    def esta_vacia(self):
        '''
        Devuelve True si la lista está vacía, False si no.
        '''
        return len(self.items) == 0
    
    def ver_tope(self):
        return self.items[-1]

    def apilar(self, x):
        '''
        Apila un elemento en la pila.
        '''
        self.items.append(x)

    def desapilar(self):
        '''
        Devuelve el elemento tope y lo elimina de la pila.
        Si la pila está vacía levanta una excepción.
        '''
        if self.esta_vacia():
            raise IndexError("La pila está vacía")
        return self.items.pop()
    
    # Este método está para simplificar las pruebas
    def apilar_muchos(self, iterable):
        '''
        Apila todos los elementos del iterable en la pila.
        '''
        for elem in iterable:
            self.apilar(elem)

    # Este método está para simplificar las pruebas
    def __str__(self):
        '''
        Devuelve una representación de la pila en la forma: 
        | e1, e2, ..., <TOPE
        '''
        return '| ' + ', '.join(map(str, self.items)) + ' <TOPE'
