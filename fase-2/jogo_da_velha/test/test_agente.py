"""
Módulo: 🧪 test_agente.py
Projeto: 📘 AI Game Learning

Este arquivo contém testes para a classe AgenteQLearning, verificando
se o "cérebro" da nossa IA funciona como esperado.

Para executar, use o comando no terminal:
python fase-2_jogo_velha/test_agente.py
"""

from agente import AgenteQLearning

def testar_inicializacao():
    """Verifica se o Agente é criado com os atributos corretos."""
    print("--- INICIANDO TESTE 1: INICIALIZAÇÃO DO AGENTE ---")
    agente = AgenteQLearning(jogador=2)
    
    assert agente.jogador == 2
    assert agente.simbolo == 'O'
    assert agente.alpha == 0.5
    assert len(agente.tabela_q) == 0
    
    print("✅ Agente criado com sucesso como jogador 'O'.")
    print("--- TESTE 1 FINALIZADO ---\n")

def testar_atualizacao_q_valor():
    """Testa se a Equação de Bellman está sendo aplicada corretamente."""
    print("--- INICIANDO TESTE 2: APRENDIZADO (ATUALIZAÇÃO DE Q-VALOR) ---")
    agente = AgenteQLearning(alpha=0.5, gamma=0.9)
    
    estado_inicial = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    acao = 4 # Jogar no centro
    proximo_estado = (0, 0, 0, 0, 1, 0, 0, 0, 0)
    recompensa = 0.0
    
    # Simula que a melhor jogada futura vale 0.8
    agente.tabela_q[proximo_estado] = {0: 0.5, 1: 0.8, 2: 0.3}
    
    valor_antigo = agente.obter_valor_q(estado_inicial, acao)
    print(f"Opinião antiga sobre jogar no centro: {valor_antigo}")
    
    agente.atualizar_valor_q(estado_inicial, acao, recompensa, proximo_estado)
    
    valor_novo = agente.obter_valor_q(estado_inicial, acao)
    # Cálculo esperado: 0 + 0.5 * (0 + 0.9 * 0.8 - 0) = 0.36
    print(f"Nova opinião sobre jogar no centro: {valor_novo:.2f}")
    assert round(valor_novo, 2) == 0.36
    
    print("✅ O Agente ajustou sua estratégia corretamente!")
    print("--- TESTE 2 FINALIZADO ---\n")

def testar_escolha_de_acao():
    """Verifica se a estratégia Epsilon-Greedy funciona."""
    print("--- INICIANDO TESTE 3: ESCOLHA DE AÇÃO (EPSILON-GREEDY) ---")
    estado = (1, 2, 0, 0, 0, 0, 0, 0, 0)
    acoes_validas = [2, 3, 4, 5, 6, 7, 8]
    
    # Cenário 1: Agente Aventureiro (epsilon alto)
    agente_aventureiro = AgenteQLearning(epsilon=1.0) # 100% de chance de explorar
    acao_escolhida = agente_aventureiro.escolher_acao(estado, acoes_validas)
    print(f"Agente Aventureiro (ε=1.0) escolheu a ação: {acao_escolhida}")
    assert acao_escolhida in acoes_validas

    # Cenário 2: Agente Estrategista (epsilon baixo)
    agente_estrategista = AgenteQLearning(epsilon=0.0) # 0% de chance de explorar
    agente_estrategista.tabela_q[estado] = {2: 0.5, 3: 0.1, 4: 0.9} # Ação 4 é a melhor
    acao_escolhida = agente_estrategista.escolher_acao(estado, acoes_validas)
    print(f"Agente Estrategista (ε=0.0) escolheu a ação: {acao_escolhida}")
    assert acao_escolhida == 4
    
    print("✅ O Agente está balanceando exploração e estratégia como esperado.")
    print("--- TESTE 3 FINALIZADO ---\n")

def executar_todos_testes():
    """Função principal para rodar toda a suíte de testes."""
    print("\n" + "="*50)
    print("🧪 INICIANDO BATERIA DE TESTES DO AGENTE 🧪")
    print("="*50 + "\n")
    
    testar_inicializacao()
    testar_atualizacao_q_valor()
    testar_escolha_de_acao()
    
    print("="*50)
    print("✅ TODOS OS TESTES DO AGENTE CONCLUÍDOS COM SUCESSO!")
    print("="*50 + "\n")

if __name__ == "__main__":
    executar_todos_testes()