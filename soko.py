def crear_grilla(desc):
    """Crea una grilla a partir de la descripción del estado inicial.

    La descripción es una lista de cadenas, cada cadena representa una
    fila y cada caracter una celda. Los caracteres pueden ser los siguientes:

    Caracter  Contenido de la celda
    --------  ---------------------
           #  Pared
           $  Caja
           @  Jugador
           .  Objetivo
           *  Objetivo + Caja
           +  Objetivo + Jugador

    Ejemplo:

    >>> crear_grilla([
        '#####',
        '#.$ #',
        '#@  #',
        '#####',
    ])
    """
    grilla = []
    for fila in range(len(desc)):
        grilla.append(list(desc[fila]))
    return grilla
    
def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    return len(grilla[0]), len(grilla)

def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).''' 
    return grilla[f][c] == "#"
    	    	
def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    celda = grilla[f][c]
    return celda == "." or celda == "+" or celda == "*"

def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    celda = grilla[f][c]
    return celda == "$" or celda == "*"

def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    celda = grilla[f][c]
    return celda == "@" or celda == "+"

def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''
    for fila in grilla:
        for columna in fila:
            if columna == "." or columna == "+":
                return False
    return True

def encontrar_jugador(grilla):
    """ Devuelve una tupla que indica la posicion (columna, fila) en la que se encuentra el jugador"""
    for fila in range(len(grilla)):
        for columna in range(len(grilla[0])):
            if hay_jugador(grilla, columna, fila):
                return (columna, fila)

def es_movimiento_valido(grilla, direccion):
    columna, fila = encontrar_jugador(grilla)
    x, y = direccion
    if hay_pared(grilla, columna+x, fila+y) or hay_caja(grilla, columna+x, fila+y) and hay_pared(grilla, columna+2*x, fila+2*y)\
       or hay_caja(grilla, columna+x, fila+y) and hay_caja(grilla, columna+2*x, fila+2*y):
       return False
    return True

def mover(grilla, direccion):
    '''Mueve el jugador en la dirección indicada.

    La dirección es una tupla con el movimiento horizontal y vertical. Dado que
    no se permite el movimiento diagonal, la dirección puede ser una de cuatro
    posibilidades:

    direccion  significado
    ---------  -----------
    (-1, 0)    Oeste
    (1, 0)     Este
    (0, -1)    Norte
    (0, 1)     Sur

    La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado. La grilla recibida NO se modifica; es decir, en caso
    de que el movimiento sea válido, la función devuelve una nueva grilla.
    '''
    nueva_grilla = []
    for fila in grilla:
        nueva_grilla.append(list(fila))

    columna, fila = encontrar_jugador(grilla)
    x, y = direccion
    celda_vecina = grilla[fila+(y)][columna+(x)]

    if not es_movimiento_valido(nueva_grilla, direccion):
        return nueva_grilla

    if hay_objetivo(grilla, columna, fila):
        nueva_grilla[fila][columna] = "."
    else:
        nueva_grilla[fila][columna] = " "

    if hay_objetivo(grilla, columna+x, fila+y):
        nueva_grilla[fila+(y)][columna+(x)] = "+"
    else:
        nueva_grilla[fila+(y)][columna+(x)] = "@"

    if hay_caja(grilla, columna+x, fila+y):

        if hay_objetivo(grilla, columna+2*x, fila+2*y):
            nueva_grilla[fila+(2*y)][columna+(2*x)] = "*"
        else:
            nueva_grilla[fila+(2*y)][columna+(2*x)] = "$"

    return nueva_grilla