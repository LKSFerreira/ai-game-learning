"""
Módulo: 🧠 agente.py
Projeto: 📘 AI Game Learning

Este módulo define o Agente que utiliza o algoritmo Q-Learning.
Ele é projetado para ser compatível tanto com o treinamento em massa (treinador.py)
quanto com o aprendizado interativo (jogar.py).
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
    """

    def __init__(self,
                 alpha: float = 0.5,
                 gamma: float = 1.0,
                 epsilon: float = 1.0,
                 epsilon_minimo: float = 0.001,
                 taxa_decaimento_epsilon: float = 0.99999,
                 jogador: int = 1):
        """ Inicializa os atributos e a memória do Agente. """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_minimo = epsilon_minimo
        self.taxa_decaimento_epsilon = taxa_decaimento_epsilon
        self.jogador = jogador
        self.simbolo = 'X' if jogador == 1 else 'O'
        self.tabela_q: Dict[Tuple, Dict[int, float]] = {}
        
        # Atributos para o treinamento em massa (gerenciados pelo treinador.py)
        self.partidas_treinadas = 0
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0
        self.historico_partida: List[Tuple[Tuple, int]] = []

    def obter_valor_q(self, estado: Tuple, acao: int) -> float:
        """ Consulta a "memória" para ver o valor de uma ação em um estado. """
        if estado not in self.tabela_q:
            self.tabela_q[estado] = {}
        if acao not in self.tabela_q[estado]:
            self.tabela_q[estado][acao] = 0.0
        return self.tabela_q[estado][acao]

    def aprender(self, estado: Tuple, acao: int, recompensa: float, proximo_estado: Tuple, finalizado: bool):
        """
        Método de aprendizado a cada passo (TD Learning), usado pelo jogar.py.
        """
        opiniao_antiga = self.obter_valor_q(estado, acao)
        
        melhor_valor_futuro = 0.0 if finalizado else self._obter_melhor_valor_q_do_estado(proximo_estado)
        
        valor_real_da_jogada = recompensa + self.gamma * melhor_valor_futuro
        surpresa = valor_real_da_jogada - opiniao_antiga
        novo_valor_q = opiniao_antiga + self.alpha * surpresa
        self.tabela_q[estado][acao] = novo_valor_q

    def _obter_melhor_valor_q_do_estado(self, estado: Tuple) -> float:
        """ Verifica na "memória" qual é a melhor jogada possível a partir de um estado. """
        if estado not in self.tabela_q or not self.tabela_q[estado]:
            return 0.0
        return max(self.tabela_q[estado].values())

    def escolher_acao(self, estado: Tuple, acoes_validas: List[int], em_treinamento: bool = True) -> int:
        """ Decide qual jogada fazer usando a estratégia Epsilon-Greedy. """
        if not acoes_validas:
            raise ValueError("Não há ações válidas para escolher.")
        if not em_treinamento:
            return self._escolher_melhor_acao(estado, acoes_validas)
        if random.random() < self.epsilon:
            return random.choice(acoes_validas)
        else:
            return self._escolher_melhor_acao(estado, acoes_validas)

    def _escolher_melhor_acao(self, estado: Tuple, acoes_validas: List[int]) -> int:
        """ Consulta a "memória" e escolhe a ação com o maior valor Q. """
        valores_q_das_acoes = {acao: self.obter_valor_q(estado, acao) for acao in acoes_validas}
        valor_maximo_q = max(valores_q_das_acoes.values())
        melhores_acoes = [acao for acao, valor in valores_q_das_acoes.items() if valor == valor_maximo_q]
        return random.choice(melhores_acoes)

    # --- MÉTODOS PARA O TREINAMENTO EM MASSA (usados pelo treinador.py) ---

    def iniciar_nova_partida(self):
        """ Limpa a memória de curto prazo para o início de uma nova partida. """
        self.historico_partida = []

    def registrar_jogada(self, estado: Tuple, acao: int):
        """ Guarda a jogada (estado, ação) feita nesta partida. """
        self.historico_partida.append((estado, acao))

    def aprender_com_fim_de_partida(self, recompensa_final: float):
        """
        Processa o histórico da partida finalizada para aprender com ela (Método Monte Carlo).
        """
        self.partidas_treinadas += 1
        if recompensa_final > 0: self.vitorias += 1
        elif recompensa_final < 0: self.derrotas += 1
        else: self.empates += 1

        # Reutiliza o método 'aprender' para manter a lógica centralizada
        for estado, acao in reversed(self.historico_partida):
            self.aprender(estado, acao, recompensa_final, estado, True) # finalizado=True
            recompensa_final *= self.gamma
        
        self.reduzir_epsilon()

    def reduzir_epsilon(self):
        """ Reduz a "curiosidade" do Agente. """
        self.epsilon = max(self.epsilon_minimo, self.epsilon * self.taxa_decaimento_epsilon)

    def salvar_memoria(self, caminho: str):
        """ Salva o conhecimento do Agente (a Tabela Q) em um arquivo. """
        caminho_arquivo = Path(caminho)
        caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho_arquivo, 'wb') as arquivo:
            pickle.dump(self.tabela_q, arquivo)
        # Removido o print daqui para que o salvamento possa ser silencioso

    @classmethod
    def carregar(cls, caminho: str, **kwargs) -> 'AgenteQLearning':
        """ Cria uma instância de Agente e carrega seu conhecimento de um arquivo. """
        agente = cls(**kwargs)
        caminho_arquivo = Path(caminho)
        if caminho_arquivo.exists():
            with open(caminho_arquivo, 'rb') as arquivo:
                agente.tabela_q = pickle.load(arquivo)
            print(f"✅ Memória do Agente ({agente.simbolo}) carregada de: {caminho_arquivo}")
        else:
            print(f"⚠️  Aviso: Nenhum arquivo de memória encontrado em {caminho}. O Agente ({agente.simbolo}) começará do zero.")
        return agente

    def imprimir_estatisticas(self):
        """ Imprime as estatísticas de forma legível no console. """
        total_jogos = self.vitorias + self.derrotas + self.empates
        if total_jogos == 0:
            taxa_vitoria, taxa_empate, taxa_derrota = 0.0, 0.0, 0.0
        else:
            taxa_vitoria = self.vitorias / total_jogos
            taxa_empate = self.empates / total_jogos
            taxa_derrota = self.derrotas / total_jogos

        print(f"\n{'='*50}")
        print(f"📊 ESTATÍSTICAS DO AGENTE ({self.simbolo})")
        print(f"{'='*50}")
        print(f"Partidas treinadas:   {self.partidas_treinadas:,}")
        print(f"Estados conhecidos:   {len(self.tabela_q):,}")
        print(f"Curiosidade (Epsilon):{self.epsilon:.4f}")
        print(f"\n--- Desempenho ---")
        print(f"Vitórias:   {self.vitorias:>6} ({taxa_vitoria*100:>5.1f}%)")
        print(f"Empates:    {self.empates:>6} ({taxa_empate*100:>5.1f}%)")
        print(f"Derrotas:   {self.derrotas:>6} ({taxa_derrota*100:>5.1f}%)")
        print(f"{'='*50}\n")