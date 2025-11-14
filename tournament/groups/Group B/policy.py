import numpy as np
from connect4.policy import Policy
from connect4.connect_state import ConnectState
from typing import override

class juanesagente(Policy):

    @override
    def mount(self) -> None:
        self.move_count = 0

    @override
    def act(self, s: np.ndarray) -> int:
        estado = ConnectState(board=s)
        available_cols = estado.get_free_cols()
        
        # jugada segun experiencia
        if self.move_count == 0:
            if 3 in available_cols:
                self.move_count += 1
                return 3
            else :
                self.move_count += 1
                return 1  
        
        # funcion de si puede ganar jugando en esa fila que la retorne
        def puede_ganar(estado: ConnectState, col: int) -> int:
            nuevo_estado = estado.transition(col)
            if nuevo_estado.is_final() and nuevo_estado.get_winner() == estado.player:
                self.move_count += 1
                return col
        
        #funcion que bloquee si el oponente puede ganar en la siguiente jugada
        def bloquear_ganar_oponente(estado: ConnectState, col: int) -> int:
            nuevo_estado = estado.transition(col)
            opponent_cols = nuevo_estado.get_free_cols()
            for opp_col in opponent_cols:
                opp_estado = nuevo_estado.transition(opp_col)
                if opp_estado.is_final() and opp_estado.get_winner() == -estado.player:
                    self.move_count += 1
                    return col  # Bloquea
        #aplicar ambas funciones
        for col in available_cols:
            resultado = puede_ganar(estado, col)
            if resultado is not None:
                return resultado
        
        for col in available_cols:
            resultado = bloquear_ganar_oponente(estado, col)
            if resultado is not None:
                return resultado
                
        # Si no hay jugadas estratégicas, elige aleatoriamente
        self.move_count += 1
        return np.random.choice(available_cols)
