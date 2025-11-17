# fase_2/labirinto/demonstracao_terminal.py

"""
Script de demonstração para interagir com o ambiente do labirinto no terminal.

Este arquivo serve como um ponto de entrada para testar e visualizar o sistema
completo, orquestrando a geração do labirinto e a interação com ele.

Funcionalidades:
1. Gera um labirinto de tamanho configurável.
2. Permite que um jogador humano jogue o labirinto via terminal.
3. Rastreia estatísticas (movimentos, tempo, recompensa acumulada).
4. Demonstra o reinício do ambiente e o tratamento de ações inválidas.
"""

import time
from typing import List, Dict, Any

# Importa as ferramentas necessárias: o gerador e o ambiente.
from gerador_labirinto import gerar_labirinto
from ambiente import Labirinto, Posicao


class EstatisticasJogo:
    """
    Classe para rastrear estatísticas do jogo.
    
    Mantém registro de todas as métricas importantes durante a partida,
    como um "placar" ou "contador de status" no Ragnarok.
    """
    
    def __init__(self) -> None:
        """Inicializa as estatísticas do jogo."""
        self.numero_movimentos: int = 0
        self.recompensa_acumulada: float = 0.0
        self.historico_movimentos: List[Dict[str, Any]] = []
        self.tempo_inicio: float = time.time()
    
    def registrar_movimento(self, acao: str, recompensa: float) -> None:
        """
        Registra um movimento realizado.
        
        Args:
            acao (str): A ação executada (W, A, S, D, etc.)
            recompensa (float): A recompensa recebida
        """
        self.numero_movimentos += 1
        self.recompensa_acumulada += recompensa
        self.historico_movimentos.append({'acao': acao, 'recompensa': recompensa})
    
    def obter_tempo_decorrido(self) -> float:
        """
        Calcula o tempo decorrido desde o início.
        
        Returns:
            float: Tempo em segundos
        """
        return round(time.time() - self.tempo_inicio, 1)
    
    def exibir_resumo(self) -> None:
        """Exibe um resumo das estatísticas."""
        print('\n--- 📊 Estatísticas da Partida ---')
        print(f'Total de movimentos: {self.numero_movimentos}')
        print(f'Recompensa acumulada: {self.recompensa_acumulada:.2f}')
        print(f'Tempo decorrido: {self.obter_tempo_decorrido()}s')
        
        if self.historico_movimentos:
            ultimos_movimentos = self.historico_movimentos[-5:]
            acoes = ', '.join([m['acao'] for m in ultimos_movimentos])
            print(f'\nÚltimos movimentos: {acoes}')


def limpar_tela() -> None:
    """
    Limpa a tela do terminal.
    
    É como limpar a HUD do jogo para mostrar informações atualizadas.
    Funciona em Windows, Linux e macOS.
    """
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def jogar_no_terminal(ambiente: Labirinto) -> None:
    """
    Inicia um loop de jogo interativo no terminal.

    Permite que um usuário jogue o labirinto inserindo as teclas W, A, S, D.
    O loop continua até que o jogador chegue ao ponto final ou digite 'sair'.

    É como o loop principal de um jogo: atualiza estado → renderiza → espera input → repete.

    Args:
        ambiente (Labirinto): A instância do ambiente do labirinto a ser jogada.
    """
    stats = EstatisticasJogo()
    
    print("\n--- 🕹️ Modo de Jogo Interativo ---")
    print("Use as teclas W (cima), A (esquerda), S (baixo), D (direita) para mover.")
    print("Digite 'sair' para terminar o jogo.")
    print("Digite 'stats' para ver estatísticas.")
    print("Digite 'limpar' para limpar a tela.\n")

    while True:
        # Exibe o estado atual do jogo a cada turno.
        ambiente.imprimir_labirinto()
        print(f"\n📍 Sua posição: {ambiente.posicao_agente}")
        print(f"📊 Movimentos: {stats.numero_movimentos} | Recompensa: {stats.recompensa_acumulada:.2f}")

        # Pede a próxima ação ao jogador.
        acao = input("Qual seu próximo movimento? ").strip()

        # Processa comandos especiais
        if acao.lower() == 'sair':
            print("\n👋 Jogo encerrado pelo usuário.")
            stats.exibir_resumo()
            break

        if acao.lower() == 'stats':
            stats.exibir_resumo()
            continue

        if acao.lower() == 'limpar':
            limpar_tela()
            continue

        # Processa movimento normal
        try:
            _, recompensa, terminou = ambiente.executar_acao(acao)
            stats.registrar_movimento(acao, recompensa)
            
            print(f"\n✅ Ação '{acao}' executada. Recompensa: {recompensa}")

            if terminou:
                limpar_tela()
                ambiente.imprimir_labirinto()
                print("\n🎉🎉🎉 PARABÉNS! Você encontrou a saída! 🎉🎉🎉")
                stats.exibir_resumo()
                break

        except ValueError as e:
            # Captura e informa sobre ações inválidas (ex: 'p', 'x', etc.)
            if 'Ação inválida' in str(e):
                print(f"\n⚠️ Erro: {e}")
                print("💡 Dica: Use W, A, S, D ou os nomes completos (cima, baixo, esquerda, direita).")
            else:
                print(f"\n❌ Ocorreu um erro inesperado: {e}")
                break
        except Exception as e:
            print(f"\n❌ Ocorreu um erro inesperado: {e}")
            break


def main() -> None:
    """
    Função principal que orquestra a demonstração.
    
    Esta é a "sala de controle" do programa, coordenando todas as partes:
    geração → configuração → jogo → demonstrações extras.
    """
    print("--- 🚀 Iniciando a Demonstração do Ambiente do Labirinto ---")

    # 1. Configurações do Labirinto
    # Altere estes valores para gerar labirintos de diferentes tamanhos.
    ALTURA_CELULAS = 6
    LARGURA_CELULAS = 10

    print(f"\n1. Gerando um labirinto de {ALTURA_CELULAS}x{LARGURA_CELULAS} células...")
    
    try:
        matriz_gerada = gerar_labirinto(ALTURA_CELULAS, LARGURA_CELULAS)

        # 2. Definição dos Pontos de Início e Fim
        ponto_inicial: Posicao = (1, 1)
        ultima_linha_caminho = ALTURA_CELULAS * 2 - 1
        ultima_coluna_caminho = LARGURA_CELULAS * 2 - 1
        ponto_final: Posicao = (ultima_linha_caminho, ultima_coluna_caminho)

        print(f"   - Ponto inicial definido em {ponto_inicial}.")
        print(f"   - Ponto final definido em {ponto_final}.")

        # 3. Criação do Ambiente
        ambiente_jogo = Labirinto(
            matriz_labirinto=matriz_gerada,
            ponto_inicial=ponto_inicial,
            ponto_final=ponto_final
        )
        print("2. Ambiente do labirinto criado com sucesso.\n")

        # 4. Inicia o modo de jogo interativo
        # Esta é a parte principal da demonstração, onde o usuário pode jogar.
        jogar_no_terminal(ambiente_jogo)

        # 5. Demonstração de funcionalidades adicionais após o jogo
        print("\n" + "="*50)
        print("--- 🧪 Demonstração de Funcionalidades Adicionais ---")

        # Demonstra o reinício do ambiente
        print("\n1. Testando o reinício do ambiente...")
        ambiente_jogo.reiniciar()
        ambiente_jogo.imprimir_labirinto()
        print(f"Posição do agente foi resetada para: {ambiente_jogo.posicao_agente}")

        # Demonstra o tratamento de erro para uma ação inválida
        print("\n2. Testando uma ação com nome inválido ('pular')...")
        try:
            ambiente_jogo.executar_acao("pular")
        except ValueError as e:
            print(f"   -> Erro capturado com sucesso: {e}")

        print("\n--- 🏁 Demonstração Concluída ---")

    except Exception as e:
        print(f"\n❌ Erro fatal ao criar o ambiente: {e}")
        import traceback
        traceback.print_exc()
        return  # Encerra o script se o ambiente não puder ser criado


if __name__ == "__main__":
    main()
