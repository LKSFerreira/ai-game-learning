import numpy as np
import pickle
import random
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, TypeVar, Generic, Optional, Any

# Definimos um tipo genérico para o Estado, pois ele pode mudar de jogo para jogo.
# No Jogo da Velha é uma Tupla de 9 inteiros. No Labirinto é uma Tupla (linha, coluna).

Estado = TypeVar('Estado')


class AgenteQLearningBase(ABC, Generic[Estado]):
    """
    Classe Base para Agentes de Q-Learning (Aprendizado por Reforço).

    Esta classe implementa a lógica central do algoritmo Q-Learning de forma genérica,
    permitindo que ela seja reutilizada em diferentes jogos (Jogo da Velha, Labirinto, etc).

    ---
    🧠 O QUE É Q-LEARNING? (Conceito Rápido)

    Imagine que você tem um caderno (Q-Table). Em cada página desse caderno, você anota
    uma situação do jogo (Estado). Nessa página, você lista todas as ações possíveis
    e dá uma nota (Valor Q) para cada uma.

    - No começo, todas as notas são 0 (você não sabe nada).
    - Você joga e vê o que acontece.
    - Se uma ação te levou à vitória, você aumenta a nota dela.
    - Se te levou à derrota, você diminui.

    Com o tempo, seu caderno se torna um guia perfeito de "o que fazer em cada situação".
    Esta classe é o "gerenciador desse caderno".
    ---
    """

    def __init__(
        self,
        alpha: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995
    ):
        """
        Inicializa o Agente Q-Learning.

        Args:
            alpha (float): Taxa de Aprendizado (0.0 a 1.0).
                           O quanto o agente substitui o conhecimento antigo pelo novo.
                           - 0.0: Não aprende nada novo.
                           - 1.0: Esquece tudo e só confia na última experiência.

            gamma (float): Fator de Desconto (0.0 a 1.0).
                           O quanto o agente valoriza recompensas futuras.
                           - 0.0: Míope (só liga para a recompensa imediata).
                           - 1.0: Visionário (valoriza recompensas a longo prazo igualmente).

            epsilon (float): Taxa de Exploração Inicial (0.0 a 1.0).
                             Probabilidade de fazer uma ação aleatória para descobrir coisas novas.

            epsilon_min (float): Valor mínimo para o epsilon.
                                 Garante que o agente nunca pare de explorar totalmente (opcional).

            epsilon_decay (float): Fator de decaimento do epsilon a cada episódio.
                                   Reduz a exploração gradualmente conforme o agente aprende.
        """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        # A Q-Table é o nosso "cérebro".
        # Mapeia: Estado -> {Ação: Valor Q}
        # Exemplo: (0,0) -> { 'cima': 0.5, 'baixo': -0.1 }
        self.q_table: Dict[Estado, Dict[Any, float]] = {}

        # Estatísticas para acompanhamento
        self.treinamento_epocas = 0

    def obter_valor_q(self, estado: Estado, acao: Any) -> float:
        """
        Retorna o valor Q para um determinado par (estado, ação).

        Se o estado ou a ação não existirem na tabela, retorna 0.0.
        """
        if estado not in self.q_table:
            return 0.0
        return self.q_table[estado].get(acao, 0.0)

    def escolher_acao(self, estado: Estado, acoes_possiveis: List[Any]) -> Any:
        """
        Escolhe uma ação baseada na política Epsilon-Greedy.

        PENSAMENTO DO SENIOR:
        "Devo explorar ou aproveitar o que já sei?"

        1. Exploração (Exploration): Com chance 'epsilon', escolho qualquer coisa.
           Isso é vital para não ficar preso em estratégias ruins só porque deram sorte uma vez.

        2. Aproveitamento (Exploitation): Caso contrário, escolho a MELHOR ação conhecida.
           Olho na minha Q-Table e vejo qual ação tem a maior nota.

        """

        # 1. Exploração
        if random.random() < self.epsilon:
            return random.choice(acoes_possiveis)

        # 2. Aproveitamento (Exploitation)
        return self._obter_melhor_acao(estado, acoes_possiveis)

    def _obter_melhor_acao(self, estado: Estado, acoes_possiveis: List[Any]) -> Any:
        """
        Retorna a ação com o maior valor Q para o estado.
        Se houver empate, escolhe aleatoriamente entre as melhores.
        """
        # Se o estado é novo, qualquer ação vale 0.0, então escolha aleatória
        if estado not in self.q_table:
            return random.choice(acoes_possiveis)

        # Obtém os valores Q para as ações possíveis
        valores_q = {acao: self.obter_valor_q(
            estado, acao) for acao in acoes_possiveis}

        # Encontra o valor máximo
        max_q = max(valores_q.values())

        # Encontra todas as ações que têm esse valor máximo (para desempate)
        melhores_acoes = [acao for acao, q in valores_q.items() if q == max_q]

        return random.choice(melhores_acoes)

    def atualizar_q_table(
        self,
        estado: Estado,
        acao: Any,
        recompensa: float,
        proximo_estado: Estado,
        acoes_proximo_estado: List[Any],
        finalizado: bool = False
    ):
        """
        Atualiza a Q-Table usando a Equação de Bellman (Temporal Difference Learning).

        Fórmula Mágica:
        Q(s,a) = Q(s,a) + alpha * (R + gamma * max(Q(s',a')) - Q(s,a))

        PENSAMENTO DO SENIOR:
        "O valor de uma ação é o que eu ganhei agora (R) mais a minha melhor estimativa
        do que vou ganhar no futuro (max Q do próximo estado), tudo isso ajustado pela
        minha taxa de aprendizado (alpha)."

        Se o jogo acabou (finalizado=True), não existe futuro, então o termo 'gamma * max(...)' some.

        """
        # Garante que o estado existe na tabela
        if estado not in self.q_table:
            self.q_table[estado] = {}

        q_atual = self.obter_valor_q(estado, acao)

        # Calcula o valor máximo esperado para o próximo estado
        if finalizado:
            max_q_futuro = 0.0
        else:
            # Se o próximo estado não foi visitado, seus valores são 0.0
            valores_futuros = [self.obter_valor_q(
                proximo_estado, a) for a in acoes_proximo_estado]
            max_q_futuro = max(valores_futuros) if valores_futuros else 0.0

        # Equação de Bellman
        novo_q = q_atual + self.alpha * \
            (recompensa + (self.gamma * max_q_futuro) - q_atual)

        # Atualiza a tabela
        self.q_table[estado][acao] = novo_q

    def decair_epsilon(self):
        """
        Reduz a taxa de exploração após cada episódio.
        Isso faz o agente ficar mais "sério" e confiar mais no que aprendeu conforme o tempo passa.
        """
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def salvar_modelo(self, caminho_arquivo: str):
        """Salva a Q-Table em um arquivo pickle."""
        try:
            with open(caminho_arquivo, 'wb') as f:
                pickle.dump(self.q_table, f)
            print(f"💾 Modelo salvo com sucesso em: {caminho_arquivo}")
        except Exception as e:
            print(f"❌ Erro ao salvar modelo: {e}")

    def carregar_modelo(self, caminho_arquivo: str):
        """Carrega a Q-Table de um arquivo pickle."""
        try:
            with open(caminho_arquivo, 'rb') as f:
                self.q_table = pickle.load(f)
            print(f"📂 Modelo carregado de: {caminho_arquivo}")
        except FileNotFoundError:
            print(
                f"⚠️ Arquivo {caminho_arquivo} não encontrado. Iniciando com Q-Table vazia.")
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
