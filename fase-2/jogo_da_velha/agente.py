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
        # A Tabela Q armazena o valor de cada "tática" (ação) em cada
        # "situação de batalha" (estado).
        # Estrutura: { estado_do_tabuleiro: { acao: valor_q } }
        self.tabela_q: Dict[Tuple, Dict[int, float]] = {}

        # --- ESTATÍSTICAS DE TREINO ---
        self.partidas_treinadas = 0
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0

    def obter_valor_q(self, estado: Tuple, acao: int) -> float:
        """
        Consulta a "memória" para ver o valor de uma ação em um estado.
        Se o Agente nunca viu essa situação antes, ele assume que o valor é 0.
        
        Args:
            estado: A configuração atual do tabuleiro.
            acao: A jogada que queremos consultar.
            
        Returns:
            O valor Q aprendido para o par (estado, ação).
        """
        # Se o estado é novo, adiciona uma nova página à "enciclopédia".
        if estado not in self.tabela_q:
            self.tabela_q[estado] = {}
        
        # Se a ação nunca foi tentada nesse estado, anota com valor inicial 0.
        if acao not in self.tabela_q[estado]:
            self.tabela_q[estado][acao] = 0.0
            
        return self.tabela_q[estado][acao]

    def atualizar_valor_q(self, estado: Tuple, acao: int, recompensa: float, proximo_estado: Tuple):
        """
        Atualiza a "memória" do Agente usando a Equação de Bellman.
        É aqui que o aprendizado realmente acontece.
        
        Fórmula em "linguagem gamer":
        NovaOpinião = OpiniãoAntiga + VelocidadeAprendizado * (RecompensaReal - OpiniãoAntiga)
        
        Onde a RecompensaReal = (O que ganhei agora + Potencial da próxima jogada)
        """
        # 1. Pega a opinião antiga (o valor Q que o agente *achava* que a jogada valia).
        opiniao_antiga = self.obter_valor_q(estado, acao)

        # 2. Calcula o melhor resultado possível a partir do próximo estado.
        #    É o "potencial da próxima jogada".
        melhor_valor_futuro = self._obter_melhor_valor_q_do_estado(proximo_estado)

        # 3. Calcula o valor que a jogada *realmente* teve.
        valor_real_da_jogada = recompensa + self.gamma * melhor_valor_futuro

        # 4. A "surpresa" ou "erro de previsão" é a diferença entre o real e o esperado.
        surpresa = valor_real_da_jogada - opiniao_antiga

        # 5. Atualiza a opinião antiga, ajustando-a um pouco na direção da surpresa.
        #    O `alpha` controla o "tamanho do passo" desse ajuste.
        novo_valor_q = opiniao_antiga + self.alpha * surpresa
        
        self.tabela_q[estado][acao] = novo_valor_q

    def _obter_melhor_valor_q_do_estado(self, estado: Tuple) -> float:
        """
        Verifica na "memória" qual é a melhor jogada possível a partir de um estado.
        
        Returns:
            O maior valor Q para o estado fornecido. Retorna 0 se o estado for novo.
        """
        if estado not in self.tabela_q or not self.tabela_q[estado]:
            return 0.0
        return max(self.tabela_q[estado].values())

    def escolher_acao(self, estado: Tuple, acoes_validas: List[int], em_treinamento: bool = True) -> int:
        """
        Decide qual jogada fazer usando a estratégia Epsilon-Greedy.
        
        Args:
            estado: A configuração atual do tabuleiro.
            acoes_validas: Lista de jogadas permitidas.
            em_treinamento: Se True, usa o "Medidor de Curiosidade" (epsilon).
                            Se False, sempre usa a melhor tática conhecida.
        
        Returns:
            A ação (índice da casa) escolhida pelo Agente.
        """
        if not acoes_validas:
            raise ValueError("Não há ações válidas para escolher.")

        # Se não estiver em treinamento, joga para ganhar (sempre a melhor tática).
        if not em_treinamento:
            return self._escolher_melhor_acao(estado, acoes_validas)

        # Lógica Epsilon-Greedy:
        if random.random() < self.epsilon:
            # "Modo Aventura": Tenta uma tática aleatória para explorar.
            return random.choice(acoes_validas)
        else:
            # "Modo Farm": Usa a melhor tática conhecida para garantir o resultado.
            return self._escolher_melhor_acao(estado, acoes_validas)

    def _escolher_melhor_acao(self, estado: Tuple, acoes_validas: List[int]) -> int:
        """
        Consulta a "memória" e escolhe a ação com o maior valor Q.
        Se houver empate entre as melhores ações, escolhe uma delas aleatoriamente.
        """
        valores_q_das_acoes = {acao: self.obter_valor_q(estado, acao) for acao in acoes_validas}
        
        valor_maximo_q = max(valores_q_das_acoes.values())
        
        melhores_acoes = [acao for acao, valor in valores_q_das_acoes.items() if valor == valor_maximo_q]
        
        return random.choice(melhores_acoes)

    def aprender_com_partida(self, historico_da_partida: List, recompensa_final: float):
        """
        Processa o histórico de uma partida finalizada para aprender com ela.
        Este método é chamado pelo Treinador ao final de cada jogo.
        
        Pense nisso como o jogador, após derrotar um MVP, refletindo sobre
        todas as ações que o levaram à vitória.
        """
        self.partidas_treinadas += 1
        if recompensa_final > 0: self.vitorias += 1
        elif recompensa_final < 0: self.derrotas += 1
        else: self.empates += 1

        # Propaga a recompensa final para trás, valorizando as jogadas
        # que levaram a este resultado.
        for estado, acao, proximo_estado in reversed(historico_da_partida):
            self.atualizar_valor_q(estado, acao, recompensa_final, proximo_estado)
            # A recompensa perde um pouco de força a cada passo para trás,
            # controlado pela "Visão de Futuro" (gamma).
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
        Salva o conhecimento do Agente (a Tabela Q e os hiperparâmetros) em um arquivo.
        """
        caminho_arquivo = Path(caminho)
        caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
        
        with open(caminho_arquivo, 'wb') as arquivo:
            pickle.dump(self.tabela_q, arquivo)
        print(f"💾 Memória do Agente salva em: {caminho_arquivo}")

    def carregar_memoria(self, caminho: str):
        """
        Carrega o conhecimento de um Agente previamente treinado.
        """
        caminho_arquivo = Path(caminho)
        if not caminho_arquivo.exists():
            print(f"⚠️  Aviso: Nenhum arquivo de memória encontrado em {caminho}. O Agente começará do zero.")
            return

        with open(caminho_arquivo, 'rb') as arquivo:
            self.tabela_q = pickle.load(arquivo)
        print(f"✅ Memória do Agente carregada de: {caminho_arquivo}")
        print(f"   - O Agente conhece {len(self.tabela_q):,} situações de jogo.")