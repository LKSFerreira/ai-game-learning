"""
Ponto de entrada para jogar o Labirinto manualmente.

Este é o "maestro" do jogo. Ele apenas orquestra as peças:
1. Gera o labirinto (com seed configurável)
2. Cria o ambiente
3. Chama a interface gráfica

Uso:
    python jogar.py                          -> Padrão (10x10, seed aleatória, célula 20px)
    
Para personalizar, edite os valores na chamada de main() no final do arquivo.
"""

import random
from .ambiente import Labirinto
from .gerador_labirinto import gerar_labirinto
from .jogo_grafico import JogoGrafico

# --- PENSAMENTO 1: Limites de Seeds ---
# Definimos o intervalo de seeds que será usado no treinamento da IA.
# 100 mapas é suficiente para dar variedade sem inviabilizar a Q-Table.
MIN_SEED = 1
MAX_SEED = 100


def jogar(
    seed: int | None = None,
    altura: int = 10,
    largura: int = 10,
    tamanho_celula: int = 20
) -> None:
    """
    Inicia o jogo do Labirinto com as configurações fornecidas.
    
    Args:
        seed (int | None): Número da seed para gerar o mapa. Se None, será aleatória.
        altura (int): Número de células de altura do labirinto. Padrão: 10.
        largura (int): Número de células de largura do labirinto. Padrão: 10.
        tamanho_celula (int): Tamanho em pixels de cada célula. Padrão: 20.
    """
    # --- PENSAMENTO 2: Definição da Seed ---
    # Se não foi fornecida uma seed, sorteamos uma dentro do intervalo permitido.
    if seed is None:
        seed = random.randint(MIN_SEED, MAX_SEED)
        print(f"🎲 Seed aleatória sorteada: {seed}")
    else:
        print(f"🗺️  Carregando Mapa {seed}...")

    # --- PENSAMENTO 3: Validação da Seed ---
    # Avisamos se a seed está fora do intervalo de treinamento.
    if not (MIN_SEED <= seed <= MAX_SEED):
        print(
            f"⚠️  Aviso: Seed {seed} fora do intervalo de treinamento "
            f"({MIN_SEED}-{MAX_SEED})."
        )

    # --- PENSAMENTO 4: Geração do Labirinto ---
    matriz = gerar_labirinto(altura, largura, semente=seed)

    # --- PENSAMENTO 5: Definição dos Pontos Inicial e Final ---
    # O gerador usa coordenadas ímpares para caminhos, então (1,1) é sempre válido.
    ponto_inicial = (1, 1)
    ponto_final = (altura * 2 - 1, largura * 2 - 1)

    # --- PENSAMENTO 6: Criação do Ambiente ---
    ambiente = Labirinto(matriz, ponto_inicial, ponto_final)

    # --- PENSAMENTO 7: Criação e Execução da Interface Gráfica ---
    jogo = JogoGrafico(ambiente, seed_usada=seed, tamanho_celula=tamanho_celula)
    jogo.executar()

    print("✅ Jogo finalizado. Até a próxima!")


if __name__ == "__main__":
    # --- PENSAMENTO 8: Configuração Padrão ---
    # Valores padrão definidos pelo escopo do projeto.
    # Para mudar, basta alterar os parâmetros aqui:
    jogar(
        seed=None,           # None = aleatória, ou escolha um número (1-100)
        altura=10,           # Altura do labirinto em células
        largura=10,          # Largura do labirinto em células
        tamanho_celula=20    # Tamanho de cada célula em pixels
    )
