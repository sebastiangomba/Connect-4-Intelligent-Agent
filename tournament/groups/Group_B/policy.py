
import numpy as np
import math
import random
from connect4.policy import Policy
from connect4.connect_state import ConnectState


class juanes_agente(Policy):
    def __init__(self):
        self.episodio_completo = []
        self.jugadas_del_agente = 0

    def mount(self) -> None:
        self.episodio_completo = []
        self.jugadas_del_agente = 0

    def id_estado(self, board: np.ndarray, jugador: int) -> str:
        plano = board.flatten()
        lista = []
        for celda in plano:
            if celda == -1:
                lista.append("R")
            elif celda == 1:
                lista.append("Y")
            else:
                lista.append("0")

        lista.append("|")
        lista.append("R" if jugador == -1 else "Y")

        estado = ""
        for x in lista:
            estado += x

        return estado

    def act(self, s: np.ndarray) -> int:
        estado_obj = ConnectState(board=s)
        jugador_actual = estado_obj.player
        acciones_posibles = estado_obj.get_free_cols()
        estado_actual = self.id_estado(s, jugador_actual)

        #codigo de juanes de que si puede ganar que gane
        for col in acciones_posibles:
            test = ConnectState(board=s, player=jugador_actual)
            nuevo = test.transition(col)
            if nuevo.is_final() and nuevo.get_winner() == jugador_actual:
                self.episodio_completo.append((estado_actual, col))
                self.jugadas_del_agente += 1
                return int(col)

        #codigo de juanes de que si el oponente puede ganar que bloquee
        for col in acciones_posibles:
            test = ConnectState(board=s, player=-jugador_actual)
            nuevo = test.transition(col)
            if nuevo.is_final() and nuevo.get_winner() == -jugador_actual:
                self.episodio_completo.append((estado_actual, col))
                self.jugadas_del_agente += 1
                return int(col)


        #despues usar MCTS
        accion = mcts_search(estado_obj, iterations=100)

        self.episodio_completo.append((estado_actual, accion))
        self.jugadas_del_agente += 1

        return int(accion)