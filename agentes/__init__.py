"""
Pacote de Agentes de Inteligência Artificial.

Este pacote contém as implementações base e específicas de agentes
para o projeto AI Game Learning.

Classes Disponíveis:
    - AgenteQLearningBase: Classe base abstrata que implementa o algoritmo
                           Q-Learning de forma genérica, podendo ser
                           reutilizada em diferentes ambientes de jogo.

Exemplo de Uso:
    >>> from agentes import AgenteQLearningBase
    >>> # Crie sua classe derivada específica para seu jogo
"""

from .q_learning_base import AgenteQLearningBase

__all__ = ['AgenteQLearningBase']
