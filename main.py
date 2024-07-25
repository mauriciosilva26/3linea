import pygame
import sys

# Inicialización de pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Dimensiones y configuración
ANCHO, ALTO = 300, 300
GROSOR_LINEA = 15
TAMAÑO_CUADRADO = ANCHO // 3
FUENTE_TEXTO = pygame.font.Font(None, 36)
FUENTE_BOTONES = pygame.font.Font(None, 28)

# Configuración de la ventana
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Tres en Raya')

def dibujar_lineas():
    """Dibuja las líneas del tablero."""
    pygame.draw.line(VENTANA, NEGRO, (0, TAMAÑO_CUADRADO), (ANCHO, TAMAÑO_CUADRADO), GROSOR_LINEA)
    pygame.draw.line(VENTANA, NEGRO, (0, 2 * TAMAÑO_CUADRADO), (ANCHO, 2 * TAMAÑO_CUADRADO), GROSOR_LINEA)
    pygame.draw.line(VENTANA, NEGRO, (TAMAÑO_CUADRADO, 0), (TAMAÑO_CUADRADO, ALTO), GROSOR_LINEA)
    pygame.draw.line(VENTANA, NEGRO, (2 * TAMAÑO_CUADRADO, 0), (2 * TAMAÑO_CUADRADO, ALTO), GROSOR_LINEA)

def dibujar_marcas(tablero):
    """Dibuja las marcas de los jugadores en el tablero."""
    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == 'X':
                pygame.draw.line(VENTANA, NEGRO, (columna * TAMAÑO_CUADRADO + TAMAÑO_CUADRADO // 5, fila * TAMAÑO_CUADRADO + TAMAÑO_CUADRADO // 5),
                                 (columna * TAMAÑO_CUADRADO + 4 * TAMAÑO_CUADRADO // 5, fila * TAMAÑO_CUADRADO + 4 * TAMAÑO_CUADRADO // 5), GROSOR_LINEA)
                pygame.draw.line(VENTANA, NEGRO, (columna * TAMAÑO_CUADRADO + TAMAÑO_CUADRADO // 5, fila * TAMAÑO_CUADRADO + 4 * TAMAÑO_CUADRADO // 5),
                                 (columna * TAMAÑO_CUADRADO + 4 * TAMAÑO_CUADRADO // 5, fila * TAMAÑO_CUADRADO + TAMAÑO_CUADRADO // 5), GROSOR_LINEA)
            elif tablero[fila][columna] == 'O':
                pygame.draw.circle(VENTANA, NEGRO, (columna * TAMAÑO_CUADRADO + TAMAÑO_CUADRADO // 2, fila * TAMAÑO_CUADRADO + TAMAÑO_CUADRADO // 2),
                                   TAMAÑO_CUADRADO // 3, GROSOR_LINEA)

def verificar_ganador(tablero, jugador):
    """Verifica si el jugador actual ha ganado."""
    for fila in range(3):
        if tablero[fila][0] == tablero[fila][1] == tablero[fila][2] == jugador:
            return True
    for columna in range(3):
        if tablero[0][columna] == tablero[1][columna] == tablero[2][columna] == jugador:
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == jugador:
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] == jugador:
        return True
    return False

def verificar_empate(tablero):
    """Verifica si el tablero está lleno sin ganador (empate)."""
    for fila in tablero:
        if '' in fila:
            return False
    return True

def evaluar_tablero(tablero):
    """Evalúa el tablero y devuelve un puntaje para el Minimax."""
    if verificar_ganador(tablero, 'X'):
        return 10
    elif verificar_ganador(tablero, 'O'):
        return -10
    return 0

def minimax(tablero, profundidad, es_maximizador):
    """Algoritmo Minimax para encontrar el mejor movimiento."""
    puntuacion = evaluar_tablero(tablero)

    if puntuacion == 10:
        return puntuacion
    if puntuacion == -10:
        return puntuacion
    if verificar_empate(tablero):
        return 0

    if es_maximizador:
        mejor = -float('inf')
        for fila in range(3):
            for columna in range(3):
                if tablero[fila][columna] == '':
                    tablero[fila][columna] = 'X'
                    mejor = max(mejor, minimax(tablero, profundidad + 1, not es_maximizador))
                    tablero[fila][columna] = ''
        return mejor
    else:
        mejor = float('inf')
        for fila in range(3):
            for columna in range(3):
                if tablero[fila][columna] == '':
                    tablero[fila][columna] = 'O'
                    mejor = min(mejor, minimax(tablero, profundidad + 1, not es_maximizador))
                    tablero[fila][columna] = ''
        return mejor

def encontrar_mejor_movimiento(tablero):
    """Encuentra el mejor movimiento para el jugador 'X' usando Minimax."""
    mejor_valor = -float('inf')
    mejor_movimiento = (-1, -1)
    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == '':
                tablero[fila][columna] = 'X'
                valor = minimax(tablero, 0, False)
                tablero[fila][columna] = ''
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_movimiento = (fila, columna)
    return mejor_movimiento

def mostrar_mensaje(texto):
    """Muestra un mensaje en pantalla."""
    mensaje = FUENTE_TEXTO.render(texto, True, NEGRO)
    rectangulo = mensaje.get_rect(center=(ANCHO // 2, ALTO // 2 - 20))
    VENTANA.blit(mensaje, rectangulo)

def mostrar_pantalla_inicio():
    """Muestra la pantalla de inicio y opciones para seleccionar el modo de juego."""
    VENTANA.fill(BLANCO)
    mostrar_mensaje('Selecciona el modo de juego')

    # Botón para jugar contra la IA
    ia_boton = pygame.Rect(ANCHO // 4, ALTO // 2 - 30, ANCHO // 2, 40)
    pygame.draw.rect(VENTANA, VERDE, ia_boton)
    texto_boton = FUENTE_BOTONES.render('Jugar contra IA', True, BLANCO)
    texto_rect = texto_boton.get_rect(center=ia_boton.center)
    VENTANA.blit(texto_boton, texto_rect)

    # Botón para jugar con otro jugador
    amigo_boton = pygame.Rect(ANCHO // 4, ALTO // 2 + 30, ANCHO // 2, 40)
    pygame.draw.rect(VENTANA, AZUL, amigo_boton)
    texto_boton = FUENTE_BOTONES.render('Jugar con amigo', True, BLANCO)
    texto_rect = texto_boton.get_rect(center=amigo_boton.center)
    VENTANA.blit(texto_boton, texto_rect)

    pygame.display.update()
    return ia_boton, amigo_boton

def mostrar_pantalla_final(mensaje):
    """Muestra la pantalla final y opciones para reiniciar o salir."""
    VENTANA.fill(BLANCO)
    mostrar_mensaje(mensaje)

    # Botón para reiniciar el juego
    reiniciar_boton = pygame.Rect(ANCHO // 4, ALTO // 2 + 50, ANCHO // 4, 40)
    pygame.draw.rect(VENTANA, VERDE, reiniciar_boton)
    texto_boton = FUENTE_BOTONES.render('Reiniciar', True, BLANCO)
    texto_rect = texto_boton.get_rect(center=reiniciar_boton.center)
    VENTANA.blit(texto_boton, texto_rect)

    # Botón para salir
    salir_boton = pygame.Rect(ANCHO // 2 + 10, ALTO // 2 + 50, ANCHO // 4, 40)
    pygame.draw.rect(VENTANA, ROJO, salir_boton)
    texto_boton = FUENTE_BOTONES.render('Salir', True, BLANCO)
    texto_rect = texto_boton.get_rect(center=salir_boton.center)
    VENTANA.blit(texto_boton, texto_rect)

    pygame.display.update()
    return reiniciar_boton, salir_boton

def main():
    """Función principal del juego."""
    juego_en_pantalla_inicio = True
    juego_con_ia = False
    tablero = [['' for _ in range(3)] for _ in range(3)]
    jugador = 'X'
    mensaje = ''

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if juego_en_pantalla_inicio:
                ia_boton, amigo_boton = mostrar_pantalla_inicio()
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if ia_boton.collidepoint(evento.pos):
                        juego_con_ia = True
                        juego_en_pantalla_inicio = False
                    elif amigo_boton.collidepoint(evento.pos):
                        juego_con_ia = False
                        juego_en_pantalla_inicio = False
            else:
                if not mensaje:
                    if jugador == 'X' and evento.type == pygame.MOUSEBUTTONDOWN:
                        mouseX, mouseY = evento.pos
                        fila_click = mouseY // TAMAÑO_CUADRADO
                        columna_click = mouseX // TAMAÑO_CUADRADO

                        if tablero[fila_click][columna_click] == '':
                            tablero[fila_click][columna_click] = jugador
                            if verificar_ganador(tablero, jugador):
                                mensaje = f'Ganó {jugador}'
                            elif verificar_empate(tablero):
                                mensaje = 'Empate'
                            else:
                                jugador = 'O'
                    
                    if jugador == 'O' and juego_con_ia:
                        fila, columna = encontrar_mejor_movimiento(tablero)
                        tablero[fila][columna] = jugador
                        if verificar_ganador(tablero, jugador):
                            mensaje = 'Ganó la IA'
                        elif verificar_empate(tablero):
                            mensaje = 'Empate'
                        else:
                            jugador = 'X'
                    
                    if jugador == 'O' and not juego_con_ia:
                        if evento.type == pygame.MOUSEBUTTONDOWN:
                            mouseX, mouseY = evento.pos
                            fila_click = mouseY // TAMAÑO_CUADRADO
                            columna_click = mouseX // TAMAÑO_CUADRADO

                            if tablero[fila_click][columna_click] == '':
                                tablero[fila_click][columna_click] = jugador
                                if verificar_ganador(tablero, jugador):
                                    mensaje = f'Ganó {jugador}'
                                elif verificar_empate(tablero):
                                    mensaje = 'Empate'
                                else:
                                    jugador = 'X'

                else:
                    reiniciar_boton, salir_boton = mostrar_pantalla_final(mensaje)
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if reiniciar_boton.collidepoint(evento.pos):
                            tablero = [['' for _ in range(3)] for _ in range(3)]
                            jugador = 'X'
                            mensaje = ''
                            juego_en_pantalla_inicio = True
                        elif salir_boton.collidepoint(evento.pos):
                            pygame.quit()
                            sys.exit()

        if not juego_en_pantalla_inicio and not mensaje:
            VENTANA.fill(BLANCO)
            dibujar_lineas()
            dibujar_marcas(tablero)
            pygame.display.update()

if __name__ == '__main__':
    main()


