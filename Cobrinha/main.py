import pygame
import numpy as np
from cobrinha import Snake
from comida import Comida
import a
import manipulacaoMatriz as mm


pygame.init()

exec = True

#CONFIGURAÇÔES DE TELA
DISPLAY_SIZE = (390, 390)
display = pygame.display.set_mode(DISPLAY_SIZE)

#MATRIZ
TAMANHO_PIXEL = 15
TAMANHO_X_GRID = int(DISPLAY_SIZE[0]/TAMANHO_PIXEL)
TAMANHO_Y_GRID = int(DISPLAY_SIZE[1]/TAMANHO_PIXEL)
matriz = np.zeros((TAMANHO_Y_GRID, TAMANHO_X_GRID))

#POSICOES INICIAIS
pos_x = 15
pos_y = 15
direcao = 0

#TEMPO DO JOGO
tick = pygame.time.Clock()

#RECEBER TODAS AS POSICOES POSSIVEIS PARA COMIDA
def plotarTabuleiro(tela, x, y, tamanhoPixel, caminho):
  for i in range(x):
    for j in range(y):
      cor = 0,0,0
      if (i,j) in caminho:
        cor = 230, 70, 0
      pygame.draw.rect(tela, cor, (i*tamanhoPixel, j*tamanhoPixel, tamanhoPixel, tamanhoPixel), 1)


def main():

  snake = Snake(pos_x, pos_y, direcao, TAMANHO_PIXEL)
  comida = Comida(mm.posicoesPossiveis(matriz), TAMANHO_PIXEL)

  caminho = a.AEstrela(matriz, snake.pos_matriz, comida.pos_matriz)
  caminho_cobra = caminho.calcCaminho(snake.cauda)

  while exec:
    tick.tick(20)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()

    display.fill((50,60,60))

    #MOVIMENTACAO DA COBRA
    # snake.pos_matriz = caminho_cobra.pop(snake.pos_matriz)

    snake.pos_matriz = caminho_cobra.pop(snake.pos_matriz)
    snake.atualizarPosicao(False)

    # snake.movimentacao()





    #GERAR COMIDA
    if snake.pos_matriz == comida.pos_matriz:
      comida = Comida(mm.posicoesPossiveis(matriz), TAMANHO_PIXEL)
      snake.tamanho += 1
      caminho = a.AEstrela(matriz, snake.pos_matriz, comida.pos_matriz)
      caminho_cobra = caminho.calcCaminho(snake.cauda)

    #ATUALIZAR POSICAO DA CAUDA
    if snake.tamanho > len(snake.cauda):
      snake.cauda.append((int(snake.pos_matriz[0]), int(snake.pos_matriz[1])))

    if len(snake.cauda) >= snake.tamanho:
      mm.setElementoMatriz(matriz, snake.cauda.pop(0), 0)

    #COBRA BATEU NO PROPRIO CORPO
    if len(snake.cauda) != len(set(snake.cauda)):
      quit()




    plotarTabuleiro(display, TAMANHO_X_GRID, TAMANHO_Y_GRID, TAMANHO_PIXEL, caminho_cobra)
    comida.desenhar(display, TAMANHO_PIXEL)
    snake.desenhar(matriz, display)
    pygame.display.flip()

if __name__ == "__main__":
  main()
