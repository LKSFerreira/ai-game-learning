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

# Começamos importando os tipos que usaremos. Fazer isso no início do arquivo
# é uma boa prática em Python, pois deixa claro quais ferramentas de tipagem
# nosso código irá utilizar.
from typing import TypeAlias, Literal

# Para tornar o código mais legível, vamos criar "apelidos" (TypeAlias) para os
# tipos de dados mais complexos que usaremos repetidamente.
Posicao: TypeAlias = tuple[int, int]
Acao: TypeAlias = Literal["cima", "baixo", "esquerda", "direita"]


# --- PENSAMENTO 1: A Estrutura Fundamental (A Classe e o Construtor) ---
# A primeira coisa que precisamos é de uma maneira de "criar" um labirinto.
# Isso nos leva diretamente à necessidade de uma classe e seu construtor, o `__init__`.
# O que um labirinto precisa para existir?
# 1. Uma matriz (lista de listas) que define sua estrutura.
# 2. Um ponto de partida para o agente.
# 3. Um ponto final (a saída).
# Esses serão os parâmetros do nosso construtor.

class Labirinto:
    """
    Representa o ambiente do labirinto, gerenciando o estado, ações e recompensas.

    Atributos:
        matriz (list[list[str]]): A grade 2D que representa o labirinto.
        estado_inicial (Posicao): A posição de início do agente.
        ponto_final (Posicao): A posição da saída do labirinto.
        posicao_agente (Posicao): A posição atual do agente, que muda a cada passo.
    """

    def __init__(
        self,
        matriz_labirinto: list[list[str]],
        ponto_inicial: Posicao,
        ponto_final: Posicao
    ) -> None:
        """
        Inicializa o ambiente do Labirinto.

        Args:
            matriz_labirinto (list[list[str]]): Uma grade representando o labirinto,
                onde ' ' é caminho, '#' é parede e 'S' é a saída.
            ponto_inicial (Posicao): Uma tupla (linha, coluna) para a posição inicial.
            ponto_final (Posicao): Uma tupla (linha, coluna) para a posição final.
        """
        # Armazenamos os parâmetros recebidos como atributos da instância.
        # O prefixo `_` em `_matriz` sugere que ele não deve ser modificado
        # diretamente de fora da classe após a criação.
        self._matriz = matriz_labirinto
        self.estado_inicial = ponto_inicial
        self.ponto_final = ponto_final

        # A posição do agente é a parte "dinâmica" do nosso ambiente.
        # Ela começa, naturalmente, no ponto inicial.
        self.posicao_agente = self.estado_inicial

        # Guardamos as dimensões para facilitar verificações futuras.
        self._numero_linhas = len(self._matriz)
        self._numero_colunas = len(self._matriz[0])


    # --- PENSAMENTO 2: Reiniciando uma Tentativa ---
    # No treinamento de IA, o agente tentará resolver o labirinto milhares de vezes.
    # Cada tentativa é um "episódio". Precisamos de uma maneira de resetar o ambiente
    # para o estado inicial no começo de cada episódio. O método `reiniciar` faz isso.
    def reiniciar(self) -> Posicao:
        """
        Reinicia o ambiente para o estado inicial.

        Isso coloca o agente de volta na posição de partida. É chamado no início
        de cada novo episódio de treinamento.

        Returns:
            Posicao: O estado inicial do agente após reiniciar.
        """
        self.posicao_agente = self.estado_inicial
        # É convencional que a função de reset retorne o estado inicial,
        # para que o agente saiba onde está começando o novo episódio.
        return self.posicao_agente


    # --- PENSAMENTO 3: A Ação Principal (Movimento) ---
    # Agora, a parte mais importante: como o agente interage com o mundo?
    # Ele executa uma ação. Precisamos de um método que receba uma ação
    # (como "cima") e atualize o estado do mundo de acordo.
    # Este método é o coração do ciclo de Aprendizado por Reforço.
    def executar_acao(self, acao: Acao) -> tuple[Posicao, float, bool]:
        """
        Executa uma ação e atualiza o estado do ambiente.

        Args:
            acao (Acao): A ação a ser executada ('cima', 'baixo', 'esquerda', 'direita').

        Returns:
            tuple[Posicao, float, bool]: Uma tupla contendo:
                - O novo estado (a nova posição do agente).
                - A recompensa recebida por realizar a ação.
                - Um booleano indicando se o episódio terminou (agente na saída).
        """
        # Para manter este método limpo, vamos delegar a lógica de calcular
        # a próxima posição para um método auxiliar (que criaremos a seguir).
        proxima_posicao = self._calcular_proxima_posicao(acao)

        # Antes de mover o agente, verificamos se o movimento é válido.
        # Novamente, delegaremos essa lógica para outro método auxiliar.
        if self._eh_posicao_valida(proxima_posicao):
            self.posicao_agente = proxima_posicao

        # Após o movimento (ou tentativa), calculamos a recompensa.
        # E, mais uma vez, usaremos um método auxiliar para isso.
        recompensa = self._calcular_recompensa()

        # Verificamos se o episódio terminou.
        terminou = self.posicao_agente == self.ponto_final

        return self.posicao_agente, recompensa, terminou


    # --- PENSAMENTO 4: A Lógica Interna (Métodos Auxiliares) ---
    # O método `executar_acao` precisa de várias verificações. Para manter o código
    # organizado e legível (Princípio da Responsabilidade Única), criamos
    # métodos "privados" (iniciados com `_`) para cada tarefa específica.

    def _calcular_proxima_posicao(self, acao: Acao) -> Posicao:
        """Calcula a posição resultante de uma ação, sem mover o agente."""
        linha_atual, coluna_atual = self.posicao_agente
        if acao == "cima":
            return (linha_atual - 1, coluna_atual)
        if acao == "baixo":
            return (linha_atual + 1, coluna_atual)
        if acao == "esquerda":
            return (linha_atual, coluna_atual - 1)
        if acao == "direita":
            return (linha_atual, coluna_atual + 1)
        # Este retorno nunca deve acontecer se a tipagem de Acao for respeitada,
        # mas é uma boa prática ter um caso padrão.
        return self.posicao_agente


    def _eh_posicao_valida(self, posicao: Posicao) -> bool:
        """Verifica se uma posição está dentro dos limites e não é uma parede."""
        linha, coluna = posicao
        # Verificação 1: Está dentro dos limites verticais?
        if not (0 <= linha < self._numero_linhas):
            return False
        # Verificação 2: Está dentro dos limites horizontais?
        if not (0 <= coluna < self._numero_colunas):
            return False
        # Verificação 3: Não é uma parede?
        if self._matriz[linha][coluna] == '#':
            return False
        return True


    def _calcular_recompensa(self) -> float:
        """Calcula a recompensa com base na posição atual do agente."""
        # Recompensa máxima por atingir o objetivo.
        if self.posicao_agente == self.ponto_final:
            return 10.0
        # Penalidade pequena para cada movimento. Isso incentiva o agente a
        # encontrar o caminho mais curto, em vez de vagar indefinidamente.
        # É uma técnica comum chamada "reward shaping".
        else:
            return -0.1


    # --- PENSAMENTO 5: Uma Forma de "Ver" o Ambiente ---
    # Para depuração e visualização, é extremamente útil poder imprimir o estado
    # atual do labirinto. O método especial `__str__` do Python é perfeito para isso.
    # Ele define o que acontece quando chamamos `print(objeto_labirinto)`.
    def __str__(self) -> str:
        """Retorna uma representação em string do labirinto com o agente."""
        # Criamos uma cópia da matriz para não modificar a original.
        matriz_para_exibicao = [list(linha) for linha in self._matriz]

        # Marcamos a posição do agente com 'A'.
        linha_agente, coluna_agente = self.posicao_agente
        matriz_para_exibicao[linha_agente][coluna_agente] = 'A'

        # Marcamos a saída com 'S' para clareza.
        linha_saida, coluna_saida = self.ponto_final
        matriz_para_exibicao[linha_saida][coluna_saida] = 'S'

        # Convertemos a matriz de caracteres em uma única string formatada.
        linhas_formatadas = [" ".join(celula for celula in linha) for linha in matriz_para_exibicao]
        return "\n".join(linhas_formatadas)


# --- PENSAMENTO 6: Teste Rápido e Demonstração ---
# Como sabemos se a nossa classe funciona? Podemos adicionar um bloco de código
# que só é executado quando rodamos este arquivo diretamente.
# Isso nos permite testar a classe de forma isolada e serve como um exemplo
# de como usá-la.
if __name__ == '__main__':
    # Criamos uma matriz de exemplo para o labirinto.
    LABIRINTO_EXEMPLO = [
        [' ', '#', ' ', ' ', ' '],
        [' ', '#', ' ', '#', ' '],
        [' ', ' ', ' ', '#', ' '],
        ['#', '#', ' ', ' ', ' '],
        [' ', ' ', ' ', '#', 'S']  # 'S' aqui é apenas um marcador visual
    ]

    PONTO_INICIAL_EXEMPLO = (0, 0)
    PONTO_FINAL_EXEMPLO = (4, 4)

    # 1. Criamos uma instância do nosso ambiente.
    ambiente = Labirinto(
        matriz_labirinto=LABIRINTO_EXEMPLO,
        ponto_inicial=PONTO_INICIAL_EXEMPLO,
        ponto_final=PONTO_FINAL_EXEMPLO
    )

    # 2. Exibimos o estado inicial.
    print("--- Estado Inicial ---")
    print(ambiente)
    print(f"Posição do Agente: {ambiente.posicao_agente}")

    # 3. Executamos algumas ações para testar a lógica.
    print("\n--- Executando Ações ---")
    # Movimento válido
    estado, recompensa, terminou = ambiente.executar_acao("baixo")
    print(f"Ação: 'baixo' -> Novo Estado: {estado}, Recompensa: {recompensa}, Terminou: {terminou}")

    # Movimento inválido (bater na parede)
    estado, recompensa, terminou = ambiente.executar_acao("direita")
    print(f"Ação: 'direita' -> Novo Estado: {estado}, Recompensa: {recompensa}, Terminou: {terminou}")
    print("\n--- Estado Após Ações ---")
    print(ambiente)

    # 4. Testamos o reinício.
    ambiente.reiniciar()
    print("\n--- Após Reiniciar ---")
    print(ambiente)
    print(f"Posição do Agente: {ambiente.posicao_agente}")