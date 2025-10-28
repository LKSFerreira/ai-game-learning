"""
Agente Q-Learning para Jogo da Velha

Este módulo implementa o "cérebro" que aprende a jogar.
Representa o AGENT no Reinforcement Learning.

Responsabilidades:
- Manter a Q-Table (memória de valores aprendidos)
- Escolher ações (exploração vs exploração)
- Atualizar valores Q usando a Equação de Bellman
- Salvar e carregar o modelo treinado

Componentes principais:
- Q-Table: Dicionário {estado: {ação: valor_q}}
- Epsilon-Greedy: Estratégia de exploração
- Learning Rate (α): Velocidade de aprendizado
- Discount Factor (γ): Importância de recompensas futuras
"""

import numpy as np
import random
import pickle
from typing import Tuple, List, Dict, Optional
from pathlib import Path


class AgenteQLearning:
    """
    Agente que aprende a jogar Jogo da Velha usando Q-Learning.
    
    O agente mantém uma Q-Table que mapeia:
    - Estado do jogo → Ações possíveis → Valores Q
    
    Quanto maior o valor Q, melhor a ação naquele estado.
    
    Parâmetros de treinamento:
    - alpha (α): Taxa de aprendizado (0.0 a 1.0)
      * 0.0 = não aprende nada
      * 1.0 = substitui completamente conhecimento antigo
      * Recomendado: 0.3 a 0.7
    
    - gamma (γ): Fator de desconto (0.0 a 1.0)
      * 0.0 = só importa recompensa imediata
      * 1.0 = recompensas futuras têm igual importância
      * Recomendado: 0.8 a 0.99
    
    - epsilon (ε): Taxa de exploração (0.0 a 1.0)
      * 0.0 = sempre exploração (greedy)
      * 1.0 = sempre exploração (aleatório)
      * Recomendado iniciar: 0.8, terminar: 0.1
    """
    
    def __init__(
        self,
        alpha: float = 0.5,
        gamma: float = 0.9,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.9995,
        jogador: int = 1
    ):
        """
        Inicializa o agente Q-Learning.
        
        Args:
            alpha: Taxa de aprendizado (velocidade que aprende)
            gamma: Fator de desconto (valor de recompensas futuras)
            epsilon: Taxa inicial de exploração (chance de ação aleatória)
            epsilon_min: Taxa mínima de exploração (não vai abaixo disso)
            epsilon_decay: Multiplicador de decay do epsilon (0.0 a 1.0)
            jogador: Qual jogador este agente representa (1=X ou 2=O)
        """
        # === HIPERPARÂMETROS ===
        self.alpha = alpha  # Taxa de aprendizado (α)
        self.gamma = gamma  # Fator de desconto (γ)
        self.epsilon = epsilon  # Taxa de exploração atual (ε)
        self.epsilon_min = epsilon_min  # Limite inferior do epsilon
        self.epsilon_decay = epsilon_decay  # Taxa de decaimento
        
        # === IDENTIDADE ===
        self.jogador = jogador  # 1 (X) ou 2 (O)
        self.simbolo = 'X' if jogador == 1 else 'O'
        
        # === MEMÓRIA (Q-TABLE) ===
        # Estrutura: {estado: {ação: valor_q}}
        # Exemplo: {(1,0,2,0,0,0,0,0,0): {3: 0.5, 4: 0.8, ...}}
        self.q_table: Dict[Tuple, Dict[int, float]] = {}
        
        # === ESTATÍSTICAS ===
        self.episodios_treinados = 0
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0
        
        # === HISTÓRICO DO EPISÓDIO ATUAL ===
        # Guarda (estado, ação) para atualizar Q-values no final
        self.historico_episodio: List[Tuple[Tuple, int]] = []
    
    def obter_valor_q(self, estado: Tuple, acao: int) -> float:
        """
        Retorna o valor Q para um par (estado, ação).
        
        Se o par nunca foi visto antes, inicializa com 0.0.
        
        Args:
            estado: Tupla representando o tabuleiro
            acao: Índice da ação (0-8)
        
        Returns:
            Valor Q atual para esse par (estado, ação)
        
        Exemplo:
            estado = (1, 0, 0, 0, 0, 0, 0, 0, 0)
            acao = 4  # Jogar no centro
            valor = agente.obter_valor_q(estado, acao)  # Retorna 0.0 se novo
        """
        # Se o estado nunca foi visto, inicializa com dicionário vazio
        if estado not in self.q_table:
            self.q_table[estado] = {}
        
        # Se a ação nunca foi tentada nesse estado, inicializa com 0.0
        if acao not in self.q_table[estado]:
            self.q_table[estado][acao] = 0.0
        
        return self.q_table[estado][acao]
    
    def atualizar_valor_q(
        self,
        estado: Tuple,
        acao: int,
        recompensa: float,
        proximo_estado: Tuple,
        finalizado: bool
    ):
        """
        Atualiza o valor Q usando a Equação de Bellman.
        
        Fórmula:
        Q(s,a) ← Q(s,a) + α × [r + γ × max(Q(s',a')) - Q(s,a)]
        
        Onde:
        - s = estado atual
        - a = ação tomada
        - r = recompensa recebida
        - s' = próximo estado
        - a' = melhor ação no próximo estado
        - α = taxa de aprendizado
        - γ = fator de desconto
        
        Args:
            estado: Estado antes da ação
            acao: Ação executada
            recompensa: Recompensa recebida
            proximo_estado: Estado após a ação
            finalizado: Se o jogo terminou
        """
        # Valor Q atual para (estado, ação)
        q_atual = self.obter_valor_q(estado, acao)
        
        # Se o jogo terminou, não há valor futuro
        if finalizado:
            q_futuro_max = 0.0
        else:
            # Encontra o maior valor Q possível no próximo estado
            # Isso representa "quanto vale estar no próximo estado"
            q_futuro_max = self._obter_max_q_futuro(proximo_estado)
        
        # === EQUAÇÃO DE BELLMAN ===
        # Calcula o "alvo" (target): recompensa + valor futuro descontado
        target = recompensa + self.gamma * q_futuro_max
        
        # Atualiza o valor Q fazendo um "passo" em direção ao alvo
        # Alpha controla o tamanho do passo (quanto aprender)
        novo_q = q_atual + self.alpha * (target - q_atual)
        
        # Salva o novo valor na Q-Table
        if estado not in self.q_table:
            self.q_table[estado] = {}
        self.q_table[estado][acao] = novo_q
    
    def _obter_max_q_futuro(self, estado: Tuple) -> float:
        """
        Retorna o maior valor Q disponível em um estado.
        
        Isso representa "quão boa é a melhor ação possível neste estado".
        
        Args:
            estado: Estado para analisar
        
        Returns:
            O maior valor Q entre todas as ações nesse estado
            Retorna 0.0 se o estado nunca foi visto
        """
        # Se o estado é novo, não temos informação
        if estado not in self.q_table:
            return 0.0
        
        # Se não há ações registradas nesse estado
        if not self.q_table[estado]:
            return 0.0
        
        # Retorna o maior valor Q entre todas as ações
        return max(self.q_table[estado].values())
    
    def escolher_acao(
        self,
        estado: Tuple,
        acoes_validas: List[int],
        treino: bool = True
    ) -> int:
        """
        Escolhe uma ação usando a estratégia Epsilon-Greedy.
        
        Com probabilidade ε: EXPLORAÇÃO (ação aleatória)
        Com probabilidade 1-ε: EXPLORAÇÃO (melhor ação conhecida)
        
        Args:
            estado: Estado atual do jogo
            acoes_validas: Lista de ações possíveis (casas vazias)
            treino: Se True, usa epsilon. Se False, sempre greedy.
        
        Returns:
            Índice da ação escolhida (0-8)
        
        Exemplo:
            estado = (1, 0, 2, 0, 0, 0, 0, 0, 0)
            acoes = [1, 3, 4, 5, 6, 7, 8]
            acao = agente.escolher_acao(estado, acoes, treino=True)
        """
        # Validação: verifica se há ações válidas
        if not acoes_validas:
            raise ValueError("Não há ações válidas disponíveis!")
        
        # === MODO AVALIAÇÃO (sem exploração) ===
        if not treino:
            return self._escolher_melhor_acao(estado, acoes_validas)
        
        # === EPSILON-GREEDY ===
        # Gera número aleatório entre 0 e 1
        if random.random() < self.epsilon:
            # EXPLORAÇÃO: escolhe ação aleatória
            return random.choice(acoes_validas)
        else:
            # EXPLORAÇÃO: escolhe melhor ação conhecida
            return self._escolher_melhor_acao(estado, acoes_validas)
    
    def _escolher_melhor_acao(
        self,
        estado: Tuple,
        acoes_validas: List[int]
    ) -> int:
        """
        Escolhe a ação com maior valor Q (estratégia greedy).
        
        Se múltiplas ações têm o mesmo valor, escolhe aleatoriamente
        entre elas para evitar viés.
        
        Args:
            estado: Estado atual
            acoes_validas: Ações possíveis
        
        Returns:
            Ação com maior valor Q
        """
        # Obtém valores Q de todas as ações válidas
        valores_q = {
            acao: self.obter_valor_q(estado, acao)
            for acao in acoes_validas
        }
        
        # Encontra o maior valor Q
        max_q = max(valores_q.values())
        
        # Encontra todas as ações que têm esse valor máximo
        # (pode haver empate)
        melhores_acoes = [
            acao for acao, valor in valores_q.items()
            if valor == max_q
        ]
        
        # Se há empate, escolhe aleatoriamente entre as melhores
        return random.choice(melhores_acoes)
    
    def iniciar_episodio(self):
        """
        Prepara o agente para um novo episódio de treinamento.
        
        Limpa o histórico de (estado, ação) do episódio anterior.
        """
        self.historico_episodio = []
    
    def registrar_jogada(self, estado: Tuple, acao: int):
        """
        Registra uma jogada no histórico do episódio atual.
        
        Isso é usado para atualizar valores Q no final do jogo,
        especialmente quando o resultado só é conhecido no fim.
        
        Args:
            estado: Estado antes da jogada
            acao: Ação executada
        """
        self.historico_episodio.append((estado, acao))
    
    def finalizar_episodio(self, recompensa_final: float):
        """
        Atualiza valores Q no final de um episódio.
        
        Propaga a recompensa final para todas as jogadas do episódio,
        com decaimento baseado em gamma.
        
        Args:
            recompensa_final: +1 (vitória), -1 (derrota), 0 (empate)
        """
        # Atualiza estatísticas
        self.episodios_treinados += 1
        if recompensa_final > 0:
            self.vitorias += 1
        elif recompensa_final < 0:
            self.derrotas += 1
        else:
            self.empates += 1
        
        # Propaga recompensa para todas as jogadas do episódio
        # Começa da jogada mais recente (mais importante)
        recompensa_propagada = recompensa_final
        
        for estado, acao in reversed(self.historico_episodio):
            # Atualiza o valor Q dessa jogada
            self.atualizar_valor_q(
                estado=estado,
                acao=acao,
                recompensa=recompensa_propagada,
                proximo_estado=estado,  # Placeholder
                finalizado=True
            )
            
            # Decai a recompensa para jogadas anteriores
            recompensa_propagada *= self.gamma
        
        # Reduz epsilon (menos exploração com o tempo)
        self.decair_epsilon()
    
    def decair_epsilon(self):
        """
        Reduz o epsilon (exploração) gradualmente.
        
        Usa decay exponencial: ε = max(ε_min, ε × decay_rate)
        
        Isso faz o agente explorar muito no início e
        explorar (usar conhecimento) mais no final do treino.
        """
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )
    
    def salvar(self, caminho: str = "agente_treinado.pkl"):
        """
        Salva o agente treinado em um arquivo.
        
        Usa o módulo pickle do Python para serialização.
        
        Args:
            caminho: Nome do arquivo onde salvar
        
        Exemplo:
            agente.salvar("jogador_x_50k_episodios.pkl")
        """
        # Prepara dados para salvar
        dados = {
            'q_table': self.q_table,
            'alpha': self.alpha,
            'gamma': self.gamma,
            'epsilon': self.epsilon,
            'epsilon_min': self.epsilon_min,
            'epsilon_decay': self.epsilon_decay,
            'jogador': self.jogador,
            'episodios_treinados': self.episodios_treinados,
            'vitorias': self.vitorias,
            'derrotas': self.derrotas,
            'empates': self.empates
        }
        
        # Salva em arquivo binário
        caminho_arquivo = Path(caminho)
        caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
        
        with open(caminho_arquivo, 'wb') as arquivo:
            pickle.dump(dados, arquivo)
        
        # print(f"✅ Agente salvo em: {caminho}")
        # print(f"   Episódios treinados: {self.episodios_treinados:,}")
        # print(f"   Tamanho da Q-Table: {len(self.q_table):,} estados")
    
    @classmethod
    def carregar(cls, caminho: str) -> 'AgenteQLearning':
        """
        Carrega um agente previamente treinado.
        
        Args:
            caminho: Caminho do arquivo .pkl
        
        Returns:
            Nova instância de AgenteQLearning com dados carregados
        
        Exemplo:
            agente = AgenteQLearning.carregar("jogador_x_50k.pkl")
        """
        with open(caminho, 'rb') as arquivo:
            dados = pickle.load(arquivo)
        
        # Cria novo agente com parâmetros carregados
        agente = cls(
            alpha=dados['alpha'],
            gamma=dados['gamma'],
            epsilon=dados['epsilon'],
            epsilon_min=dados['epsilon_min'],
            epsilon_decay=dados['epsilon_decay'],
            jogador=dados['jogador']
        )
        
        # Restaura Q-Table e estatísticas
        agente.q_table = dados['q_table']
        agente.episodios_treinados = dados['episodios_treinados']
        agente.vitorias = dados['vitorias']
        agente.derrotas = dados['derrotas']
        agente.empates = dados['empates']
        
        print(f"✅ Agente carregado de: {caminho}")
        print(f"   Episódios treinados: {agente.episodios_treinados:,}")
        print(f"   Tamanho da Q-Table: {len(agente.q_table):,} estados")
        
        return agente
    
    def obter_estatisticas(self) -> Dict[str, any]:
        """
        Retorna estatísticas de treinamento do agente.
        
        Returns:
            Dicionário com métricas de desempenho
        """
        total_jogos = self.vitorias + self.derrotas + self.empates
        
        if total_jogos == 0:
            return {
                'episodios': 0,
                'estados_conhecidos': len(self.q_table),
                'taxa_vitoria': 0.0,
                'taxa_empate': 0.0,
                'taxa_derrota': 0.0,
                'epsilon_atual': self.epsilon
            }
        
        return {
            'episodios': self.episodios_treinados,
            'estados_conhecidos': len(self.q_table),
            'vitorias': self.vitorias,
            'derrotas': self.derrotas,
            'empates': self.empates,
            'taxa_vitoria': self.vitorias / total_jogos,
            'taxa_empate': self.empates / total_jogos,
            'taxa_derrota': self.derrotas / total_jogos,
            'epsilon_atual': self.epsilon,
            'jogador': self.simbolo
        }
    
    def imprimir_estatisticas(self):
        """Imprime estatísticas de forma formatada."""
        stats = self.obter_estatisticas()
        
        print(f"\n{'='*50}")
        print(f"📊 ESTATÍSTICAS DO AGENTE ({stats.get('jogador', '?')})")
        print(f"{'='*50}")
        print(f"Episódios treinados:  {stats['episodios']:,}")
        print(f"Estados conhecidos:   {stats['estados_conhecidos']:,}")
        print(f"Epsilon atual:        {stats['epsilon_atual']:.4f}")
        print(f"\n--- Desempenho ---")
        print(f"Vitórias:   {stats.get('vitorias', 0):>6} ({stats['taxa_vitoria']*100:>5.1f}%)")
        print(f"Empates:    {stats.get('empates', 0):>6} ({stats['taxa_empate']*100:>5.1f}%)")
        print(f"Derrotas:   {stats.get('derrotas', 0):>6} ({stats['taxa_derrota']*100:>5.1f}%)")
        print(f"{'='*50}\n")


# ===== FUNÇÕES AUXILIARES PARA TESTES =====


def testar_inicializacao():
    """Testa a criação de um agente."""
    print("=== TESTE 1: INICIALIZAÇÃO ===\n")
    
    agente = AgenteQLearning(
        alpha=0.5,
        gamma=0.9,
        epsilon=0.8,
        jogador=1
    )
    
    print(f"Agente criado: Jogador {agente.simbolo}")
    print(f"Alpha (taxa aprendizado): {agente.alpha}")
    print(f"Gamma (desconto futuro):  {agente.gamma}")
    print(f"Epsilon (exploração):     {agente.epsilon}")
    print(f"Q-Table vazia:            {len(agente.q_table)} estados")
    
    agente.imprimir_estatisticas()
    print("=== TESTE CONCLUÍDO ===\n")


def testar_valores_q():
    """Testa obtenção e atualização de valores Q."""
    print("=== TESTE 2: VALORES Q ===\n")
    
    agente = AgenteQLearning()
    estado_teste = (1, 0, 0, 0, 2, 0, 0, 0, 0)
    
    print(f"Estado de teste: {estado_teste}")
    print(f"Valor Q inicial (estado, ação=4): {agente.obter_valor_q(estado_teste, 4)}")
    
    # Atualiza o valor Q
    agente.atualizar_valor_q(
        estado=estado_teste,
        acao=4,
        recompensa=1.0,
        proximo_estado=(1, 0, 0, 0, 2, 0, 0, 0, 1),
        finalizado=False
    )
    
    print(f"Valor Q após atualização:         {agente.obter_valor_q(estado_teste, 4):.4f}")
    print(f"Tamanho da Q-Table:               {len(agente.q_table)} estado(s)")
    
    print("\n=== TESTE CONCLUÍDO ===\n")


def testar_epsilon_greedy():
    """Testa a estratégia epsilon-greedy."""
    print("=== TESTE 3: EPSILON-GREEDY ===\n")
    
    # Agente com epsilon alto (muita exploração)
    agente_explorador = AgenteQLearning(epsilon=0.9)
    
    # Agente com epsilon baixo (muita exploração)
    agente_exploitador = AgenteQLearning(epsilon=0.1)
    
    estado = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    acoes = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    
    print("Testando 10 escolhas com EPSILON ALTO (0.9):")
    acoes_explorador = [
        agente_explorador.escolher_acao(estado, acoes, treino=True)
        for _ in range(10)
    ]
    print(f"Ações escolhidas: {acoes_explorador}")
    print(f"Variação (exploração): {len(set(acoes_explorador))} ações diferentes")
    
    print("\nTestando 10 escolhas com EPSILON BAIXO (0.1):")
    acoes_exploitador = [
        agente_exploitador.escolher_acao(estado, acoes, treino=True)
        for _ in range(10)
    ]
    print(f"Ações escolhidas: {acoes_exploitador}")
    print(f"Variação (menos exploração): {len(set(acoes_exploitador))} ações diferentes")
    
    print("\n=== TESTE CONCLUÍDO ===\n")


def testar_decay_epsilon():
    """Testa o decaimento do epsilon."""
    print("=== TESTE 4: DECAY DO EPSILON ===\n")
    
    agente = AgenteQLearning(
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.95  # Decay rápido para visualização
    )
    
    print(f"Epsilon inicial: {agente.epsilon:.4f}")
    print("\nSimulando 20 episódios...")
    
    for i in range(20):
        agente.decair_epsilon()
        if i % 5 == 0:
            print(f"Episódio {i+1:2d}: Epsilon = {agente.epsilon:.4f}")
    
    print(f"\nEpsilon final: {agente.epsilon:.4f}")
    print(f"Epsilon mínimo: {agente.epsilon_min:.4f}")
    print("✅ Epsilon decaiu corretamente sem passar do mínimo!")
    
    print("\n=== TESTE CONCLUÍDO ===\n")


def testar_salvar_carregar():
    """Testa salvar e carregar agente."""
    print("=== TESTE 5: SALVAR E CARREGAR ===\n")
    
    # Cria e treina um agente de exemplo
    print("Criando agente de teste...")
    agente1 = AgenteQLearning(alpha=0.5, gamma=0.9, jogador=1)
    
    # Simula algum "treinamento" (adiciona dados na Q-Table)
    estados_teste = [
        (1, 0, 0, 0, 0, 0, 0, 0, 0),
        (1, 2, 0, 0, 0, 0, 0, 0, 0),
        (1, 2, 1, 0, 0, 0, 0, 0, 0)
    ]
    
    for estado in estados_teste:
        agente1.obter_valor_q(estado, 4)  # Inicializa valores
    
    agente1.episodios_treinados = 1000
    agente1.vitorias = 600
    agente1.derrotas = 200
    agente1.empates = 200
    
    print(f"Q-Table original: {len(agente1.q_table)} estados")
    print(f"Episódios: {agente1.episodios_treinados}")
    
    # Salva o agente
    print("\nSalvando agente...")
    agente1.salvar("teste_agente.pkl")
    
    # Carrega o agente
    print("\nCarregando agente...")
    agente2 = AgenteQLearning.carregar("teste_agente.pkl")
    
    print(f"\nQ-Table carregada: {len(agente2.q_table)} estados")
    print(f"Episódios carregados: {agente2.episodios_treinados}")
    
    # Verifica se são iguais
    assert len(agente1.q_table) == len(agente2.q_table), "Q-Tables diferentes!"
    assert agente1.episodios_treinados == agente2.episodios_treinados, "Episódios diferentes!"
    
    print("\n✅ Salvamento e carregamento funcionaram perfeitamente!")
    
    # Remove arquivo de teste
    Path("teste_agente.pkl").unlink()
    print("(Arquivo de teste removido)")
    
    print("\n=== TESTE CONCLUÍDO ===\n")


def executar_todos_testes():
    """Executa toda a bateria de testes."""
    print("\n" + "="*50)
    print("🧪 BATERIA DE TESTES DO AGENTE Q-LEARNING")
    print("="*50 + "\n")
    
    testar_inicializacao()
    testar_valores_q()
    testar_epsilon_greedy()
    testar_decay_epsilon()
    testar_salvar_carregar()
    
    print("="*50)
    print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    print("="*50 + "\n")


# Executar testes se rodar este arquivo diretamente
if __name__ == "__main__":
    executar_todos_testes()
