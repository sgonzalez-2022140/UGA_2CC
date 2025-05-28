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

# Inicializar tablero global
tablero = [["" for _ in range(4)] for _ in range(4)]
fila1, fila2, fila3, fila4 = tablero[0], tablero[1], tablero[2], tablero[3]

# Generar tablero inicial con dos casillas llenas
def generar_tablero_inicial():
    global tablero, fila1, fila2, fila3, fila4
    tablero = [["" for _ in range(4)] for _ in range(4)]
    fila1, fila2, fila3, fila4 = tablero[0], tablero[1], tablero[2], tablero[3]
    for _ in range(2):
        while True:
            i, j = random.randint(0, 3), random.randint(0, 3)
            if tablero[i][j] == "":
                tablero[i][j] = random.choice([2, 4])
                break

def mostrar_tablero(tablero, posiciones_iniciales=None, posicion_actual=None):
    print("+" + "-------+" * 4)
    for i, fila in enumerate(tablero):
        fila_str = "|"
        for j, valor in enumerate(fila):
            celda = f" {valor if valor != '' else ' '} "
            if posicion_actual == (i, j):
                celda = f"->{valor if valor != '' else ' '}<-"
            elif posiciones_iniciales and (i, j) in posiciones_iniciales:
                celda = f"[{valor if valor != '' else ' '}]"
            fila_str += f"{celda:^7}|"
        print(fila_str)
        print("+" + "-------+" * 4)



def sumas_filas(fila1, fila2, fila3, fila4):
    for c in range(len(fila1)):
        if fila1[c] == fila2[c] and fila1[c] != "":
            fila1[c] += fila2[c]
            fila2[c] = ""
    for a in range(len(fila2)):
        if fila2[a] == fila3[a] and fila2[a] != "":
            fila2[a] += fila3[a]
            fila3[a] = ""
    for z in range(len(fila4)):
        if fila3[z] == fila4[z] and fila3[z] != "":
            fila3[z] += fila4[z]
            fila4[z] = ""
    for c in range(4):
        if fila4[c]== fila1[c] and fila3[c]== "" and fila2[c] == "":
            fila4[c] += fila1[c]
            fila1[c] = ""
        if fila4[c]== fila2[c] and fila3[c]== "":
            fila4[c] += fila2[c]
            fila2[c] = ""
        if fila1[c]== fila3[c] and fila2[c]== "":
            fila3[c] += fila1[c]
            fila1[c] = ""

def sumas_columnas(matriz):
    for f in range(4):
        for c in range(3):
            if matriz[f][c] == matriz[f][c+1] and matriz[f][c] != "":
                matriz[f][c+1] += matriz[f][c]
                matriz[f][c] = ""
    for f in range(4):
        if matriz[f][0]== matriz[f][3] and matriz[f][2]== "" and matriz[f][1] == "":
            matriz[f][3] += matriz[f][0]
            matriz[f][0] = ""
        if matriz[f][0]== matriz[f][2] and matriz[f][1]== "":
            matriz[f][2] += matriz[f][0]
            matriz[f][0] = ""
        if matriz[f][1]== matriz[f][3] and matriz[f][2]== "":
            matriz[f][3] += matriz[f][1]
            matriz[f][1] = ""

def mov_izquierda(tablero):
    for _ in range(4):
        for f in range(4):
            for c in range(3):
                if tablero[f][c] == "":
                    tablero[f][c] = tablero[f][c+1]
                    tablero[f][c+1] = ""

def mov_derecha(tablero):
    for _ in range(4):
        for f in range(4):
            for c in reversed(range(1, 4)):
                if tablero[f][c] == "":
                    tablero[f][c] = tablero[f][c-1]
                    tablero[f][c-1] = ""

def mov_arriba(fila1, fila2, fila3, fila4):
    for _ in range(4):
        for r in range(4):
            if fila1[r] == "":
                fila1[r], fila2[r] = fila2[r], ""
            if fila2[r] == "":
                fila2[r], fila3[r] = fila3[r], ""
            if fila3[r] == "":
                fila3[r], fila4[r] = fila4[r], ""

def mov_abajo(fila1, fila2, fila3, fila4):
    for _ in range(4):
        for r in range(4):
            if fila4[r] == "":
                fila4[r], fila3[r] = fila3[r], ""
            if fila3[r] == "":
                fila3[r], fila2[r] = fila2[r], ""
            if fila2[r] == "":
                fila2[r], fila1[r] = fila1[r], ""

def aparicion(tablero):
    while True:
        posf, posc = random.randint(0, 3), random.randint(0, 3)
        if tablero[posf][posc] == "":
            tablero[posf][posc] = random.choice([2, 4])
            break

def teclas():
    while True:
        tecla = input("Movimiento (a=izquierda, d=derecha, w=arriba, s=abajo, q=salir): ")
        if tecla == "q":
            print("¡Juego terminado!")
            return
        elif tecla == "a":
            mov_izquierda(tablero)
            sumas_columnas(tablero)
            mov_izquierda(tablero)
        elif tecla == "d":
            mov_derecha(tablero)
            sumas_columnas(tablero)
            mov_derecha(tablero)
        elif tecla == "w":
            mov_arriba(fila1, fila2, fila3, fila4)
            sumas_filas(fila1, fila2, fila3, fila4)
            mov_arriba(fila1, fila2, fila3, fila4)
        elif tecla == "s":
            mov_abajo(fila1, fila2, fila3, fila4)
            sumas_filas(fila1, fila2, fila3, fila4)
            mov_abajo(fila1, fila2, fila3, fila4)
        aparicion(tablero)
        mostrar_tablero(tablero)

def modo_individual():
    generar_tablero_inicial()
    mostrar_tablero(tablero)
    teclas()

def modo_multijugador():
    pass

def modo_maquina():
    pass

def manejar_modo(modo):
    if modo == 1:
        print("Modo Normal")
        modo_individual()
    elif modo == 2:
        print("Modo Jugador vs Jugador")
    elif modo == 3:
        print("Modo Jugador vs Máquina")

def mostrar_menu():
    ventana = tk.Tk()
    ventana.geometry("300x200")
    ventana.title("Juego 2048 - Menú")
    tk.Label(ventana, text="Seleccione un modo de juego:").pack(pady=10)
    tk.Button(ventana, text="1 Jugador", command=lambda: [ventana.destroy(), manejar_modo(1)]).pack(pady=5)
    tk.Button(ventana, text="Jugador vs Jugador", command=lambda: [ventana.destroy(), manejar_modo(2)]).pack(pady=5)
    tk.Button(ventana, text="Jugador vs Máquina", command=lambda: [ventana.destroy(), manejar_modo(3)]).pack(pady=5)
    ventana.mainloop()

mostrar_menu()
