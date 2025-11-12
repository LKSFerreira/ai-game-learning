"""
Módulo: 🧪 test_treinador.py
Projeto: 📘 AI Game Learning

Este módulo contém testes de integração para a classe Treinador, verificando se
o ciclo completo de treinamento funciona corretamente.

Os testes verificam:
- Se o Treinador consegue executar múltiplas partidas sem erros
- Se os agentes realmente aprendem durante o treinamento (tabela Q não vazia)
- Se as estatísticas são registradas corretamente
- Se o processo de self-play está funcionando como esperado

Este é um teste de integração, pois verifica a interação entre múltiplos
componentes (Treinador, Agentes, Ambiente) trabalhando juntos, não apenas
a funcionalidade isolada de cada um.

Para executar os testes, use um dos seguintes comandos:
    - python fase-2/jogo_da_velha/test/test_treinador.py
    - py -m test.test_treinador (a partir do diretório fase-2/jogo_da_velha)
"""

from ambiente import AmbienteJogoDaVelha
from agente import AgenteQLearning
from treinador import Treinador


def testar_ciclo_de_treinamento_rapido():
    """
    Testa se o Treinador consegue executar um ciclo completo de treinamento.

    Este teste de integração verifica se todos os componentes trabalham juntos
    corretamente:
    1. O Treinador consegue executar múltiplas partidas
    2. Os agentes aprendem durante o treinamento (adquirem conhecimento)
    3. As estatísticas são registradas corretamente
    4. O processo de self-play funciona sem erros

    O teste executa um treinamento curto (100 partidas) para validar que o
    sistema funciona, sem demorar muito tempo. Em um cenário real, o treinamento
    executaria milhares ou centenas de milhares de partidas.

    O que é verificado:
    - Nenhuma exceção é levantada durante o treinamento
    - Ambos os agentes adquirem conhecimento (tabela Q não vazia)
    - O número de partidas treinadas é registrado corretamente
    - Os agentes conhecem diferentes estados do jogo após o treinamento

    Raises:
        AssertionError: Se qualquer verificação falhar, indicando um problema
            no sistema de treinamento.

    Note:
        Este é um teste de integração, não um teste unitário. Ele verifica
        a interação entre múltiplos componentes do sistema.

    Example:
        >>> testar_ciclo_de_treinamento_rapido()
        --- INICIANDO TESTE 1: CICLO DE TREINAMENTO RÁPIDO ---
        Executando um mini-treinamento de 100 partidas...
        ...
        ✅ O ciclo de treinamento rápido foi concluído com sucesso!
    """
    print("--- INICIANDO TESTE 1: CICLO DE TREINAMENTO RÁPIDO ---")
    
    # --- FASE 1: CONFIGURAÇÃO DO CENÁRIO DE TESTE ---
    # Cria um ambiente de jogo 3x3 (padrão do Jogo da Velha)
    ambiente_teste = AmbienteJogoDaVelha(dimensao=3)
    
    # Cria dois agentes Q-Learning, um para cada jogador
    # Ambos começam sem conhecimento prévio (tabela Q vazia)
    agente_x_teste = AgenteQLearning(jogador=1)
    agente_o_teste = AgenteQLearning(jogador=2)
    
    # Cria o Treinador que orquestrará o treinamento
    treinador_teste = Treinador(agente_x_teste, agente_o_teste, ambiente_teste)
    
    # Define um número pequeno de partidas para o teste ser rápido
    # Em treinamento real, este número seria muito maior (10.000+)
    numero_de_partidas_teste = 100
    
    print(f"Executando um mini-treinamento de {numero_de_partidas_teste} partidas...")
    
    # --- FASE 2: EXECUÇÃO DO TREINAMENTO ---
    # Executa o método de treinamento e captura qualquer erro
    # Se houver erro, o teste falha imediatamente
    try:
        treinador_teste.treinar(
            numero_de_partidas=numero_de_partidas_teste,
            intervalo_log=50  # Reseta estatísticas a cada 50 partidas
        )
    except Exception as erro:
        # Se qualquer erro ocorrer durante o treinamento, o teste falha
        # Isso garante que problemas no sistema sejam detectados imediatamente
        assert False, (
            f"O treinamento falhou com um erro: {erro}. "
            "Isso indica um problema no sistema de treinamento que precisa ser corrigido."
        )
        
    # --- FASE 3: VERIFICAÇÃO DOS RESULTADOS ---
    
    # Verificação 1: Os agentes aprenderam algo?
    # Se a tabela Q estiver vazia, significa que os agentes não aprenderam nada,
    # o que indicaria um problema grave no sistema de aprendizado.
    assert len(agente_x_teste.tabela_q) > 0, (
        "A Tabela Q do Agente X não deveria estar vazia após o treinamento. "
        "Isso indica que o agente não está aprendendo corretamente."
    )
    assert len(agente_o_teste.tabela_q) > 0, (
        "A Tabela Q do Agente O não deveria estar vazia após o treinamento. "
        "Isso indica que o agente não está aprendendo corretamente."
    )
    
    # Verificação 2: As estatísticas foram registradas corretamente?
    # Verifica se o número de partidas treinadas corresponde ao esperado.
    # Isso garante que o contador de partidas está funcionando corretamente.
    assert agente_x_teste.partidas_treinadas == numero_de_partidas_teste, (
        f"O Agente X deveria ter treinado {numero_de_partidas_teste} partidas, "
        f"mas registrou {agente_x_teste.partidas_treinadas}. "
        "O contador de partidas pode estar com problema."
    )
    assert agente_o_teste.partidas_treinadas == numero_de_partidas_teste, (
        f"O Agente O deveria ter treinado {numero_de_partidas_teste} partidas, "
        f"mas registrou {agente_o_teste.partidas_treinadas}. "
        "O contador de partidas pode estar com problema."
    )
    
    # Exibe informações sobre o conhecimento adquirido
    # Cada estado único conhecido representa uma situação do jogo que o agente
    # já encontrou e para a qual tem uma estratégia (valor Q).
    print(f"\n✅ O Agente X conhece {len(agente_x_teste.tabela_q)} situações.")
    print(f"✅ O Agente O conhece {len(agente_o_teste.tabela_q)} situações.")
    print("✅ O ciclo de treinamento rápido foi concluído com sucesso!")
    print("--- TESTE 1 FINALIZADO ---\n")


def executar_todos_testes():
    """
    Executa toda a suíte de testes do Treinador.

    Esta função orquestra a execução de todos os testes de integração,
    fornecendo feedback claro sobre o progresso e resultados de cada teste.

    Se todos os testes passarem, uma mensagem de sucesso é exibida. Se algum
    teste falhar, uma exceção AssertionError será levantada com detalhes
    sobre o que falhou.

    Note:
        Este é o ponto de entrada principal para validar a funcionalidade
        do Treinador através de testes de integração.

    Raises:
        AssertionError: Se algum dos testes falhar.

    Example:
        >>> executar_todos_testes()
        ==================================================
        🧪 INICIANDO BATERIA DE TESTES DO TREINADOR 🧪
        ==================================================
        ...
        ==================================================
        ✅ TODOS OS TESTES DO TREINADOR CONCLUÍDOS COM SUCESSO!
        ==================================================
    """
    print("\n" + "="*50)
    print("🧪 INICIANDO BATERIA DE TESTES DO TREINADOR 🧪")
    print("="*50 + "\n")
    
    # Executa os testes na ordem lógica
    testar_ciclo_de_treinamento_rapido()
    
    print("="*50)
    print("✅ TODOS OS TESTES DO TREINADOR CONCLUÍDOS COM SUCESSO!")
    print("="*50 + "\n")


# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    """
    Ponto de entrada do módulo quando executado diretamente.

    Quando o arquivo é executado como script (não importado como módulo),
    executa automaticamente toda a suíte de testes do Treinador.
    """
    executar_todos_testes()
