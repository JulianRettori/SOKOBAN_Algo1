import soko
from pila_apunte import Pila
DIRECCIONES  = {"SUR":(0, 1), "OESTE":(-1, 0), "ESTE":(1, 0), "NORTE":(0, -1),}

def devuelve_estado_inmutable(estado):
    """
    Recibe un nivel de sokoban, como una lista de listas, y devuelve una version inmutable del mismo.
    """
    nuevo_estado = []
    for secuencia in estado:
        secuencia = "".join(secuencia)
        nuevo_estado.append(secuencia)
    nuevo_estado = tuple(nuevo_estado)

    return nuevo_estado

def buscar_solucion(estado_inicial):
    visitados = {}
    pistas = Pila()
    return backtrack(estado_inicial, visitados, pistas)

def backtrack(estado, visitados, pistas):
    visitados[devuelve_estado_inmutable(estado)] = True

    if soko.juego_ganado(estado):
        return True, Pila()

    for direccion in DIRECCIONES:
        nuevo_estado = soko.mover(estado, DIRECCIONES[direccion])
        nuevo_estado = devuelve_estado_inmutable(nuevo_estado)

        if nuevo_estado in visitados:
           continue

        solucion_encontrada, acciones = backtrack(nuevo_estado, visitados, pistas)
        if solucion_encontrada:
            pistas.apilar(direccion)
            return True, pistas
    return False, Pila()