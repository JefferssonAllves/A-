from random import choice
from pygame.draw import rect

class Comida():
  def __init__(self, posicoes_possiveis, tamanho_pixel):
    posicao = choice(posicoes_possiveis)
    self.pos_matriz = (posicao[0], posicao[1])
    self.pos_x = posicao[0] * tamanho_pixel
    self.pos_y = posicao[1] * tamanho_pixel

  def desenhar(self, display, TAMANHO_PIXEL):
    rect(display, (200,0,0), (self.pos_x, self.pos_y, TAMANHO_PIXEL, TAMANHO_PIXEL), 0)
    rect(display, (200, 70, 0), (self.pos_x, self.pos_y, TAMANHO_PIXEL, TAMANHO_PIXEL), 1)