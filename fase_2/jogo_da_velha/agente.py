"""
Módulo: 🧠 agente.py
Projeto: 📘 AI Game Learning

Este módulo implementa um Agente de Aprendizado por Reforço que utiliza o algoritmo
Q-Learning para aprender a jogar Jogo da Velha de forma autônoma.

O agente é projetado para ser compatível com dois modos de operação:
    - Treinamento em massa: utilizado pelo módulo treinador.py para treinar o agente
      através de milhares de partidas em modo self-play.
    - Aprendizado interativo: utilizado pelo módulo jogar.py para permitir que o
      agente aprenda enquanto joga contra um humano.

O algoritmo Q-Learning funciona através de uma tabela Q que armazena o valor esperado
de cada ação possível em cada estado do jogo. Com o tempo, o agente aprende quais
ações levam a melhores resultados e ajusta sua estratégia automaticamente.
"""

import random
import pickle
from typing import List, Tuple, Dict
from pathlib import Path


class AgenteQLearning:
    """
    Agente de Aprendizado por Reforço que utiliza Q-Learning para jogar Jogo da Velha.

    Este agente aprende através da exploração (tentando ações aleatórias) e exploração
    (usando o conhecimento adquirido). A estratégia Epsilon-Greedy equilibra esses dois
    comportamentos, permitindo que o agente descubra novas estratégias enquanto também
    aproveita o conhecimento já adquirido.

    Analogia didática: Pense neste Agente como um jogador de Ragnarok Online que está
    aprendendo a melhor estratégia para derrotar monstros. Inicialmente, ele tenta
    diferentes abordagens (exploração), mas com o tempo, ele passa a usar as estratégias
    que funcionaram melhor no passado (exploração).

    Attributes:
        alpha (float): Taxa de aprendizado (0.0 a 1.0). Controla o quanto o agente
            atualiza seus valores Q a cada aprendizado. Valores maiores fazem o agente
            aprender mais rápido, mas podem torná-lo instável.
        gamma (float): Fator de desconto (0.0 a 1.0). Determina o quanto o agente
            valoriza recompensas futuras em relação às imediatas. 1.0 significa que
            recompensas futuras são tão importantes quanto as atuais.
        epsilon (float): Taxa de exploração (0.0 a 1.0). Probabilidade de escolher
            uma ação aleatória ao invés da melhor ação conhecida. Inicia em 1.0
            (100% exploração) e decai com o tempo.
        epsilon_minimo (float): Valor mínimo que epsilon pode atingir. Garante que
            o agente sempre mantenha um mínimo de exploração, mesmo após muito treino.
        taxa_decaimento_epsilon (float): Taxa pela qual epsilon é multiplicado a
            cada partida. Valores próximos de 1.0 fazem o epsilon decair lentamente.
        jogador (int): Identificador do jogador (1 para 'X', 2 para 'O').
        simbolo (str): Símbolo visual do jogador ('X' ou 'O').
        tabela_q (Dict[Tuple, Dict[int, float]]): Tabela Q que armazena o valor
            esperado de cada ação em cada estado. Estrutura: {estado: {acao: valor_q}}.
        partidas_treinadas (int): Contador total de partidas em que o agente participou.
        vitorias (int): Número de partidas vencidas pelo agente.
        derrotas (int): Número de partidas perdidas pelo agente.
        empates (int): Número de partidas que terminaram em empate.
        historico_partida (List[Tuple[Tuple, int]]): Lista de (estado, ação) registradas
            durante a partida atual. Usado para aprendizado Monte Carlo no final da partida.

    Example:
        >>> agente = AgenteQLearning(alpha=0.5, gamma=1.0, jogador=1)
        >>> estado = ((0, 0, 0, 0, 0, 0, 0, 0, 0),)
        >>> acoes_validas = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        >>> acao_escolhida = agente.escolher_acao(estado, acoes_validas)
        >>> print(f"Agente escolheu a ação: {acao_escolhida}")
    """

    def __init__(self,
                 alpha: float = 0.5,
                 gamma: float = 1.0,
                 epsilon: float = 1.0,
                 epsilon_minimo: float = 0.001,
                 taxa_decaimento_epsilon: float = 0.99999,
                 jogador: int = 1
                ):
        """
        Inicializa uma nova instância do Agente Q-Learning.

        Args:
            alpha: Taxa de aprendizado. Padrão: 0.5. Valores típicos: 0.1 a 0.9.
            gamma: Fator de desconto para recompensas futuras. Padrão: 1.0.
                Para Jogo da Velha, 1.0 é apropriado pois todas as jogadas
                são igualmente importantes.
            epsilon: Taxa inicial de exploração. Padrão: 1.0 (100% exploração).
                O agente começa totalmente exploratório e se torna mais
                explorador com o tempo.
            epsilon_minimo: Valor mínimo de epsilon após decaimento. Padrão: 0.001.
                Garante que o agente sempre mantenha um mínimo de exploração.
            taxa_decaimento_epsilon: Taxa de decaimento de epsilon por partida.
                Padrão: 0.99999 (decai muito lentamente). Valores menores
                fazem o epsilon decair mais rápido.
            jogador: Identificador do jogador. Padrão: 1 (jogador 'X').
                Use 2 para o jogador 'O'.

        Note:
            Todos os atributos de estatísticas (vitorias, derrotas, empates)
            são inicializados em zero e atualizados durante o treinamento.
        """
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
        """
        Obtém o valor Q (valor esperado) de uma ação específica em um estado.

        Se o estado ou a ação não existirem na tabela Q, eles são criados
        automaticamente com valor inicial de 0.0. Isso permite que o agente
        aprenda sobre novos estados e ações conforme os encontra.

        Args:
            estado: Tupla representando o estado atual do tabuleiro.
            acao: Índice da ação (posição no tabuleiro de 0 a 8).

        Returns:
            Valor Q da ação no estado especificado. Retorna 0.0 se o estado
            ou ação ainda não foram explorados.

        Note:
            Este método é idempotente: múltiplas chamadas com os mesmos
            parâmetros retornam o mesmo valor, mas podem criar entradas
            na tabela Q se elas não existirem.
        """
        if estado not in self.tabela_q:
            self.tabela_q[estado] = {}
        if acao not in self.tabela_q[estado]:
            self.tabela_q[estado][acao] = 0.0
        return self.tabela_q[estado][acao]

    def atualizar_valor_q(self, estado: Tuple, acao: int, recompensa: float, proximo_estado: Tuple, finalizado: bool):
        """
        Atualiza o valor Q usando Temporal Difference (TD) Learning.

        Este é o método principal de atualização do valor Q do agente. Ele implementa a
        fórmula clássica do Q-Learning:

            Q(estado, acao) = Q(estado, acao) + alpha * (recompensa + gamma * max(Q(proximo_estado)) - Q(estado, acao))

        O aprendizado funciona da seguinte forma:
        1. O agente compara sua "opinião antiga" (valor Q atual) com o "valor real"
           (recompensa imediata + melhor valor futuro).
        2. A diferença entre esses valores é a "surpresa" (erro de predição).
        3. O agente ajusta seu valor Q proporcionalmente à surpresa e à taxa de aprendizado.

        Este método é usado tanto para aprendizado incremental (TD Learning) durante
        partidas interativas quanto internamente pelo método de aprendizado Monte Carlo.

        Args:
            estado: Estado do tabuleiro antes da ação ser executada.
            acao: Ação que foi tomada no estado.
            recompensa: Recompensa imediata recebida após executar a ação.
                Valores típicos: +1.0 (vitória), -1.0 (derrota), 0.0 (empate/continua).
            proximo_estado: Estado do tabuleiro após a ação ser executada.
            finalizado: Se True, indica que o jogo terminou após esta ação.
                Quando True, não há valor futuro a considerar.

        Note:
            Este método modifica diretamente a tabela Q do agente. O aprendizado
            é incremental e baseado na diferença temporal (TD error), permitindo
            que o agente aprenda mesmo sem esperar o fim da partida.
        """
        opiniao_antiga = self.obter_valor_q(estado, acao)
        
        # Se o jogo terminou, não há valor futuro a considerar
        melhor_valor_futuro = 0.0 if finalizado else self._obter_melhor_valor_q_futuro(proximo_estado)
        
        # Calcula o valor real da jogada (recompensa imediata + valor futuro descontado)
        valor_real_da_jogada = recompensa + self.gamma * melhor_valor_futuro
        
        # Calcula a "surpresa" (erro de predição)
        surpresa = valor_real_da_jogada - opiniao_antiga
        
        # Atualiza o valor Q proporcionalmente à surpresa
        novo_valor_q = opiniao_antiga + self.alpha * surpresa
        self.tabela_q[estado][acao] = novo_valor_q

    def _obter_melhor_valor_q_futuro(self, estado: Tuple) -> float:
        """
        Obtém o maior valor Q disponível para um estado futuro específico.

        Este método é usado para calcular o valor futuro esperado em um estado,
        assumindo que o agente escolherá sempre a melhor ação conhecida. É usado
        na fórmula do Q-Learning para estimar o valor das recompensas futuras.

        Args:
            estado: Tupla representando o estado futuro do tabuleiro.

        Returns:
            O maior valor Q entre todas as ações conhecidas para este estado.
            Retorna 0.0 se o estado não existe na tabela Q ou não tem ações registradas.

        Note:
            Este é um método privado (prefixo _) usado internamente pelo método
            atualizar_valor_q() para calcular valores futuros esperados na fórmula
            do Q-Learning.
        """
        if estado not in self.tabela_q or not self.tabela_q[estado]:
            return 0.0
        return max(self.tabela_q[estado].values())

    def escolher_acao(self, estado: Tuple, acoes_validas: List[int], em_treinamento: bool = True) -> int:
        """
        Escolhe uma ação usando a estratégia Epsilon-Greedy.

        A estratégia Epsilon-Greedy equilibra exploração e exploração:
        - Com probabilidade epsilon: escolhe uma ação aleatória (exploração)
        - Com probabilidade (1 - epsilon): escolhe a melhor ação conhecida (exploração)

        Quando em_treinamento=False, o agente sempre escolhe a melhor ação,
        ignorando epsilon. Isso é útil para avaliação ou quando o agente já
        está suficientemente treinado.

        Args:
            estado: Tupla representando o estado atual do tabuleiro.
            acoes_validas: Lista de índices de ações válidas (posições vazias no tabuleiro).
            em_treinamento: Se False, sempre escolhe a melhor ação conhecida,
                ignorando epsilon. Padrão: True.

        Returns:
            Índice da ação escolhida (0 a 8, representando posições no tabuleiro).

        Raises:
            ValueError: Se a lista de ações válidas estiver vazia.

        Example:
            >>> agente = AgenteQLearning(epsilon=0.1)
            >>> estado = ((1, 0, 0, 0, 2, 0, 0, 0, 1),)
            >>> acoes = [1, 2, 3, 5, 6, 7]
            >>> acao = agente.escolher_acao(estado, acoes, em_treinamento=True)
            >>> # 90% das vezes escolhe a melhor ação, 10% escolhe aleatória
        """
        if not acoes_validas:
            raise ValueError("Não há ações válidas para escolher.")
        
        # Se não está em treinamento, sempre escolhe a melhor ação
        if not em_treinamento:
            return self._escolher_melhor_acao(estado, acoes_validas)
        
        # Estratégia Epsilon-Greedy: exploração vs exploração
        if random.random() < self.epsilon:
            # Exploração: escolhe uma ação aleatória
            return random.choice(acoes_validas)
        else:
            # Exploração: escolhe a melhor ação conhecida
            return self._escolher_melhor_acao(estado, acoes_validas)

    def _escolher_melhor_acao(self, estado: Tuple, acoes_validas: List[int]) -> int:
        """
        Escolhe a ação com o maior valor Q entre as ações válidas.

        Se múltiplas ações tiverem o mesmo valor Q máximo, uma delas é
        escolhida aleatoriamente. Isso adiciona um elemento de aleatoriedade
        mesmo na exploração, evitando que o agente fique preso em padrões
        determinísticos.

        Args:
            estado: Tupla representando o estado atual do tabuleiro.
            acoes_validas: Lista de índices de ações válidas.

        Returns:
            Índice da ação com o maior valor Q. Se houver empate, retorna
            uma das ações empatadas escolhida aleatoriamente.

        Note:
            Este é um método privado (prefixo _) usado internamente pelo
            método escolher_acao(). Ele assume que acoes_validas não está vazia.
        """
        # Calcula o valor Q de cada ação válida
        valores_q_das_acoes = {acao: self.obter_valor_q(estado, acao) for acao in acoes_validas}
        
        # Encontra o maior valor Q
        valor_maximo_q = max(valores_q_das_acoes.values())
        
        # Seleciona todas as ações que têm o valor máximo
        melhores_acoes = [acao for acao, valor in valores_q_das_acoes.items() if valor == valor_maximo_q]
        
        # Se houver empate, escolhe aleatoriamente entre as melhores
        return random.choice(melhores_acoes)

    # --- MÉTODOS PARA O TREINAMENTO EM MASSA (usados pelo treinador.py) ---

    def limpar_historico_partida(self):
        """
        Limpa o histórico de jogadas da partida atual.

        Este método deve ser chamado no início de cada partida durante o
        treinamento em massa. Ele limpa o histórico de jogadas da partida
        anterior, permitindo que o agente comece a registrar novas jogadas
        para a nova partida.

        Note:
            Este método não afeta a tabela Q nem as estatísticas gerais do agente.
            Apenas limpa o histórico de curto prazo da partida atual, que será
            usado para aprendizado Monte Carlo no final da partida.
        """
        self.historico_partida = []

    def adicionar_jogada_ao_historico(self, estado: Tuple, acao: int):
        """
        Adiciona uma jogada ao histórico da partida atual.

        Durante o treinamento em massa, todas as jogadas são registradas
        no histórico para que o agente possa aprender com elas no final da
        partida usando o método Monte Carlo. O histórico armazena a sequência
        de (estado, ação) que levaram ao resultado final.

        Args:
            estado: Estado do tabuleiro no momento da jogada.
            acao: Ação (posição) escolhida pelo agente.

        Note:
            Este método deve ser chamado para cada jogada do agente durante
            uma partida. O histórico é processado no final da partida pelo
            método processar_aprendizado_monte_carlo().
        """
        self.historico_partida.append((estado, acao))

    def processar_aprendizado_monte_carlo(self, recompensa_final: float):
        """
        Processa o aprendizado usando o método Monte Carlo baseado no resultado final.

        Este método implementa aprendizado Monte Carlo, onde o agente aprende
        com base no resultado final da partida. Ele percorre o histórico de
        jogadas de trás para frente, atribuindo recompensas descontadas a cada
        jogada anterior usando o método atualizar_valor_q().

        O processo funciona assim:
        1. Atualiza as estatísticas (vitórias, derrotas, empates).
        2. Percorre o histórico de jogadas de trás para frente.
        3. Para cada jogada, aplica a recompensa final descontada pelo fator gamma.
        4. A recompensa é descontada exponencialmente: jogadas mais recentes
           recebem mais crédito do que jogadas antigas.
        5. Reduz epsilon (taxa de exploração) para o próximo treinamento.

        Este método é usado principalmente pelo módulo treinador.py durante
        o treinamento em massa (self-play).

        Args:
            recompensa_final: Recompensa recebida no final da partida.
                Valores típicos: +1.0 (vitória), -1.0 (derrota), 0.0 (empate).

        Note:
            Este método modifica a tabela Q e as estatísticas do agente.
            Após chamar este método, o histórico da partida ainda está disponível,
            mas será limpo na próxima chamada de limpar_historico_partida().
        """
        # Atualiza contadores de estatísticas
        self.partidas_treinadas += 1
        if recompensa_final > 0:
            self.vitorias += 1
        elif recompensa_final < 0:
            self.derrotas += 1
        else:
            self.empates += 1

        # Aprendizado Monte Carlo: percorre o histórico de trás para frente
        # A recompensa é descontada exponencialmente (jogadas recentes valem mais)
        recompensa_atual = recompensa_final
        for estado, acao in reversed(self.historico_partida):
            # Reutiliza o método atualizar_valor_q() para manter a lógica centralizada
            # finalizado=True porque estamos processando uma partida já finalizada
            self.atualizar_valor_q(estado, acao, recompensa_atual, estado, finalizado=True)
            # Desconta a recompensa para a próxima jogada (mais antiga)
            recompensa_atual *= self.gamma
        
        # Reduz a taxa de exploração após cada partida
        self.reduzir_epsilon()

    def reduzir_epsilon(self):
        """
        Reduz a taxa de exploração (epsilon) do agente.

        Este método implementa o decaimento de epsilon, fazendo com que o
        agente se torne gradualmente menos exploratório e mais explorador
        conforme ganha experiência. O epsilon nunca cai abaixo de
        epsilon_minimo, garantindo que o agente sempre mantenha um mínimo
        de exploração.

        A fórmula aplicada é:
            epsilon = max(epsilon_minimo, epsilon * taxa_decaimento_epsilon)

        Note:
            Este método é chamado automaticamente após cada partida durante
            o treinamento em massa. Para aprendizado interativo, o decaimento
            pode ser controlado manualmente.
        """
        self.epsilon = max(self.epsilon_minimo, self.epsilon * self.taxa_decaimento_epsilon)

    def salvar_memoria(self, caminho: str):
        """
        Salva a tabela Q do agente em um arquivo usando pickle.

        A tabela Q contém todo o conhecimento adquirido pelo agente durante
        o treinamento. Salvar a memória permite que o agente retome seu
        aprendizado de onde parou, sem precisar treinar novamente do zero.

        O arquivo é salvo em formato binário (pickle), o que permite preservar
        a estrutura completa da tabela Q (dicionários aninhados).

        Args:
            caminho: Caminho do arquivo onde a tabela Q será salva.
                Se o diretório não existir, ele será criado automaticamente.
                Exemplo: "modelos/agente_x.pkl"

        Note:
            Este método não imprime mensagens de confirmação, permitindo que
            o salvamento seja silencioso quando necessário. Se você precisar
            de feedback, verifique o retorno ou trate exceções.

        Example:
            >>> agente = AgenteQLearning()
            >>> # ... treinar o agente ...
            >>> agente.salvar_memoria("modelos/meu_agente.pkl")
        """
        caminho_arquivo = Path(caminho)
        caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)
        with open(caminho_arquivo, 'wb') as arquivo:
            pickle.dump(self.tabela_q, arquivo)

    @classmethod
    def carregar(cls, caminho: str, **kwargs) -> 'AgenteQLearning':
        """
        Cria uma instância do agente e carrega sua tabela Q de um arquivo.

        Este método de classe permite criar um agente já treinado a partir de
        um arquivo salvo anteriormente. Se o arquivo não existir, o agente será
        criado com uma tabela Q vazia (sem conhecimento prévio).

        Args:
            caminho: Caminho do arquivo contendo a tabela Q salva.
                Exemplo: "modelos/agente_x.pkl"
            **kwargs: Argumentos adicionais passados para o construtor do agente.
                Permite personalizar parâmetros como alpha, gamma, epsilon, etc.
                mesmo ao carregar um modelo existente.

        Returns:
            Instância de AgenteQLearning com a tabela Q carregada (se o arquivo
            existir) ou vazia (se o arquivo não existir).

        Note:
            Este método imprime mensagens informativas sobre o carregamento.
            Se o arquivo não existir, o agente começará do zero, mas manterá
            os parâmetros especificados em **kwargs.

        Example:
            >>> # Carregar agente com parâmetros padrão
            >>> agente = AgenteQLearning.carregar("modelos/agente_x.pkl")
            >>> 
            >>> # Carregar agente com parâmetros personalizados
            >>> agente = AgenteQLearning.carregar(
            ...     "modelos/agente_x.pkl",
            ...     alpha=0.3,
            ...     epsilon=0.01
            ... )
        """
        agente = cls(**kwargs)
        caminho_arquivo = Path(caminho)
        if caminho_arquivo.exists():
            with open(caminho_arquivo, 'rb') as arquivo:
                agente.tabela_q = pickle.load(arquivo)
            print(f"✅ Memória do Agente ({agente.simbolo}) carregada de: {caminho_arquivo}")
        else:
            print(f"⚠️  Aviso: Nenhum arquivo de memória encontrado em {caminho}. "
                  f"O Agente ({agente.simbolo}) começará do zero.")
        return agente

    def imprimir_estatisticas(self):
        """
        Imprime as estatísticas de treinamento do agente de forma formatada.

        Exibe informações sobre o desempenho do agente, incluindo:
        - Número total de partidas treinadas
        - Quantidade de estados únicos conhecidos (tamanho da tabela Q)
        - Taxa de exploração atual (epsilon)
        - Estatísticas de desempenho: vitórias, empates e derrotas com percentuais

        A saída é formatada de forma legível, com separadores visuais e
        números formatados com separadores de milhar.

        Note:
            Este método não retorna nada, apenas imprime no console.
            Se nenhuma partida foi treinada, todas as taxas serão 0.0%.
        """
        total_jogos = self.vitorias + self.derrotas + self.empates
        
        # Calcula as taxas de desempenho
        if total_jogos == 0:
            taxa_vitoria, taxa_empate, taxa_derrota = 0.0, 0.0, 0.0
        else:
            taxa_vitoria = self.vitorias / total_jogos
            taxa_empate = self.empates / total_jogos
            taxa_derrota = self.derrotas / total_jogos

        # Imprime as estatísticas formatadas
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