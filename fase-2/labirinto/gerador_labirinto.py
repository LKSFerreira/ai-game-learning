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

# Reutilizamos o mx'x'esmo apelido de tipo para manter a consistência com o ambiente.
Posicao: TypeAlias = tuple[int, int]


# --- PENSAMENTO 1: A Função Principal (A Interface Pública) ---
# O que um usuário deste módulo precisa? Uma única função fácil de usar.
# Vamos chamá-la de `gerar_labirinto`. Ela precisa saber o tamanho do labirinto
# desejado (altura e largura das "células" de caminho) e deve retornar a matriz
# pronta para ser usada pela nossa classe `Labirinto`.
def gerar_labirinto(altura: int, largura: int) -> list[list[str]]:
    """
    Gera uma matriz de labirinto aleatório usando o algoritmo Recursive Backtracking.

    Args:
        altura (int): O número de células de caminho na vertical.
        largura (int): O número de células de caminho na horizontal.

    Returns:
        list[list[str]]: Uma matriz representando o labirinto, onde ' ' é
                         caminho e '#' é parede.
    """
    # --- PENSAMENTO 2: A Estrutura da Matriz ---
    # Um labirinto de, por exemplo, 5x5 células não pode ser representado por uma
    # matriz 5x5, pois precisamos de espaço para as paredes ENTRE as células.
    # Portanto, a matriz real precisa ser maior.
    # A fórmula é: tamanho_real = tamanho_celula * 2 + 1.
    # Ex: 5 células de largura -> 5*2+1 = 11 colunas na matriz.
    # C C C C C  -> # # # # # # # # # # #
    #                #P#P#P#P#P#
    #                # # # # # # # # # # #
    #                #P#P#P#P#P#
    #                ...
    altura_matriz = altura * 2 + 1
    largura_matriz = largura * 2 + 1

    # Começamos com um bloco sólido de paredes.
    matriz = [['#' for _ in range(largura_matriz)] for _ in range(altura_matriz)]

    # --- PENSAMENTO 3: O Ponto de Partida do "Escultor" ---
    # O algoritmo precisa começar a "cavar" de algum lugar. Vamos escolher uma
    # célula de início aleatória. Lembre-se que as células de caminho estão
    # sempre em coordenadas ímpares (1,1), (1,3), (3,1), etc.
    linha_inicial = random.randrange(1, altura_matriz, 2)
    coluna_inicial = random.randrange(1, largura_matriz, 2)

    # A primeira célula é marcada como um caminho.
    matriz[linha_inicial][coluna_inicial] = ' '

    # --- PENSAMENTO 4: A Lógica Recursiva (O Coração do Algoritmo) ---
    # Agora, chamamos a função auxiliar que fará todo o trabalho pesado de
    # forma recursiva. Delegar a complexidade para uma função interna mantém
    # a função principal limpa e fácil de entender.
    _percorrer_recursivamente(linha_inicial, coluna_inicial, matriz)

    return matriz


# --- PENSAMENTO 5: A Função Auxiliar Recursiva ---
# Esta é a função que implementa a "mágica". Ela visita uma célula, olha para
# os vizinhos não visitados, escolhe um aleatoriamente, derruba a parede no
# caminho e se chama recursivamente para o novo vizinho. Se não houver vizinhos
# para visitar, ela simplesmente retorna (o "backtracking").
def _percorrer_recursivamente(linha: int, coluna: int, matriz: list[list[str]]) -> None:
    """
    Função auxiliar que "esculpe" o labirinto recursivamente.

    A partir de uma célula atual, ela explora os vizinhos em uma ordem aleatória,
    derrubando paredes e visitando novas células até que não haja mais para onde ir.

    Args:
        linha (int): A linha da célula atual na matriz.
        coluna (int): A coluna da célula atual na matriz.
        matriz (list[list[str]]): A matriz do labirinto que está sendo modificada.
    """
    # Define as quatro direções possíveis (Norte, Sul, Leste, Oeste).
    # Cada tupla representa (mudança_na_linha, mudança_na_coluna).
    vizinhos = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    random.shuffle(vizinhos)  # A aleatoriedade é a chave para labirintos diferentes!

    for delta_linha, delta_coluna in vizinhos:
        nova_linha = linha + delta_linha
        nova_coluna = coluna + delta_coluna

        # Verifica se o vizinho está dentro dos limites da matriz.
        if 0 < nova_linha < len(matriz) and 0 < nova_coluna < len(matriz[0]):
            # E o mais importante: verifica se o vizinho ainda não foi visitado
            # (ou seja, se ainda é uma parede '#').
            if matriz[nova_linha][nova_coluna] == '#':
                # Se o vizinho é válido e não visitado, derrubamos a parede
                # que fica ENTRE a célula atual e o vizinho.
                parede_linha = linha + delta_linha // 2
                parede_coluna = coluna + delta_coluna // 2
                matriz[parede_linha][parede_coluna] = ' '

                # E também marcamos o vizinho como um caminho visitado.
                matriz[nova_linha][nova_coluna] = ' '

                # Agora, o passo recursivo: chamamos a mesma função para o vizinho.
                # A exploração continua a partir deste novo ponto.
                _percorrer_recursivamente(nova_linha, nova_coluna, matriz)


# --- PENSAMENTO 6: Teste Rápido e Demonstração ---
# Para garantir que nosso gerador funciona, adicionamos um bloco de execução
# que nos permite rodar este arquivo diretamente e ver um labirinto sendo
# impresso no terminal.
if __name__ == '__main__':
    print("--- Gerando um Labirinto de Exemplo (10x15) ---")
    try:
        # Define o tamanho do labirinto em termos de "células de caminho".
        altura_celulas = 10
        largura_celulas = 15

        labirinto_gerado = gerar_labirinto(altura_celulas, largura_celulas)

        # Imprime a matriz gerada de forma legível.
        for linha_matriz in labirinto_gerado:
            # O 'join' junta todos os caracteres da linha em uma única string.
            print(" ".join(linha_matriz))

        print(f"\nLabirinto gerado com sucesso!")
        print(f"Dimensões da matriz: {len(labirinto_gerado)} linhas x {len(labirinto_gerado[0])} colunas.")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar o labirinto: {e}")