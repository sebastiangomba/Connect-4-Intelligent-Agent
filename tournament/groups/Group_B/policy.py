import numpy as np
from connect4.policy import Policy
from connect4.connect_state import ConnectState
from typing import override

class juanes_agente(Policy):

    @override
    def mount(self) -> None:
        self.jugadas_del_agente = 0
       

    @override
    def act(self, s: np.ndarray) -> int:
        estado = ConnectState(board=s)
        available_cols = estado.get_free_cols()
        if self.jugadas_del_agente == 0:
            epsilon = 1 
        else:
            epsilon = 1 / self.jugadas_del_agente
         
        def puede_ganar(estado: ConnectState, col: int) -> int | None:
            nuevo_estado = estado.transition(col)
            if nuevo_estado.is_final() and nuevo_estado.get_winner() == estado.player:
                return col
            return None
        
        def simular_partida(estado: ConnectState) -> int:
            estado_simulado = estado
            while not estado_simulado.is_final():
                movimientos_disponibles = estado_simulado.get_free_cols()
                movimiento_aleatorio = np.random.choice(movimientos_disponibles)
                estado_simulado = estado_simulado.transition(movimiento_aleatorio)
            return estado_simulado.get_winner()
        
        def bloquear_ganar_oponente(estado: ConnectState, available_cols: list) -> int | None:
            for col in available_cols:
                opp_estado = estado.transition(col)  # Simula si jugando ahi ganaria el oponente
                if opp_estado.is_final() and opp_estado.get_winner() == -estado.player:
                    return col  # Bloquear jugando aquí
            return None
            
        def jugar_con_montecarlo(estado: ConnectState, numero_de_simulaciones: int = 200) -> int:
            victorias = {}
            for col in estado.get_free_cols():
                victorias[col] = 0
                for i in range(numero_de_simulaciones):
                    nuevo_estado = estado.transition(col)
                    ganador = simular_partida(nuevo_estado)
                    if ganador == estado.player:
                        victorias[col] += 1
            mejor_col = 0
            max_victorias = 0

            for col, victorias_col in victorias.items():
                if victorias_col > max_victorias:
                    max_victorias = victorias_col
                    mejor_col = col

            return mejor_col
            
        
        # jugada segun experiencia
        if self.jugadas_del_agente == 0:
            if 3 in available_cols:
                self.jugadas_del_agente += 1
                return 3
            else :
                self.jugadas_del_agente += 1
                return 1  
       
        for col in available_cols:
            if puede_ganar(estado, col) is not None:
                self.jugadas_del_agente += 1
                return col
        
        resultado = bloquear_ganar_oponente(estado, available_cols)
        if resultado is not None:
            self.jugadas_del_agente += 1
            return resultado
                
        # Si no hay jugadas estratégicas, elige aleatoriamente
        if np.random.rand() < epsilon:
            self.jugadas_del_agente += 1
            return np.random.choice(available_cols)
        else:
            col = jugar_con_montecarlo(estado)
            self.jugadas_del_agente += 1
            return col
