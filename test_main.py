"""Verifica os controles na interface real com um vídeo virtual."""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import sys
import unittest
from unittest.mock import patch
import pygame
import main
from snake_game import CobraAutonoma


class TestesDaInterface(unittest.TestCase):
    def simular_eventos(self, lotes_eventos):
        jogos = []

        def criar_jogo(*parametros_posicionais, **parametros_nomeados):
            jogo = CobraAutonoma(*parametros_posicionais, **parametros_nomeados)
            jogos.append(jogo)
            return jogo
        with patch.object(sys, "argv", ["main.py", "--fps", "0", "--frames", "8"]), \
             patch.object(main, "CobraAutonoma", side_effect=criar_jogo), \
             patch.object(pygame.event, "get", side_effect=lotes_eventos):
            main.executar_jogo()
        self.assertFalse(pygame.get_init())
        return jogos

    def test_pausar_continuar_e_sair(self):
        def pressionar_tecla(tecla):
            return pygame.event.Event(pygame.KEYDOWN, key=tecla)

        jogos = self.simular_eventos([
            [pressionar_tecla(pygame.K_SPACE)],
            [],
            [pressionar_tecla(pygame.K_SPACE)],
            [pressionar_tecla(pygame.K_ESCAPE)],
        ])
        self.assertEqual(jogos[0].movimentos, 1)

    def test_reiniciar_e_fechar(self):
        jogos = self.simular_eventos([
            [],
            [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)],
            [pygame.event.Event(pygame.QUIT)],
        ])
        self.assertEqual(len(jogos), 2)
        self.assertEqual([jogo.movimentos for jogo in jogos], [1, 1])


if __name__ == "__main__":
    unittest.main()
