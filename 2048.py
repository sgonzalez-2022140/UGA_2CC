"""
    Nombre del Juego: 2048
    Interfaz: Tkinter
    Grupo: xx
    ---------------------------
    Modalidad del Juego
    ---------------------------
    ** Normal **
    - Se inicia con 2 números (colocados aleatoreamente)
    - Se puede realizar movimientos con W, A, S, D
    - El juego termina cuando se alcanza 2048 o no haya mas movimientos
    - Mostrar: Movimientos realizados, tablero actualizado, casillas vacias, movimientos hechos y número mayor alcanzado

    ** Jugador vs Jugador **
    - Dos jugadores usan el mismo tablero inicial
    - Juega uno y luego el otro
    - Gana quien llegue a mayor número, si emptanan gana el que uso menos movimientos y hay empate real si tienen mismos resultados
    
    ** Jugador vs Maquina ** 
    - El jugador juega primero, luego la maquina
    - La maquina debe usar un algoritmo determinista
    - Gana bajo las mismas reglas que Jugador vs Jugador

    ---------------------------
    Mecánicas del juego 
    ---------------------------
    - Se inicia con un menú para seleccionar la modalidad
    - Se solicita el nombre del o los jugadores
    - Se crea el tablero 4x4 con 2 casillas iniciales
    - Cuando nos movamos se reacomodan los números, se suma donde sea posible y aparece un nuevo número (2 o 4) si hubo movimiento
    - Se detiene al alcanzar 2048
    - Al finalizar se comparan sus resultados
    ---------------------------
    Pts Extra
    ---------------------------
    - Permitir llegar más allá del 2048 (por ejemplo 4096)
    - Llevar punteo acumulativo cada vez que se hace una suma
    - Sistema de Replay: Guardar y reproducir jugadas
    - Botón de Ayuda: Mostrar instrucciones del juego
    - Opcion de retroceso (Undo)
"""
# Importaciones
import tkinter as tk
import random

def inciar_juego():
    pass


def modo_individual():
    pass 

def modo_multijugador():
    pass

def modo_maquina():
    pass

def generar_tablero_inicial():
    tablero = [["" for _ in range(4)] for _ in range(4)]
    
    # Elección del 1er numero entre 2 y 4
    i1, j1 = random.randint(0, 3), random.randint(0, 3)
    tablero[i1][j1] = random.choice([2, 4])

    # Elección del 2do numero con posición diferente
    while True:
        i2, j2 = random.randint(0, 3), random.randint(0, 3)
        if (i2, j2) != (i1, j1):
            tablero[i2][j2] = random.choice([2, 4])
            break

    return tablero

#Mostrar el tablero
def mostrar_tablero():
    tablero = generar_tablero_inicial()
    for fila in tablero:
        print(fila)
    print()



#Modo de juegos
def manejar_modo(modo):
    print("Probando")
    if modo == 1:
        print("Vista 1: Modo Normal")
    elif modo == 2:
        print("Vista 2: Modo Jugador vs Jugador")
    elif modo == 3:
        print("Vista 3: Modo Jugador vs Máquina")
    mostrar_tablero()

def mostrar_menu():
    ventana = tk.Tk()
    ventana.geometry("300x200")
    ventana.title("Juego 2048 - Menú")

    tk.Label(ventana, text="Seleccione un modo de juego:").pack(pady=10)

    tk.Button(ventana, text="1 Jugador", command=lambda: manejar_modo(1)).pack(pady=5)
    tk.Button(ventana, text="Jugador vs Jugador", command=lambda: manejar_modo(2)).pack(pady=5)
    tk.Button(ventana, text="Jugador vs Maquina", command=lambda: manejar_modo(3)).pack(pady=5)

    ventana.mainloop()

mostrar_menu()