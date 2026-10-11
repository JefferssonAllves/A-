# Snake com A*

A cobra joga sozinha. A linha azul mostra a rota calculada até a comida.
O rodapé informa quantos movimentos usaram A* e quantos usaram a reserva segura.

## Executar

```sh
git clone https://github.com/JefferssonAllves/A-.git
cd A-
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
venv/bin/python main.py
```

Espaço pausa, R reinicia e Esc fecha. Use `--semente 7` para repetir uma partida
ou `--quadros-por-segundo 60` para mudar a velocidade.

## Como o código funciona

- `a.py`: A* com fila de prioridade e distância Manhattan. Respeita obstáculos
  e retorna uma lista ordenada de posições, inclusive início e destino.
- `snake_game.py`: corpo, comida e regras. Recalcula A* a cada passo porque o
  corpo muda. Só permite primeiros passos que preservem a ordem do ciclo
  Hamiltoniano. Sem rota, avança no ciclo para liberar espaço.
- `main.py`: janela, desenho e teclado, separados da busca.
- `test_snake_game.py`: caminhos, colisões e partidas completas.

O A* encontra o menor caminho na grade recebida, com as restrições do primeiro
passo. O jogo combina essa busca com segurança Hamiltoniana; não promete o
menor número total de movimentos numa partida. A rota desenhada é uma previsão,
pois considera o corpo atual. O jogo padrão é 16×16, sem paredes fixas.
O motor exige dimensões >= 2 e ao menos uma dimensão par.

A pasta `Cobrinha/` preserva a versão antiga e não é usada pelo novo jogo.

## Verificar

```sh
venv/bin/python -m unittest -v test_snake_game test_main
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy venv/bin/python main.py --seed 7 --fps 0 --frames 30000 --exit-on-win --screenshot resultados/vitoria.png
```

O segundo comando executa e desenha uma partida usando vídeo virtual e salva
sua tela final. Sem as variáveis SDL, o jogo abre uma janela normal.

## Resultado verificado

Em 11/10/2026, os 12 testes de busca, regras e teclado passaram no ambiente virtual.
O Pygame foi recompilado para corrigir o carregamento das fontes.
A janela real também foi verificada nesse ambiente por 120 quadros.
A busca também foi comparada com BFS em 100 grades aleatórias.
Na validação local, 35 partidas em quatro tamanhos de tabuleiro terminaram em vitória.
Uma partida adicional, seed 7, foi renderizada tanto em janela real quanto com
vídeo virtual: 253 comidas, 17.443 movimentos, 5.944 passos por A* e 11.499
pela reserva segura. O comando da seção anterior permite gerar uma nova
imagem da tela final.

## Material para o LinkedIn

Foram preparados seis prints comentados e um vídeo de 24 segundos mostrando
a expansão real da busca, o desvio pelo corpo e a reserva segura.
Esse material e seus scripts de geração são mantidos localmente e não
integram este repositório.

## Leitura do código em português

O código atual usa nomes em português, inclusive os testes.
Os nomes oficiais de Python, Pygame e outras bibliotecas seguem
as APIs dessas ferramentas.

Comece por `a.py`: `encontrar_caminho` mantém a `fila_prioridades`, os `custos`
e as posições `anteriores`. Depois, leia `snake_game.py`: `CobraAutonoma`
consulta os `movimentos_seguros`, escolhe o caminho e libera a cauda ao andar.
`main.py` contém `desenhar` e `executar_jogo`, responsáveis pela janela.

```python
from snake_game import CobraAutonoma

jogo = CobraAutonoma(semente=7)
jogo.avancar()            # Executa um movimento.
print(jogo.cabeca)        # Posição da cabeça após esse movimento.
print(jogo.corpo)         # Cabeça no início; cauda no fim.
```

Os argumentos também têm nomes em português:

```sh
venv/bin/python main.py --semente 7 --quadros-por-segundo 30
```

As formas anteriores (`--seed`, `--fps`, `--frames`, `--screenshot` e
`--exit-on-win`) continuam aceitas.
