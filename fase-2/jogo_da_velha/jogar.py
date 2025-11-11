"""
Módulo: 🕹️ jogar.py
Projeto: 📘 AI Game Learning

Este módulo é a arena onde um jogador humano pode desafiar a IA que treinamos.
"""

import os
import sys
from pathlib import Path
import random
import time

from ambiente import AmbienteJogoDaVelha
from agente import AgenteQLearning

def limpar_tela():
    """ Limpa o console para uma melhor experiência de usuário. """
    os.system('cls' if os.name == 'nt' else 'clear')

def obter_jogada_humano(ambiente: AmbienteJogoDaVelha) -> int:
    """ Pede ao jogador humano para escolher uma jogada válida e a retorna. """
    acoes_validas = ambiente.obter_acoes_validas()
    
    print("\n--- Tabuleiro com Posições Livres ---")
    simbolos = {0: ' ', 1: 'X', 2: 'O'}
    for i in range(ambiente.dimensao):
        inicio = i * ambiente.dimensao
        fim = inicio + ambiente.dimensao
        linha = [str(idx) if ambiente.tabuleiro[idx] == 0 else simbolos[ambiente.tabuleiro[idx]] for idx in range(inicio, fim)]
        print(" " + " | ".join(linha))
        if i < ambiente.dimensao - 1:
            print("---" + "+---" * (ambiente.dimensao - 1))
    print("------------------------------------")

    while True:
        try:
            posicao_str = input(f"Sua vez. Escolha uma posição livre ({acoes_validas}): ")
            posicao = int(posicao_str)
            if posicao in acoes_validas:
                return posicao
            else:
                print("❌ Jogada inválida! A posição não está livre ou não existe.")
        except ValueError:
            print("❌ Entrada inválida. Por favor, digite um número.")

def determinar_jogador_inicial(resultado_anterior: int, jogador_humano: int) -> int:
    """ Determina quem começa a próxima partida com base no resultado anterior. """
    jogador_ia = 2 if jogador_humano == 1 else 1
    
    if resultado_anterior == -1 or resultado_anterior == 0:
        print("\n🎲 Resultado anterior foi empate ou é a primeira partida. Sorteando quem começa...")
        time.sleep(1)
        return random.choice([1, 2])
    elif resultado_anterior == jogador_ia:
        print("\n🤖 Você perdeu a última partida. A IA começa como punição!")
        time.sleep(1)
        return jogador_ia
    else:
        print("\n🏆 Você venceu a última partida! Como recompensa, você escolhe quem começa.")
        while True:
            escolha = input("Você quer começar (S) ou deixar a IA começar (N)? [S/N]: ").upper()
            if escolha == 'S':
                return jogador_humano
            elif escolha == 'N':
                return jogador_ia
            else:
                print("Opção inválida.")

def exibir_regras_iniciais():
    """ Exibe as regras especiais do jogo no início da primeira partida. """
    print("\n" + "-"*50)
    print("📜 REGRAS ESPECIAIS DE QUEM COMEÇA 📜")
    print("-"*50)
    print("A cada nova partida, a ordem de início é decidida assim:")
    print(" • Se você VENCEU: Você tem o direito de escolher quem começa.")
    print(" • Se você PERDEU: A IA sempre começará a próxima partida.")
    print(" • Se houve EMPATE: Um novo sorteio decidirá quem começa.")
    print("-"*50)
    input("\nPressione Enter para continuar...")

def iniciar_partida_humano_vs_ia(agente_ia: AgenteQLearning, resultado_anterior: int = -1, jogador_humano_definido: int = None) -> tuple[int, int]:
    """
    Gerencia o fluxo de uma única partida entre um humano e a IA.
    Retorna uma tupla (vencedor, jogador_humano).
    """
    limpar_tela()
    print("\n" + "="*50)
    print("⚔️ NOVA PARTIDA ⚔️")
    print("="*50)

    ambiente = AmbienteJogoDaVelha(dimensao=3)
    
    jogador_humano = jogador_humano_definido
    if resultado_anterior == -1:
        while jogador_humano is None:
            escolha = input("Você quer ser 'X' ou 'O'? [X/O]: ").upper()
            if escolha == 'X': jogador_humano = 1
            elif escolha == 'O': jogador_humano = 2
            else: print("Opção inválida.")
        
        agente_ia.jogador = 2 if jogador_humano == 1 else 1
        agente_ia.simbolo = 'O' if agente_ia.jogador == 2 else 'X'
    
    print(f"\nVocê joga como '{'X' if jogador_humano == 1 else 'O'}'. A IA jogará como '{agente_ia.simbolo}'.")
    
    ambiente.jogador_atual = determinar_jogador_inicial(resultado_anterior, jogador_humano)
    print(f"O jogador '{'X' if ambiente.jogador_atual == 1 else 'O'}' começa a partida!")
    
    if resultado_anterior == -1:
        exibir_regras_iniciais()
    else:
        input("\nPressione Enter para começar a partida...")

    while not ambiente.partida_finalizada:
        limpar_tela()
        print(f"Você ('{'X' if jogador_humano == 1 else 'O'}') vs. IA ('{agente_ia.simbolo}')\n")
        ambiente.exibir_tabuleiro()
        
        estado_atual = ambiente.obter_estado_como_tupla()
        acoes_validas = ambiente.obter_acoes_validas()

        if ambiente.jogador_atual == jogador_humano:
            acao = obter_jogada_humano(ambiente)
        else:
            print(f"\nTurno da IA ({agente_ia.simbolo})... pensando...")
            time.sleep(1)
            acao = agente_ia.escolher_acao(estado_atual, acoes_validas, em_treinamento=False)
            print(f"IA escolheu a posição {acao}.")
            time.sleep(1)

        ambiente.executar_jogada(acao)

    limpar_tela()
    print("\n" + "="*50)
    print("FIM DE JOGO!")
    print("="*50)
    ambiente.exibir_tabuleiro()
    
    if ambiente.vencedor == 0:
        print("Resultado: 🤝 EMPATE! Você conseguiu igualar o mestre!")
    elif ambiente.vencedor == jogador_humano:
        print("Resultado: 🏆 IMPOSSÍVEL! Você venceu! Encontrou um bug ou uma falha no treinamento?")
    else:
        print("Resultado: 🤖 DERROTA! A IA venceu, como esperado.")
    
    print("="*50 + "\n")
    return ambiente.vencedor, jogador_humano

def main():
    """ Função principal que gerencia o jogo e as novas partidas. """
    limpar_tela()
    print("\n" + "="*50)
    print("🤖 BEM-VINDO AO DESAFIO CONTRA A IA MESTRE! 🤖")
    print("="*50)

    caminho_modelo = Path("modelos_treinados") / "superagente_final_3x3.pkl"
    if not caminho_modelo.exists():
        print(f"\n❌ ERRO: Modelo '{caminho_modelo}' não encontrado.")
        sys.exit(1)
        
    agente_ia = AgenteQLearning.carregar(str(caminho_modelo), jogador=0, epsilon=0)

    jogar_novamente = True
    resultado_anterior = -1
    jogador_humano = None

    while jogar_novamente:
        resultado_atual, jogador_humano_atual = iniciar_partida_humano_vs_ia(agente_ia, resultado_anterior, jogador_humano)
        resultado_anterior = resultado_atual
        if jogador_humano is None:
            jogador_humano = jogador_humano_atual
        
        resposta = input("🎮 Jogar novamente? (s/n): ").strip().lower()
        if resposta not in ['s', 'sim']:
            jogar_novamente = False
    
    print("\n👋 Obrigado por jogar! Até a próxima.")

if __name__ == "__main__":
    main()