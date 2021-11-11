import soko
import gamelib
import backtracking
from pila_apunte import Pila

DIRECCIONES  = {"SUR":(0, 1), "OESTE":(-1, 0), "ESTE":(1, 0), "NORTE":(0, -1),}

def crea_juego(archivo_entrada):
    """Dado un archivo de texto con niveles del sokoban separados por una linea vacia, devuelve un diccionario con los nombres de los niveles
       como clave y sus respectivas grillas asociadas como valor."""   
    niveles = {}
    with open("niveles.txt") as archivo:
        entrada = archivo.readlines()
        for linea in entrada:
            linea = linea.rstrip("\n")

            if len(linea) == 0 or "'" in linea:
                continue

            if "#" not in linea:
                linea = linea.split()
                linea.pop(0)
                nombre_de_nivel = linea[0]
                niveles[nombre_de_nivel] = []
                continue
            niveles[nombre_de_nivel].append(linea)
        return niveles

def devuelve_cadenas_igual_tamaño(grilla):
    """Dada una grilla, devuelve la misma con sus filas proporcionales en tamaño."""
    linea_mas_larga  = []
    grilla_proporcional = []

    for linea in grilla:
        if len(linea) > len(linea_mas_larga):
            linea_mas_larga = linea
    mayor_largo = len(linea_mas_larga)

    for linea in grilla:
        linea += (" " * (mayor_largo - len(linea)))
        grilla_proporcional.append(linea)

    return grilla_proporcional

def asigna_teclas(archivo_entrada):
    """
    Dado un archivo de texto, donde cada linea es de la forma <tecla>=<acción>, devuelve un diccionario
    donde las claves son las teclas que figuran en dicho archivo y los valores son las acciones que las 
    representan.
    """
    asignacion_teclas = {}
    with open("teclas.txt") as entrada:
        
        for linea in entrada:

            if len(linea) == 1:
                continue

            linea = linea.rstrip("\n")
            tecla, accion = linea.split("=")

            if tecla not in asignacion_teclas:
                asignacion_teclas[tecla] = accion
        return asignacion_teclas

def dibuja_juego(nivel, grilla):
    """Actualiza la ventana del juego."""

    largo_de_celda = 64 #Representa el largo de una celda en relación con las imagenes de la carpeta "img"
    columnas_nivel_actual = len(grilla[0])
    filas_nivel_actual = len(grilla)

    gamelib.resize((largo_de_celda*columnas_nivel_actual), (largo_de_celda*filas_nivel_actual))
    gamelib.title("Sokoban" + " - " + "Level " + str(nivel))

    for fila in range(filas_nivel_actual):
        for columna in range(columnas_nivel_actual):
            x, y = columna*largo_de_celda, fila*largo_de_celda

            gamelib.draw_image('img/ground.gif', x, y)
            if soko.hay_jugador(grilla, columna, fila):
                gamelib.draw_image('img/player.gif', x, y)
            if soko.hay_caja(grilla, columna, fila):
                gamelib.draw_image('img/box.gif', x, y)
            if soko.hay_objetivo(grilla, columna, fila):
                gamelib.draw_image('img/goal.gif', x , y)
            if soko.hay_pared(grilla, columna, fila):
                gamelib.draw_image('img/wall.gif', x, y)

def main():
    juego = crea_juego("niveles.txt")
    controles = asigna_teclas("teclas.txt")
    nivel_actual = 1
    grilla = devuelve_cadenas_igual_tamaño(juego[str(nivel_actual)])
    pistas = Pila()
    registro_de_movimientos = Pila()
    while gamelib.is_alive():
        
        if soko.juego_ganado(grilla):
            nivel_actual += 1
            grilla = devuelve_cadenas_igual_tamaño(juego[str(nivel_actual)])

        gamelib.draw_begin()
        dibuja_juego(nivel_actual, grilla)
        gamelib.draw_end()

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key
        if tecla not in controles:
            continue

        if controles[tecla] == "PISTA":
            if pistas.esta_vacia():
                _, pistas = backtracking.buscar_solucion(grilla)
                continue
            grilla = soko.mover(grilla,DIRECCIONES[pistas.desapilar()])

        if controles[tecla] == "DESHACER":
            if registro_de_movimientos.esta_vacia():
                continue
            grilla = registro_de_movimientos.desapilar()

        if controles[tecla] == "SALIR":
            return 

        if controles[tecla] == "REINICIAR":
            grilla = devuelve_cadenas_igual_tamaño(juego[str(nivel_actual)])

        if ev.type == gamelib.EventType.KeyPress:
            accion = controles[tecla]
            if accion in DIRECCIONES:
                pistas = Pila()
                registro_de_movimientos.apilar(grilla)
                grilla = soko.mover(grilla, DIRECCIONES[accion])
                if grilla == registro_de_movimientos.ver_tope():
                    registro_de_movimientos.desapilar()

gamelib.init(main)