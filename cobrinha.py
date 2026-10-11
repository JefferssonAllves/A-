from pygame.key import get_pressed
from pygame import K_w, K_s, K_a, K_d
import manipulacaoMatriz as mm
from pygame.draw import rect

class Snake():
  def __init__(self, pos_x_matriz, pos_y_matriz, direcao, tamanho_pixel):
    self.TAMANHO_PIXEL = tamanho_pixel
    self.pos_x_matriz = pos_x_matriz
    self.pos_y_matriz = pos_y_matriz
    self.pos_matriz = (self.pos_x_matriz, self.pos_y_matriz)
    self.pos_x = self.pos_x_matriz * self.TAMANHO_PIXEL
    self.pos_y = self.pos_y_matriz * self.TAMANHO_PIXEL
    self.direcao = direcao
    self.tamanho = 3
    self.cauda = [(self.pos_x_matriz, self.pos_y_matriz)]


  def movimentacao(self):
    if get_pressed()[K_w] and self.direcao != 1:
      self.direcao = 0
    elif get_pressed()[K_s] and self.direcao != 0:
      self.direcao = 1
    elif get_pressed()[K_a] and self.direcao != 3:
      self.direcao = 2
    elif get_pressed()[K_d] and self.direcao != 2:
      self.direcao = 3

  def atualizarPosicao(self, player=True):
    if player:
      if self.direcao == 0:
        self.pos_y -= self.TAMANHO_PIXEL
      elif self.direcao == 1:
        self.pos_y += self.TAMANHO_PIXEL
      elif self.direcao == 2:
        self.pos_x -= self.TAMANHO_PIXEL
      elif self.direcao == 3:
        self.pos_x += self.TAMANHO_PIXEL

      self.pos_matriz = (int(self.pos_x / self.TAMANHO_PIXEL), int(self.pos_y / self.TAMANHO_PIXEL))
    else:
      self.pos_x = self.pos_matriz[0] * self.TAMANHO_PIXEL
      self.pos_y = self.pos_matriz[1] * self.TAMANHO_PIXEL

  def desenhar(self, matriz, display):
    rect(display, (0, 255, 0), (self.pos_x, self.pos_y, self.TAMANHO_PIXEL, self.TAMANHO_PIXEL), 0)
    cor = 0
    degrade = 255 / len(self.cauda)
    for posicao in self.cauda:
      mm.setElementoMatriz(matriz, posicao, 1)
      rect(display, (0, cor, 0), (posicao[0] * self.TAMANHO_PIXEL, posicao[1] * self.TAMANHO_PIXEL, self.TAMANHO_PIXEL, self.TAMANHO_PIXEL), 0)
      rect(display, (0, 80, 0), (posicao[0] * self.TAMANHO_PIXEL, posicao[1] * self.TAMANHO_PIXEL, self.TAMANHO_PIXEL, self.TAMANHO_PIXEL), 1)
      cor += degrade