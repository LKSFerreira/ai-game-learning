"""
Módulo: 🧩 ambiente.py
Projeto: 📘 AI Game Learning

Este módulo define o ambiente para o Jogo da Velha (Tic-Tac-Toe).
No paradigma de Aprendizado por Reforço (Reinforcement Learning),
este código representa o "Environment".

A classe principal, `AmbienteJogoDaVelha`, é responsável por:
- Manter e gerenciar o estado do tabuleiro.
- Processar e validar as ações (jogadas) dos jogadores.
- Verificar o fim da partida (vitória, derrota ou empate).
- Fornecer recompensas com base no resultado da partida.

💡 Implementado com NumPy para eficiência, mas espelhando a lógica
   de uma implementação em JavaScript puro.
"""

import numpy as np
from typing import List, Tuple

class AmbienteJogoDaVelha:
    """
    Representa o ambiente completo do Jogo da Velha, com suporte a tabuleiros
    de tamanho N x N (Mínimo de 3x3 até 9x9).
    
    O estado do tabuleiro é um array onde:
    - 0 representa uma casa vazia.
    - 1 representa o jogador 'X'.
    - 2 representa o jogador 'O'.
    """

    def __init__(self, dimensao: int = 3):
        """
        Inicializa o ambiente do jogo.
        
        Args:
            dimensao (int): Tamanho do tabuleiro (entre 3 e 9). Padrão é 3.
        
        Raises:
            ValueError: Se o tamanho for fora dos limites permitidos.
        """
        if not 3 <= dimensao <= 9:
            raise ValueError("O tamanho do tabuleiro deve estar entre 3 e 9.")

        self.dimensao: int = dimensao
        self.numero_de_casas: int = dimensao * dimensao
        self.jogador_inicial: int = 1  # Significa que o jogador 'X' sempre inicia

        self.combinacoes_de_vitoria: List[List[int]] = self._gerar_combinacoes_de_vitoria()

        self.reiniciar_partida()

    def _gerar_combinacoes_de_vitoria(self) -> List[List[int]]:
        """
        Gera todas as combinações vencedoras para o tabuleiro atual.
        Condição para vitória: Completar uma linha, uma coluna ou uma diagonal.
        
        Returns:
            Uma lista de listas com todas as combinações de vitória.
        """
        combinacoes = []

        # 1️⃣ Linhas
        combinacoes.extend([list(range(i, i + self.dimensao)) for i in range(0, self.numero_de_casas, self.dimensao)])
        
        # 2️⃣ Colunas
        combinacoes.extend([list(range(i, self.numero_de_casas, self.dimensao)) for i in range(self.dimensao)])
        
        # 3️⃣ Diagonal principal
        combinacoes.append(list(range(0, self.numero_de_casas, self.dimensao + 1)))
        
        # 4️⃣ Diagonal secundária
        combinacoes.append(list(range(self.dimensao - 1, self.numero_de_casas - 1, self.dimensao - 1)))
        
        return combinacoes

    def reiniciar_partida(self) -> np.ndarray:
        """
        Reinicia o jogo, limpando o tabuleiro e resetando as variáveis internas.
        
        Returns:
            O estado inicial do tabuleiro (vetor de zeros).
        """
        self.tabuleiro: np.ndarray = np.zeros(self.numero_de_casas, dtype=int)
        self.jogador_atual: int = self.jogador_inicial
        self.partida_finalizada: bool = False
        self.vencedor: int | None = None
        return self.obter_estado()

    def obter_estado(self) -> np.ndarray:
        """
        Retorna uma cópia do estado atual do tabuleiro.
        
        Returns:
            Estado atual do tabuleiro.
        """
        return self.tabuleiro.copy()

    def obter_acoes_validas(self) -> List[int]:
        """
        Retorna uma lista de índices de todas as jogadas possíveis.
        
        Returns:
            Lista de casas vazias.
        """
        return np.where(self.tabuleiro == 0)[0].tolist()
    
    def obter_estado_como_tupla(self) -> Tuple:
        """
        Retorna o estado como tupla (imutável), essencial para a Q-Table.
        
        Returns:
            Versão imutável do estado.
        """
        return tuple(self.tabuleiro)

    def executar_jogada(self, acao: int) -> Tuple[np.ndarray, float, bool]:
        """
        Executa uma jogada no ambiente.
        
        Args:
            acao (int): Índice da casa vazia (0 a N²-1).
        
        Returns:
            Uma tupla contendo: (próximo_estado, recompensa, partida_finalizada).
        
        Raises:
            ValueError: Se a jogada for inválida.
        """
        if self.tabuleiro[acao] != 0:
            raise ValueError(f"Ação inválida: posição {acao} ocupada.")
        if self.partida_finalizada:
            raise ValueError("Partida finalizada.")

        self.tabuleiro[acao] = self.jogador_atual
        recompensa = 0.0

        if self._verificar_vitoria(self.jogador_atual):
            self.partida_finalizada = True
            self.vencedor = self.jogador_atual
            recompensa = 1.0
        elif len(self.obter_acoes_validas()) == 0:
            self.partida_finalizada = True
            self.vencedor = 0  # 0 significa empate
            # Mantemos a recompensa em 0.0 para empate

        self._trocar_jogador()
        return self.obter_estado(), recompensa, self.partida_finalizada

    def _verificar_vitoria(self, jogador: int) -> bool:
        """
        Verifica se o jogador atual venceu.
        
        Args:
            jogador (int): 1 ('X') ou 2 ('O').
            
        Returns:
            True se venceu.
        """
        return any(all(self.tabuleiro[casa] == jogador for casa in combinacao) for combinacao in self.combinacoes_de_vitoria)

    def _trocar_jogador(self):
        """Altera o jogador atual."""
        self.jogador_atual = 2 if self.jogador_atual == 1 else 1

    def exibir_tabuleiro(self):
        """Exibe o tabuleiro no formato console."""
        simbolos = {0: " ", 1: "X", 2: "O"}
        print()
        for i in range(self.dimensao):
            inicio = i * self.dimensao
            fim = inicio + self.dimensao
            linha = [simbolos[casa] for casa in self.tabuleiro[inicio:fim]]
            print(" " + " │ ".join(linha))
            if i < self.dimensao - 1:
                print("───" + "┼───" * (self.dimensao - 1))
        print()