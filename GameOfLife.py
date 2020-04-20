import pygame
import numpy as np
import time
import sys

pygame.init()

height, width = 1000, 1000
screen = pygame.display.set_mode((height, width))

#Control de la ejecucion
pauseExec = False

# Color de fondo
bg = (25, 25, 25)
screen.fill(bg)

# Numero de celdas
nxC, nyC = 50, 50

# Dimensiones de las celdas
dimCW = width  / nxC
dimCH = height / nyC

#Estado de las Celdas; Vivas = 1; Muertas = 0;
gameState = np.zeros((nxC, nyC))

#Bucle de ejecucion
while True:

    newGameState = np.copy(gameState) # Copia del estado anterior
    screen.fill(bg) # Limpieza de pantalla (le reasigno el color de base xD)
    time.sleep(0.1) # Delay
    ev = pygame.event.get() # Lectura de perifericos

    for event in ev:
        if event.type == pygame.KEYDOWN: # Lectura de teclado (para pausar la ejecucion)
            pauseExec = not pauseExec # Pausar Ejecucion

        mouseClick = pygame.mouse.get_pressed() # Lectura de teclas del mouse

        if mouseClick == (0,1,0): # Si se presiona la rueda del mouse
            sys.exit() # Cerrar Programa

        if sum(mouseClick) > 0: # Suma de la matriz de los clicks del mouse
            posX, posY = pygame.mouse.get_pos() # obtener la posicion del cursor
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH)) # Convertir a enteros
            newGameState[celX, celY] = not mouseClick[2] # Dar vida a casilla [Mouse 1] / Matar Casilla [Mouse 3]

        
    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExec:
                    
                # Calculo del numero de vecinos cercanos
                n_neigh=gameState[(x - 1) % nxC, (y-1) % nyC] + \
                        gameState[(x)     % nxC, (y-1) % nyC] + \
                        gameState[(x + 1) % nxC, (y-1) % nyC] + \
                        gameState[(x - 1) % nxC, (y)   % nyC] + \
                        gameState[(x + 1) % nxC, (y)   % nyC] + \
                        gameState[(x - 1) % nxC, (y+1) % nyC] + \
                        gameState[(x)     % nxC, (y+1) % nyC] + \
                        gameState[(x + 1) % nxC, (y+1) % nyC]

                # Regla 1: celula muerta con 3 vecinas revive
                if (gameState[x, y] == 0 and n_neigh == 3):
                    newGameState[x, y] = 1

                # Regla 2: celula viva, con mas de 3 vecinas o menos de 2 muere (sobrepoblacion o soledad)
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Poligono de cada celda 
            poly = [((x)   * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x)   * dimCW, (y+1) * dimCH)]
            
            # Dibujado de la celda con los datos de "poly"
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizacion del estado del juego (x ciclo) 
    gameState = np.copy(newGameState) 

    # Actualizacion de Pantalla
    pygame.display.flip()
