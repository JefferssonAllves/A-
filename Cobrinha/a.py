from queue import PriorityQueue
import manipulacaoMatriz as mm

class AEstrela():
  def __init__(self, matriz, posicao, comida):
    self.matriz = matriz
    self.MAX_ITER = 50000
    self.f_score = self.dicAEstrela(matriz)
    self.g_score = {}
    self.g_score[posicao] = 0


    self.posicao_inicial = posicao
    self.comida = comida

    self.f_score[self.posicao_inicial] = self.g_score[posicao] + self.h_score(self.posicao_inicial, self.comida)

    self.fila = PriorityQueue()
    self.fila.put((self.f_score[self.posicao_inicial], self.h_score(self.posicao_inicial, self.comida), self.posicao_inicial))


    self.caminho = {}

  def dicAEstrela(self, matriz):
    f_secore = {}
    for linha in range(len(matriz)):
      for coluna in range(len(matriz[linha])):
        f_secore[(linha,coluna)] = float("inf")
    return f_secore

  def h_score(self, posicaoAtual, posicaoComida):
    return abs(posicaoAtual[0] - posicaoComida[0]) + abs(posicaoAtual[1] - posicaoComida[1])

  def posicoes_possiveis(self, matriz, posicao):
    coluna, linha = posicao

    linhas = len(self.matriz)
    colunas = len(self.matriz[0])

    return [
      int(matriz[linha-1][coluna]) if linha > 0 else 1,           # cima
      int(matriz[linha+1][coluna]) if linha < linhas - 1 else 1,  # baixo
      int(matriz[linha][coluna-1]) if coluna > 0 else 1,          # esquerda
      int(matriz[linha][coluna+1]) if coluna < colunas - 1 else 1 # direita
    ]

  def calcCaminho(self, cauda_inicial):
    iteracoes = 0

    fila = PriorityQueue()

    # estado inicial
    estado_inicial = (self.posicao_inicial, tuple(cauda_inicial))
    fila.put((0 + self.h_score(self.posicao_inicial, self.comida),self.h_score(self.posicao_inicial, self.comida),self.posicao_inicial,tuple(cauda_inicial)))

    visitados = set()
    g_score = {estado_inicial: 0}
    caminho = {}

    linhas = len(self.matriz)
    colunas = len(self.matriz[0])

    while not fila.empty():
      _, _, posicao, cauda = fila.get()

      estado = (posicao, cauda)

      if estado in visitados:
          continue

      visitados.add(estado)

      if posicao == self.comida:
          # reconstruir caminho
          caminho_final = {}
          atual = estado

          while atual in caminho:
            pos, _ = atual
            anterior = caminho[atual]
            caminho_final[anterior[0]] = pos
            atual = anterior

          return caminho_final

      coluna, linha = posicao

      # movimentos (cima, baixo, esquerda, direita)
      movimentos = [
        (coluna, linha - 1),
        (coluna, linha + 1),
        (coluna - 1, linha),
        (coluna + 1, linha),
      ]

      for nova_pos in movimentos:

        # dentro dos limites
        if not (0 <= nova_pos[0] < colunas and 0 <= nova_pos[1] < linhas):
          continue

        # simular nova cauda
        nova_cauda = list(cauda)

        if len(nova_cauda) > 0:
          nova_cauda.pop(0)

        nova_cauda.append(nova_pos)

        nova_cauda_tuple = tuple(nova_cauda)
        novo_estado = (nova_pos, nova_cauda_tuple)

        # colisão com o corpo (usando cauda, não matriz)
        if nova_pos in cauda:
          continue

        novo_g = g_score[estado] + 1

        if novo_estado not in g_score or novo_g < g_score[novo_estado]:
          g_score[novo_estado] = novo_g

          h = self.h_score(nova_pos, self.comida)
          f = novo_g + h

          fila.put((f, h, nova_pos, nova_cauda_tuple))
          caminho[novo_estado] = estado

    return {}  
