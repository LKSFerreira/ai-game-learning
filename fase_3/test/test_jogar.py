# fase_3/test/test_jogar.py

import pytest
from unittest.mock import MagicMock
import pygame

# Note os pontos (..) para subir um nível e importar da fase_3
from ..jogar import JogoGrafico
from ..ambiente import Labirinto

# ========================================
# FIXTURE DO LABIRINTO (MOCKADO)
# ========================================


@pytest.fixture
def ambiente_mock() -> MagicMock:
    matriz = [['#', '#', '#'], ['#', ' ', '#'], ['#', '#', '#']]
    labirinto_real = Labirinto(matriz, (1, 1), (1, 1))
    return MagicMock(wraps=labirinto_real)

# ========================================
# TESTES DE JogoGrafico
# ========================================


def test_inicializacao_jogo_grafico(mocker, ambiente_mock: MagicMock) -> None:
    # Mock das funções principais do pygame
    mocker.patch('pygame.init')
    mocker.patch('pygame.display.set_mode')
    mocker.patch('pygame.display.set_caption')

    jogo = JogoGrafico(ambiente_mock, tamanho_celula=10)

    assert jogo.labirinto is ambiente_mock
    assert jogo.tamanho_celula == 10

    pygame.init.assert_called_once()
    pygame.display.set_mode.assert_called_once()
    pygame.display.set_caption.assert_called_once()


def test_processar_movimento_continuo(mocker, ambiente_mock: MagicMock) -> None:
    # Mock de init/display
    mocker.patch('pygame.init')
    mocker.patch('pygame.display.set_mode')
    mocker.patch('pygame.display.set_caption')

    # Mock do tempo para permitir movimento
    mocker.patch('pygame.time.get_ticks', return_value=200)

    # Mock das funções de evento
    mocker.patch('pygame.event.post')
    mocker.patch('pygame.event.Event', return_value="EVENTO_FAKE")
    mocker.patch('pygame.time.wait')

    # Mock do teclado pressionado
    teclado_falso = [False] * 512
    # Agora funciona porque importamos pygame lá em cima
    teclado_falso[pygame.K_w] = True
    mocker.patch('pygame.key.get_pressed', return_value=teclado_falso)

    # Instância do jogo
    jogo = JogoGrafico(ambiente_mock, tamanho_celula=10)
    jogo.ultimo_movimento = 0

    # Executa o método
    jogo.processar_movimento_continuo()

    # Verifica se a ação "W" foi chamada no ambiente
    # Nota: Verifique se seu código usa "W" maiúsculo ou minúsculo.
    # Se o teste falhar aqui, troque "W" por "w"
    ambiente_mock.executar_acao.assert_called_once_with("W")

    # O último movimento deve ter sido atualizado para o tempo atual (200)
    assert jogo.ultimo_movimento == 200
