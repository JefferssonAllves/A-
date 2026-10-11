"""Snake autônomo: execute com ``python main.py``."""

from __future__ import annotations

import argparse
from pathlib import Path

import pygame

from snake_game import CobraAutonoma, ALTURA_TABULEIRO, LARGURA_TABULEIRO

TAMANHO_CELULA = 30
QUADROS_POR_SEGUNDO = 30
COR_FUNDO = (17, 20, 24)
COR_GRADE = (31, 36, 42)
COR_CABECA = (124, 255, 107)
COR_CORPO = (47, 196, 86)
COR_COMIDA = (255, 75, 75)
COR_TEXTO = (235, 238, 240)


def desenhar(
    tela: pygame.Surface,
    jogo: CobraAutonoma,
    fonte: pygame.font.Font,
    *,
    atualizar_tela: bool = True,
) -> None:
    """Desenha o estado da partida; não toma decisões nem move a cobra."""
    tela.fill(COR_FUNDO)

    for x in range(LARGURA_TABULEIRO + 1):
        pygame.draw.line(tela, COR_GRADE, (x * TAMANHO_CELULA, 0),
                         (x * TAMANHO_CELULA, ALTURA_TABULEIRO * TAMANHO_CELULA))
    for y in range(ALTURA_TABULEIRO + 1):
        pygame.draw.line(tela, COR_GRADE, (0, y * TAMANHO_CELULA),
                         (LARGURA_TABULEIRO * TAMANHO_CELULA, y * TAMANHO_CELULA))

    # A linha mostra a previsão do A*. Ela muda quando o corpo se move.
    if len(jogo.caminho_planejado) > 1:
        pontos = [(x * TAMANHO_CELULA + TAMANHO_CELULA // 2,
                   y * TAMANHO_CELULA + TAMANHO_CELULA // 2) for x, y in jogo.caminho_planejado]
        pygame.draw.lines(tela, (66, 110, 145), False, pontos, 2)

    if jogo.comida is not None:
        comida_x, comida_y = jogo.comida
        pygame.draw.rect(tela, COR_COMIDA,
                         (comida_x * TAMANHO_CELULA + 4, comida_y * TAMANHO_CELULA + 4,
                          TAMANHO_CELULA - 8, TAMANHO_CELULA - 8), border_radius=8)

    for indice, (x, y) in enumerate(jogo.corpo):
        cor = COR_CABECA if indice == 0 else COR_CORPO
        pygame.draw.rect(tela, cor,
                         (x * TAMANHO_CELULA + 2, y * TAMANHO_CELULA + 2,
                          TAMANHO_CELULA - 4, TAMANHO_CELULA - 4), border_radius=6)

    fim_tabuleiro = ALTURA_TABULEIRO * TAMANHO_CELULA
    if jogo.venceu:
        mensagem = "VITÓRIA — tabuleiro completo!"
    else:
        mensagem = (
            f"Comidas: {jogo.pontuacao}/{jogo.capacidade - 3} "
            f"| Movimentos: {jogo.movimentos}"
        )
    tela.blit(fonte.render(mensagem, True, COR_TEXTO), (10, fim_tabuleiro + 10))
    detalhe = f"A*: {jogo.movimentos_astar} | Reserva segura: {jogo.movimentos_reserva}"
    tela.blit(fonte.render(detalhe, True, COR_TEXTO), (10, fim_tabuleiro + 35))
    tela.blit(fonte.render("Espaço: pausar | R: reiniciar | Esc: sair", True, COR_TEXTO),
                (10, fim_tabuleiro + 60))
    if atualizar_tela:
        pygame.display.flip()


def executar_jogo() -> None:
    """Abre a janela e cuida dos controles até o usuário encerrar a partida."""
    argumentos = argparse.ArgumentParser(description="Snake autônomo com busca A*")
    argumentos.add_argument(
        "--semente", "--seed", dest="semente", type=int,
        help="repete a mesma partida",
    )
    argumentos.add_argument(
        "--quadros-por-segundo", "--fps", dest="quadros_por_segundo", type=int,
        default=QUADROS_POR_SEGUNDO, help="0 executa sem limite de velocidade",
    )
    argumentos.add_argument(
        "--quadros", "--frames", dest="quadros", type=int,
        help="encerra após esta quantidade de quadros",
    )
    argumentos.add_argument(
        "--captura", "--screenshot", dest="captura", type=Path,
        help="salva a tela ao encerrar",
    )
    argumentos.add_argument(
        "--sair-ao-vencer", "--exit-on-win", dest="sair_ao_vencer",
        action="store_true", help="encerra ao completar o tabuleiro",
    )
    opcoes = argumentos.parse_args()
    if opcoes.quadros_por_segundo < 0 or (opcoes.quadros is not None and opcoes.quadros < 1):
        argumentos.error("quadros por segundo deve ser >= 0 e quadros deve ser >= 1")

    pygame.init()
    try:
        tela = pygame.display.set_mode((LARGURA_TABULEIRO * TAMANHO_CELULA,
                                          ALTURA_TABULEIRO * TAMANHO_CELULA + 90))
        pygame.display.set_caption("Snake — A* em ação")
        fonte = pygame.font.Font(None, 24)
        relogio = pygame.time.Clock()
        jogo = CobraAutonoma(semente=opcoes.semente)
        pausado = False
        quadros = 0
        executando = True

        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        executando = False
                    elif evento.key == pygame.K_SPACE:
                        pausado = not pausado
                    elif evento.key == pygame.K_r:
                        jogo = CobraAutonoma(semente=opcoes.semente)
                        pausado = False
            if not executando:
                break
            if not jogo.venceu and not pausado:
                jogo.avancar()
            desenhar(tela, jogo, fonte)
            quadros += 1
            atingiu_limite = opcoes.quadros is not None and quadros >= opcoes.quadros
            encerra_com_vitoria = opcoes.sair_ao_vencer and jogo.venceu
            if atingiu_limite or encerra_com_vitoria:
                executando = False
            relogio.tick(opcoes.quadros_por_segundo)

        if opcoes.captura is not None:
            opcoes.captura.parent.mkdir(parents=True, exist_ok=True)
            # Redesenha antes de capturar: o buffer pode mudar após o flip.
            desenhar(tela, jogo, fonte, atualizar_tela=False)
            pygame.image.save(tela, str(opcoes.captura))
        print(f"Vitória: {jogo.venceu} | Comidas: {jogo.pontuacao} | Movimentos: {jogo.movimentos} "
              f"| A*: {jogo.movimentos_astar} | Reserva: {jogo.movimentos_reserva}")
    finally:
        pygame.quit()


if __name__ == "__main__":
    executar_jogo()
