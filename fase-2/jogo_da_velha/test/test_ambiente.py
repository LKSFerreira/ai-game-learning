"""
Módulo: 🧪 test_ambiente.py
Projeto: 📘 AI Game Learning

Este módulo contém uma suíte completa de testes para a classe AmbienteJogoDaVelha,
verificando se o ambiente do jogo funciona corretamente em diferentes cenários.

Os testes verificam:
- Criação de ambientes com diferentes tamanhos de tabuleiro
- Execução de jogadas válidas e inválidas
- Detecção correta de vitórias (linhas, colunas, diagonais)
- Detecção correta de empates
- Validação de ações (posições ocupadas, partidas finalizadas)
- Funcionamento correto em tabuleiros de tamanhos diferentes (3x3, 4x4, etc.)

Os testes são projetados para serem visuais e didáticos, simulando partidas
completas e exibindo o tabuleiro em cada etapa, facilitando a compreensão
do funcionamento do ambiente.

Para executar os testes, use um dos seguintes comandos:
    - python fase-2/jogo_da_velha/test/test_ambiente.py
    - py -m test.test_ambiente (a partir do diretório fase-2/jogo_da_velha)
"""

from typing import List
from ambiente import AmbienteJogoDaVelha


def simular_partida_completa(ambiente: AmbienteJogoDaVelha, titulo: str, sequencia_jogadas: List[int]):
    """
    Simula uma partida completa do jogo executando uma sequência de jogadas.

    Esta função auxiliar permite testar cenários específicos do jogo de forma
    visual e didática. Ela executa cada jogada na sequência, exibe o tabuleiro
    após cada jogada e identifica quando a partida termina.

    A função é útil para:
    - Testar cenários de vitória específicos
    - Verificar detecção de empates
    - Validar o comportamento do ambiente em situações controladas
    - Demonstrar visualmente como o jogo funciona

    Args:
        ambiente: Instância do AmbienteJogoDaVelha a ser testada.
        titulo: Título descritivo do cenário de teste.
            Exemplo: "X vence na primeira linha", "Empate (Velha)"
        sequencia_jogadas: Lista de índices representando as posições onde
            as jogadas serão executadas, na ordem especificada.
            Cada jogada será executada pelo jogador da vez.

    Note:
        A função para automaticamente quando a partida termina (vitória ou empate).
        Se a sequência de jogadas terminar antes do fim da partida, uma mensagem
        de aviso é exibida.

    Example:
        >>> ambiente = AmbienteJogoDaVelha()
        >>> simular_partida_completa(
        ...     ambiente,
        ...     "X vence na diagonal",
        ...     [0, 3, 4, 1, 8]  # X vence na diagonal principal
        ... )
    """
    print("=" * 50)
    print(f"➡️  Cenário: {titulo}")
    print("=" * 50)

    # Reinicia o ambiente para começar uma partida limpa
    ambiente.reiniciar_partida()
    print("Tabuleiro Inicial:")
    ambiente.exibir_tabuleiro()

    # Executa cada jogada na sequência
    for numero_turno, posicao_jogada in enumerate(sequencia_jogadas, start=1):
        # Identifica qual jogador está jogando neste turno
        simbolo_jogador = 'X' if ambiente.jogador_atual == 1 else 'O'
        print(f"Turno {numero_turno}: Jogador '{simbolo_jogador}' joga na posição {posicao_jogada}.")
        
        try:
            # Executa a jogada e obtém o resultado
            _, _, partida_terminou = ambiente.executar_jogada(posicao_jogada)
            
            # Exibe o tabuleiro após a jogada
            ambiente.exibir_tabuleiro()

            # Verifica se a partida terminou
            if partida_terminou:
                if ambiente.vencedor == 0:
                    # Empate (velha)
                    print(f"🏁 Partida finalizada! Resultado: Empate (Velha)!\n")
                else:
                    # Vitória de um jogador
                    simbolo_vencedor = 'X' if ambiente.vencedor == 1 else 'O'
                    print(f"🏁 Partida finalizada! Vencedor: Jogador '{simbolo_vencedor}'\n")
                return  # Termina a simulação para este cenário
                
        except ValueError as erro:
            # Captura erros de jogadas inválidas (ex: posição ocupada)
            print(f"❌ ERRO AO EXECUTAR JOGADA: {erro}")
            return
            
    # Se chegou aqui, a sequência de jogadas terminou antes do fim da partida
    print("⚠️  A sequência de jogadas terminou antes do fim da partida.")


def executar_todos_testes():
    """
    Executa toda a suíte de testes do AmbienteJogoDaVelha.

    Esta função orquestra a execução de todos os testes, organizando-os por
    tamanho de tabuleiro e tipo de cenário. Os testes são executados de forma
    visual, exibindo o tabuleiro em cada etapa para facilitar a compreensão.

    Os testes cobrem:
    - Criação de ambientes com diferentes dimensões
    - Cenários de vitória (linhas, colunas, diagonais)
    - Cenários de empate
    - Funcionamento em tabuleiros maiores (4x4)

    Note:
        Este é o ponto de entrada principal para validar a funcionalidade
        do ambiente através de testes visuais e didáticos.

    Example:
        >>> executar_todos_testes()
        ==================================================
        🧪 INICIANDO BATERIA DE TESTES DO AMBIENTE 🧪
        ...
        ==================================================
        ✅ BATERIA DE TESTES CONCLUÍDA!
        ==================================================
    """
    print("\n" + "=" * 50)
    print("🧪 INICIANDO BATERIA DE TESTES DO AMBIENTE 🧪")
    print("=" * 50)

    # --- TESTES PARA TABULEIRO 3X3 (TRADICIONAL) ---
    ambiente_3x3 = AmbienteJogoDaVelha(dimensao=3)
    print("\n✅ Jogo 3x3 criado com sucesso!")
    
    # Teste 1: Vitória na primeira linha (horizontal)
    # X joga: 0, 1, 2 (primeira linha)
    # O joga: 4, 5 (tentando bloquear, mas X vence primeiro)
    simular_partida_completa(
        ambiente_3x3,
        "X vence na primeira linha",
        [0, 4, 1, 5, 2]
    )
    
    # Teste 2: Empate (velha)
    # Sequência que resulta em empate: todas as casas ocupadas sem vencedor
    simular_partida_completa(
        ambiente_3x3,
        "Empate (Velha)",
        [0, 4, 8, 2, 6, 3, 5, 7, 1]
    )
    
    # Teste 3: Vitória na coluna do meio (vertical)
    # O vence na coluna central: posições 1, 4, 7
    simular_partida_completa(
        ambiente_3x3,
        "O vence na coluna do meio",
        [0, 4, 2, 1, 3, 7]
    )

    # --- TESTES PARA TABULEIRO 4X4 (EXTENDIDO) ---
    ambiente_4x4 = AmbienteJogoDaVelha(dimensao=4)
    print("\n✅ Jogo 4x4 criado com sucesso!")
    
    # Teste 4: Vitória na diagonal principal em tabuleiro 4x4
    # X vence na diagonal: posições 0, 5, 10, 15
    simular_partida_completa(
        ambiente_4x4,
        "X vence na diagonal principal (4x4)",
        [0, 1, 5, 2, 10, 3, 15]
    )

    print("\n" + "=" * 50)
    print("✅ BATERIA DE TESTES CONCLUÍDA!")
    print("=" * 50 + "\n")


# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    """
    Ponto de entrada do módulo quando executado diretamente.

    Quando o arquivo é executado como script (não importado como módulo),
    executa automaticamente toda a suíte de testes do ambiente.
    """
    executar_todos_testes()
