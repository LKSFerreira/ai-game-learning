"""
Módulo: 🕹️ jogar.py
Projeto: 📘 AI Game Learning

Este módulo implementa a interface de jogo interativa, permitindo que um
jogador humano desafie a IA treinada em uma partida de Jogo da Velha.

O módulo gerencia todo o fluxo de interação humano-IA:
- Carregamento do modelo treinado (Superagente)
- Interface de usuário para escolha de símbolo e jogadas
- Sistema de regras especiais para determinar quem começa cada partida
- Exibição visual do tabuleiro e feedback sobre o progresso
- Gerenciamento de múltiplas partidas consecutivas

Sistema de Regras Especiais:
O jogo implementa um sistema dinâmico de escolha do jogador inicial baseado
no resultado da partida anterior:
- Se o humano venceu: Pode escolher quem começa (recompensa)
- Se o humano perdeu: A IA sempre começa (dificuldade adicional)
- Se houve empate: Sorteio aleatório (justiça)

Este sistema torna o jogo mais interessante e desafiador, criando uma
experiência de jogo mais envolvente e dinâmica.
"""

import os
import sys
from pathlib import Path
import random
import time
from typing import Optional, Tuple

from .ambiente import AmbienteJogoDaVelha
from .agente import AgenteQLearning


def limpar_tela():
    """
    Limpa o console para melhorar a experiência visual do usuário.

    Detecta automaticamente o sistema operacional e usa o comando apropriado:
    - Windows: 'cls'
    - Unix/Linux/Mac: 'clear'

    Note:
        Este método não retorna nada, apenas executa o comando de limpeza.
        Útil para manter a interface limpa entre turnos e partidas.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def obter_jogada_humano(ambiente: AmbienteJogoDaVelha) -> int:
    """
    Solicita e valida a jogada do jogador humano.

    Esta função exibe o tabuleiro atual com as posições disponíveis numeradas,
    permitindo que o jogador veja claramente onde pode jogar. Ela valida a
    entrada do usuário, garantindo que:
    - A entrada seja um número válido
    - A posição escolhida esteja realmente vazia
    - A posição exista no tabuleiro

    Args:
        ambiente: Instância do ambiente do jogo contendo o estado atual.

    Returns:
        Índice da posição escolhida pelo jogador (0 a N²-1).

    Note:
        Esta função entra em um loop até que o jogador forneça uma entrada válida.
        Ela fornece feedback claro sobre erros (posição ocupada, entrada inválida, etc.).
    """
    acoes_validas = ambiente.obter_acoes_validas()
    
    # Exibe o tabuleiro com números nas posições vazias para facilitar a escolha
    print("\n--- Tabuleiro com Posições Livres ---")
    simbolos = {0: ' ', 1: 'X', 2: 'O'}
    
    # Itera sobre cada linha do tabuleiro
    for indice_linha in range(ambiente.dimensao):
        inicio_linha = indice_linha * ambiente.dimensao
        fim_linha = inicio_linha + ambiente.dimensao
        
        # Cria a linha: mostra números nas posições vazias, símbolos nas ocupadas
        linha = [
            str(indice) if ambiente.tabuleiro[indice] == 0 
            else simbolos[ambiente.tabuleiro[indice]]
            for indice in range(inicio_linha, fim_linha)
        ]
        print(" " + " | ".join(linha))
        
        # Adiciona separador horizontal entre linhas
        if indice_linha < ambiente.dimensao - 1:
            print("---" + "+---" * (ambiente.dimensao - 1))
    
    print("------------------------------------")

    # Loop de validação: continua até receber uma entrada válida
    while True:
        try:
            posicao_str = input(f"Sua vez. Escolha uma posição livre ({acoes_validas}): ")
            posicao = int(posicao_str)
            
            # Verifica se a posição escolhida está na lista de ações válidas
            if posicao in acoes_validas:
                return posicao
            else:
                print("❌ Jogada inválida! A posição não está livre ou não existe.")
        except ValueError:
            print("❌ Entrada inválida. Por favor, digite um número.")


def determinar_jogador_inicial(resultado_anterior: int, jogador_humano: int) -> int:
    """
    Determina qual jogador começa a partida baseado no resultado anterior.

    Este método implementa um sistema de regras dinâmico que torna o jogo
    mais interessante e desafiador:

    - Primeira partida ou empate anterior: Sorteio aleatório (justiça)
    - Humano perdeu: IA começa (aumenta dificuldade como "punição")
    - Humano venceu: Humano escolhe quem começa (recompensa)

    Este sistema cria uma experiência de jogo mais envolvente, onde o
    desempenho do jogador afeta as condições da próxima partida.

    Args:
        resultado_anterior: Resultado da partida anterior.
            -1: Primeira partida (ainda não houve resultado)
            0: Empate
            1 ou 2: Vencedor (1='X', 2='O')
        jogador_humano: Identificador do jogador humano (1 para 'X', 2 para 'O').

    Returns:
        Identificador do jogador que começará a partida (1 para 'X', 2 para 'O').

    Note:
        Se o humano venceu, esta função solicita input do usuário para escolher
        quem começa. Em outros casos, a decisão é automática.
    """
    # Calcula qual é o jogador da IA (oposto ao humano)
    jogador_ia = 2 if jogador_humano == 1 else 1
    
    # Caso 1: Primeira partida ou empate anterior
    # Sorteio aleatório para ser justo
    if resultado_anterior == -1 or resultado_anterior == 0:
        print("\n🎲 Resultado anterior foi empate ou é a primeira partida. Sorteando quem começa...")
        time.sleep(1)  # Pausa para dar tempo de ler a mensagem
        return random.choice([1, 2])
    
    # Caso 2: Humano perdeu a última partida
    # IA começa como "punição" (aumenta a dificuldade)
    elif resultado_anterior == jogador_ia:
        print("\n🤖 Você perdeu a última partida. A IA começa como punição!")
        time.sleep(1)
        return jogador_ia
    
    # Caso 3: Humano venceu a última partida
    # Humano escolhe quem começa como recompensa
    else:
        print("\n🏆 Você venceu a última partida! Como recompensa, você escolhe quem começa.")
        while True:
            escolha = input("Você quer começar (S) ou deixar a IA começar (N)? [S/N]: ").upper()
            if escolha == 'S':
                return jogador_humano
            elif escolha == 'N':
                return jogador_ia
            else:
                print("Opção inválida. Digite 'S' para sim ou 'N' para não.")


def exibir_regras_iniciais():
    """
    Exibe as regras especiais do jogo na primeira partida.

    Informa o jogador sobre o sistema dinâmico de escolha do jogador inicial,
    explicando como o resultado de cada partida afeta a próxima. Isso ajuda
    o jogador a entender as regras e estratégias do jogo.

    Note:
        Esta função pausa a execução aguardando o jogador pressionar Enter,
        garantindo que ele tenha tempo para ler as regras.
    """
    print("\n" + "-"*50)
    print("📜 REGRAS ESPECIAIS DE QUEM COMEÇA 📜")
    print("-"*50)
    print("A cada nova partida, a ordem de início é decidida assim:")
    print(" • Se você VENCEU: Você tem o direito de escolher quem começa.")
    print(" • Se você PERDEU: A IA sempre começará a próxima partida.")
    print(" • Se houve EMPATE: Um novo sorteio decidirá quem começa.")
    print("-"*50)
    input("\nPressione Enter para continuar...")


def iniciar_partida_humano_vs_ia(agente_ia: AgenteQLearning, resultado_anterior: int = -1, jogador_humano_definido: Optional[int] = None) -> Tuple[int, int]:
    """
    Gerencia o fluxo completo de uma partida entre humano e IA.

    Esta função coordena toda a partida do início ao fim:
    1. Configura o ambiente e os jogadores
    2. Determina quem começa (baseado no resultado anterior)
    3. Alterna entre jogador humano e IA até a partida terminar
    4. Exibe o resultado final
    5. Retorna informações para a próxima partida

    O jogo é executado em modo de performance máxima (sem exploração),
    garantindo que a IA sempre escolha a melhor ação conhecida.

    Args:
        agente_ia: Instância do agente Q-Learning treinado (Superagente).
        resultado_anterior: Resultado da partida anterior.
            -1: Primeira partida
            0: Empate anterior
            1 ou 2: Vencedor anterior
        jogador_humano_definido: Identificador do jogador humano (1='X', 2='O').
            Se None, solicita ao jogador na primeira partida.

    Returns:
        Tupla contendo:
        - vencedor (int): Identificador do vencedor (1, 2, ou 0 para empate)
        - jogador_humano (int): Identificador do jogador humano (1 ou 2)

    Note:
        - A IA joga com em_treinamento=False (sempre escolhe a melhor ação)
        - O ambiente é reiniciado automaticamente para uma nova partida
        - A função exibe o tabuleiro após cada jogada
    """
    limpar_tela()
    print("\n" + "="*50)
    print("⚔️ NOVA PARTIDA ⚔️")
    print("="*50)

    # Cria um novo ambiente para esta partida
    ambiente = AmbienteJogoDaVelha(dimensao=3)
    
    # --- CONFIGURAÇÃO INICIAL DOS JOGADORES ---
    jogador_humano = jogador_humano_definido
    
    # Se é a primeira partida, solicita ao jogador escolher seu símbolo
    if resultado_anterior == -1:
        while jogador_humano is None:
            escolha = input("Você quer ser 'X' ou 'O'? [X/O]: ").upper()
            if escolha == 'X':
                jogador_humano = 1
            elif escolha == 'O':
                jogador_humano = 2
            else:
                print("Opção inválida. Digite 'X' ou 'O'.")
        
        # Configura o agente IA para jogar com o símbolo oposto
        agente_ia.jogador = 2 if jogador_humano == 1 else 1
        agente_ia.simbolo = 'O' if agente_ia.jogador == 2 else 'X'
    
    # Exibe a configuração dos jogadores
    simbolo_humano = 'X' if jogador_humano == 1 else 'O'
    print(f"\nVocê joga como '{simbolo_humano}'. A IA jogará como '{agente_ia.simbolo}'.")
    
    # Determina quem começa baseado no resultado anterior
    ambiente.jogador_atual = determinar_jogador_inicial(resultado_anterior, jogador_humano)
    simbolo_inicial = 'X' if ambiente.jogador_atual == 1 else 'O'
    print(f"O jogador '{simbolo_inicial}' começa a partida!")
    
    # Exibe regras na primeira partida, ou aguarda confirmação nas demais
    if resultado_anterior == -1:
        exibir_regras_iniciais()
    else:
        input("\nPressione Enter para começar a partida...")

    # --- LOOP PRINCIPAL DA PARTIDA ---
    while not ambiente.partida_finalizada:
        limpar_tela()
        simbolo_humano = 'X' if jogador_humano == 1 else 'O'
        print(f"Você ('{simbolo_humano}') vs. IA ('{agente_ia.simbolo}')\n")
        ambiente.exibir_tabuleiro()
        
        # Obtém o estado atual e as ações válidas
        estado_atual = ambiente.obter_estado_como_tupla()
        acoes_validas = ambiente.obter_acoes_validas()

        # Decide se é a vez do humano ou da IA
        if ambiente.jogador_atual == jogador_humano:
            # Turno do jogador humano
            acao = obter_jogada_humano(ambiente)
        else:
            # Turno da IA
            print(f"\nTurno da IA ({agente_ia.simbolo})... pensando...")
            time.sleep(1)  # Pausa para criar suspense
            
            # IA escolhe a melhor ação conhecida (sem exploração)
            acao = agente_ia.escolher_acao(estado_atual, acoes_validas, em_treinamento=False)
            print(f"IA escolheu a posição {acao}.")
            time.sleep(1)  # Pausa para o jogador ver a escolha

        # Executa a jogada escolhida no ambiente
        ambiente.executar_jogada(acao)

    # --- EXIBIÇÃO DO RESULTADO FINAL ---
    limpar_tela()
    print("\n" + "="*50)
    print("FIM DE JOGO!")
    print("="*50)
    ambiente.exibir_tabuleiro()
    
    # Determina e exibe o resultado
    if ambiente.vencedor == 0:
        print("Resultado: 🤝 EMPATE! Você conseguiu igualar o mestre!")
    elif ambiente.vencedor == jogador_humano:
        print("Resultado: 🏆 IMPOSSÍVEL! Você venceu! Encontrou um bug ou uma falha no treinamento?")
    else:
        print("Resultado: 🤖 DERROTA! A IA venceu, como esperado.")
    
    print("="*50 + "\n")
    return ambiente.vencedor, jogador_humano


def main():
    """
    Função principal que gerencia o jogo completo e múltiplas partidas.

    Esta função:
    1. Carrega o modelo treinado (Superagente)
    2. Gerencia o loop principal de múltiplas partidas
    3. Mantém o estado entre partidas (resultado anterior, jogador escolhido)
    4. Permite ao jogador continuar jogando ou sair

    O jogo continua até que o jogador decida parar, mantendo o histórico
    de resultados para aplicar as regras especiais de quem começa.

    Note:
        - O modelo esperado é o Superagente final (resultado da mesclagem)
        - Se o modelo não for encontrado, o programa encerra com erro
        - O jogador escolhe seu símbolo apenas na primeira partida
    """
    limpar_tela()
    print("\n" + "="*50)
    print("🤖 BEM-VINDO AO DESAFIO CONTRA A IA MESTRE! 🤖")
    print("="*50)

    # Define o caminho do modelo treinado (Superagente)
    caminho_modelo = Path("modelos_treinados") / "superagente_final_3x3.pkl"
    
    # Verifica se o modelo existe antes de tentar carregar
    if not caminho_modelo.exists():
        print(f"\n❌ ERRO: Modelo '{caminho_modelo}' não encontrado.")
        print("   Execute o treinamento e a mesclagem dos modelos primeiro.")
        sys.exit(1)
        
    # Carrega o Superagente treinado
    # epsilon=0 garante que a IA sempre escolha a melhor ação (sem exploração)
    agente_ia = AgenteQLearning.carregar(str(caminho_modelo), jogador=0, epsilon=0)

    # Variáveis de controle do loop de partidas
    jogar_novamente = True
    resultado_anterior = -1  # -1 indica primeira partida
    jogador_humano: Optional[int] = None  # Será definido na primeira partida

    # Loop principal: continua até o jogador decidir parar
    while jogar_novamente:
        # Executa uma partida completa
        resultado_atual, jogador_humano_atual = iniciar_partida_humano_vs_ia(
            agente_ia,
            resultado_anterior,
            jogador_humano
        )
        
        # Atualiza o resultado anterior para a próxima partida
        resultado_anterior = resultado_atual
        
        # Salva o jogador escolhido na primeira partida
        if jogador_humano is None:
            jogador_humano = jogador_humano_atual
        
        # Pergunta se o jogador quer continuar
        resposta = input("🎮 Jogar novamente? (s/n): ").strip().lower()
        if resposta not in ['s', 'sim']:
            jogar_novamente = False
    
    print("\n👋 Obrigado por jogar! Até a próxima.")


if __name__ == "__main__":
    """
    Ponto de entrada do módulo quando executado diretamente.

    Quando o arquivo é executado como script, inicia automaticamente
    o jogo contra a IA.
    """
    main()
