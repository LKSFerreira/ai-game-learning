"""
Define o ambiente do Labirinto, que servirá como o 'mundo' para o nosso agente.

Este módulo contém a classe `Labirinto`, que é responsável por:
- Armazenar a estrutura do labirinto (paredes, caminhos, saída).
- Rastrear a posição atual do agente.
- Fornecer as ações possíveis que o agente pode tomar.
- Executar uma ação e retornar o resultado (novo estado, recompensa, se terminou).
- Reiniciar o ambiente para um novo episódio de treinamento.

A classe é projetada para ser independente do algoritmo de IA, seguindo os
padrões de ambientes de Aprendizado por Reforço.
"""

from typing import TypeAlias, Literal

# Apelidos de tipo para melhorar a legibilidade do código.
Posicao: TypeAlias = tuple[int, int]
DirecaoPadrao: TypeAlias = Literal["cima", "baixo", "esquerda", "direita"]
AcaoUsuario: TypeAlias = Literal[
    "W", "w", "A", "a", "S", "s", "D", "d", "cima", "baixo", "esquerda", "direita"
]

# Mapeamento de teclas WASD para direções padronizadas.
#
# É como mapear os controles do teclado para movimentos no jogo.
# Isso permite que jogadores humanos usem W,A,S,D enquanto o código
# internamente trabalha com nomes descritivos e legíveis.
MAPEAMENTO_TECLAS: dict[str, DirecaoPadrao] = {
    "W": "cima",
    "w": "cima",
    "A": "esquerda",
    "a": "esquerda",
    "S": "baixo",
    "s": "baixo",
    "D": "direita",
    "d": "direita",
    "cima": "cima",
    "baixo": "baixo",
    "esquerda": "esquerda",
    "direita": "direita",
}

# Conjunto de todas as ações válidas (para validação rápida).
ACOES_VALIDAS: set[str] = set(MAPEAMENTO_TECLAS.keys())


class Labirinto:
    """
    Representa o ambiente do labirinto, gerenciando o estado, ações e recompensas.

    É como a "arena" ou "dungeon" no Ragnarok onde as batalhas acontecem.
    O ambiente mantém as regras do jogo e garante que tudo funcione corretamente.

    O labirinto é representado por uma matriz onde:
    - ' ' (espaço) representa um caminho livre
    - '#' representa uma parede/obstáculo
    - 'A' é usado apenas para visualização (posição do agente)
    - 'S' é usado apenas para visualização (saída do labirinto)

    Atributos:
        _matriz (list[list[str]]): A grade 2D que representa o labirinto.
        estado_inicial (Posicao): A posição de início do agente.
        ponto_final (Posicao): A posição da saída do labirinto.
        posicao_agente (Posicao): A posição atual do agente, que muda a cada passo.
        _numero_linhas (int): Quantidade de linhas do labirinto.
        _numero_colunas (int): Quantidade de colunas do labirinto.
    """

    def __init__(
        self,
        matriz_labirinto: list[list[str]],
        ponto_inicial: Posicao,
        ponto_final: Posicao,
    ) -> None:
        """
        Inicializa o ambiente do Labirinto.

        É como criar uma nova "dungeon" no Ragnarok com um mapa específico.
        O agente começa em uma posição inicial e deve encontrar a saída.

        Args:
            matriz_labirinto (list[list[str]]): Uma grade representando o labirinto,
                onde ' ' é caminho, '#' é parede.
            ponto_inicial (Posicao): Uma tupla (linha, coluna) para a posição inicial.
            ponto_final (Posicao): Uma tupla (linha, coluna) para a posição final.

        Raises:
            ValueError: Se a matriz do labirinto estiver vazia ou malformada.
        """
        if not matriz_labirinto or len(matriz_labirinto) == 0:
            raise ValueError("A matriz do labirinto não pode estar vazia.")
        if not matriz_labirinto[0] or len(matriz_labirinto[0]) == 0:
            raise ValueError("A matriz do labirinto está malformada.")

        self._matriz = matriz_labirinto
        self.estado_inicial = ponto_inicial
        self.ponto_final = ponto_final
        self.posicao_agente = self.estado_inicial
        self._numero_linhas = len(self._matriz)
        self._numero_colunas = len(self._matriz[0])

    def reiniciar(self) -> Posicao:
        """
        Reinicia o ambiente para o estado inicial.

        Isso coloca o agente de volta na posição de partida. É chamado no início
        de cada novo episódio de treinamento. É como resetar a dungeon para uma
        nova tentativa no Ragnarok.

        Returns:
            Posicao: O estado inicial do agente após reiniciar.
        """
        self.posicao_agente = self.estado_inicial
        return self.posicao_agente

    def executar_acao(self, acao: AcaoUsuario) -> tuple[Posicao, float, bool]:
        """
        Executa uma ação e atualiza o estado do ambiente.

        É como um jogador fazer um movimento na dungeon: o ambiente processa
        a ação, atualiza o estado, verifica se chegou na saída e retorna as
        informações necessárias para o aprendizado.

        Aceita tanto teclas WASD quanto nomes completos (cima, baixo, esquerda, direita).

        Args:
            acao (AcaoUsuario): A ação a ser executada ('W'/'w'/'cima', 'S'/'s'/'baixo',
                'A'/'a'/'esquerda', 'D'/'d'/'direita').

        Returns:
            tuple[Posicao, float, bool]: Uma tupla contendo:
                - O novo estado (a nova posição do agente).
                - A recompensa recebida por realizar a ação.
                - Um booleano indicando se o episódio terminou (agente na saída).

        Raises:
            ValueError: Se a ação fornecida for inválida.
        """
        # Valida se a ação está no mapeamento
        if acao not in ACOES_VALIDAS:
            raise ValueError(
                f'Ação inválida: "{acao}". Use: W/A/S/D (ou cima/baixo/esquerda/direita)'
            )

        # Normaliza a ação para o formato padrão interno
        direcao_padrao = self._normalizar_acao(acao)

        proxima_posicao = self._calcular_proxima_posicao(direcao_padrao)

        if self._eh_posicao_valida(proxima_posicao):
            self._matriz[self.posicao_agente[0]][self.posicao_agente[1]] = "•"
            self.posicao_agente = proxima_posicao

        recompensa = self._calcular_recompensa()
        terminou = self._verificar_se_chegou_no_final()

        return self.posicao_agente, recompensa, terminou

    def _normalizar_acao(self, acao: AcaoUsuario) -> DirecaoPadrao:
        """
        Normaliza a entrada do usuário para o formato padrão interno.

        Converte teclas WASD (maiúsculas ou minúsculas) para as direções
        padronizadas que o código usa internamente. Isso mantém o código
        legível enquanto permite entradas amigáveis ao usuário.

        Args:
            acao (AcaoUsuario): A ação fornecida pelo usuário.

        Returns:
            DirecaoPadrao: A direção normalizada.
        """
        return MAPEAMENTO_TECLAS[acao]

    def _calcular_proxima_posicao(self, direcao: DirecaoPadrao) -> Posicao:
        """
        Calcula a posição resultante de uma ação, sem mover o agente.

        É como simular o movimento antes de executá-lo de fato. Útil para
        verificar se a posição é válida antes de atualizar o estado.

        Args:
            direcao (DirecaoPadrao): A direção normalizada.

        Returns:
            Posicao: A posição resultante da ação.
        """
        linha_atual, coluna_atual = self.posicao_agente

        if direcao == "cima":
            return (linha_atual - 1, coluna_atual)
        if direcao == "baixo":
            return (linha_atual + 1, coluna_atual)
        if direcao == "esquerda":
            return (linha_atual, coluna_atual - 1)
        if direcao == "direita":
            return (linha_atual, coluna_atual + 1)

        return self.posicao_agente

    def _eh_posicao_valida(self, posicao: Posicao) -> bool:
        """
        Verifica se uma posição está dentro dos limites e não é uma parede.

        É como verificar se o jogador pode andar naquela célula da dungeon
        ou se há um obstáculo bloqueando o caminho.

        Args:
            posicao (Posicao): A posição a ser verificada (linha, coluna).

        Returns:
            bool: True se a posição é válida, False caso contrário.
        """
        linha, coluna = posicao

        # Verifica se está dentro dos limites verticais
        if not (0 <= linha < self._numero_linhas):
            return False

        # Verifica se está dentro dos limites horizontais
        if not (0 <= coluna < self._numero_colunas):
            return False

        # Verifica se não é uma parede
        if self._matriz[linha][coluna] == "#":
            return False

        return True

    def _calcular_recompensa(self) -> float:
        """
        Calcula a recompensa com base na posição atual do agente.

        Sistema de recompensas:
        - +10.0 * (tamanho da matriz): Chegou na saída (objetivo alcançado!)
        - -0.1: Qualquer outro movimento (incentiva caminhos mais curtos)

        É como ganhar XP no Ragnarok: você ganha muito ao completar o objetivo,
        mas perde um pouco a cada passo para incentivar eficiência.

        Returns:
            float: A recompensa calculada.
        """
        if self._verificar_se_chegou_no_final():
            return 10.0 * (self._numero_linhas * self._numero_colunas)
        else:
            return -0.1

    def _verificar_se_chegou_no_final(self) -> bool:
        """
        Verifica se o agente chegou ao ponto final.

        Returns:
            bool: True se chegou na saída, False caso contrário.
        """
        return self.posicao_agente == self.ponto_final

    def __str__(self) -> str:
        """
        Retorna uma representação em string do labirinto com o agente.

        Exibe o labirinto no console de forma visual, mostrando:
        - 'A' para a posição atual do agente
        - 'S' para a saída (ponto final)
        - '#' para paredes
        - Espaços para caminhos livres

        É como o minimapa do Ragnarok, mostrando onde você está e onde
        precisa chegar.

        Returns:
            str: Representação visual do labirinto.
        """
        # Cria uma cópia profunda da matriz para não modificar o original
        matriz_para_exibicao = [list(linha) for linha in self._matriz]

        # Marca a posição do agente
        linha_agente, coluna_agente = self.posicao_agente
        matriz_para_exibicao[linha_agente][coluna_agente] = "A"

        # Marca a saída
        linha_saida, coluna_saida = self.ponto_final
        matriz_para_exibicao[linha_saida][coluna_saida] = "S"

        # Formata cada linha com espaçamento entre células
        linhas_formatadas = [
            " ".join(celula for celula in linha) for linha in matriz_para_exibicao
        ]

        return "\n".join(linhas_formatadas)

    def imprimir_labirinto(lab):
        """
        Função auxiliar para imprimir o estado atual do labirinto
        em formato de GRADE, usando caracteres de desenho de caixa.

        Marca:
        'A' = Posição atual do Agente
        'F' = Posição Final (objetivo)
        '#' = Parede
        ' ' = Caminho livre
        '•' = Caminho por qual passou
        """

        try:
            # Cria uma cópia da matriz para "desenhar" nela
            visualizacao = [list(linha) for linha in lab._matriz]
            linhas = len(visualizacao)
            if linhas == 0:
                print("Labirinto vazio.")
                return
            colunas = len(visualizacao[0])

            ponto_final = lab.ponto_final
            pos_agente = lab.posicao_agente

        except AttributeError as e:
            print(f"Erro: O objeto Labirinto não possui um atributo esperado: {e}")
            print(str(lab))  # Fallback para o print antigo
            return
        except Exception as e:
            print(f"Erro inesperado ao ler o labirinto: {e}")
            print(str(lab))
            return

        # 1. Marcar o ponto final (F)
        if 0 <= ponto_final[0] < linhas and 0 <= ponto_final[1] < colunas:
            if visualizacao[ponto_final[0]][ponto_final[1]] != "#":
                visualizacao[ponto_final[0]][ponto_final[1]] = "F"

        # 2. Marcar o agente (A) (sobrepõe 'F' se estiver no final)
        if 0 <= pos_agente[0] < linhas and 0 <= pos_agente[1] < colunas:
            visualizacao[pos_agente[0]][pos_agente[1]] = "A"

        # --- Caracteres de Desenho (Baseado na sua sugestão) ---
        BARRA_H = "───"  # A barra horizontal que você pediu
        BARRA_V = "│"

        # Cantos
        CANTO_SE = "┌"
        CANTO_SD = "┐"
        CANTO_IE = "└"
        CANTO_ID = "┘"

        # Junções
        JUNCAO_CIMA = "┬"
        JUNCAO_BAIXO = "┴"
        JUNCAO_ESQ = "├"
        JUNCAO_DIR = "┤"
        JUNCAO_MEIO = "┼"  # A junção que você pediu

        # --- Lógica de Impressão da Grade ---

        # 1. Linha Superior (Ex: ┌───┬───┬───┐)
        linha_superior = CANTO_SE + JUNCAO_CIMA.join([BARRA_H] * colunas) + CANTO_SD
        print(linha_superior)

        # 2. Loop pelas linhas de conteúdo e separadores
        for i, linha in enumerate(visualizacao):

            # Linha de Conteúdo (Ex: │ A │ # │ F │)
            # Usamos " {c} " para centralizar (3 caracteres, igual ao BARRA_H)
            celulas_conteudo = [f" {c} " for c in linha]
            linha_conteudo = BARRA_V + BARRA_V.join(celulas_conteudo) + BARRA_V
            print(linha_conteudo)

            # Linha Separadora (se não for a última)
            # Ex: ├───┼───┼───┤
            if i < linhas - 1:
                linha_meio = (
                    JUNCAO_ESQ + JUNCAO_MEIO.join([BARRA_H] * colunas) + JUNCAO_DIR
                )
                print(linha_meio)

        # 3. Linha Inferior (Ex: └───┴───┴───┘)
        linha_inferior = CANTO_IE + JUNCAO_BAIXO.join([BARRA_H] * colunas) + CANTO_ID
        print(linha_inferior)
