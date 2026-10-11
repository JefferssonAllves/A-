import unittest
from collections import deque
from unittest.mock import patch

from a import encontrar_caminho

from snake_game import CobraAutonoma, criar_ciclo_hamiltoniano


class TestesDaCobra(unittest.TestCase):
    def test_ciclo_cobre_tabuleiro_com_passos_vizinhos(self):
        ciclo = criar_ciclo_hamiltoniano(16, 16)
        self.assertEqual(len(ciclo), 256)
        self.assertEqual(len(set(ciclo)), 256)
        for primeira, segunda in zip(ciclo, ciclo[1:] + ciclo[:1]):
            self.assertEqual(abs(primeira[0] - segunda[0]) + abs(primeira[1] - segunda[1]), 1)

    def test_cobra_vence_varias_partidas_sem_colisao(self):
        for semente in range(20):
            jogo = CobraAutonoma(8, 8, semente=semente)
            jogo.jogar_ate_vencer()
            self.assertTrue(jogo.venceu)
            self.assertEqual(len(jogo.corpo), jogo.capacidade)
            self.assertEqual(len(jogo.ocupadas), jogo.capacidade)


class TestesDoAEstrela(unittest.TestCase):
    def test_menor_caminho_contorna_parede(self):
        paredes = {(2, y) for y in range(4)}
        caminho = encontrar_caminho(5, 5, (0, 0), (4, 0), paredes)
        self.assertEqual(len(caminho) - 1, 12)
        self.assertEqual(caminho[0], (0, 0))
        self.assertEqual(caminho[-1], (4, 0))
        self.assertFalse(set(caminho) & paredes)
        for primeira, segunda in zip(caminho, caminho[1:]):
            self.assertEqual(abs(primeira[0]-segunda[0])+abs(primeira[1]-segunda[1]), 1)

    def test_astar_confere_com_bfs_em_100_tabuleiros(self):
        from random import Random
        sorteador = Random(2026)
        for caso in range(100):
            inicio, destino = (0, 0), (6, 5)
            paredes = {(x, y) for x in range(7) for y in range(6)
                     if (x, y) not in (inicio, destino) and sorteador.random() < 0.3}
            fila = deque([(inicio, 0)])
            visitadas = {inicio}
            menor_distancia = None
            while fila:
                posicao, custo = fila.popleft()
                if posicao == destino:
                    menor_distancia = custo
                    break
                x, y = posicao
                for proxima_posicao in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                    vizinha_x, vizinha_y = proxima_posicao
                    if 0 <= vizinha_x < 7 and 0 <= vizinha_y < 6 and proxima_posicao not in paredes | visitadas:
                        visitadas.add(proxima_posicao)
                        fila.append((proxima_posicao, custo + 1))
            caminho = encontrar_caminho(7, 6, inicio, destino, paredes)
            with self.subTest(caso=caso):
                self.assertEqual(len(caminho)-1 if caminho else None, menor_distancia)
                self.assertFalse(set(caminho) & paredes)

    def test_partidas_preservam_corpo_a_cada_passo(self):
        for semente in range(5):
            jogo = CobraAutonoma(16, 16, semente=semente)
            while not jogo.venceu and jogo.movimentos < 30000:
                cabeca_anterior = jogo.cabeca
                jogo.avancar()
                self.assertEqual(abs(jogo.cabeca[0]-cabeca_anterior[0])+abs(jogo.cabeca[1]-cabeca_anterior[1]), 1)
                self.assertEqual(len(jogo.corpo), len(set(jogo.corpo)))
                self.assertEqual(set(jogo.corpo), jogo.ocupadas)
                self.assertEqual(len(jogo.corpo), jogo.pontuacao + 3)
                self.assertTrue(all(0 <= x < 16 and 0 <= y < 16 for x, y in jogo.corpo))
            self.assertTrue(jogo.venceu)
            self.assertGreater(jogo.movimentos_astar, 0)

    def test_comida_sem_caminho(self):
        self.assertEqual(encontrar_caminho(3, 3, (0, 1), (2, 1), {(1, y) for y in range(3)}), [])

    def test_inicio_ja_e_destino(self):
        self.assertEqual(encontrar_caminho(3, 3, (1, 1), (1, 1), set()), [(1, 1)])

    def test_jogo_usa_astar(self):
        jogo = CobraAutonoma(8, 8, semente=1)
        with patch("snake_game.encontrar_caminho", wraps=encontrar_caminho) as busca:
            jogo.avancar()
            busca.assert_called_once()

    def test_cauda_libera_celula_quando_cobra_nao_cresce(self):
        jogo = CobraAutonoma(4, 2, semente=0)
        jogo.corpo = deque([(0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (1, 0)])
        jogo.ocupadas = set(jogo.corpo)
        jogo.comida = (3, 0)
        self.assertEqual(jogo.escolher_movimento(), (1, 0))
        jogo.avancar()
        self.assertEqual(len(jogo.corpo), len(jogo.ocupadas))

    def test_reserva_segura_quando_busca_nao_encontra_rota(self):
        jogo = CobraAutonoma(8, 8, semente=2)
        with patch("snake_game.encontrar_caminho", return_value=[]):
            movimento = jogo.escolher_movimento()
        self.assertTrue(jogo._movimento_seguro(movimento))


if __name__ == "__main__":
    unittest.main()
