
import numpy as np
import math
import random
from connect4.policy import Policy
from connect4.connect_state import ConnectState


class MCTS:
    def __init__(self, state: ConnectState, parent=None, action=None):
        self.state = state                  
        self.parent = parent                 
        self.action = action                 
        self.children = []                  
        self.visits = 0                       
        self.wins = 0                       
        self.untried_actions = self.get_actions() 

    def get_actions(self):
         return self.state.get_free_cols()

    def is_terminal(self):
        return self.state.is_final()

    def all_actions_tried(self):
        return len(self.untried_actions) == 0

    def check_winner(self):
        return self.state.get_winner()

    def expand(self):
        action = self.untried_actions.pop()
        new_state = self.state.transition(action)
        child = MCTS(new_state, parent=self, action=action)
        self.children.append(child)
        return child

    def best_child(self, c=1.4):
        return max(self.children, key=lambda child:
                   (child.wins / child.visits) +
                   c * math.sqrt(math.log(self.visits) / child.visits))

    def rollout(self):
        current_state = self.state
        initial_player = self.state.player
        while not current_state.is_final():
            actions = current_state.get_free_cols()
            if not actions:
                return 0  
            action = random.choice(actions)
            current_state = current_state.transition(action)
        winner = current_state.get_winner()
        if winner == initial_player:
            return 1.0
        elif winner == 0:
            return 0
        else:
            return -1.0

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)


def mcts_search(root_state: ConnectState, iterations=100):
    root = MCTS(root_state)
    for iteration in range(iterations):
        node = root
        # Seleccion
        while not node.is_terminal() and node.all_actions_tried():
            node = node.best_child()
        # Expansion de un nodo hijo
        if not node.is_terminal():
            node = node.expand()
        # Simulatcion
        result = node.rollout()
        # transferencia de resultados
        node.backpropagate(result)
    return root.best_child(c=0).action  


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