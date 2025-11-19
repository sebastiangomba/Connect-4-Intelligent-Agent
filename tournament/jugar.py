import numpy as np
from connect4.connect_state import ConnectState
from groups.Group_A.policy import SebastianAgent
#from groups.Group_B.policy import juanes_agente  # cambia Group_A si tu carpeta se llama distinto


def imprimir_tablero(board: np.ndarray):
    for fila in board:
        print(" ".join(str(int(x)) for x in fila))
    print()


def jugar_contra_agente():
    estado = ConnectState()
    agente = SebastianAgent()
    #agente = juanes_agente()

    agente.mount()

    print("Comienza el juego.")
    print("Tú eres 1 (amarillo). El agente es -1 (rojo).")
    imprimir_tablero(estado.board)

    while not estado.is_final():
        if estado.player == 1:
            # TU TURNO (jugador 1 / amarillo)
            while True:
                try:
                    col = int(input("Tu jugada (0-6): "))
                    if not estado.is_applicable(col):
                        print("Movimiento no válido, intenta otra columna.")
                        continue
                    break
                except ValueError:
                    print("Ingresa un número entre 0 y 6.")
            estado = estado.transition(col)
        else:
            # TURNO DEL AGENTE (jugador -1 / rojo)
            accion = agente.act(estado.board)
            print(f"El agente juega columna {accion}")
            estado = estado.transition(accion)

        imprimir_tablero(estado.board)

    ganador = estado.get_winner()
    if ganador == 1:
        print("Ganaste.")
    elif ganador == -1:
        print("El agente ganó.")
    else:
        print("Empate (tablero lleno sin cuatro en línea).")


if __name__ == "__main__":
    jugar_contra_agente()