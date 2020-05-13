from sense_emu import SenseHat
import numpy as np
import time

#Definición de variables
x = y = 0
nxC, nyC = 8, 8    #celdas del sense HAT
gameState = np.zeros((nxC, nyC))


#Definición de funciones
def estado_inicial():
    global gameState
    hat.clear()
    # Autómata caminante
    gameState[1, 2] = 1
    gameState[1, 1] = 1
    gameState[2, 1] = 1
    gameState[2, 0] = 1
    gameState[0, 0] = 1
    
    hat.set_pixel(1, 2, 250, 250, 250)
    hat.set_pixel(1, 1, 250, 250, 250)
    hat.set_pixel(2, 1, 250, 250, 250)
    hat.set_pixel(2, 0, 250, 250, 250)
    hat.set_pixel(0, 0, 250, 250, 250)

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def move_dot(event):
    global x, y
    if event.action in ('pressed', 'held'):
        x = clamp(x + {
            'left': -1,
            'right': 1,
            }.get(event.direction, 0))
        y = clamp(y + {
            'up': -1,
            'down': 1,
            }.get(event.direction, 0))
                
hat = SenseHat()
hat.clear()
y= x =0

#Si quieres probar el juego con un estado inicial desde consola, descomenta la línea siguiente
#estado_inicial()


#Inicio del juego
while True:
    newGameState = np.copy(gameState)
    time.sleep(0.2)
    
    #Registros de actividad del joystick
    if hat.get_humidity() < 100 :
        #pausamos el juego para agregar o modificar células
        for event in hat.stick.get_events():
            move_dot(event)
                
            if event.direction == "middle":
                #ponemos una célula viva en la posición x, y
                hat.set_pixel(x, y, 255, 255, 255)
                gameState[x, y] = 1
                newGameState = np.copy(gameState)
                
            else:
                #ubicamos el cursor
                hat.set_pixel(x, y, 255, 255, 255)
                time.sleep(0.2)
                hat.set_pixel(x, y, 25, 25, 25)
                    
    else:
        
        for y in range(0, 8):
            for x in range(0, 8):

                if hat.get_humidity() == 100 :
                    
                    # Calculamos el número de vecinos cercanos.
                    n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC ] + \
                        gameState[(x) % nxC    , (y - 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                        gameState[(x - 1) % nxC, (y) % nyC] + \
                        gameState[(x + 1) % nxC, (y) % nyC] + \
                        gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                        gameState[(x) % nxC    , (y + 1) % nyC] + \
                        gameState[(x + 1) % nxC, (y + 1) % nyC]  

                    #Regla #1 : Una célula muerta con exactamente 3 vecinas vivas, "revive"         
                    if gameState[x, y] == 0 and n_neigh == 3:
                        newGameState[x, y] = 1
                    
                    # Regla  #2 : Una célula viva con menos de 2 o más de 3 vecinas vivas, "muere"
                    elif gameState[x, y] ==1 and (n_neigh < 2 or n_neigh > 3):
                        newGameState[x, y] =0
            
                # Dibujamos las celdas dependiendo si la célula está viva o muerta
                if newGameState[x, y] == 1:
                    hat.set_pixel(x, y, 255, 255, 255)
                else:
                    hat.set_pixel(x, y, 25, 25, 25) 
    
    # Actualizamos el estado del juego.
    gameState = np.copy(newGameState)
        
        

   
    
    
       


