# fase_2/labirinto/test/test_jogar.py

import pytest
import pygame
from unittest.mock import MagicMock

# Importa as classes e funções testadas
from ..jogar import JogoGrafico, calcular_dimensoes_ideais
from ..ambiente import Labirinto


# ========================================
# FIXTURE DO LABIRINTO (MOCKADO)
# ========================================

@pytest.fixture
def ambiente_mock() -> MagicMock:
    matriz = [['#','#','#'], ['#',' ','#'], ['#','#','#']]
    labirinto_real = Labirinto(matriz, (1,1), (1,1))
    return MagicMock(wraps=labirinto_real)


# ========================================
# TESTE DE DIMENSÕES
# ========================================

@pytest.mark.parametrize(
    "largura_tela, altura_tela, tamanho_celula, esperado",
    [
        (1920, 1080, 10, (30, 40)),
        (1000, 600, 10, (24, 40)),
        (800, 800, 10, (30, 34)),
        (400, 400, 10, (14, 14)),
    ]
)
def test_calcular_dimensoes_ideais(
    largura_tela: int, altura_tela: int, tamanho_celula: int, esperado: tuple[int, int]
) -> None:
    resultado = calcular_dimensoes_ideais(largura_tela, altura_tela, tamanho_celula)
    assert resultado == esperado


# ========================================
# TESTES DE JogoGrafico
# ========================================

def test_inicializacao_jogo_grafico(mocker, ambiente_mock: MagicMock) -> None:
    # Mock das funções principais do pygame
    mocker.patch('pygame.init')
    mocker.patch('pygame.display.set_mode')
    mocker.patch('pygame.display.set_caption')

    jogo = JogoGrafico(ambiente_mock, 10)

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

    # Mock das funções de evento que detonam quando não há display
    mocker.patch('pygame.event.post')
    mocker.patch('pygame.event.Event', return_value="EVENTO_FAKE")
    mocker.patch('pygame.time.wait')

    # Mock do teclado pressionado
    teclado_falso = [False] * 512
    teclado_falso[pygame.K_w] = True
    mocker.patch('pygame.key.get_pressed', return_value=teclado_falso)

    # Instância do jogo
    jogo = JogoGrafico(ambiente_mock, 10)
    jogo.ultimo_movimento = 0

    # Executa o método
    jogo.processar_movimento_continuo()

    ambiente_mock.executar_acao.assert_called_once_with("W")
    assert jogo.ultimo_movimento == 200
