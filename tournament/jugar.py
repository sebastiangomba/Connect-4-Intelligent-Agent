import numpy as np
from connect4.connect_state import ConnectState
from groups.Group_A.policy import SebastianAgent


def imprimir_tablero(estado: ConnectState):
    board = estado.board  # matriz numpy 6x7

    print("\n    0     1     2     3     4     5     6")
    print("  +" + "-----+" * 7)

    for r in range(board.shape[0]):
        fila = "  |"
        for c in range(board.shape[1]):
            valor = board[r, c]
            # Mostrar exactamente -1, 0, 1 con espacio fijo
            ficha = f"{valor:>3}"  # ancho fijo de 3 chars
            fila += f" {ficha} |"
        print(fila)
        print("  +" + "-----+" * 7)
    print()


def pedir_columna(estado: ConnectState) -> int:
    free_cols = estado.get_free_cols()
    while True:
        entrada = input(f"Tu turno (1). Elige columna {free_cols}: ")
        try:
            col = int(entrada)
        except ValueError:
            print("Ingresa un número válido.")
            continue

        if col not in free_cols:
            print("Columna inválida o llena. Intenta de nuevo.")
            continue

        return col


def main():
    estado = ConnectState()
    agente = SebastianAgent()
    agente.mount()

    print("Conecta 4 — Tú eres 1, el agente es -1")
    imprimir_tablero(estado)

    while not estado.is_final():

        # Turno del humano (1)
        if estado.player == 1:
            col = pedir_columna(estado)
            estado = estado.transition(col)
            imprimir_tablero(estado)

            if estado.is_final():
                break

        # Turno del agente (-1)
        else:
            print("Turno del agente (-1)...")
            col_agente = agente.act(estado.board.copy())

            if not estado.is_applicable(col_agente):
                free_cols = estado.get_free_cols()
                col_agente = free_cols[0]

            estado = estado.transition(col_agente)
            imprimir_tablero(estado)

            if estado.is_final():
                break

    ganador = estado.get_winner()
    print("\n=== RESULTADO ===")
    if ganador == 1:
        print("Ganaste!")
    elif ganador == -1:
        print("El agente ganó.")
    else:
        print("Empate (tablero lleno).")


if __name__ == "__main__":
    main()