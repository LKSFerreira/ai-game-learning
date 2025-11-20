"""
Módulo: 🏛️ treinador.py
Projeto: 📘 AI Game Learning

Este módulo implementa o Treinador, que é responsável por orquestrar o treinamento
de dois agentes Q-Learning através de self-play (autoaprendizado).

O Treinador funciona como um "Mestre da Guilda" ou "Dungeon Master" que:
- Coordena milhares de partidas entre os dois agentes
- Gerencia o ciclo completo de treinamento (partida → aprendizado → estatísticas)
- Fornece interfaces visuais ricas para acompanhamento em tempo real
- Salva checkpoints periódicos e modelos finais treinados
- Avalia o desempenho dos agentes após o treinamento

O processo de self-play é fundamental para o aprendizado: os agentes jogam
uns contra os outros, aprendendo com cada vitória, derrota e empate. Com o
tempo, ambos os agentes melhoram simultaneamente, criando um ciclo virtuoso
de aprendizado.

Este módulo suporta duas interfaces visuais:
- Rich (avançada): Interface rica com painéis, tabelas e atualizações em tempo real
- TQDM (básica): Barra de progresso simples, usada como fallback
"""

from datetime import datetime
import os
from pathlib import Path
from typing import Tuple, Dict, List, Optional

# Tenta importar a biblioteca 'rich' para uma interface visual avançada.
# Se não estiver instalada, define RICH_DISPONIVEL como False.
try:
    from rich.live import Live
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    RICH_DISPONIVEL = True
except ImportError:
    RICH_DISPONIVEL = False

# Tqdm é usado como uma alternativa mais simples se 'rich' não estiver disponível.
from tqdm import tqdm

from .ambiente import AmbienteJogoDaVelha
from .agente import AgenteQLearning


class Treinador:
    """
    Orquestra o treinamento de dois agentes Q-Learning através de self-play.

    O Treinador coordena o processo completo de treinamento, gerenciando:
    - Execução de partidas entre os agentes
    - Aplicação de recompensas e aprendizado
    - Salvamento de checkpoints periódicos
    - Exibição de estatísticas em tempo real
    - Avaliação do desempenho final

    O self-play funciona assim:
    1. Os dois agentes jogam uma partida completa
    2. No final, cada agente recebe uma recompensa baseada no resultado
    3. Os agentes aprendem usando o método Monte Carlo
    4. O processo se repete milhares de vezes
    5. Com o tempo, ambos os agentes melhoram simultaneamente

    Attributes:
        agente_x (AgenteQLearning): Agente que joga como 'X' (jogador 1).
        agente_o (AgenteQLearning): Agente que joga como 'O' (jogador 2).
        ambiente (AmbienteJogoDaVelha): Ambiente do jogo onde as partidas ocorrem.
        pasta_modelos (Path): Caminho da pasta onde os modelos são salvos.
        _checkpoints (List[Dict]): Lista de metadados dos checkpoints salvos.

    Example:
        >>> ambiente = AmbienteJogoDaVelha(dimensao=3)
        >>> agente_x = AgenteQLearning(jogador=1)
        >>> agente_o = AgenteQLearning(jogador=2)
        >>> treinador = Treinador(agente_x, agente_o, ambiente)
        >>> treinador.treinar(numero_de_partidas=10000)
    """

    def __init__(self, agente_x: AgenteQLearning, agente_o: AgenteQLearning, ambiente: AmbienteJogoDaVelha):
        """
        Inicializa uma nova instância do Treinador.

        Args:
            agente_x: Agente que jogará como 'X' (jogador 1).
            agente_o: Agente que jogará como 'O' (jogador 2).
            ambiente: Ambiente do jogo onde as partidas serão executadas.

        Note:
            A pasta de modelos será criada automaticamente se não existir.
            Os checkpoints são inicializados como uma lista vazia.
        """
        self.agente_x = agente_x
        self.agente_o = agente_o
        self.ambiente = ambiente
        self.pasta_modelos = Path("modelos_treinados")
        self.pasta_modelos.mkdir(exist_ok=True)
        self._checkpoints: List[Dict] = []  # Lista para armazenar metadados dos checkpoints

    def executar_uma_partida(self) -> int:
        """
        Executa uma única partida completa entre os dois agentes.

        Este método coordena uma partida do início ao fim:
        1. Reinicia o ambiente e limpa os históricos dos agentes
        2. Alterna entre os agentes até a partida terminar
        3. Calcula as recompensas baseadas no resultado
        4. Aplica o aprendizado Monte Carlo em ambos os agentes

        O processo de self-play acontece aqui: os agentes jogam uns contra
        os outros, registrando suas jogadas e aprendendo no final.

        Returns:
            Identificador do vencedor: 1 (agente X), 2 (agente O), ou 0 (empate).

        Note:
            Este método não modifica os parâmetros de treinamento dos agentes
            (como epsilon), apenas executa a partida e aplica o aprendizado.
        """
        # Reinicia o ambiente para uma nova partida
        self.ambiente.reiniciar_partida()
        
        # Limpa os históricos dos agentes para começar uma nova partida
        self.agente_x.limpar_historico_partida()
        self.agente_o.limpar_historico_partida()

        # Loop principal da partida: continua até alguém vencer ou empatar
        while not self.ambiente.partida_finalizada:
            # Determina qual agente deve jogar nesta rodada
            agente_atual = self.agente_x if self.ambiente.jogador_atual == 1 else self.agente_o
            
            # Obtém o estado atual do tabuleiro e as ações válidas
            estado_atual = self.ambiente.obter_estado_como_tupla()
            acoes_validas = self.ambiente.obter_acoes_validas()
            
            # O agente escolhe uma ação usando sua estratégia Epsilon-Greedy
            acao_escolhida = agente_atual.escolher_acao(estado_atual, acoes_validas, em_treinamento=True)
            
            # Registra a jogada no histórico para aprendizado Monte Carlo posterior
            agente_atual.adicionar_jogada_ao_historico(estado_atual, acao_escolhida)
            
            # Executa a ação escolhida no ambiente
            self.ambiente.executar_jogada(acao_escolhida)

        # Calcula as recompensas baseadas no resultado final
        if self.ambiente.vencedor == 1:
            # Agente X venceu: recompensa positiva para X, negativa para O
            recompensa_x, recompensa_o = 1.0, -1.0
        elif self.ambiente.vencedor == 2:
            # Agente O venceu: recompensa positiva para O, negativa para X
            recompensa_x, recompensa_o = -1.0, 1.0
        else:
            # Empate: recompensa neutra para ambos
            recompensa_x, recompensa_o = 0.0, 0.0
            
        # Aplica o aprendizado Monte Carlo em ambos os agentes
        # Cada agente aprende com base no histórico de sua partida
        self.agente_x.processar_aprendizado_monte_carlo(recompensa_x)
        self.agente_o.processar_aprendizado_monte_carlo(recompensa_o)
        
        return self.ambiente.vencedor

    def treinar(self, numero_de_partidas: int = 50000, intervalo_log: int = 1000, intervalo_checkpoint: int = 10000):
        """
        Executa o loop principal de treinamento com interface visual em tempo real.

        Este método coordena todo o processo de treinamento, executando milhares
        de partidas e fornecendo feedback visual sobre o progresso. Ele suporta
        duas interfaces: Rich (avançada) e TQDM (básica).

        O treinamento funciona através de self-play: os agentes jogam uns contra
        os outros repetidamente, melhorando gradualmente com cada partida.

        Args:
            numero_de_partidas: Número total de partidas a serem executadas.
                Padrão: 50.000. Valores típicos: 10.000 a 500.000.
            intervalo_log: Intervalo (em partidas) para resetar a janela de
                estatísticas. Padrão: 1.000. Usado para calcular taxas recentes.
            intervalo_checkpoint: Intervalo (em partidas) para salvar checkpoints.
                Padrão: 10.000. Permite recuperar o treinamento se interrompido.

        Note:
            - Checkpoints são salvos automaticamente nos intervalos especificados
            - As estatísticas são exibidas em tempo real durante o treinamento
            - Ao final, os modelos finais são salvos automaticamente
            - O método detecta automaticamente se Rich está disponível

        Example:
            >>> treinador = Treinador(agente_x, agente_o, ambiente)
            >>> treinador.treinar(
            ...     numero_de_partidas=100000,
            ...     intervalo_log=5000,
            ...     intervalo_checkpoint=20000
            ... )
        """
        print("\n" + "="*50)
        print("⚔️ INICIANDO TREINAMENTO INTENSIVO (SELF-PLAY) ⚔️")
        print("="*50)
        print(f"Total de Partidas: {numero_de_partidas:,}")
        print(f"Interface Gráfica: {'Rich (Avançada)' if RICH_DISPONIVEL else 'TQDM (Básica)'}")
        print("="*50 + "\n")

        # Inicializa lista de checkpoints e contadores de estatísticas
        self._checkpoints = []
        vitorias_x_janela, vitorias_o_janela, empates_janela = 0, 0, 0
        ultimo_checkpoint: Optional[str] = None

        if RICH_DISPONIVEL:
            # --- MODO RICH (Interface Avançada) ---
            # Cria uma barra de progresso com informações detalhadas
            progresso = Progress(
                TextColumn("[bold blue]{task.description}"), 
                BarColumn(), 
                TextColumn("{task.percentage:>3.0f}%"), 
                TimeRemainingColumn()
            )
            id_tarefa = progresso.add_task("Treinando", total=numero_de_partidas)

            def gerar_painel_estatisticas() -> Panel:
                """
                Gera um painel com estatísticas em tempo real do treinamento.

                As estatísticas incluem:
                - Vitórias, derrotas e empates na janela atual
                - Taxa de empate (indicador de qualidade do treinamento)
                - Epsilon atual de cada agente (taxa de exploração)
                - Número de estados conhecidos (tamanho da tabela Q)
                - Informações sobre o último checkpoint salvo
                """
                tabela = Table.grid(expand=True)
                tabela.add_column(justify="left")
                tabela.add_column(justify="right")
                
                # Calcula o total para evitar divisão por zero
                total_janela = vitorias_x_janela + vitorias_o_janela + empates_janela or 1
                
                # Estatísticas da janela atual (últimas N partidas)
                tabela.add_row("Vitórias X (janela)", f"[bold green]{vitorias_x_janela}[/]")
                tabela.add_row("Vitórias O (janela)", f"[bold yellow]{vitorias_o_janela}[/]")
                tabela.add_row("Empates (janela)", f"{empates_janela}")
                tabela.add_row("Taxa de Empate %", f"{(empates_janela / total_janela) * 100:.1f}%")
                tabela.add_row("-" * 20, "-" * 20)
                
                # Parâmetros de treinamento
                tabela.add_row("Epsilon X", f"{self.agente_x.epsilon:.6f}")
                tabela.add_row("Epsilon O", f"{self.agente_o.epsilon:.6f}")
                
                # Conhecimento adquirido
                tabela.add_row("Estados Conhecidos X", f"{len(self.agente_x.tabela_q):,}")
                tabela.add_row("Estados Conhecidos O", f"{len(self.agente_o.tabela_q):,}")
                
                # Informações de checkpoint
                tabela.add_row("Último Checkpoint", f"{ultimo_checkpoint or 'Nenhum'}")
                
                return Panel(tabela, title="[bold]Estatísticas da Janela[/]", border_style="blue")

            def gerar_layout():
                """
                Gera o layout completo da interface Rich.

                O layout combina a barra de progresso com o painel de estatísticas,
                criando uma interface visual rica e informativa.
                """
                layout = Table.grid(expand=True)
                layout.add_row(
                    Panel(progresso, title="[bold]Progresso Geral[/]", border_style="green"), 
                    gerar_painel_estatisticas()
                )
                return layout

            # Loop principal de treinamento com interface Rich
            with Live(gerar_layout(), refresh_per_second=10) as live:
                for indice_partida in range(numero_de_partidas):
                    # Executa uma partida completa
                    vencedor = self.executar_uma_partida()
                    
                    # Atualiza contadores da janela de estatísticas
                    if vencedor == 1: 
                        vitorias_x_janela += 1
                    elif vencedor == 2: 
                        vitorias_o_janela += 1
                    else: 
                        empates_janela += 1

                    # Atualiza a barra de progresso
                    progresso.update(id_tarefa, advance=1)

                    # Reseta a janela de estatísticas no intervalo especificado
                    if (indice_partida + 1) % intervalo_log == 0:
                        vitorias_x_janela, vitorias_o_janela, empates_janela = 0, 0, 0
                    
                    # Salva checkpoint no intervalo especificado
                    if (indice_partida + 1) % intervalo_checkpoint == 0:
                        self._salvar_checkpoint(indice_partida + 1)
                        ultimo_checkpoint = f"{indice_partida+1:,}"

                    # Atualiza o layout completo periodicamente para melhor performance
                    if indice_partida % 250 == 0:
                        live.update(gerar_layout())
                
                # Atualização final para garantir que tudo está visível
                live.update(gerar_layout())
        else:
            # --- MODO TQDM (Interface Básica) ---
            # Fallback para quando Rich não está disponível
            for indice_partida in tqdm(range(numero_de_partidas), desc="Treinando"):
                vencedor = self.executar_uma_partida()
                
                # Atualiza contadores (não exibidos em TQDM, mas mantidos para consistência)
                if vencedor == 1: 
                    vitorias_x_janela += 1
                elif vencedor == 2: 
                    vitorias_o_janela += 1
                else: 
                    empates_janela += 1

                # Salva checkpoint no intervalo especificado
                if (indice_partida + 1) % intervalo_checkpoint == 0:
                    self._salvar_checkpoint(indice_partida + 1)
        
        # Exibe resumo de checkpoints salvos
        self._exibir_resumo_checkpoints()
        
        print("\n" + "="*50)
        print("✅ TREINAMENTO CONCLUÍDO!")
        print("="*50)
        
        # Exibe estatísticas finais dos agentes
        self.agente_x.imprimir_estatisticas()
        self.agente_o.imprimir_estatisticas()
        
        # Salva os modelos finais
        self._salvar_modelos_finais()

    def _salvar_checkpoint(self, numero_partida: int):
        """
        Salva o estado atual dos agentes em um checkpoint e registra metadados.

        Checkpoints permitem recuperar o treinamento de um ponto específico,
        útil para treinamentos longos que podem ser interrompidos. Cada checkpoint
        salva a tabela Q completa de ambos os agentes.

        Args:
            numero_partida: Número da partida atual (usado no nome do arquivo).

        Note:
            Este método registra metadados sobre o checkpoint (sucesso/falha,
            timestamp, etc.) para rastreamento posterior. Se houver erro ao salvar,
            o erro é registrado mas não interrompe o treinamento.
        """
        caminho_x = self.pasta_modelos / f"agente_x_checkpoint_{numero_partida}.pkl"
        caminho_o = self.pasta_modelos / f"agente_o_checkpoint_{numero_partida}.pkl"
        
        try:
            # Salva as tabelas Q de ambos os agentes
            self.agente_x.salvar_memoria(str(caminho_x))
            self.agente_o.salvar_memoria(str(caminho_o))
            
            # Registra metadados do checkpoint bem-sucedido
            self._checkpoints.append({
                'numero_partida': numero_partida,
                'timestamp': datetime.now(),
                'pasta': str(self.pasta_modelos),
                'sucesso': True
            })
        except Exception as e:
            # Registra falha sem interromper o treinamento
            self._checkpoints.append({
                'numero_partida': numero_partida,
                'timestamp': datetime.now(),
                'erro': str(e),
                'sucesso': False
            })

    def _salvar_modelos_finais(self):
        """
        Salva os modelos finais após o término do treinamento.

        Os modelos finais são salvos com um nome padronizado que inclui a
        dimensão do tabuleiro, facilitando a identificação e uso posterior.

        Note:
            Este método é chamado automaticamente ao final do treinamento.
            Os modelos são salvos na pasta de modelos com nomes descritivos.
        """
        caminho_x = self.pasta_modelos / f"agente_x_final_{self.ambiente.dimensao}x{self.ambiente.dimensao}.pkl"
        caminho_o = self.pasta_modelos / f"agente_o_final_{self.ambiente.dimensao}x{self.ambiente.dimensao}.pkl"
        self.agente_x.salvar_memoria(str(caminho_x))
        self.agente_o.salvar_memoria(str(caminho_o))

    def _exibir_resumo_checkpoints(self):
        """
        Exibe um resumo organizado dos checkpoints salvos durante o treinamento.

        Este método formata e exibe informações sobre todos os checkpoints criados,
        incluindo sucessos e falhas, com timestamps e números de partida formatados.

        Note:
            Se nenhum checkpoint foi salvo, exibe uma mensagem de aviso.
            Checkpoints com erro são listados separadamente dos bem-sucedidos.
        """
        if not self._checkpoints or len(self._checkpoints) == 0:
            print('\n⚠️  Nenhum checkpoint foi salvo.\n')
            return

        # Separa checkpoints bem-sucedidos dos que falharam
        checkpoints_sucesso = [cp for cp in self._checkpoints if cp.get('sucesso', False)]
        
        print('\n' + '━' * 80)
        print('💾 CHECKPOINTS SALVOS')
        print('━' * 80 + '\n')
        
        if checkpoints_sucesso:
            print(f'✅ {len(checkpoints_sucesso)} checkpoint(s) criado(s) com sucesso\n')
            print(f'📁 Pasta: {checkpoints_sucesso[0]["pasta"]}\n')
            
            # Exibe cada checkpoint bem-sucedido com formatação
            for cp in checkpoints_sucesso:
                data_formatada = cp['timestamp'].strftime('%d/%m/%Y às %H:%M')
                partida_formatada = f"{cp['numero_partida']:,}".replace(',', '.')
                print(f'  🎯 Partida {partida_formatada} — {data_formatada}')
        
        # Exibe erros se houver
        checkpoints_erro = [cp for cp in self._checkpoints if not cp.get('sucesso', False)]
        if checkpoints_erro:
            print(f'\n❌ {len(checkpoints_erro)} checkpoint(s) com erro:\n')
            for cp in checkpoints_erro:
                partida_formatada = f"{cp['numero_partida']:,}".replace(',', '.')
                print(f'  ⚠️  Partida {partida_formatada} — {cp.get("erro", "Erro desconhecido")}')
        
        print('\n' + '━' * 80 + '\n')

    def avaliar_agentes(self, numero_de_partidas: int = 10000):
        """
        Avalia o desempenho dos agentes em modo de performance máxima (sem exploração).

        Este método coloca os agentes para jogar uns contra os outros com
        epsilon=0 (sem exploração aleatória), permitindo avaliar o conhecimento
        real adquirido durante o treinamento. É útil para verificar se o
        treinamento foi bem-sucedido.

        O método tenta carregar modelos automaticamente se os agentes não estiverem
        treinados, facilitando a avaliação de modelos salvos anteriormente.

        Args:
            numero_de_partidas: Número de partidas a serem executadas para avaliação.
                Padrão: 10.000. Valores maiores fornecem estatísticas mais confiáveis.

        Note:
            - Os agentes jogam com em_treinamento=False (sem exploração)
            - Se os agentes não estiverem treinados, tenta carregar modelos do disco
            - As estatísticas são exibidas em tempo real durante a avaliação
            - Ao final, exibe um resumo completo dos resultados

        Example:
            >>> treinador.avaliar_agentes(numero_de_partidas=5000)
        """
        print("\n" + "="*50)
        print("🏆 INICIANDO MODO DE AVALIAÇÃO (SEM EXPLORAÇÃO) 🏆")
        print("="*50)

        # --- LÓGICA DE CARREGAMENTO AUTOMÁTICO ---
        # Se os agentes não estiverem treinados, tenta carregar modelos salvos
        if not self.agente_x.tabela_q:
            print("Agente X não treinado. Tentando carregar modelo do disco...")
            caminho_x = self.pasta_modelos / f"superagente_final_{self.ambiente.dimensao}x{self.ambiente.dimensao}.pkl"
            self.agente_x = AgenteQLearning.carregar(str(caminho_x), jogador=1)

        if not self.agente_o.tabela_q:
            print("Agente O não treinado. Tentando carregar modelo do disco...")
            caminho_o = self.pasta_modelos / f"agente_o_final_{self.ambiente.dimensao}x{self.ambiente.dimensao}.pkl"
            self.agente_o = AgenteQLearning.carregar(str(caminho_o), jogador=2)
        
        # Inicializa contadores de resultados
        vitorias_x, vitorias_o, empates = 0, 0, 0

        if RICH_DISPONIVEL:
            # --- MODO RICH (Interface Avançada) ---
            progresso = Progress(
                TextColumn("[bold blue]{task.description}"), 
                BarColumn(), 
                TextColumn("{task.percentage:>3.0f}%"), 
                TimeRemainingColumn()
            )
            id_tarefa = progresso.add_task("Avaliando", total=numero_de_partidas)

            def gerar_painel_estatisticas_avaliacao() -> Panel:
                """
                Gera um painel com estatísticas da avaliação em tempo real.

                As estatísticas incluem:
                - Vitórias, derrotas e empates acumulados
                - Taxa de empate (indicador de qualidade)
                - Número de estados conhecidos por cada agente
                """
                tabela = Table.grid(expand=True)
                tabela.add_column(justify="left")
                tabela.add_column(justify="right")
                total_partidas = vitorias_x + vitorias_o + empates or 1
                
                tabela.add_row("Vitórias X", f"[bold green]{vitorias_x}[/]")
                tabela.add_row("Vitórias O", f"[bold yellow]{vitorias_o}[/]")
                tabela.add_row("Empates", f"{empates}")
                tabela.add_row("-" * 20, "-" * 20)
                tabela.add_row("Taxa de Empate %", f"{(empates / total_partidas) * 100:.2f}%")
                tabela.add_row("Estados Conhecidos X", f"{len(self.agente_x.tabela_q):,}")
                tabela.add_row("Estados Conhecidos O", f"{len(self.agente_o.tabela_q):,}")
                
                return Panel(tabela, title="[bold]Estatísticas em Tempo Real[/]", border_style="blue")

            def gerar_layout():
                """Gera o layout completo da interface de avaliação."""
                layout = Table.grid(expand=True)
                layout.add_row(
                    Panel(progresso, title="[bold]Progresso da Avaliação[/]", border_style="green"), 
                    gerar_painel_estatisticas_avaliacao()
                )
                return layout

            # Loop principal de avaliação com interface Rich
            with Live(gerar_layout(), refresh_per_second=10) as live:
                for indice_partida in range(numero_de_partidas):
                    # Reinicia o ambiente para uma nova partida
                    self.ambiente.reiniciar_partida()
                    
                    # Executa a partida sem exploração (em_treinamento=False)
                    while not self.ambiente.partida_finalizada:
                        agente_atual = self.agente_x if self.ambiente.jogador_atual == 1 else self.agente_o
                        estado = self.ambiente.obter_estado_como_tupla()
                        acoes = self.ambiente.obter_acoes_validas()
                        # em_treinamento=False: sempre escolhe a melhor ação conhecida
                        acao = agente_atual.escolher_acao(estado, acoes, em_treinamento=False)
                        self.ambiente.executar_jogada(acao)

                    # Atualiza contadores baseado no resultado
                    if self.ambiente.vencedor == 1: 
                        vitorias_x += 1
                    elif self.ambiente.vencedor == 2: 
                        vitorias_o += 1
                    else: 
                        empates += 1
                    
                    # Atualiza a barra de progresso
                    progresso.update(id_tarefa, advance=1)
                    
                    # Atualiza o layout periodicamente
                    if indice_partida % 250 == 0:
                        live.update(gerar_layout())
                    
                # Atualização final garantida
                live.update(gerar_layout())

        else:
            # --- MODO TQDM (Interface Básica) ---
            # Fallback para quando Rich não está disponível
            for _ in tqdm(range(numero_de_partidas), desc="Avaliando Performance"):
                self.ambiente.reiniciar_partida()
                
                # Executa a partida sem exploração
                while not self.ambiente.partida_finalizada:
                    agente_atual = self.agente_x if self.ambiente.jogador_atual == 1 else self.agente_o
                    estado = self.ambiente.obter_estado_como_tupla()
                    acoes = self.ambiente.obter_acoes_validas()
                    acao = agente_atual.escolher_acao(estado, acoes, em_treinamento=False)
                    self.ambiente.executar_jogada(acao)

                # Atualiza contadores
                if self.ambiente.vencedor == 1: 
                    vitorias_x += 1
                elif self.ambiente.vencedor == 2: 
                    vitorias_o += 1
                else: 
                    empates += 1

        # Exibe resumo final da avaliação
        print("\n--- RESULTADO FINAL DA AVALIAÇÃO ---")
        print(f"Partidas Jogadas: {numero_de_partidas}")
        print(f"Vitórias de X: {vitorias_x} ({(vitorias_x/numero_de_partidas)*100:.1f}%)")
        print(f"Vitórias de O: {vitorias_o} ({(vitorias_o/numero_de_partidas)*100:.1f}%)")
        print(f"Empates: {empates} ({(empates/numero_de_partidas)*100:.1f}%)")
        print("="*50 + "\n")
    
    def mesclar_agentes_treinados(self):
        """
        Executa o script mesclar_modelos.py para criar o superagente.

        O superagente é criado mesclando o conhecimento de ambos os agentes
        treinados, resultando em um agente mais forte que combina as melhores
        estratégias aprendidas por cada um.

        Note:
            Este método executa o script externo mesclar_modelos.py.
            O código de retorno indica sucesso (0) ou falha (diferente de 0).
        """
        print("\n" + "="*50)
        print("🔄 EXECUTANDO MESCLAGEM DOS MODELOS...")
        print("="*50 + "\n")
        
        # Executa o script Python de mesclagem
        codigo_retorno = os.system('py -m mesclar_modelos')
        
        if codigo_retorno == 0:
            print("\n✅ Mesclagem concluída com sucesso!")
        else:
            print(f"\n❌ Erro ao executar mesclagem (código: {codigo_retorno})")


# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    # Opção 1: Treinamento Padrão (3x3, 200.000 partidas)
    # Roda um treinamento completo e salva os modelos.
    ambiente_padrao = AmbienteJogoDaVelha(dimensao=3)
    agente_x_padrao = AgenteQLearning(jogador=1)
    agente_o_padrao = AgenteQLearning(jogador=2)
    
    treinador_padrao = Treinador(agente_x_padrao, agente_o_padrao, ambiente_padrao)
    treinador_padrao.treinar(numero_de_partidas=200000, intervalo_log=500, intervalo_checkpoint=40000)
    
    treinador_padrao.avaliar_agentes()
    
    treinador_padrao.mesclar_agentes_treinados()
    
    # Opção 2: Treinamento Customizado (ex: 4x4, 100.000 partidas)
    # Descomente as linhas abaixo para rodar um treino diferente.
    # print("\n--- INICIANDO TREINAMENTO CUSTOMIZADO 4x4 ---")
    # ambiente_4x4 = AmbienteJogoDaVelha(dimensao=4)
    # agente_x_4x4 = AgenteQLearning(jogador=1, taxa_decaimento_epsilon=0.9999)
    # agente_o_4x4 = AgenteQLearning(jogador=2, taxa_decaimento_epsilon=0.9999)
    #
    # treinador_4x4 = Treinador(agente_x_4x4, agente_o_4x4, ambiente_4x4)
    # treinador_4x4.treinar(numero_de_partidas=100000, intervalo_log=10000)
