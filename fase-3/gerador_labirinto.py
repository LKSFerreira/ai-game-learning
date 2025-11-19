# fase_2/labirinto/gerador_labirinto.py

"""
Módulo responsável por gerar labirintos aleatórios.

Utiliza o algoritmo "Recursive Backtracking" (Busca em Profundidade Recursiva)
para criar labirintos perfeitos, o que significa que sempre haverá um e
apenas um caminho entre quaisquer dois pontos do labirinto.

A função principal, `gerar_labirinto`, é a única que precisa ser chamada
de fora deste módulo.
"""

import random
from typing import TypeAlias

# Reutilizamos o mesmo apelido de tipo para manter a consistência com o ambiente.
Posicao: TypeAlias = tuple[int, int]


def gerar_labirinto(altura: int, largura: int, semente: int | None = None) -> list[list[str]]:
    """
    Gera uma matriz de labirinto aleatório usando o algoritmo Recursive Backtracking.

    Args:
        altura (int): O número de células de caminho na vertical.
        largura (int): O número de células de caminho na horizontal.
        semente (int | None): Semente para o gerador de números aleatórios. 
                              Se fornecido, o labirinto será sempre o mesmo para a mesma semente.

    Returns:
        list[list[str]]: Uma matriz representando o labirinto, onde ' ' é
                         caminho e '#' é parede.
    """
    # Instância local do gerador de números aleatórios para não afetar o global
    rng = random.Random(semente)

    # A fórmula é: tamanho_real = tamanho_celula * 2 + 1.
    altura_matriz = altura * 2 + 1
    largura_matriz = largura * 2 + 1

    # Começamos com um bloco sólido de paredes.
    matriz = [['#' for _ in range(largura_matriz)] for _ in range(altura_matriz)]

    # O algoritmo precisa começar a "cavar" de algum lugar.
    linha_inicial = rng.randrange(1, altura_matriz, 2)
    coluna_inicial = rng.randrange(1, largura_matriz, 2)

    # A primeira célula é marcada como um caminho.
    matriz[linha_inicial][coluna_inicial] = ' '

    # Chamamos a função auxiliar recursiva
    _percorrer_recursivamente(linha_inicial, coluna_inicial, matriz, rng)

    return matriz


def _percorrer_recursivamente(linha: int, coluna: int, matriz: list[list[str]], rng: random.Random) -> None:
    """
    Função auxiliar que "esculpe" o labirinto recursivamente.
    """
    # Define as quatro direções possíveis (Norte, Sul, Leste, Oeste).
    vizinhos = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    rng.shuffle(vizinhos)

    for delta_linha, delta_coluna in vizinhos:
        nova_linha = linha + delta_linha
        nova_coluna = coluna + delta_coluna

        # Verifica se o vizinho está dentro dos limites da matriz.
        if 0 < nova_linha < len(matriz) and 0 < nova_coluna < len(matriz[0]):
            # Verifica se o vizinho ainda não foi visitado (é parede)
            if matriz[nova_linha][nova_coluna] == '#':
                # Derruba a parede entre a célula atual e o vizinho
                parede_linha = linha + delta_linha // 2
                parede_coluna = coluna + delta_coluna // 2
                matriz[parede_linha][parede_coluna] = ' '

                # Marca o vizinho como caminho
                matriz[nova_linha][nova_coluna] = ' '

                # Recursão
                _percorrer_recursivamente(nova_linha, nova_coluna, matriz, rng)


if __name__ == '__main__':
    print("--- Gerando um Labirinto de Exemplo (10x10) ---")
    try:
        # Define o tamanho do labirinto em termos de "células de caminho".
        altura_celulas = 10
        largura_celulas = 10

        labirinto_gerado = gerar_labirinto(altura_celulas, largura_celulas)

        # Imprime a matriz gerada de forma legível.
        for linha_matriz in labirinto_gerado:
            print(" ".join(linha_matriz))

        print(f"\nLabirinto gerado com sucesso!")
        print(f"Dimensões da matriz: {len(labirinto_gerado)} linhas x {len(labirinto_gerado[0])} colunas.")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o labirinto: {e}")