"""Regras da cobrinha e escolha dos movimentos, sem depender do Pygame.

O A* procura um caminho até a comida. O ciclo Hamiltoniano protege a saída
da cabeça e oferece um passo de reserva quando a busca não encontra rota.
O propósito é observar o algoritmo, sem buscar um recorde de movimentos.
"""

from __future__ import annotations

from a import encontrar_caminho
from collections import deque
from random import Random
from typing import Iterable

Posicao = tuple[int, int]
LARGURA_TABULEIRO = 16
ALTURA_TABULEIRO = 16
DIRECOES = ((0, -1), (-1, 0), (1, 0), (0, 1))


def criar_ciclo_hamiltoniano(largura: int, altura: int) -> tuple[Posicao, ...]:
    if largura < 2 or altura < 2 or (largura % 2 and altura % 2):
        raise ValueError("ao menos uma dimensão do tabuleiro deve ser par")
    if altura % 2:
        # A construção abaixo exige altura par; transpor resolve largura par.
        return tuple((y, x) for x, y in criar_ciclo_hamiltoniano(altura, largura))

    celulas: list[Posicao] = [(x, 0) for x in range(largura)]
    for y in range(1, altura):
        colunas_da_linha = range(largura - 1, 0, -1) if y % 2 else range(1, largura)
        celulas.extend((x, y) for x in colunas_da_linha)
    celulas.extend((0, y) for y in range(altura - 1, 0, -1))
    return tuple(celulas)


class CobraAutonoma:
    """Mantém o corpo, a comida e as decisões de uma partida.

    No corpo, a primeira posição é a cabeça e a última é a cauda.
    Uma semente fixa permite repetir a mesma sequência de comidas.
    """

    def __init__(
        self,
        largura: int = LARGURA_TABULEIRO,
        altura: int = ALTURA_TABULEIRO,
        semente: int | None = None,
    ) -> None:
        self.largura = largura
        self.altura = altura
        self.capacidade = largura * altura
        self.ciclo = criar_ciclo_hamiltoniano(largura, altura)
        self.ordem_no_ciclo = {
            posicao: indice for indice, posicao in enumerate(self.ciclo)
        }
        indice_cabeca = self.ordem_no_ciclo[(largura // 2, altura // 2)]
        self.corpo: deque[Posicao] = deque(
            self.ciclo[(indice_cabeca - deslocamento) % self.capacidade]
            for deslocamento in range(3)
        )
        self.ocupadas = set(self.corpo)
        self.sorteador = Random(semente)
        self.comida: Posicao | None = None
        self.caminho_planejado: list[Posicao] = []
        self.movimentos_astar = 0
        self.movimentos_reserva = 0
        self.movimentos = 0
        self.pontuacao = 0
        self.venceu = False
        self._sortear_comida()

    @property
    def cabeca(self) -> Posicao:
        return self.corpo[0]

    def _posicoes_vizinhas(self, posicao: Posicao) -> Iterable[Posicao]:
        x, y = posicao
        for deslocamento_x, deslocamento_y in DIRECOES:
            candidata = x + deslocamento_x, y + deslocamento_y
            if 0 <= candidata[0] < self.largura and 0 <= candidata[1] < self.altura:
                yield candidata

    def _distancia_no_ciclo(self, inicio: Posicao, fim: Posicao) -> int:
        return (self.ordem_no_ciclo[fim] - self.ordem_no_ciclo[inicio]) % self.capacidade

    def _movimento_seguro(self, posicao: Posicao) -> bool:
        """Confere a colisão imediata e a ordem do corpo no ciclo."""
        vai_crescer = posicao == self.comida
        cauda = self.corpo[-1]
        entra_na_cauda_liberada = posicao == cauda and not vai_crescer
        if posicao in self.ocupadas and not entra_na_cauda_liberada:
            return False

        # A última comida encerra a partida; não existe estado futuro a
        # proteger, portanto basta que a colisão imediata seja impossível.
        if vai_crescer and len(self.corpo) == self.capacidade - 1:
            return True

        # Não ultrapassar a cauda preserva a ordem Hamiltoniana e a garantia
        # de vitória. O próximo ponto do ciclo sempre satisfaz esta condição.
        distancia = self._distancia_no_ciclo(self.cabeca, posicao)
        distancia_cauda = self._distancia_no_ciclo(self.cabeca, cauda)
        fica_antes_da_cauda = 0 < distancia < distancia_cauda
        if not (fica_antes_da_cauda or entra_na_cauda_liberada):
            return False

        # Um atalho jamais pode saltar por cima da comida na ordem do ciclo;
        # caso contrário uma sequência de atalhos poderia adiá-la para sempre.
        if self.comida is not None:
            distancia_comida = self._distancia_no_ciclo(self.cabeca, self.comida)
            if distancia_comida < distancia_cauda and distancia > distancia_comida:
                return False
        return True

    def escolher_movimento(self) -> Posicao:
        """Usa A* para buscar comida, respeitando os movimentos seguros."""
        movimentos_seguros = {
            posicao
            for posicao in self._posicoes_vizinhas(self.cabeca)
            if self._movimento_seguro(posicao)
        }
        if not movimentos_seguros:
            raise RuntimeError("estado inválido: a cobra ficou sem movimento seguro")

        # A cauda libera sua célula quando a cobra não come. Ela pode ser
        # usada como passagem; o restante do corpo continua sendo obstáculo.
        bloqueadas = self.ocupadas - {self.cabeca, self.corpo[-1]}
        self.caminho_planejado = []
        if self.comida is not None:
            self.caminho_planejado = encontrar_caminho(
                self.largura,
                self.altura,
                self.cabeca,
                self.comida,
                bloqueadas,
                primeiros_passos=movimentos_seguros,
            )

        if len(self.caminho_planejado) > 1:
            self.movimentos_astar += 1
            return self.caminho_planejado[1]

        # Sem rota até a comida, avançamos no ciclo para liberar espaço.
        # Esta reserva de segurança evita inventar um movimento perigoso.
        self.movimentos_reserva += 1
        return self.ciclo[(self.ordem_no_ciclo[self.cabeca] + 1) % self.capacidade]

    def avancar(self) -> None:
        """Anda uma célula e, se comer, aumenta o corpo."""
        if self.venceu:
            return
        nova_cabeca = self.escolher_movimento()
        comeu = nova_cabeca == self.comida

        if not comeu:
            cauda_liberada = self.corpo.pop()
            self.ocupadas.remove(cauda_liberada)
        self.corpo.appendleft(nova_cabeca)
        self.ocupadas.add(nova_cabeca)
        self.movimentos += 1

        if comeu:
            self.pontuacao += 1
            self._sortear_comida()

    def _sortear_comida(self) -> None:
        if len(self.corpo) == self.capacidade:
            self.comida = None
            self.venceu = True
            return
        livres = tuple(
            posicao for posicao in self.ciclo if posicao not in self.ocupadas
        )
        self.comida = self.sorteador.choice(livres)

    def jogar_ate_vencer(self, limite_movimentos: int | None = None) -> int:
        """Executa sem janela, útil para testar partidas completas."""
        limite = limite_movimentos if limite_movimentos is not None else self.capacidade ** 3
        while not self.venceu and self.movimentos < limite:
            self.avancar()
        if not self.venceu:
            raise RuntimeError(f"o jogo não terminou após {limite} movimentos")
        return self.movimentos
