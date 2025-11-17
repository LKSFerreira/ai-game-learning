# fase_2/labirinto/test/test_gerador_labirinto.py

"""
Testes unitários para o módulo gerador_labirinto.

Este arquivo verifica se a função `gerar_labirinto` produz matrizes
válidas e consistentes, garantindo que as propriedades fundamentais de um
labirinto sejam sempre respeitadas.
"""

import pytest
from ..gerador_labirinto import gerar_labirinto

# ========================================
# TESTES DE DIMENSÕES E ESTRUTURA
# ========================================

def test_dimensoes_da_matriz_gerada() -> None:
    """
    Verifica se a matriz gerada tem as dimensões corretas.

    A fórmula para o tamanho real da matriz é (tamanho_celula * 2 + 1).
    Este teste garante que essa fórmula seja sempre aplicada corretamente.
    """
    # Arrange: Define os tamanhos de células desejados.
    altura_celulas, largura_celulas = 5, 10
    altura_esperada = altura_celulas * 2 + 1  # 11
    largura_esperada = largura_celulas * 2 + 1  # 21

    # Act: Gera o labirinto.
    matriz = gerar_labirinto(altura_celulas, largura_celulas)

    # Assert: Verifica as dimensões.
    assert len(matriz) == altura_esperada, "A altura da matriz gerada está incorreta."
    assert len(matriz[0]) == largura_esperada, "A largura da matriz gerada está incorreta."


@pytest.mark.parametrize(
    "altura_celulas, largura_celulas",
    [
        (1, 1),      # Labirinto mínimo
        (2, 2),      # Pequeno e quadrado
        (10, 3),     # Alto e estreito
        (3, 10),     # Baixo e largo
        (20, 20),    # Grande
    ]
)
def test_dimensoes_parametrizadas(altura_celulas: int, largura_celulas: int) -> None:
    """
    Testa as dimensões para uma variedade de tamanhos usando parametrização.
    Isso aumenta a confiança de que a lógica funciona para casos diferentes.
    """
    # Arrange
    altura_esperada = altura_celulas * 2 + 1
    largura_esperada = largura_celulas * 2 + 1

    # Act
    matriz = gerar_labirinto(altura_celulas, largura_celulas)

    # Assert
    assert len(matriz) == altura_esperada
    assert len(matriz[0]) == largura_esperada


# ========================================
# TESTES DAS PROPRIEDADES DO LABIRINTO
# ========================================

def test_bordas_sao_sempre_paredes() -> None:
    """
    Verifica se a moldura externa do labirinto é sempre composta por paredes ('#').
    Um labirinto válido nunca deve ter uma entrada ou saída nas bordas externas.
    """
    # Arrange
    matriz = gerar_labirinto(5, 5)
    num_linhas = len(matriz)
    num_colunas = len(matriz[0])

    # Act & Assert
    # Verifica a primeira e a última linha
    for coluna in range(num_colunas):
        assert matriz[0][coluna] == '#', f"Borda superior deve ser parede na coluna {coluna}."
        assert matriz[num_linhas - 1][coluna] == '#', f"Borda inferior deve ser parede na coluna {coluna}."

    # Verifica a primeira e a última coluna
    for linha in range(num_linhas):
        assert matriz[linha][0] == '#', f"Borda esquerda deve ser parede na linha {linha}."
        assert matriz[linha][num_colunas - 1] == '#', f"Borda direita deve ser parede na linha {linha}."


def test_celulas_de_caminho_sao_validas() -> None:
    """
    Verifica se todas as células que deveriam ser caminhos (' ') ou paredes
    internas ('#') estão corretas.

    Garante que o algoritmo não gerou caracteres estranhos e que as posições
    de "cruzamento" (coordenadas par, par) são sempre paredes.
    """
    # Arrange
    matriz = gerar_labirinto(4, 4)

    # Act & Assert
    for i, linha in enumerate(matriz):
        for j, celula in enumerate(linha):
            # Células de caminho (ímpar, ímpar) devem ser ' '
            if i % 2 == 1 and j % 2 == 1:
                assert celula == ' ', f"Célula de caminho em ({i},{j}) deveria ser ' '."
            # Cruzamentos de paredes (par, par) devem ser '#'
            elif i % 2 == 0 and j % 2 == 0:
                assert celula == '#', f"Cruzamento em ({i},{j}) deveria ser uma parede."
            # O restante (paredes entre caminhos) pode ser ' ' ou '#'
            else:
                assert celula in (' ', '#'), f"Caractere inválido '{celula}' em ({i},{j})."


def test_labirinto_eh_totalmente_conectado() -> None:
    """
    Verifica a propriedade mais importante: se todas as células de caminho
    são alcançáveis a partir de um ponto de partida.

    Isso confirma que o labirinto não tem áreas isoladas. Usamos um algoritmo
    de busca (Flood Fill) para fazer essa verificação.
    """
    # Arrange
    altura_celulas, largura_celulas = 8, 8
    matriz = gerar_labirinto(altura_celulas, largura_celulas)
    
    # Pega todas as posições que deveriam ser caminhos
    posicoes_de_caminho = set()
    for i in range(1, altura_celulas * 2, 2):
        for j in range(1, largura_celulas * 2, 2):
            posicoes_de_caminho.add((i, j))

    # Act: Realiza a busca a partir do canto (1, 1)
    visitados = set()
    pilha = [(1, 1)]  # Começa a busca a partir do primeiro caminho

    while pilha:
        linha, coluna = pilha.pop()
        if (linha, coluna) not in visitados:
            visitados.add((linha, coluna))

            # Adiciona vizinhos válidos (caminhos ' ') à pilha
            for dl, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nl, nc = linha + dl, coluna + dc
                if 0 <= nl < len(matriz) and 0 <= nc < len(matriz[0]) and matriz[nl][nc] == ' ':
                    pilha.append((nl, nc))
    
    # Filtra o conjunto de visitados para conter apenas as células principais
    caminhos_alcancados = {pos for pos in visitados if pos in posicoes_de_caminho}

    # Assert
    assert caminhos_alcancados == posicoes_de_caminho, \
        "Nem todas as células de caminho são alcançáveis. O labirinto está quebrado."


# ========================================
# TESTES DE CASOS EXTREMOS (EDGE CASES)
# ========================================

def test_gerar_labirinto_tamanho_minimo() -> None:
    """
    Testa o menor labirinto possível (1x1).
    O resultado deve ser uma matriz 3x3 com um único caminho no centro.
    """
    # Arrange
    labirinto_esperado = [
        ['#', '#', '#'],
        ['#', ' ', '#'],
        ['#', '#', '#']
    ]
    # Act
    matriz = gerar_labirinto(1, 1)
    # Assert
    assert matriz == labirinto_esperado, "O labirinto de tamanho mínimo (1x1) não foi gerado corretamente."