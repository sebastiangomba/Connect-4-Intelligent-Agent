import numpy as np
from connect4.policy import Policy
#from typing import override
import random


class SebastianAgent(Policy):
    def __init__(self):
        self.generador = random.Random()
        self.epsilon = 0.2 # por ahora un epsilon aleatorio
        self.U_total = {}      
        self.N_visitas = {}
        self.episodio_completo = []

 #   @override
    def mount(self) -> None:
        self.episodio_completo = []

    def id_estado(self, board: np.ndarray, jugador: int) -> str:
        plano = board.flatten()
        lista_caracteres = []
        i = 0
        while i < plano.shape[0]:
            celda = plano[i]
            if celda == -1:
                lista_caracteres.append("R")
            elif celda == 1:
                lista_caracteres.append("Y")
            else:
                lista_caracteres.append("0")
            i = i + 1

        lista_caracteres.append("|")
        if jugador == -1:
            lista_caracteres.append("R")
        else:
            lista_caracteres.append("Y")

        estado = ""
        j = 0
        while j < len(lista_caracteres):
            estado = estado + lista_caracteres[j]
            j = j + 1

        return estado

    def columnas_disponibles(self, board: np.ndarray):
        cols = []
        c = 0
        while c < 7:
            if board[0, c] == 0:
                cols.append(c)
            c = c + 1
        return cols

    def e_greedy(self, estado: str, acciones: list[int]) -> int:
        if len(acciones) == 0:
            return 0

        k = 0
        while k < len(acciones):
            a = acciones[k]
            clave = (estado, a)
            if clave not in self.U_total:
                self.U_total[clave] = 0.0
                self.N_visitas[clave] = 0
            k = k + 1

        r = self.generador.random()
        if r < self.epsilon:
            indice = self.generador.randint(0, len(acciones) - 1)
            return acciones[indice]

        mejor_accion = acciones[0]
        clave_mejor = (estado, mejor_accion)
        visitas = self.N_visitas[clave_mejor]

        if visitas == 0:
            mejor_valor = 0.0
        else:
            mejor_valor = self.U_total[clave_mejor] / float(visitas)

        t = 1
        while t < len(acciones):
            a = acciones[t]
            clave = (estado, a)
            n = self.N_visitas[clave]
            if n == 0:
                q = 0.0
            else:
                q = self.U_total[clave] / float(n)
            if q > mejor_valor:
                mejor_valor = q
                mejor_accion = a
            t = t + 1

        return mejor_accion

    def inc_update(self, recompensa_final: float):
        pares_visitados = []
        U = recompensa_final
        idx = len(self.episodio_completo) - 1

        while idx >= 0:
            estado, accion = self.episodio_completo[idx]
            clave = (estado, accion)

            if clave not in pares_visitados:
                pares_visitados.append(clave)

                suma_anterior = self.U_total.get(clave, 0.0)
                visitas_anteriores = self.N_visitas.get(clave, 0)

                nueva_suma = suma_anterior + U
                nuevas_visitas = visitas_anteriores + 1

                self.U_total[clave] = nueva_suma
                self.N_visitas[clave] = nuevas_visitas

            idx = idx - 1

 #   @override
    def act(self, s: np.ndarray) -> int:
        rojas = int(np.sum(s == -1))
        amarillas = int(np.sum(s == 1))

        if rojas == amarillas:
            jugador_actual = -1
        else:
            jugador_actual = 1

        acciones_posibles = self.columnas_disponibles(s)
        estado_actual = self.id_estado(s, jugador_actual)

        accion = self.e_greedy(estado_actual, acciones_posibles)

        self.episodio_completo.append((estado_actual, accion))

        return int(accion)