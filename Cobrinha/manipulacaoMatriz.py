from numpy import where

def posicoesPossiveis(matriz):
  matriz_zeros = where(matriz == 0)
  posicoes_possiveis = []
  for i in range(len(matriz_zeros[0])):
    posicoes_possiveis.append((int(matriz_zeros[1][i]), int(matriz_zeros[0][i])))
  return posicoes_possiveis

def setElementoMatriz(matriz, posicao, valor):
  try:
    matriz[posicao[1], posicao[0]] = valor
  except:
    print("VALOR ACIMA DA MATRIZ")

def printMatriz(matriz):
  for linha in matriz:
    for elemento in linha:
      print(int(elemento), end=", ")
    print()
  print()
