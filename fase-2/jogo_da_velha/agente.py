"""
Módulo: 🧠 agente.py
Projeto: 📘 AI Game Learning

Este módulo define o Agente que utiliza o algoritmo Q-Learning.
No paradigma de Aprendizado por Reforço, este código representa o "Agent".

Responsabilidades do Agente:
- Manter uma "memória de jogo", a Tabela Q (Q-Table).
- Decidir qual ação tomar, balanceando entre explorar e usar seu conhecimento.
- Aprender com os resultados de suas ações, atualizando sua memória.
"""

import random
import pickle
from typing import List, Tuple, Dict
from pathlib import Path

class AgenteQLearning:
    """
    Um Agente que aprende a jogar Jogo da Velha usando Q-Learning.
    
    Pense neste Agente como um jogador de Ragnarok Online que está aprendendo
    a melhor estratégia para derrotar monstros.

    Hiperparâmetros (os "atributos" do nosso jogador):
    - alpha (α): A "Velocidade de Aprendizado".
      * Quão rápido o jogador ajusta sua estratégia após uma batalha.
      * Valores altos = impulsivo, aprende rápido com uma única experiência.
      * Valores baixos = cético, precisa de muitas experiências para mudar de ideia.

    - gamma (γ): A "Visão de Futuro" (Fator de Desconto).
      * O quanto o jogador valoriza recompensas futuras.
      * Valor alto = estrategista, pensa nos próximos passos.
      * Valor baixo = imediatista, foca apenas na recompensa de agora.

    - epsilon (ε): O "Medidor de Curiosidade" (Taxa de Exploração).
      * A chance do jogador tentar uma tática nova e desconhecida.
      * Valor alto = aventureiro, adora explorar o mapa.
      * Valor baixo = conservador, prefere usar a tática que já sabe que funciona.
    """

    def __init__(self,
                 alpha: float = 0.5,
                 gamma: float = 0.9,
                 epsilon: float = 1.0,
                 epsilon_minimo: float = 0.01,
                 taxa_decaimento_epsilon: float = 0.9995,
                 jogador: int = 1):
        """
        Inicializa os atributos e a memória do Agente.
        """
        # --- HIPERPARÂMETROS (Atributos do Agente) ---
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_minimo = epsilon_minimo
        self.taxa_decaimento_epsilon = taxa_decaimento_epsilon

        # --- IDENTIDADE ---
        self.jogador = jogador
        self.simbolo = 'X' if jogador == 1 else 'O'

        # --- MEMÓRIA (A "Enciclopédia de Monstros" do Jogador) ---
        self.tabela_q: Dict[Tuple, Dict[int, float]] = {}

        # --- ESTATÍSTICAS DE TREINO ---
        self.partidas_treinadas = 0
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0
        
        # --- MEMÓRIA DE CURTO PRAZO (para a partida atual) ---
        self.historico_partida: List[Tuple[Tuple, int]] = []

    def obter_valor_q(self, estado: Tuple, acao: int) -> float:
        """
        Consulta a "memória" para ver o valor de uma ação em um estado.
        Se o Agente nunca viu essa situação antes, ele assume que o valor é 0.
        """
        if estado not in self.tabela_q:
            self.tabela_q[estado] = {}
        if acao not in self.tabela_q[estado]:
            self.tabela_q[estado][acao] = 0.0
        return self.tabela_q[estado][acao]

    def atualizar_valor_q(self, estado: Tuple, acao: int, recompensa: float, proximo_estado: Tuple):
        """
        Atualiza a "memória" do Agente usando a Equação de Bellman.
        É aqui que o aprendizado realmente acontece.
        """
        opiniao_antiga = self.obter_valor_q(estado, acao)
        melhor_valor_futuro = self._obter_melhor_valor_q_do_estado(proximo_estado)
        valor_real_da_jogada = recompensa + self.gamma * melhor_valor_futuro
        surpresa = valor_real_da_jogada - opiniao_antiga
        novo_valor_q = opiniao_antiga + self.alpha * surpresa
        self.tabela_q[estado][acao] = novo_valor_q

    def _obter_melhor_valor_q_do_estado(self, estado: Tuple) -> float:
        """
        Verifica na "memória" qual é a melhor jogada possível a partir de um estado.
        """
        if estado not in self.tabela_q or not self.tabela_q[estado]:
            return 0.0
        return max(self.tabela_q[estado].values())

    def escolher_acao(self, estado: Tuple, acoes_validas: List[int], em_treinamento: bool = True) -> int:
        """
        Decide qual jogada fazer usando a estratégia Epsilon-Greedy.
        """
        if not acoes_validas:
            raise ValueError("Não há ações válidas para escolher.")
        if not em_treinamento:
            return self._escolher_melhor_acao(estado, acoes_validas)
        if random.random() < self.epsilon:
            return random.choice(acoes_validas)
        else:
            return self._escolher_melhor_acao(estado, acoes_validas)

    def _escolher_melhor_acao(self, estado: Tuple, acoes_validas: List[int]) -> int:
        """
        Consulta a "memória" e escolhe a ação com o maior valor Q.
        """
        valores_q_das_acoes = {acao: self.obter_valor_q(estado, acao) for acao in acoes_validas}
        valor_maximo_q = max(valores_q_das_acoes.values())
        melhores_acoes = [acao for acao, valor in valores_q_das_acoes.items() if valor == valor_maximo_q]
        return random.choice(melhores_acoes)

    # --- MÉTODOS PARA O CICLO DE TREINAMENTO (GERENCIADOS PELO TREINADOR) ---

    def iniciar_nova_partida(self):
        """ Limpa a memória de curto prazo para o início de uma nova partida. """
        self.historico_partida = []

    def registrar_jogada(self, estado: Tuple, acao: int):
        """ Guarda a jogada (estado, ação) feita nesta partida. """
        self.historico_partida.append((estado, acao))

    def aprender_com_fim_de_partida(self, recompensa_final: float):
        """
        Processa o histórico da partida finalizada para aprender com ela.
        Este método é chamado pelo Treinador ao final de cada jogo.
        """
        self.partidas_treinadas += 1
        if recompensa_final > 0: self.vitorias += 1
        elif recompensa_final < 0: self.derrotas += 1
        else: self.empates += 1

        # Propaga a recompensa final para trás, valorizando as jogadas
        # que levaram a este resultado.
        for estado, acao in reversed(self.historico_partida):
            # Para este método de aprendizado, o "próximo estado" não é relevante,
            # apenas a recompensa final que foi alcançada.
            self.atualizar_valor_q(estado, acao, recompensa_final, estado)
            # A recompensa perde um pouco de força a cada passo para trás.
            recompensa_final *= self.gamma
        
        self.reduzir_epsilon()

    def reduzir_epsilon(self):
        """
        Reduz a "curiosidade" do Agente, tornando-o mais confiante em seu
        conhecimento com o passar do tempo.
        """
        self.epsilon = max(self.epsilon_minimo, self.epsilon * self.taxa_decaimento_epsilon)

    def salvar_memoria(self, caminho: str = "agente_treinado.pkl"):
        """
        Salva o conhecimento do Agente (a Tabela Q) em um arquivo.
        """
        caminho_arquivo = Path(caminho)
        caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
        
        with open(caminho_arquivo, 'wb') as arquivo:
            pickle.dump(self.tabela_q, arquivo)
        print(f"💾 Memória do Agente ({self.simbolo}) salva em: {caminho_arquivo}")

    @classmethod
    def carregar(cls, caminho: str, **kwargs) -> 'AgenteQLearning':
        """
        Cria uma instância de Agente e carrega seu conhecimento de um arquivo.
        Permite sobrescrever hiperparâmetros no momento do carregamento.
        """
        # Cria um novo agente, passando quaisquer hiperparâmetros customizados
        agente = cls(**kwargs)
        
        caminho_arquivo = Path(caminho)
        if caminho_arquivo.exists():
            with open(caminho_arquivo, 'rb') as arquivo:
                agente.tabela_q = pickle.load(arquivo)
            print(f"✅ Memória do Agente ({agente.simbolo}) carregada de: {caminho_arquivo}")
            print(f"   - O Agente conhece {len(agente.tabela_q):,} situações de jogo.")
        else:
            print(f"⚠️  Aviso: Nenhum arquivo de memória encontrado em {caminho}. O Agente ({agente.simbolo}) começará do zero.")
        return agente

    def obter_estatisticas(self) -> Dict:
        """ Retorna um dicionário com as estatísticas de desempenho do Agente. """
        total_jogos = self.vitorias + self.derrotas + self.empates
        if total_jogos == 0: return {"taxa_vitoria": 0.0, "taxa_empate": 0.0, "taxa_derrota": 0.0}

        return {
            'partidas_treinadas': self.partidas_treinadas,
            'estados_conhecidos': len(self.tabela_q),
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
        """ Imprime as estatísticas de forma legível no console. """
        stats = self.obter_estatisticas()
        
        print(f"\n{'='*50}")
        print(f"📊 ESTATÍSTICAS DO AGENTE ({stats.get('jogador', '?')})")
        print(f"{'='*50}")
        print(f"Partidas treinadas:   {stats.get('partidas_treinadas', 0):,}")
        print(f"Estados conhecidos:   {stats.get('estados_conhecidos', 0):,}")
        print(f"Curiosidade (Epsilon):{stats.get('epsilon_atual', 0.0):.4f}")
        print(f"\n--- Desempenho ---")
        print(f"Vitórias:   {stats.get('vitorias', 0):>6} ({stats.get('taxa_vitoria', 0.0)*100:>5.1f}%)")
        print(f"Empates:    {stats.get('empates', 0):>6} ({stats.get('taxa_empate', 0.0)*100:>5.1f}%)")
        print(f"Derrotas:   {stats.get('derrotas', 0):>6} ({stats.get('taxa_derrota', 0.0)*100:>5.1f}%)")
        print(f"{'='*50}\n")