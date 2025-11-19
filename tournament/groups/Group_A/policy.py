import numpy as np
from connect4.policy import Policy
import random
from connect4.connect_state import ConnectState


class SebastianAgent(Policy):
    def __init__(self):
        self.generador = random.Random()
        self.epsilon = 0.2
        self.U_total = {}
        self.N_visitas = {}
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

    def e_greedy(self, estado: str, acciones, tablero, jugador_actual) -> int:
        #codigo de juanes de que en la primera jugada juegue en el centro
        if self.jugadas_del_agente == 0 and jugador_actual == -1:
            return 3
        
        

        simulaciones = 20

        for a in acciones:
            clave = (estado, a)
            if clave not in self.U_total:
                self.U_total[clave] = 0.0
                self.N_visitas[clave] = 0

            for _ in range(simulaciones):
                recompensa = self.simular_partida(tablero, jugador_actual, a)
                self.U_total[clave] += recompensa
                self.N_visitas[clave] += 1

        # Exploración
        if self.generador.random() < self.epsilon:
            return acciones[self.generador.randint(0, len(acciones) - 1)]

        # Explotación
        mejor_accion = acciones[0]
        clave_mejor = (estado, mejor_accion)
        mejor_valor = (
            0.0
            if self.N_visitas[clave_mejor] == 0
            else self.U_total[clave_mejor] / self.N_visitas[clave_mejor]
        )

        for a in acciones[1:]:
            clave = (estado, a)
            q = (
                0.0
                if self.N_visitas[clave] == 0
                else self.U_total[clave] / self.N_visitas[clave]
            )
            if q > mejor_valor:
                mejor_valor = q
                mejor_accion = a

        return mejor_accion

    def simular_partida(self, tablero, jugador_inicial, primera_accion):
        estado = ConnectState(board=tablero, player=jugador_inicial)

        if not estado.is_applicable(primera_accion):
            return 0.0

        estado = estado.transition(primera_accion)

        if estado.is_final():
            ganador = estado.get_winner()
            if ganador == jugador_inicial:
                return 1.0
            elif ganador == 0:
                return 0.0
            else:
                return -1.0

        jugador = -jugador_inicial

        while True:
            cols = estado.get_free_cols()
            if len(cols) == 0:
                return 0.0

            col = cols[self.generador.randint(0, len(cols) - 1)]
            estado = estado.transition(col)

            if estado.is_final():
                ganador = estado.get_winner()
                if ganador == jugador_inicial:
                    return 1.0
                elif ganador == 0:
                    return 0.0
                else:
                    return -1.0

            jugador = -jugador

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

        #codifo de juanes de que si el oponente puede ganar que bloquee
        for col in acciones_posibles:
            test = ConnectState(board=s, player=-jugador_actual)
            nuevo = test.transition(col)
            if nuevo.is_final() and nuevo.get_winner() == -jugador_actual:
                self.episodio_completo.append((estado_actual, col))
                self.jugadas_del_agente += 1
                return int(col)

        #despues si probar montecarlo
        accion = self.e_greedy(estado_actual, acciones_posibles, s, jugador_actual)

        self.episodio_completo.append((estado_actual, accion))
        self.jugadas_del_agente += 1

        return int(accion)