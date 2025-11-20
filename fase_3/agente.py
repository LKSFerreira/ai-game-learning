"""
Módulo: 🧠 agente.py
Projeto: 📘 AI Game Learning (Fase 3 - Labirinto)

Este módulo implementa o Agente que aprende a navegar no labirinto.
Ele herda toda a inteligência (Q-Learning) da classe base `AgenteQLearningBase`,
focando apenas em traduzir o mundo do labirinto para o formato que o cérebro entende.
"""

from typing import Tuple, List
from agentes.q_learning_base import AgenteQLearningBase

# O estado no Labirinto é uma tupla (linha, coluna)
EstadoLabirinto = Tuple[int, int]

class AgenteLabirinto(AgenteQLearningBase[EstadoLabirinto]):
    """
    Agente que aprende a resolver o labirinto.
    
    A lógica de aprendizado (Q-Learning) vem da classe mãe.
    Aqui só definimos as especificidades do Labirinto.
    """

    def __init__(self, linhas: int, colunas: int):
        """
        Inicializa o agente do labirinto.
        
        Args:
            linhas: Número de linhas do labirinto (não usado diretamente na lógica, mas útil para info).
            colunas: Número de colunas do labirinto.
        """
        # Chama o construtor da classe base com hiperparâmetros ajustados para o Labirinto
        super().__init__(
            alpha=0.1,        # Taxa de aprendizado (0.1 é bom para ambientes determinísticos)
            gamma=0.9,        # Fator de desconto (0.9 valoriza o futuro, incentivando chegar na saída)
            epsilon=1.0,      # Começa explorando tudo
            epsilon_min=0.01, # Mantém um mínimo de curiosidade
            epsilon_decay=0.995 # Decai lentamente
        )
        
        # Define as ações possíveis (strings que o ambiente entende)
        self.acoes = ['cima', 'baixo', 'esquerda', 'direita']
        
    def escolher_acao(self, estado: EstadoLabirinto) -> str:
        """
        Escolhe uma ação para o estado atual.
        Sobrescreve apenas para passar a lista de ações correta.
        """
        # Usa a lógica da classe base (Epsilon-Greedy), passando as ações possíveis do labirinto
        return super().escolher_acao(estado, self.acoes)

    def atualizar_q_table(
        self, 
        estado: EstadoLabirinto, 
        acao: str, 
        recompensa: float, 
        proximo_estado: EstadoLabirinto, 
        finalizado: bool = False
    ):
        """
        Atualiza a Q-Table.
        Sobrescreve apenas para simplificar a chamada, já que as ações possíveis
        no próximo estado são sempre as mesmas (cima, baixo, esq, dir).
        """
        super().atualizar_q_table(
            estado=estado,
            acao=acao,
            recompensa=recompensa,
            proximo_estado=proximo_estado,
            acoes_proximo_estado=self.acoes, # No labirinto, as ações possíveis são sempre as mesmas
            finalizado=finalizado
        )
