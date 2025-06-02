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
import copy
#Para el modo maquina
import time


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
    movimiento = False
    for c in range(len(fila1)):
        if fila1[c] == fila2[c] and fila1[c] != "":
            fila1[c] += fila2[c]
            fila2[c] = ""
            movimiento = True
    for a in range(len(fila2)):
        if fila2[a] == fila3[a] and fila2[a] != "":
            fila2[a] += fila3[a]
            fila3[a] = ""
            movimiento = True
    for z in range(len(fila4)):
        if fila3[z] == fila4[z] and fila3[z] != "":
            fila3[z] += fila4[z]
            fila4[z] = ""
            movimiento = True
    return movimiento

def sumas_columnas(matriz):
    movimiento = False
    for f in range(4):
        for c in range(3):
            if matriz[f][c] == matriz[f][c+1] and matriz[f][c] != "":
                matriz[f][c] += matriz[f][c+1]
                matriz[f][c+1] = ""
                movimiento = True
    return movimiento
    

def mov_izquierda(tablero):
    movimiento = False
    for _ in range(4):
        for f in range(4):
            for c in range(3):
                if tablero[f][c] == "":
                    if tablero[f][c+1] !="":
                        movimiento = True
                    tablero[f][c] = tablero[f][c+1]
                    tablero[f][c+1] = ""
    return movimiento

def mov_derecha(tablero):
    movimiento = False
    for _ in range(4):
        for f in range(4):
            for c in reversed(range(1, 4)):
                if tablero[f][c] == "":
                    if tablero[f][c-1] !="":
                        movimiento = True
                    tablero[f][c] = tablero[f][c-1]
                    tablero[f][c-1] = ""
    return movimiento

def mov_arriba(fila1, fila2, fila3, fila4):
    movimiento = False
    for _ in range(4):
        for r in range(4):
            if fila1[r] == "":
                if fila2[r] !="":
                    movimiento = True
                fila1[r], fila2[r] = fila2[r], ""
            if fila2[r] == "":
                if fila3[r] !="":
                    movimiento = True
                fila2[r], fila3[r] = fila3[r], ""
            if fila3[r] == "":
                if fila4[r]!="":
                    movimiento = True
                fila3[r], fila4[r] = fila4[r], ""
    return movimiento
    
def mov_abajo(fila1, fila2, fila3, fila4):
    movimiento = False
    for _ in range(4):
        for r in range(4):
            if fila4[r] == "":
                if fila3[r]!="":
                    movimiento = True
                fila4[r], fila3[r] = fila3[r], ""
            if fila3[r] == "":
                if fila2[r]!="":
                    movimiento = True
                fila3[r], fila2[r] = fila2[r], ""
            if fila2[r] == "":
                if fila1[r] !="":
                    movimiento = True
                fila2[r], fila1[r] = fila1[r], ""
    return movimiento

def validacion_movimientos(cond1,cond2,mov):
    pro = False
    if cond1 == True or cond2 == True:
        mov = mov + 1
        pro = True
    vacias(tablero,mov)
    if pro == True:
        aparicion(tablero)
    return mov

def vacias(tablero,mov):
    lista = []
    vacias = 0
    for c in range(4):
        for a in range(4):
            if tablero[c][a] == "":
                vacias = vacias+1
            elif tablero[c][a] != "":
                lista.append(tablero[c][a])
            elif tablero[c][a] == 2048:
                print("Juego terminado")
                #Incovar al tablero
                mostrar_tablero_final_bonito(tablero, puntaje=mov, mayor=max(lista))
                mostrar_menu()
    mayor = max(lista)
    #Para que se mire bonito
    if vacias == 0:
        print("Juego terminado")
        print("Movimientos Totales: ", mov-1)
        print("Número mayor obtenido: ", mayor)
        mostrar_tablero_final_bonito(tablero, puntaje=mov-1, mayor=mayor)  
        return
        mostrar_menu()
    print("Movimiento # " ,mov)
    print("Número mayor: ", mayor)
    print("Casillas vacías: ", vacias) 
    
def aparicion(tablero):
    while True:
        posf, posc = random.randint(0, 3), random.randint(0, 3)
        if tablero[posf][posc] == "":
            tablero[posf][posc] = random.choice([2, 4])
            break

# Ignorar el nombre XD
def mostrar_tablero_final_bonito(tablero, puntaje, mayor):
    print("\n" + "-" * 30)
    print("|{:^28}|".format(" FIN DEL JUEGO "))
    print("-" * 30)
    print("|{:^28}|".format(f"Puntaje total: {puntaje}"))
    print("|{:^28}|".format(f"Mayor número: {mayor}"))
    print("-" * 30)
    print("|{:^28}|".format("¡Gracias por jugar!"))
    print("-" * 30 + "\n")

    # Mostrar tablero con formato bonito
    print("+" + "-------+" * 4)
    for fila in tablero:
        fila_str = "|"
        for celda in fila:
            valor = celda if celda != "" else " "
            fila_str += f"{valor:^7}|"
        print(fila_str)
        print("+" + "-------+" * 4)

def teclas():
    mov = 0
    while True:
        tecla = input("Movimiento (a=izquierda, d=derecha, w=arriba, s=abajo, q=salir, h=ayuda): ")
        if tecla == "q":
            print("¡Juego terminado!")
            return
        elif tecla == "h":
            mostrar_ayuda()
            continue
        elif tecla == "a":
            cond1 = mov_izquierda(tablero)
            cond2 = sumas_columnas(tablero)
            mov_izquierda(tablero)
        elif tecla == "d":
            cond1 = mov_derecha(tablero)
            cond2 = sumas_columnas(tablero)
            mov_derecha(tablero)
        elif tecla == "w":
            cond1 = mov_arriba(fila1, fila2, fila3, fila4)
            cond2 = sumas_filas(fila1, fila2, fila3, fila4)
            mov_arriba(fila1, fila2, fila3, fila4)
        elif tecla == "s":
            cond1 = mov_abajo(fila1, fila2, fila3, fila4)
            cond2 = sumas_filas(fila1, fila2, fila3, fila4)
            mov_abajo(fila1, fila2, fila3, fila4)

        mov = validacion_movimientos(cond1,cond2,mov)
        mostrar_tablero(tablero)

def modo_individual():
    generar_tablero_inicial()
    mostrar_tablero(tablero)
    teclas()


# ----------------------------------------------
#              Jugador vs Jugador   
# ----------------------------------------------

# Necesiamos comprar los puntajes de ambos lados asi y guardarlos 


# Reutilizamos 
def jugar_turno(tablero_inicial, jugador):
    tablero_jugador = copy.deepcopy(tablero_inicial)
    fila1, fila2, fila3, fila4 = tablero_jugador[0], tablero_jugador[1], tablero_jugador[2], tablero_jugador[3]
    mov = 0
    while True:
        mostrar_tablero(tablero_jugador)
        tecla = input(f"{jugador} - Movimiento (a=izquierda, d=derecha, w=arriba, s=abajo, q=salir, h=ayuda): ").lower()
        if tecla == "q":
            break
        elif tecla == "a":
            cond1 = mov_izquierda(tablero_jugador)
            cond2 = sumas_columnas(tablero_jugador)
            mov_izquierda(tablero_jugador)
        elif tecla == "d":
            cond1 = mov_derecha(tablero_jugador)
            cond2 = sumas_columnas(tablero_jugador)
            mov_derecha(tablero_jugador)
        elif tecla == "w":
            cond1 = mov_arriba(fila1, fila2, fila3, fila4)
            cond2 = sumas_filas(fila1, fila2, fila3, fila4)
            mov_arriba(fila1, fila2, fila3, fila4)
        elif tecla == "s":
            cond1 = mov_abajo(fila1, fila2, fila3, fila4)
            cond2 = sumas_filas(fila1, fila2, fila3, fila4)
            mov_abajo(fila1, fila2, fila3, fila4)
        else:
            print("Movimiento inválido.")
            continue
        if cond1 or cond2:
            aparicion(tablero_jugador)
            mov += 1
        # Verifica si está lleno o alcanzó 2048 (usa vacías)
        lista = [tablero_jugador[f][c] for f in range(4) for c in range(4) if tablero_jugador[f][c] != ""]
        mayor = max(lista) if lista else 0
        vacias = sum(1 for f in range(4) for c in range(4) if tablero_jugador[f][c] == "")
        

        if vacias == 0 or mayor >= 2048:
            break

    # Mostrar resumen final con formato bonito:
    print("\n" + "-" * 30)
    print("|{:^28}|".format(f" FIN DEL TURNO DE {jugador} "))
    print("-" * 30)
    print("|{:^28}|".format(f"Movimientos: {mov}"))
    print("|{:^28}|".format(f"Mayor número: {mayor}"))
    print("|{:^28}|".format(f"Casillas vacías: {vacias}"))
    print("-" * 30)
    print("|{:^28}|".format("¡Gracias por jugar!"))
    print("-" * 30 + "\n")
    
    return mov, mayor


def modo_multijugador():
    generar_tablero_inicial()
    tablero_inicial = copy.deepcopy(tablero)
    print("Configuración inicial:")
    mostrar_tablero(tablero_inicial)
    primer_jugador = random.choice(["Jugador 1", "Jugador 2"])
    segundo_jugador = "Jugador 2" if primer_jugador == "Jugador 1" else "Jugador 1"
    print(f"{primer_jugador} empieza.\n")
    
    mov1, mayor1 = jugar_turno(tablero_inicial, primer_jugador)
    mov2, mayor2 = jugar_turno(tablero_inicial, segundo_jugador)
    
    print("\nResultados finales:")
    print(f"{primer_jugador} - movimientos: {mov1}, mayor: {mayor1}")
    print(f"{segundo_jugador} - movimientos: {mov2}, mayor: {mayor2}")
    
    if mayor1 > mayor2:
        print(f"¡{primer_jugador} gana!")
    elif mayor2 > mayor1:
        print(f"¡{segundo_jugador} gana!")
    else:
        if mov1 < mov2:
            print(f"¡{primer_jugador} gana por menos movimientos!")
        elif mov2 < mov1:
            print(f"¡{segundo_jugador} gana por menos movimientos!")
        else:
            print("¡Empate total!")


# ----------------------------------------------
#              Maquina vs Jugador   
# ----------------------------------------------

# Prueba No.5 de algoritmo de deteccion de movimientos
def decidir_mejor_movimiento(tablero):
    """
    Determina el mejor movimiento que puede hacer la máquina evaluando todas las opciones (a, d, w, s) usando una heurística simple.
    1. Copia el tablero original para no modificarlo.
    2. Simula cada movimiento (izquierda, derecha, arriba, abajo).
    3. Calcula si se realiza un movimiento válido y evalúa: número de casillas libres, mayor nómero alcanzado y el valor superior izquierda (numeros grandes)
    4 Selecciona el movimiento con la mayor puntuación.
    """
    movimientos = ["a", "d", "w", "s"]
    heuristicas = {}

    for mov in movimientos:
        tablero_simulado = copy.deepcopy(tablero)
        fila1, fila2, fila3, fila4 = tablero_simulado[0], tablero_simulado[1], tablero_simulado[2], tablero_simulado[3]
        movimiento_realizado = False

        if mov == "a":
            movimiento_realizado = mov_izquierda(tablero_simulado)
            movimiento_realizado |= sumas_columnas(tablero_simulado)
        elif mov == "d":
            movimiento_realizado = mov_derecha(tablero_simulado)
            movimiento_realizado |= sumas_columnas(tablero_simulado)
        elif mov == "w":
            movimiento_realizado = mov_arriba(fila1, fila2, fila3, fila4)
            movimiento_realizado |= sumas_filas(fila1, fila2, fila3, fila4)
        elif mov == "s":
            movimiento_realizado = mov_abajo(fila1, fila2, fila3, fila4)
            movimiento_realizado |= sumas_filas(fila1, fila2, fila3, fila4)

        if not movimiento_realizado:
            heuristicas[mov] = (-1000, "Movimiento inválido")
            continue

        vacias = sum(1 for f in range(4) for c in range(4) if tablero_simulado[f][c] == "")
        mayor = max([tablero_simulado[f][c] for f in range(4) for c in range(4) if tablero_simulado[f][c] != ""], default=0)
        esquina_valor = tablero_simulado[0][0] if tablero_simulado[0][0] != "" else 0

        puntuacion = vacias * 5 + mayor + esquina_valor * 2

        heuristicas[mov] = (puntuacion, mov)  # Guardamos solo el movimiento, lo demás no importa

    mejor_mov, _ = max(heuristicas.items(), key=lambda x: x[1][0])

    # Razones detalladas para cada movimiento
    if mejor_mov == "a":
        razon = "La máquina eligió A (izquierda) porque hay más espacio libre para moverse."
    elif mejor_mov == "d":
        razon = "La máquina eligió D (derecha) porque hay números grandes acumulados a la derecha."
    elif mejor_mov == "w":
        razon = "La máquina eligió W (arriba) porque puede combinar y sumar más números."
    elif mejor_mov == "s":
        razon = "La máquina eligió S (abajo) porque puede sumar números en esa dirección."

    print(f"\n{razon}\n")
    return mejor_mov



def jugar_turno_maquina(tablero_inicial):
    """
    Simula el turno completo de la máquina. La máquina hace movimientos automáticos hasta que no puede más o alcanza 2048.
    1. Copia el tablero inicial.
    2. Hace un bucle infinito el cual muestra el tablero, usa la logica de decidir_mejor_movimiento y cada movimiento genera una pausa de 2 segs
    3. Cuenta los movimientos realizados y el mayor número alcanzado.
    """
    
    
    tablero_jugador = copy.deepcopy(tablero_inicial)
    fila1, fila2, fila3, fila4 = tablero_jugador[0], tablero_jugador[1], tablero_jugador[2], tablero_jugador[3]
    mov = 0

    while True:
        mostrar_tablero(tablero_jugador)
        tecla = decidir_mejor_movimiento(tablero_jugador)
        if tecla is None:
            print("¡La máquina no puede mover más!")
            break
        print(f"Máquina decide: {tecla.upper()}")
        
        time.sleep(2)  # Pausa de 2 segundos entre movimientos

        if tecla == "a":
            mov_izquierda(tablero_jugador)
            sumas_columnas(tablero_jugador)
            mov_izquierda(tablero_jugador)
        elif tecla == "d":
            mov_derecha(tablero_jugador)
            sumas_columnas(tablero_jugador)
            mov_derecha(tablero_jugador)
        elif tecla == "w":
            mov_arriba(fila1, fila2, fila3, fila4)
            sumas_filas(fila1, fila2, fila3, fila4)
            mov_arriba(fila1, fila2, fila3, fila4)
        elif tecla == "s":
            mov_abajo(fila1, fila2, fila3, fila4)
            sumas_filas(fila1, fila2, fila3, fila4)
            mov_abajo(fila1, fila2, fila3, fila4)

        aparicion(tablero_jugador)
        mov += 1

        lista = [tablero_jugador[f][c] for f in range(4) for c in range(4) if tablero_jugador[f][c] != ""]
        mayor = max(lista) if lista else 0
        vacias = sum(1 for f in range(4) for c in range(4) if tablero_jugador[f][c] == "")
        
        if vacias == 0 or mayor >= 2048:
            break

    print(f"Máquina termina con {mov} movimientos, mayor: {mayor}")
    return mov, mayor


def modo_maquina_autonomo():
    # Modo automático donde la máquina juega sola desde un tablero inicial y muestra los resultados al final.
    
    generar_tablero_inicial()
    tablero_inicial = copy.deepcopy(tablero)
    print("Configuración inicial:")
    mostrar_tablero(tablero_inicial)
    print("La máquina juega sola...\n")
    time.sleep(1)

    mov, mayor = jugar_turno_maquina(tablero_inicial)

    print(f"\nResultados finales:")
    print(f"Máquina - movimientos: {mov}, mayor: {mayor}")


# Modo Jugador vs Máquina. La máquina juega su turno primero y luego se da al jugador la oportunidad de jugar sobre el mismo tablero.
def modo_maquina():
    generar_tablero_inicial()
    tablero_inicial = copy.deepcopy(tablero)
    print("Configuración inicial:")
    mostrar_tablero(tablero_inicial)

    # Empieza la máquina
    print("\n=== Turno de la MÁQUINA ===")
    mov_maquina, mayor_maquina = jugar_turno_maquina(tablero_inicial)

    # Ahora turno del jugador
    print("\n=== Turno del JUGADOR ===")
    mov_jugador, mayor_jugador = jugar_turno(tablero_inicial, "Jugador")

    # Mostrar resultados
    print("\nResultados finales:")
    print(f"Máquina - Movimientos: {mov_maquina}, Mayor número: {mayor_maquina}")
    print(f"Jugador - Movimientos: {mov_jugador}, Mayor número: {mayor_jugador}")

    # Determinar quién gana
    if mayor_maquina > mayor_jugador:
        print("¡La máquina gana!")
    elif mayor_jugador > mayor_maquina:
        print("¡El jugador gana!")
    else:
        if mov_maquina < mov_jugador:
            print("¡La máquina gana por menos movimientos!")
        elif mov_jugador < mov_maquina:
            print("¡El jugador gana por menos movimientos!")
        else:
            print("¡Empate total!")


def manejar_modo(modo):
    if modo == 1:
        print("Modo Normal")
        modo_individual()
    elif modo == 2:
        print("Modo Jugador vs Jugador")
        modo_multijugador()
    elif modo == 3:
        print("Modo Jugador vs Máquina (con turno humano)")
        modo_maquina() 


#PTS EXTRA 😎
#Instrucciones del juego
def mostrar_ayuda():
    print("\n=== Instrucciones del juego ===")
    print("Objetivo: Alcanzar 2048 sumando casillas con números iguales.")
    print("Controles:")
    print("- W: Mover hacia arriba")
    print("- A: Mover hacia la izquierda")
    print("- S: Mover hacia abajo")
    print("- D: Mover hacia la derecha")
    print("- H: Mostrar esta ayuda")
    print("- R: Reproducir movimientos (replay)")
    print("- Q: Salir del juego")
    print("==============================")
    print("¡Disfruta del juego!")
    print("==============================\n")


#Sistema de replay
movimientos_replay = []
#Aun me falta pensarla :V ya que no se como guardar los movimientos


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
