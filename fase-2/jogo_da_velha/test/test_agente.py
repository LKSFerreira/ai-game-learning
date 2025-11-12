"""
Módulo: 🧪 test_agente.py
Projeto: 📘 AI Game Learning

Este módulo contém uma suíte completa de testes unitários para a classe AgenteQLearning.
Os testes verificam se o agente de aprendizado por reforço está funcionando corretamente,
incluindo inicialização, aprendizado Q-Learning e estratégia de escolha de ações.

Os testes são projetados para serem didáticos e educativos, explicando claramente
o que está sendo testado e por quê. Eles servem tanto como validação do código
quanto como material de aprendizado sobre Q-Learning.

Para executar os testes, use um dos seguintes comandos:
    - python fase-2/jogo_da_velha/test/test_agente.py
    - py -m test.test_agente (a partir do diretório fase-2/jogo_da_velha)
"""

from agente import AgenteQLearning


def testar_inicializacao():
    """
    Testa se o AgenteQLearning é inicializado corretamente com os atributos esperados.

    Este teste verifica:
    - Se o agente pode ser criado com parâmetros personalizados
    - Se os atributos são definidos corretamente (jogador, símbolo, alpha, etc.)
    - Se a tabela Q começa vazia (sem conhecimento prévio)

    O teste cria um agente como jogador 'O' (jogador=2) e verifica se todos
    os atributos estão configurados conforme esperado.

    Raises:
        AssertionError: Se algum atributo do agente não estiver correto.

    Example:
        >>> testar_inicializacao()
        --- INICIANDO TESTE 1: INICIALIZAÇÃO DO AGENTE ---
        ✅ Agente criado com sucesso como jogador 'O'.
        --- TESTE 1 FINALIZADO ---
    """
    print("--- INICIANDO TESTE 1: INICIALIZAÇÃO DO AGENTE ---")
    
    # Cria um agente como jogador 'O' (jogador=2)
    agente = AgenteQLearning(jogador=2)
    
    # Verifica se o identificador do jogador está correto
    assert agente.jogador == 2, "O jogador deveria ser 2 (jogador 'O')"
    
    # Verifica se o símbolo está correto
    assert agente.simbolo == 'O', "O símbolo deveria ser 'O' para jogador 2"
    
    # Verifica se a taxa de aprendizado padrão está correta
    assert agente.alpha == 0.5, "A taxa de aprendizado (alpha) padrão deveria ser 0.5"
    
    # Verifica se a tabela Q começa vazia (sem conhecimento prévio)
    assert len(agente.tabela_q) == 0, "A tabela Q deveria começar vazia"
    
    print("✅ Agente criado com sucesso como jogador 'O'.")
    print("--- TESTE 1 FINALIZADO ---\n")


def testar_aprendizado_q_learning():
    """
    Testa se o algoritmo Q-Learning está aplicando a Equação de Bellman corretamente.

    Este teste verifica se o método aprender() está calculando e atualizando os valores Q
    de acordo com a fórmula do Q-Learning:

        Q(estado, ação) = Q(estado, ação) + alpha * (recompensa + gamma * max(Q(próximo_estado)) - Q(estado, ação))

    O teste simula um cenário específico:
    - Estado inicial: tabuleiro vazio
    - Ação escolhida: jogar no centro (posição 4)
    - Próximo estado: tabuleiro com X no centro
    - Melhor valor Q futuro conhecido: 0.8
    - Recompensa imediata: 0.0 (jogo continua)

    Cálculo esperado:
        Q_novo = 0 + 0.5 * (0 + 0.9 * 0.8 - 0) = 0.36

    Este teste é fundamental para garantir que o agente está aprendendo corretamente
    e ajustando seus valores Q baseado nas recompensas futuras esperadas.

    Raises:
        AssertionError: Se o valor Q calculado não corresponder ao valor esperado.

    Note:
        Este teste valida a implementação do aprendizado Temporal Difference (TD),
        que é o coração do algoritmo Q-Learning.
    """
    print("--- INICIANDO TESTE 2: APRENDIZADO (ATUALIZAÇÃO DE Q-VALOR) ---")
    
    # Cria um agente com parâmetros específicos para o teste
    agente = AgenteQLearning(alpha=0.5, gamma=0.9)
    
    # Define o estado inicial: tabuleiro completamente vazio
    estado_inicial = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    # Ação escolhida: jogar no centro do tabuleiro (posição 4)
    posicao_escolhida = 4
    
    # Próximo estado após a jogada: X no centro
    proximo_estado = (0, 0, 0, 0, 1, 0, 0, 0, 0)
    
    # Recompensa imediata: 0.0 (o jogo continua, não há vitória/derrota ainda)
    recompensa_imediata = 0.0
    
    # Simula que já conhecemos algumas ações no próximo estado
    # A melhor ação futura tem valor Q de 0.8
    agente.tabela_q[proximo_estado] = {0: 0.5, 1: 0.8, 2: 0.3}
    
    # Obtém o valor Q atual (deve ser 0.0, pois é um estado novo)
    valor_q_antigo = agente.obter_valor_q(estado_inicial, posicao_escolhida)
    print(f"Opinião antiga sobre jogar no centro: {valor_q_antigo}")
    
    # Aplica o aprendizado Q-Learning
    # finalizado=False porque o jogo ainda não terminou
    agente.atualizar_valor_q(
        estado_inicial,
        posicao_escolhida,
        recompensa_imediata,
        proximo_estado,
        finalizado=False
    )
    
    # Obtém o novo valor Q após o aprendizado
    valor_q_novo = agente.obter_valor_q(estado_inicial, posicao_escolhida)
    
    # Cálculo esperado usando a fórmula do Q-Learning:
    # Q_novo = 0 + 0.5 * (0 + 0.9 * 0.8 - 0) = 0.36
    print(f"Nova opinião sobre jogar no centro: {valor_q_novo:.2f}")
    
    # Verifica se o cálculo está correto (com tolerância para arredondamento)
    assert round(valor_q_novo, 2) == 0.36, (
        f"O valor Q deveria ser 0.36, mas foi {valor_q_novo:.2f}. "
        "A fórmula do Q-Learning pode estar incorreta."
    )
    
    print("✅ O Agente ajustou sua estratégia corretamente!")
    print("--- TESTE 2 FINALIZADO ---\n")


def testar_estrategia_epsilon_greedy():
    """
    Testa se a estratégia Epsilon-Greedy está funcionando corretamente.

    A estratégia Epsilon-Greedy é fundamental para o aprendizado por reforço, pois
    equilibra dois comportamentos importantes:
    - Exploração: tentar ações novas/aleatórias para descobrir estratégias melhores
    - Exploração: usar o conhecimento já adquirido para escolher as melhores ações

    Este teste verifica dois cenários extremos:
    1. Agente Aventureiro (epsilon=1.0): sempre explora, escolhendo ações aleatórias
    2. Agente Estrategista (epsilon=0.0): sempre explora, escolhendo a melhor ação conhecida

    O teste garante que:
    - Com epsilon alto, o agente escolhe ações aleatórias (exploração)
    - Com epsilon baixo, o agente escolhe a ação com maior valor Q (exploração)
    - A ação escolhida sempre está na lista de ações válidas

    Raises:
        AssertionError: Se a estratégia Epsilon-Greedy não estiver funcionando corretamente.

    Note:
        Em um cenário real, epsilon geralmente começa alto (1.0) e decai gradualmente,
        permitindo que o agente explore no início e depois explore mais conforme aprende.
    """
    print("--- INICIANDO TESTE 3: ESCOLHA DE AÇÃO (EPSILON-GREEDY) ---")
    
    # Define um estado de teste: algumas posições já ocupadas
    estado_teste = (1, 2, 0, 0, 0, 0, 0, 0, 0)
    
    # Lista de ações válidas (posições vazias no tabuleiro)
    acoes_validas = [2, 3, 4, 5, 6, 7, 8]
    
    # --- CENÁRIO 1: AGENTE AVENTUREIRO (100% Exploração) ---
    # Epsilon = 1.0 significa 100% de chance de escolher uma ação aleatória
    agente_aventureiro = AgenteQLearning(epsilon=1.0)
    acao_escolhida_aventureiro = agente_aventureiro.escolher_acao(
        estado_teste,
        acoes_validas,
        em_treinamento=True
    )
    print(f"Agente Aventureiro (ε=1.0) escolheu a ação: {acao_escolhida_aventureiro}")
    
    # Verifica se a ação escolhida está na lista de ações válidas
    assert acao_escolhida_aventureiro in acoes_validas, (
        f"A ação escolhida ({acao_escolhida_aventureiro}) deve estar na lista de ações válidas."
    )
    
    # --- CENÁRIO 2: AGENTE ESTRATEGISTA (100% Exploração) ---
    # Epsilon = 0.0 significa 0% de chance de explorar, sempre escolhe a melhor ação
    agente_estrategista = AgenteQLearning(epsilon=0.0)
    
    # Pré-popula a tabela Q com valores conhecidos
    # A ação 4 tem o maior valor Q (0.9), então deve ser escolhida
    agente_estrategista.tabela_q[estado_teste] = {
        2: 0.5,  # Ação 2: valor Q médio
        3: 0.1,  # Ação 3: valor Q baixo
        4: 0.9   # Ação 4: valor Q alto (melhor ação)
    }
    
    acao_escolhida_estrategista = agente_estrategista.escolher_acao(
        estado_teste,
        acoes_validas,
        em_treinamento=True
    )
    print(f"Agente Estrategista (ε=0.0) escolheu a ação: {acao_escolhida_estrategista}")
    
    # Verifica se escolheu a melhor ação conhecida (ação 4 com valor Q 0.9)
    assert acao_escolhida_estrategista == 4, (
        f"Com epsilon=0.0, o agente deveria escolher a melhor ação (4), "
        f"mas escolheu {acao_escolhida_estrategista}."
    )
    
    print("✅ O Agente está balanceando exploração e estratégia como esperado.")
    print("--- TESTE 3 FINALIZADO ---\n")


def executar_todos_testes():
    """
    Executa toda a suíte de testes do AgenteQLearning.

    Esta função orquestra a execução de todos os testes unitários, fornecendo
    feedback claro sobre o progresso e resultados de cada teste. Ela serve
    como ponto de entrada principal para validar a funcionalidade do agente.

    A ordem dos testes é importante:
    1. Teste de inicialização (base para todos os outros)
    2. Teste de aprendizado (validação do algoritmo Q-Learning)
    3. Teste de escolha de ação (validação da estratégia Epsilon-Greedy)

    Se todos os testes passarem, uma mensagem de sucesso é exibida. Se algum
    teste falhar, uma exceção AssertionError será levantada com detalhes sobre
    o que falhou.

    Raises:
        AssertionError: Se algum dos testes falhar.

    Example:
        >>> executar_todos_testes()
        ==================================================
        🧪 INICIANDO BATERIA DE TESTES DO AGENTE 🧪
        ==================================================
        ...
        ==================================================
        ✅ TODOS OS TESTES DO AGENTE CONCLUÍDOS COM SUCESSO!
        ==================================================
    """
    print("\n" + "="*50)
    print("🧪 INICIANDO BATERIA DE TESTES DO AGENTE 🧪")
    print("="*50 + "\n")
    
    # Executa os testes na ordem lógica
    testar_inicializacao()
    testar_aprendizado_q_learning()
    testar_estrategia_epsilon_greedy()
    
    print("="*50)
    print("✅ TODOS OS TESTES DO AGENTE CONCLUÍDOS COM SUCESSO!")
    print("="*50 + "\n")


if __name__ == "__main__":
    """
    Ponto de entrada do módulo quando executado diretamente.

    Quando o arquivo é executado como script (não importado como módulo),
    executa automaticamente toda a suíte de testes.
    """
    executar_todos_testes()
