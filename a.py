"""Busca A*: encontra o menor caminho numa grade com obstáculos.

Cada movimento custa 1. A distância Manhattan estima quantos movimentos
faltam, sem exagerar: não usamos diagonais neste jogo.
"""

from heapq import heappop, heappush
from itertools import count

Posicao = tuple[int, int]


def encontrar_caminho(
    largura: int,
    altura: int,
    inicio: Posicao,
    destino: Posicao,
    bloqueadas: set[Posicao],
    *,
    primeiros_passos: set[Posicao] | None = None,
) -> list[Posicao]:
    """Retorna a rota incluindo início e destino, ou [] se não houver rota.

    primeiros_passos limita a saída da cabeça aos movimentos seguros.
    A busca considera o corpo atual; o jogo refaz a busca depois de andar.
    As posições são pares (x, y), sem movimentos na diagonal.
    """
    def dentro_do_tabuleiro(posicao: Posicao) -> bool:
        x, y = posicao
        return 0 <= x < largura and 0 <= y < altura

    def distancia(posicao: Posicao) -> int:
        return abs(posicao[0] - destino[0]) + abs(posicao[1] - destino[1])

    if not dentro_do_tabuleiro(inicio) or not dentro_do_tabuleiro(destino) or destino in bloqueadas:
        return []

    # O contador desempata prioridades sem depender da ordem das coordenadas.
    desempate = count()
    # Cada entrada guarda: f, desempate, g e posição. O menor f sai primeiro.
    fila_prioridades = [(distancia(inicio), next(desempate), 0, inicio)]
    custos = {inicio: 0}
    anteriores: dict[Posicao, Posicao] = {}

    while fila_prioridades:
        _, _, custo, atual = heappop(fila_prioridades)
        if custo != custos[atual]:
            continue  # Uma rota melhor já substituiu esta entrada da fila.
        if atual == destino:
            # Voltamos pelos passos anteriores até chegar à cabeça.
            caminho = [atual]
            while atual != inicio:
                atual = anteriores[atual]
                caminho.append(atual)
            return caminho[::-1]

        x, y = atual
        for vizinha in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if not dentro_do_tabuleiro(vizinha) or vizinha in bloqueadas:
                continue
            if (
                atual == inicio
                and primeiros_passos is not None
                and vizinha not in primeiros_passos
            ):
                continue
            novo_custo = custo + 1
            if novo_custo >= custos.get(vizinha, float("inf")):
                continue
            custos[vizinha] = novo_custo
            anteriores[vizinha] = atual
            prioridade = novo_custo + distancia(vizinha)
            heappush(
                fila_prioridades,
                (prioridade, next(desempate), novo_custo, vizinha),
            )

    # A fila acabou sem alcançar o destino.
    return []
