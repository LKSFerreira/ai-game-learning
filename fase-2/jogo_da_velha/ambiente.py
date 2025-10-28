"""
Ambiente do Jogo da Velha (Tic-Tac-Toe)

Este módulo implementa o "mundo" onde o jogo acontece.
Representa o ENVIRONMENT no Reinforcement Learning.

Responsabilidades:
- Gerenciar o tabuleiro (3x3)
- Validar jogadas
- Verificar condições de vitória/empate
- Retornar o estado atual do jogo

No contexto de RL:
- ESTADO: Configuração atual do tabuleiro
- AÇÃO: Escolher uma casa (0-8) para jogar
- RECOMPENSA: +1 (vitória), -1 (derrota), 0 (empate/continua)
"""

import numpy as np
from typing import Tuple, Optional, List


class JogoVelha:
    """
    Classe que representa o ambiente do Jogo da Velha.
    
    O tabuleiro é representado por um vetor de 9 posições:
    - 0 = casa vazia
    - 1 = jogador X (sempre começa)
    - 2 = jogador O
    
    Posições do tabuleiro:
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    """
    
    def __init__(self):
        """Inicializa um novo jogo."""
        self.tabuleiro = np.zeros(9, dtype=int)  # 9 casas vazias
        self.jogador_atual = 1  # Jogador 1 (X) sempre começa
        self.finalizado = False  # Jogo em andamento
        self.vencedor = None  # Ninguém ganhou ainda
        
        # Todas as combinações possíveis de vitória
        # (3 linhas, 3 colunas, 2 diagonais)
        self.combinacoes_vitoria = [
            [0, 1, 2],  # Linha superior
            [3, 4, 5],  # Linha do meio
            [6, 7, 8],  # Linha inferior
            [0, 3, 6],  # Coluna esquerda
            [1, 4, 7],  # Coluna do meio
            [2, 5, 8],  # Coluna direita
            [0, 4, 8],  # Diagonal principal (\)
            [2, 4, 6],  # Diagonal secundária (/)
        ]
    
    def resetar(self) -> np.ndarray:
        """
        Reseta o jogo para o estado inicial.
        
        Returns:
            O estado inicial do tabuleiro (vetor com 9 zeros)
        """
        self.tabuleiro = np.zeros(9, dtype=int)
        self.jogador_atual = 1
        self.finalizado = False
        self.vencedor = None
        return self.tabuleiro.copy()
    
    def obter_acoes_validas(self) -> List[int]:
        """
        Retorna todas as posições vazias (ações válidas).
        
        Returns:
            Lista de índices (0-8) das casas vazias
        
        Exemplo:
            Se tabuleiro = [1, 0, 2, 0, 0, 0, 0, 0, 0]
            Retorna: [1, 3, 4, 5, 6, 7, 8]
        """
        return [i for i in range(9) if self.tabuleiro[i] == 0]
    
    def fazer_jogada(self, posicao: int) -> Tuple[np.ndarray, float, bool]:
        """
        Executa uma jogada no tabuleiro.
        
        Args:
            posicao: Índice da casa (0-8) onde jogar
        
        Returns:
            Tupla contendo:
            - novo_estado: Estado do tabuleiro após a jogada
            - recompensa: Valor numérico do resultado
              * +1.0 se o jogador atual venceu
              * -1.0 se o jogador atual perdeu (não aplicável aqui)
              *  0.0 se empatou ou jogo continua
            - finalizado: Se o jogo acabou (True/False)
        
        Raises:
            ValueError: Se a jogada for inválida
        
        Nota:
            A recompensa é sempre da perspectiva do jogador que acabou de jogar.
        """
        # Validação: verifica se a posição está vazia
        if self.tabuleiro[posicao] != 0:
            raise ValueError(f"Posição {posicao} já está ocupada!")
        
        # Validação: verifica se o jogo já acabou
        if self.finalizado:
            raise ValueError("O jogo já foi finalizado!")
        
        # Guarda quem fez a jogada (importante para recompensa)
        jogador_que_jogou = self.jogador_atual
        
        # Executa a jogada
        self.tabuleiro[posicao] = self.jogador_atual
        
        # Verifica se o jogador que acabou de jogar ganhou
        if self._verificar_vitoria(jogador_que_jogou):
            self.finalizado = True
            self.vencedor = jogador_que_jogou
            recompensa = 1.0  # Vitória = recompensa positiva
        
        # Verifica se deu empate (tabuleiro cheio sem vencedor)
        elif len(self.obter_acoes_validas()) == 0:
            self.finalizado = True
            self.vencedor = 0  # 0 significa empate
            recompensa = 0.0  # Empate = sem recompensa
        
        # Jogo continua
        else:
            self.finalizado = False
            recompensa = 0.0  # Sem recompensa ainda
        
        # Alterna para o próximo jogador
        self._alternar_jogador()
        
        return self.tabuleiro.copy(), recompensa, self.finalizado
    
    def _verificar_vitoria(self, jogador: int) -> bool:
        """
        Verifica se o jogador especificado venceu o jogo.
        
        Args:
            jogador: 1 (X) ou 2 (O)
        
        Returns:
            True se o jogador formou uma linha/coluna/diagonal, False caso contrário
        """
        for combo in self.combinacoes_vitoria:
            # Verifica se todas as 3 posições da combinação
            # pertencem ao jogador especificado
            if all(self.tabuleiro[pos] == jogador for pos in combo):
                return True
        return False
    
    def _alternar_jogador(self):
        """
        Alterna entre jogador 1 (X) e jogador 2 (O).
        
        Usa o truque matemático: 3 - 1 = 2 e 3 - 2 = 1
        """
        self.jogador_atual = 3 - self.jogador_atual
    
    def obter_estado(self) -> Tuple[int, ...]:
        """
        Retorna o estado atual como uma tupla imutável.
        
        Tuplas são usadas porque:
        1. São imutáveis (não podem ser modificadas acidentalmente)
        2. Podem ser chaves de dicionário (necessário para Q-Table)
        3. São hasheáveis (podem ser usadas em conjuntos)
        
        Returns:
            Tupla com 9 elementos representando o tabuleiro
        
        Exemplo:
            (1, 0, 2, 0, 1, 0, 0, 0, 2)
            Significa: X na posição 0, O na 2, X na 4, O na 8
        """
        return tuple(self.tabuleiro)
    
    def obter_estado_hash(self) -> int:
        """
        Retorna um hash único do estado atual.
        
        Útil para indexação rápida e comparações.
        
        Returns:
            Valor inteiro único representando este estado
        """
        return hash(self.obter_estado())
    
    def renderizar(self):
        """
        Exibe o tabuleiro no console de forma visual.
        
        Saída exemplo:
        X |   | O
        ---------
          | X |  
        ---------
          |   | O
        """
        simbolos = {0: ' ', 1: 'X', 2: 'O'}
        
        print()
        for i in range(0, 9, 3):
            # Pega 3 casas da linha atual
            linha = [simbolos[self.tabuleiro[i + j]] for j in range(3)]
            print(f" {linha[0]} | {linha[1]} | {linha[2]} ")
            if i < 6:  # Não imprime separador após a última linha
                print("---------")
        print()
    
    def renderizar_com_indices(self):
        """
        Exibe o tabuleiro mostrando os índices das casas vazias.
        
        Útil para jogadores humanos saberem onde podem jogar.
        
        Saída exemplo:
        X | 1 | O
        ---------
        3 | X | 5
        ---------
        6 | 7 | O
        """
        print()
        for i in range(0, 9, 3):
            linha = []
            for j in range(3):
                pos = i + j
                if self.tabuleiro[pos] == 0:
                    linha.append(str(pos))  # Mostra o índice
                elif self.tabuleiro[pos] == 1:
                    linha.append('X')
                else:
                    linha.append('O')
            print(f" {linha[0]} | {linha[1]} | {linha[2]} ")
            if i < 6:
                print("---------")
        print()
    
    def clonar(self) -> 'JogoVelha':
        """
        Cria uma cópia independente do jogo atual.
        
        Útil para simulações sem alterar o jogo original
        (ex: o agente testar jogadas possíveis).
        
        Returns:
            Nova instância de JogoVelha com estado idêntico
        """
        novo_jogo = JogoVelha()
        novo_jogo.tabuleiro = self.tabuleiro.copy()
        novo_jogo.jogador_atual = self.jogador_atual
        novo_jogo.finalizado = self.finalizado
        novo_jogo.vencedor = self.vencedor
        return novo_jogo
    
    @staticmethod
    def contar_estados_possiveis() -> int:
        """
        Calcula o número teórico de estados possíveis.
        
        No Jogo da Velha:
        - 9 casas
        - 3 opções por casa (vazio, X, O)
        - Total: 3^9 = 19.683 estados
        
        Porém, muitos são inválidos (ex: todos X).
        Estados válidos reais: ~5.478
        
        Returns:
            Número teórico de estados (3^9)
        """
        return 3 ** 9


# ===== FUNÇÕES AUXILIARES PARA TESTES =====


def testar_ambiente_basico():
    """Testa funcionalidades básicas do ambiente."""
    print("=== TESTE 1: AMBIENTE BÁSICO ===\n")
    
    jogo = JogoVelha()
    
    print("Estado inicial:")
    jogo.renderizar()
    print(f"Tabuleiro como tupla: {jogo.obter_estado()}")
    print(f"Ações válidas: {jogo.obter_acoes_validas()}")
    print(f"Jogador atual: {jogo.jogador_atual} ({'X' if jogo.jogador_atual == 1 else 'O'})")
    
    print("\n=== TESTE CONCLUÍDO ===\n")


def testar_vitoria_x():
    """Testa cenário de vitória do jogador X."""
    print("=== TESTE 2: VITÓRIA DO X ===\n")
    
    jogo = JogoVelha()
    
    # X ganha na linha superior
    jogadas = [
        (0, "X joga no canto superior esquerdo"),
        (3, "O joga na esquerda do meio"),
        (1, "X joga no topo do meio"),
        (4, "O joga no centro"),
        (2, "X joga no canto superior direito - VENCE!")
    ]
    
    for posicao, descricao in jogadas:
        print(f"{descricao}")
        estado, recompensa, fim = jogo.fazer_jogada(posicao)
        jogo.renderizar()
        
        if fim:
            if jogo.vencedor == 1:
                print("🎉 JOGADOR X VENCEU!")
            elif jogo.vencedor == 2:
                print("🎉 JOGADOR O VENCEU!")
            else:
                print("🤝 EMPATE!")
            print(f"Recompensa: {recompensa}")
            break
    
    print("\n=== TESTE CONCLUÍDO ===\n")


def testar_empate():
    """Testa cenário de empate."""
    print("=== TESTE 3: EMPATE ===\n")
    
    jogo = JogoVelha()
    
    # Sequência que resulta em empate
    jogadas = [0, 1, 2, 4, 3, 5, 7, 6, 8]
    
    for i, posicao in enumerate(jogadas):
        jogador = 'X' if i % 2 == 0 else 'O'
        print(f"{jogador} joga na posição {posicao}")
        estado, recompensa, fim = jogo.fazer_jogada(posicao)
        jogo.renderizar()
        
        if fim:
            if jogo.vencedor == 0:
                print("🤝 EMPATE! Ninguém venceu.")
            print(f"Recompensa: {recompensa}")
            break
    
    print("\n=== TESTE CONCLUÍDO ===\n")


def testar_clonagem():
    """Testa se a clonagem funciona corretamente."""
    print("=== TESTE 4: CLONAGEM DO AMBIENTE ===\n")
    
    jogo1 = JogoVelha()
    jogo1.fazer_jogada(0)  # X joga
    jogo1.fazer_jogada(4)  # O joga
    
    print("Jogo Original:")
    jogo1.renderizar()
    
    # Clona o jogo
    jogo2 = jogo1.clonar()
    
    # Faz uma jogada apenas no clone
    print("Fazendo jogada no CLONE...")
    jogo2.fazer_jogada(8)
    
    print("\nJogo Original (não deve ter mudado):")
    jogo1.renderizar()
    
    print("Jogo Clonado (deve ter a jogada extra):")
    jogo2.renderizar()
    
    print("✅ Clonagem funcionou! Os jogos são independentes.")
    print("\n=== TESTE CONCLUÍDO ===\n")


def executar_todos_testes():
    """Executa toda a bateria de testes."""
    print("\n" + "="*50)
    print("🧪 BATERIA DE TESTES DO AMBIENTE")
    print("="*50 + "\n")
    
    testar_ambiente_basico()
    testar_vitoria_x()
    testar_empate()
    testar_clonagem()
    
    print("="*50)
    print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    print("="*50 + "\n")


# Executar testes se rodar este arquivo diretamente
if __name__ == "__main__":
    executar_todos_testes()
