"""
Módulo: 🧩 ambiente.py
Projeto: 📘 AI Game Learning

Este módulo implementa o Ambiente do Jogo da Velha (Tic-Tac-Toe) para Aprendizado
por Reforço. No paradigma de Reinforcement Learning, o ambiente é responsável por:

- Manter o estado atual do jogo (tabuleiro)
- Processar ações dos agentes (jogadas)
- Determinar recompensas baseadas nos resultados
- Verificar condições de término (vitória, derrota, empate)
- Fornecer informações sobre o estado atual (ações válidas, estado do tabuleiro)

O ambiente funciona como uma "arena" onde os agentes interagem, recebendo
feedback sobre suas ações através de recompensas e estados atualizados.

Este módulo suporta tabuleiros de diferentes tamanhos (3x3 até 9x9), permitindo
experimentar com variações do jogo tradicional. O jogador inicial é escolhido
aleatoriamente a cada partida para aumentar a diversidade do treinamento.

💡 Implementado com NumPy para eficiência computacional, mas mantendo a lógica
   clara e didática, facilitando a compreensão do funcionamento.
"""

import random
import numpy as np
from typing import List, Tuple, Optional


class AmbienteJogoDaVelha:
    """
    Ambiente completo do Jogo da Velha para Aprendizado por Reforço.

    Esta classe representa o "mundo" onde os agentes interagem, fornecendo
    todas as informações necessárias para o aprendizado por reforço:
    - Estado atual do tabuleiro
    - Ações válidas disponíveis
    - Recompensas baseadas nos resultados
    - Sinalização de término da partida

    O ambiente suporta tabuleiros de tamanho N x N (de 3x3 até 9x9), permitindo
    experimentar com diferentes complexidades do jogo.

    Representação do Estado:
        O tabuleiro é representado como um array unidimensional onde:
        - 0 representa uma casa vazia
        - 1 representa o jogador 'X' (jogador 1)
        - 2 representa o jogador 'O' (jogador 2)

        Para um tabuleiro 3x3, as posições são numeradas assim:
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]

    Attributes:
        dimensao (int): Tamanho do tabuleiro (ex: 3 para 3x3, 4 para 4x4).
        numero_de_casas (int): Total de casas no tabuleiro (dimensão²).
        tabuleiro (np.ndarray): Array NumPy representando o estado atual do tabuleiro.
        jogador_atual (int): Jogador que deve jogar agora (1 para 'X', 2 para 'O').
        partida_finalizada (bool): Indica se a partida terminou.
        vencedor (Optional[int]): Vencedor da partida (1, 2, 0 para empate, None se não terminou).
        combinacoes_de_vitoria (List[List[int]]): Lista de todas as combinações que resultam em vitória.

    Example:
        >>> ambiente = AmbienteJogoDaVelha(dimensao=3)
        >>> estado_inicial = ambiente.reiniciar_partida()
        >>> acoes_validas = ambiente.obter_acoes_validas()
        >>> proximo_estado, recompensa, finalizado = ambiente.executar_jogada(4)
    """

    def __init__(self, dimensao: int = 3):
        """
        Inicializa o ambiente do Jogo da Velha.

        Cria um novo ambiente com as configurações especificadas, gera todas
        as combinações de vitória possíveis e prepara o ambiente para uma
        nova partida.

        Args:
            dimensao: Tamanho do tabuleiro. Deve estar entre 3 e 9.
                Padrão: 3 (tabuleiro tradicional 3x3).
                Valores maiores criam tabuleiros mais complexos.

        Raises:
            ValueError: Se a dimensão estiver fora do intervalo permitido (3-9).

        Note:
            Após a inicialização, o ambiente já está pronto para uma partida.
            O jogador inicial é escolhido aleatoriamente a cada reinício.
        """
        if not 3 <= dimensao <= 9:
            raise ValueError(
                f"O tamanho do tabuleiro deve estar entre 3 e 9. "
                f"Valor fornecido: {dimensao}"
            )

        self.dimensao: int = dimensao
        self.numero_de_casas: int = dimensao * dimensao
        
        # Gera todas as combinações de vitória possíveis para este tamanho de tabuleiro
        # Isso é feito uma vez na inicialização para eficiência
        self.combinacoes_de_vitoria: List[List[int]] = self._gerar_combinacoes_de_vitoria()

        # Inicializa o ambiente para uma nova partida
        self.reiniciar_partida()

    def _gerar_combinacoes_de_vitoria(self) -> List[List[int]]:
        """
        Gera todas as combinações de posições que resultam em vitória.

        Para vencer no Jogo da Velha, um jogador precisa completar:
        - Uma linha completa (horizontal)
        - Uma coluna completa (vertical)
        - Uma diagonal completa (principal ou secundária)

        Este método calcula todas essas combinações uma vez e as armazena,
        evitando recálculos durante a verificação de vitória.

        Returns:
            Lista de listas, onde cada lista interna contém os índices das
            posições que formam uma combinação vencedora.

        Example:
            Para um tabuleiro 3x3, retorna combinações como:
            - [0, 1, 2] (primeira linha)
            - [0, 3, 6] (primeira coluna)
            - [0, 4, 8] (diagonal principal)
            - [2, 4, 6] (diagonal secundária)
            - ... e assim por diante
        """
        combinacoes = []

        # 1️⃣ LINHAS (horizontais)
        # Para cada linha, cria uma lista com os índices das posições
        # Exemplo 3x3: [0,1,2], [3,4,5], [6,7,8]
        for indice_inicial in range(0, self.numero_de_casas, self.dimensao):
            linha = list(range(indice_inicial, indice_inicial + self.dimensao))
            combinacoes.append(linha)
        
        # 2️⃣ COLUNAS (verticais)
        # Para cada coluna, cria uma lista pulando de dimensão em dimensão
        # Exemplo 3x3: [0,3,6], [1,4,7], [2,5,8]
        for coluna_inicial in range(self.dimensao):
            coluna = list(range(coluna_inicial, self.numero_de_casas, self.dimensao))
            combinacoes.append(coluna)
        
        # 3️⃣ DIAGONAL PRINCIPAL (de cima-esquerda para baixo-direita)
        # Exemplo 3x3: [0, 4, 8]
        # Pula de (dimensão + 1) em (dimensão + 1) posições
        diagonal_principal = list(range(0, self.numero_de_casas, self.dimensao + 1))
        combinacoes.append(diagonal_principal)
        
        # 4️⃣ DIAGONAL SECUNDÁRIA (de cima-direita para baixo-esquerda)
        # Exemplo 3x3: [2, 4, 6]
        # Começa na última posição da primeira linha e pula de (dimensão - 1)
        diagonal_secundaria = list(range(
            self.dimensao - 1,
            self.numero_de_casas - 1,
            self.dimensao - 1
        ))
        combinacoes.append(diagonal_secundaria)
        
        return combinacoes

    def reiniciar_partida(self) -> np.ndarray:
        """
        Reinicia o ambiente para uma nova partida.

        Limpa o tabuleiro (todas as posições voltam a ser 0), escolhe
        aleatoriamente qual jogador começa, e reseta todas as variáveis
        de estado da partida.

        A escolha aleatória do jogador inicial é importante para o treinamento,
        pois força os agentes a aprenderem a jogar bem tanto como primeiro
        quanto como segundo jogador.

        Returns:
            Cópia do estado inicial do tabuleiro (array de zeros).

        Note:
            Este método deve ser chamado no início de cada nova partida.
            Ele não afeta as combinações de vitória (que são fixas).
        """
        # Cria um novo tabuleiro vazio (todas as posições = 0)
        self.tabuleiro: np.ndarray = np.zeros(self.numero_de_casas, dtype=int)
        
        # Escolhe aleatoriamente qual jogador começa (1='X' ou 2='O')
        # Isso aumenta a diversidade do treinamento
        self.jogador_atual = random.choice([1, 2])
        
        # Reseta as variáveis de estado da partida
        self.partida_finalizada: bool = False
        self.vencedor: Optional[int] = None
        
        return self.obter_estado()

    def obter_estado(self) -> np.ndarray:
        """
        Retorna uma cópia do estado atual do tabuleiro.

        Retorna uma cópia (não uma referência) para garantir que o estado
        não seja modificado acidentalmente de fora do ambiente.

        Returns:
            Cópia do array NumPy representando o estado atual do tabuleiro.
            Cada elemento é 0 (vazio), 1 ('X') ou 2 ('O').

        Note:
            Retorna uma cópia para evitar que modificações externas afetem
            o estado interno do ambiente.
        """
        return self.tabuleiro.copy()

    def obter_acoes_validas(self) -> List[int]:
        """
        Retorna uma lista com todas as ações válidas (posições vazias).

        Uma ação válida é uma posição no tabuleiro que está vazia (valor 0).
        Este método é essencial para o agente saber quais jogadas são possíveis
        em um determinado estado.

        Returns:
            Lista de índices (inteiros) representando as posições vazias no tabuleiro.
            Se o tabuleiro estiver cheio, retorna uma lista vazia.

        Example:
            >>> ambiente = AmbienteJogoDaVelha()
            >>> ambiente.reiniciar_partida()
            >>> acoes = ambiente.obter_acoes_validas()
            >>> # Retorna [0, 1, 2, 3, 4, 5, 6, 7, 8] para um tabuleiro vazio 3x3
        """
        # Encontra todos os índices onde o valor é 0 (casa vazia)
        indices_vazios = np.where(self.tabuleiro == 0)[0]
        return indices_vazios.tolist()
    
    def obter_estado_como_tupla(self) -> Tuple:
        """
        Retorna o estado atual como uma tupla imutável.

        Tuplas são imutáveis e podem ser usadas como chaves em dicionários,
        o que é essencial para a Tabela Q do agente. A Tabela Q usa estados
        (tuplas) como chaves para armazenar os valores Q de cada ação.

        Returns:
            Tupla representando o estado atual do tabuleiro.
            Exemplo para tabuleiro vazio 3x3: (0, 0, 0, 0, 0, 0, 0, 0, 0)

        Note:
            Este método é usado principalmente pelo agente para indexar
            sua Tabela Q. A imutabilidade da tupla garante que o estado
            não mude acidentalmente.
        """
        return tuple(self.tabuleiro)

    def executar_jogada(self, acao: int) -> Tuple[np.ndarray, float, bool]:
        """
        Executa uma jogada no ambiente e retorna o resultado.

        Este é o método principal de interação com o ambiente. Ele:
        1. Valida se a ação é permitida
        2. Atualiza o tabuleiro com a jogada
        3. Verifica se a partida terminou (vitória ou empate)
        4. Calcula a recompensa apropriada
        5. Alterna o jogador atual
        6. Retorna o novo estado, recompensa e status de término

        Args:
            acao: Índice da posição onde o jogador atual deseja jogar.
                Deve estar entre 0 e (dimensão² - 1).
                A posição deve estar vazia (valor 0 no tabuleiro).

        Returns:
            Tupla contendo três elementos:
            - proximo_estado (np.ndarray): Estado do tabuleiro após a jogada
            - recompensa (float): Recompensa recebida:
                * 1.0 se o jogador atual venceu
                * 0.0 se a partida continua ou terminou em empate
            - partida_finalizada (bool): True se a partida terminou, False caso contrário

        Raises:
            ValueError: Se a ação for inválida (posição ocupada ou partida já finalizada).

        Note:
            Após executar uma jogada, o jogador atual é automaticamente alternado.
            Se a partida terminar, nenhuma jogada adicional será permitida.

        Example:
            >>> ambiente = AmbienteJogoDaVelha()
            >>> ambiente.reiniciar_partida()
            >>> estado, recompensa, finalizado = ambiente.executar_jogada(4)
            >>> # Jogada no centro do tabuleiro 3x3
        """
        # Validação 1: Verifica se a posição está vazia
        if self.tabuleiro[acao] != 0:
            raise ValueError(
                f"Ação inválida: posição {acao} já está ocupada pelo jogador "
                f"{'X' if self.tabuleiro[acao] == 1 else 'O'}."
            )
        
        # Validação 2: Verifica se a partida ainda não terminou
        if self.partida_finalizada:
            raise ValueError(
                "Não é possível executar jogadas em uma partida já finalizada. "
                f"Vencedor: {self.vencedor if self.vencedor != 0 else 'Empate'}"
            )

        # Executa a jogada: marca a posição com o símbolo do jogador atual
        self.tabuleiro[acao] = self.jogador_atual
        
        # Inicializa a recompensa como 0.0 (padrão: partida continua ou empate)
        recompensa = 0.0

        # Verifica se o jogador atual venceu após esta jogada
        if self._verificar_vitoria(self.jogador_atual):
            self.partida_finalizada = True
            self.vencedor = self.jogador_atual
            recompensa = 1.0  # Recompensa positiva para o vencedor
        # Verifica se o tabuleiro está cheio (empate)
        elif len(self.obter_acoes_validas()) == 0:
            self.partida_finalizada = True
            self.vencedor = 0  # 0 representa empate
            # Recompensa permanece 0.0 para empate

        # Alterna para o próximo jogador (se a partida não terminou)
        self._alternar_jogador()
        
        return self.obter_estado(), recompensa, self.partida_finalizada

    def _verificar_vitoria(self, jogador: int) -> bool:
        """
        Verifica se um jogador específico venceu a partida.

        Verifica todas as combinações de vitória possíveis para determinar
        se o jogador especificado completou alguma linha, coluna ou diagonal.

        Args:
            jogador: Identificador do jogador a verificar (1 para 'X', 2 para 'O').

        Returns:
            True se o jogador venceu (completou uma combinação vencedora),
            False caso contrário.

        Note:
            Este é um método privado (prefixo _) usado internamente pelo
            método executar_jogada() para verificar vitória após cada jogada.
        """
        # Verifica se alguma das combinações de vitória está completa
        # Uma combinação está completa se todas as posições têm o mesmo jogador
        for combinacao in self.combinacoes_de_vitoria:
            if all(self.tabuleiro[posicao] == jogador for posicao in combinacao):
                return True
        return False

    def _alternar_jogador(self):
        """
        Alterna o jogador atual para o próximo turno.

        Este método é chamado automaticamente após cada jogada para garantir
        que os jogadores se alternem corretamente. Se o jogador atual é 1 ('X'),
        muda para 2 ('O'), e vice-versa.

        Note:
            Este é um método privado (prefixo _) usado internamente pelo
            método executar_jogada(). Não deve ser chamado diretamente.
        """
        self.jogador_atual = 2 if self.jogador_atual == 1 else 1

    def exibir_tabuleiro(self):
        """
        Exibe o tabuleiro atual de forma visual no console.

        Cria uma representação visual do tabuleiro usando caracteres ASCII,
        facilitando a visualização do estado atual do jogo durante testes
        e depuração.

        O formato exibido é:
        ```
          X │ O │
        ───┼───┼───
            │ X │ O
        ───┼───┼───
          O │   │ X
        ```

        Note:
            Este método não retorna nada, apenas imprime no console.
            Útil para visualização durante testes e desenvolvimento.
        """
        # Mapeia valores numéricos para símbolos visuais
        simbolos = {0: " ", 1: "X", 2: "O"}
        
        print()  # Linha em branco antes do tabuleiro
        
        # Itera sobre cada linha do tabuleiro
        for indice_linha in range(self.dimensao):
            # Calcula o intervalo de índices para esta linha
            inicio_linha = indice_linha * self.dimensao
            fim_linha = inicio_linha + self.dimensao
            
            # Converte os valores numéricos para símbolos visuais
            linha_simbolos = [simbolos[valor] for valor in self.tabuleiro[inicio_linha:fim_linha]]
            
            # Imprime a linha com separadores verticais
            print(" " + " │ ".join(linha_simbolos))
            
            # Adiciona separador horizontal entre linhas (exceto após a última)
            if indice_linha < self.dimensao - 1:
                separador_horizontal = "───" + "┼───" * (self.dimensao - 1)
                print(separador_horizontal)
        
        print()  # Linha em branco após o tabuleiro
