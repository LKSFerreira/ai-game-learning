"""
Testes unitários para a classe Labirinto do módulo ambiente.

Este arquivo verifica se o ambiente do labirinto se comporta como esperado,
incluindo a inicialização, movimentação do agente, detecção de colisões,
cálculo de recompensas, reinício do ambiente e suporte a teclas WASD.
"""

import pytest
from ..ambiente import Labirinto

# --- DADOS DE TESTE ---
# É uma boa prática definir os dados que serão usados em múltiplos testes
# como constantes no início do arquivo. Isso evita repetição de código.
LABIRINTO_EXEMPLO = [
    [' ', '#', ' '],
    [' ', ' ', ' '],
    ['#', '#', ' ']
]
PONTO_INICIAL_EXEMPLO = (0, 0)
PONTO_FINAL_EXEMPLO = (2, 2)


# ========================================
# TESTES DE INICIALIZAÇÃO
# ========================================

def test_inicializacao_labirinto() -> None:
    """
    Verifica se o labirinto é inicializado com os valores corretos.

    É como testar se a dungeon foi criada corretamente no Ragnarok,
    com o jogador no lugar certo e a saída bem definida.
    """
    # Arrange: Prepara os dados para o teste (já definidos como constantes).
    # Act: Cria uma instância da classe.
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Assert: Verifica se os atributos foram definidos corretamente.
    assert ambiente.posicao_agente == PONTO_INICIAL_EXEMPLO, "A posição inicial do agente está incorreta."
    assert ambiente.estado_inicial == PONTO_INICIAL_EXEMPLO, "O estado inicial não foi guardado corretamente."
    assert ambiente.ponto_final == PONTO_FINAL_EXEMPLO, "O ponto final não foi guardado corretamente."


def test_inicializacao_matriz_vazia() -> None:
    """Verifica se lança erro para matriz vazia."""
    with pytest.raises(ValueError, match="A matriz do labirinto não pode estar vazia"):
        Labirinto([], PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)


def test_inicializacao_matriz_malformada() -> None:
    """Verifica se lança erro para matriz malformada."""
    with pytest.raises(ValueError, match="A matriz do labirinto está malformada"):
        Labirinto([[]], PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)


# ========================================
# TESTES DE REINICIALIZAÇÃO
# ========================================

def test_reiniciar_ambiente() -> None:
    """
    Verifica se o método reiniciar coloca o agente de volta no início.

    É como testar o botão de "respawn" no Ragnarok.
    """
    # Arrange: Cria um ambiente e move o agente para uma nova posição.
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)
    ambiente.executar_acao("baixo")  # Move o agente para (1, 0)

    # Act: Chama o método que queremos testar.
    posicao_apos_reinicio = ambiente.reiniciar()

    # Assert: Verifica se a posição do agente e o valor retornado estão corretos.
    assert ambiente.posicao_agente == PONTO_INICIAL_EXEMPLO, "A posição do agente não foi resetada."
    assert posicao_apos_reinicio == PONTO_INICIAL_EXEMPLO, "O método não retornou a posição inicial."


# ========================================
# TESTES DE EXECUÇÃO DE AÇÕES (NOMES COMPLETOS)
# ========================================

def test_executar_acao_valida() -> None:
    """Testa um movimento válido usando nome completo."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act
    novo_estado, recompensa, terminou = ambiente.executar_acao("baixo")

    # Assert
    posicao_esperada = (1, 0)
    recompensa_esperada = -0.1
    assert novo_estado == posicao_esperada, f"O agente deveria estar em {posicao_esperada}."
    assert ambiente.posicao_agente == posicao_esperada, "A posição interna do agente não foi atualizada."
    assert recompensa == recompensa_esperada, f"A recompensa deveria ser {recompensa_esperada}."
    assert not terminou, "O episódio não deveria ter terminado."


def test_executar_acao_invalida_parede() -> None:
    """Testa uma colisão com uma parede usando nome completo."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act: Tenta mover para a direita, onde há uma parede ('#') em (0, 1).
    novo_estado, recompensa, terminou = ambiente.executar_acao("direita")

    # Assert: A posição do agente não deve mudar.
    assert novo_estado == PONTO_INICIAL_EXEMPLO, "O agente não deveria ter se movido."
    assert ambiente.posicao_agente == PONTO_INICIAL_EXEMPLO, "A posição interna do agente mudou incorretamente."
    assert recompensa == -0.1, "A penalidade de passo deve ser aplicada mesmo em colisões."
    assert not terminou, "O episódio não deveria ter terminado."


def test_executar_acao_fora_dos_limites() -> None:
    """Testa movimento para fora dos limites."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act: Tenta mover para cima, saindo dos limites
    novo_estado, recompensa, terminou = ambiente.executar_acao("cima")

    # Assert: A posição do agente não deve mudar.
    assert novo_estado == PONTO_INICIAL_EXEMPLO, "O agente não deveria ter se movido."
    assert recompensa == -0.1, "A penalidade deve ser aplicada."
    assert not terminou, "O episódio não deveria ter terminado."


# ========================================
# TESTES DE EXECUÇÃO DE AÇÕES (TECLAS WASD)
# ========================================

def test_executar_acao_tecla_S_maiuscula() -> None:
    """Testa movimento usando tecla 'S' maiúscula."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act
    novo_estado, recompensa, terminou = ambiente.executar_acao("S")

    # Assert
    posicao_esperada = (1, 0)
    assert novo_estado == posicao_esperada, f"O agente deveria estar em {posicao_esperada}."
    assert recompensa == -0.1
    assert not terminou


def test_executar_acao_tecla_s_minuscula() -> None:
    """Testa movimento usando tecla 's' minúscula."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act
    novo_estado, recompensa, terminou = ambiente.executar_acao("s")

    # Assert
    posicao_esperada = (1, 0)
    assert novo_estado == posicao_esperada
    assert not terminou


def test_executar_acao_tecla_W_bloqueada() -> None:
    """Testa tecla 'W' (bloqueada por limite superior)."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act
    novo_estado, _, _ = ambiente.executar_acao("W")

    # Assert: Não deve mover
    assert novo_estado == PONTO_INICIAL_EXEMPLO


def test_executar_acao_tecla_D_bloqueada() -> None:
    """Testa tecla 'D' (bloqueada por parede)."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act
    novo_estado, _, _ = ambiente.executar_acao("D")

    # Assert: Não deve mover
    assert novo_estado == PONTO_INICIAL_EXEMPLO


def test_executar_acao_tecla_A_bloqueada() -> None:
    """Testa tecla 'A' (bloqueada por limite esquerdo)."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act
    novo_estado, _, _ = ambiente.executar_acao("A")

    # Assert: Não deve mover
    assert novo_estado == PONTO_INICIAL_EXEMPLO


def test_executar_acao_tecla_minuscula_w() -> None:
    """Testa tecla 'w' minúscula."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act
    novo_estado, _, _ = ambiente.executar_acao("w")

    # Assert
    assert novo_estado == PONTO_INICIAL_EXEMPLO  # Bloqueado por limite


# ========================================
# TESTES DE VALIDAÇÃO DE AÇÕES
# ========================================

def test_acao_invalida_lanca_erro() -> None:
    """Verifica se ações inválidas lançam ValueError."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act & Assert
    with pytest.raises(ValueError, match='Ação inválida: "X"'):
        ambiente.executar_acao("X")


def test_acao_vazia_lanca_erro() -> None:
    """Verifica se string vazia lança erro."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act & Assert
    with pytest.raises(ValueError, match='Ação inválida'):
        ambiente.executar_acao("")


# ========================================
# TESTES DE CHEGADA AO PONTO FINAL
# ========================================

def test_chegar_ao_ponto_final() -> None:
    """Testa se o ambiente reconhece a chegada ao ponto final usando nome completo."""
    # Arrange: Colocamos o agente em uma posição adjacente à saída.
    posicao_pre_final = (1, 2)
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)
    ambiente.posicao_agente = posicao_pre_final  # Forçamos a posição para o teste

    # Act: Executa o movimento que leva à saída.
    novo_estado, recompensa, terminou = ambiente.executar_acao("baixo")

    # Assert
    recompensa_esperada = 10.0 * (len(LABIRINTO_EXEMPLO) * len(LABIRINTO_EXEMPLO[0]))
    assert novo_estado == PONTO_FINAL_EXEMPLO, "O agente deveria ter chegado ao ponto final."
    assert recompensa == recompensa_esperada, f"A recompensa final deveria ser {recompensa_esperada}."
    assert terminou, "O episódio deveria ter terminado ao chegar na saída."


def test_chegar_ao_ponto_final_usando_wasd() -> None:
    """Testa chegada ao ponto final usando tecla WASD."""
    # Arrange
    posicao_pre_final = (1, 2)
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)
    ambiente.posicao_agente = posicao_pre_final

    # Act: Usa tecla 'S' para mover para baixo
    novo_estado, recompensa, terminou = ambiente.executar_acao("S")

    # Assert
    assert novo_estado == PONTO_FINAL_EXEMPLO
    assert recompensa == 10.0 * (len(LABIRINTO_EXEMPLO) * len(LABIRINTO_EXEMPLO[0]))
    assert terminou


# ========================================
# TESTES DE REPRESENTAÇÃO VISUAL
# ========================================

def test_representacao_string() -> None:
    """Testa a representação em string do labirinto."""
    # Arrange
    ambiente = Labirinto(LABIRINTO_EXEMPLO, PONTO_INICIAL_EXEMPLO, PONTO_FINAL_EXEMPLO)

    # Act
    representacao = str(ambiente)

    # Assert: Verifica se contém os marcadores esperados
    assert 'A' in representacao, "Deve conter o marcador do agente."
    assert 'S' in representacao, "Deve conter o marcador da saída."
    assert '#' in representacao, "Deve conter paredes."
