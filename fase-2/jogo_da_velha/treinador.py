"""
Módulo: 🏛️ treinador.py
Projeto: 📘 AI Game Learning

Este módulo é o "Mestre da Guilda" ou o "Dungeon Master".
Ele é responsável por orquestrar o treinamento dos Agentes,
colocando-os para batalhar entre si em um processo chamado "self-play".

Responsabilidades:
- Gerenciar o loop de treinamento principal (milhares de partidas).
- Coordenar a interação entre os Agentes e o Ambiente.
- Atribuir as recompensas corretas a cada Agente no final da partida.
- Exibir estatísticas de treinamento em tempo real com uma interface rica.
- Salvar o conhecimento (modelos) e estatísticas dos Agentes treinados.
"""

import time
import json
from pathlib import Path
from typing import Tuple

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

from ambiente import AmbienteJogoDaVelha
from agente import AgenteQLearning

class Treinador:
    """
    Orquestra o treinamento de dois agentes Q-Learning através de self-play,
    com uma interface de usuário rica para acompanhamento em tempo real.
    """
    def __init__(self, agente_x: AgenteQLearning, agente_o: AgenteQLearning, ambiente: AmbienteJogoDaVelha):
        self.agente_x = agente_x
        self.agente_o = agente_o
        self.ambiente = ambiente
        self.pasta_modelos = Path("modelos_treinados")
        self.pasta_modelos.mkdir(exist_ok=True)

    def executar_uma_partida(self) -> int:
        """ Executa uma única partida (um episódio) entre os dois agentes. """
        self.ambiente.reiniciar_partida()
        self.agente_x.iniciar_nova_partida()
        self.agente_o.iniciar_nova_partida()

        while not self.ambiente.partida_finalizada:
            agente_da_vez = self.agente_x if self.ambiente.jogador_atual == 1 else self.agente_o
            estado_atual = self.ambiente.obter_estado_como_tupla()
            acoes_validas = self.ambiente.obter_acoes_validas()
            acao_escolhida = agente_da_vez.escolher_acao(estado_atual, acoes_validas, em_treinamento=True)
            agente_da_vez.registrar_jogada(estado_atual, acao_escolhida)
            self.ambiente.executar_jogada(acao_escolhida)

        if self.ambiente.vencedor == 1:
            recompensa_x, recompensa_o = 1.0, -1.0
        elif self.ambiente.vencedor == 2:
            recompensa_x, recompensa_o = -1.0, 1.0
        else:
            recompensa_x, recompensa_o = 0.0, 0.0
            
        self.agente_x.aprender_com_fim_de_partida(recompensa_x)
        self.agente_o.aprender_com_fim_de_partida(recompensa_o)
        
        return self.ambiente.vencedor

    def treinar(self, numero_de_partidas: int = 50000, intervalo_log: int = 1000, intervalo_checkpoint: int = 10000):
        """ Executa o loop de treinamento principal com interface visual. """
        print("\n" + "="*50)
        print("⚔️ INICIANDO TREINAMENTO INTENSIVO (SELF-PLAY) ⚔️")
        print("="*50)
        print(f"Total de Partidas: {numero_de_partidas:,}")
        print(f"Interface Gráfica: {'Rich (Avançada)' if RICH_DISPONIVEL else 'TQDM (Básica)'}")
        print("="*50 + "\n")

        vitorias_x_janela, vitorias_o_janela, empates_janela = 0, 0, 0
        ultimo_checkpoint = None

        if RICH_DISPONIVEL:
            # --- MODO RICH (Interface Avançada) ---
            progresso = Progress(TextColumn("[bold blue]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), TimeRemainingColumn())
            id_tarefa = progresso.add_task("Treinando", total=numero_de_partidas)

            def gerar_painel_estatisticas() -> Panel:
                tabela = Table.grid(expand=True)
                tabela.add_column(justify="left"); tabela.add_column(justify="right")
                total_janela = vitorias_x_janela + vitorias_o_janela + empates_janela or 1
                tabela.add_row("Vitórias X (janela)", f"[bold green]{vitorias_x_janela}[/]")
                tabela.add_row("Vitórias O (janela)", f"[bold yellow]{vitorias_o_janela}[/]")
                tabela.add_row("Empates (janela)", f"{empates_janela}")
                tabela.add_row("Taxa de Empate %", f"{(empates_janela / total_janela) * 100:.1f}%")
                tabela.add_row("-" * 20, "-" * 20)
                tabela.add_row("Epsilon X", f"{self.agente_x.epsilon:.6f}")
                tabela.add_row("Epsilon O", f"{self.agente_o.epsilon:.6f}")
                tabela.add_row("Estados Conhecidos X", f"{len(self.agente_x.tabela_q):,}")
                tabela.add_row("Estados Conhecidos O", f"{len(self.agente_o.tabela_q):,}")
                tabela.add_row("Último Checkpoint", f"{ultimo_checkpoint or 'Nenhum'}")
                return Panel(tabela, title="[bold]Estatísticas da Janela[/]", border_style="blue")

            layout = Table.grid(expand=True)
            layout.add_row(Panel(progresso, title="[bold]Progresso Geral[/]", border_style="green"), gerar_painel_estatisticas())

            with Live(layout, refresh_per_second=10) as live:
                for i in range(numero_de_partidas):
                    vencedor = self.executar_uma_partida()
                    if vencedor == 1: vitorias_x_janela += 1
                    elif vencedor == 2: vitorias_o_janela += 1
                    else: empates_janela += 1

                    progresso.update(id_tarefa, advance=1)

                    if (i + 1) % intervalo_log == 0:
                        live.update(layout) # Força atualização para exibir os números corretos
                        vitorias_x_janela, vitorias_o_janela, empates_janela = 0, 0, 0
                    
                    if (i + 1) % intervalo_checkpoint == 0:
                        self._salvar_checkpoint(i + 1)
                        ultimo_checkpoint = f"{i+1:,}"

                    if i % 250 == 0: # Atualiza a tabela de estatísticas periodicamente
                        layout.columns[1]._cells[0] = gerar_painel_estatisticas()
        else:
            # --- MODO TQDM (Interface Básica) ---
            for i in tqdm(range(numero_de_partidas), desc="Treinando"):
                vencedor = self.executar_uma_partida()
                # A lógica de atualização do TQDM é mais simples e já está embutida no seu loop
        
        print("\n" + "="*50)
        print("✅ TREINAMENTO CONCLUÍDO!")
        print("="*50)
        
        self.agente_x.imprimir_estatisticas()
        self.agente_o.imprimir_estatisticas()
        
        self._salvar_modelos_finais()

    def _salvar_checkpoint(self, numero_partida: int):
        """ Salva o estado atual dos agentes em um checkpoint. """
        caminho_x = self.pasta_modelos / f"agente_x_checkpoint_{numero_partida}.pkl"
        caminho_o = self.pasta_modelos / f"agente_o_checkpoint_{numero_partida}.pkl"
        self.agente_x.salvar_memoria(str(caminho_x))
        self.agente_o.salvar_memoria(str(caminho_o))

    def _salvar_modelos_finais(self):
        """ Salva os modelos finais após o término do treinamento. """
        caminho_x = self.pasta_modelos / f"agente_x_final_{self.ambiente.dimensao}x{self.ambiente.dimensao}.pkl"
        caminho_o = self.pasta_modelos / f"agente_o_final_{self.ambiente.dimensao}x{self.ambiente.dimensao}.pkl"
        self.agente_x.salvar_memoria(str(caminho_x))
        self.agente_o.salvar_memoria(str(caminho_o))
    
    def avaliar_agentes(self, numero_de_partidas: int = 100000):
            """
            Coloca os agentes para jogar um contra o outro em modo de "performance máxima",
            com uma interface rica para acompanhamento em tempo real.
            """
            print("\n" + "="*50)
            print("🏆 INICIANDO MODO DE AVALIAÇÃO (SEM EXPLORAÇÃO) 🏆")
            print("="*50)

            # --- LÓGICA DE CARREGAMENTO AUTOMÁTICO ---
            if not self.agente_x.tabela_q:
                print("Agente X não treinado. Tentando carregar modelo do disco...")
                caminho_x = self.pasta_modelos / f"superagente_final_{self.ambiente.dimensao}x{self.ambiente.dimensao}.pkl"
                self.agente_x = AgenteQLearning.carregar(str(caminho_x), jogador=1)

            if not self.agente_o.tabela_q:
                print("Agente O não treinado. Tentando carregar modelo do disco...")
                caminho_o = self.pasta_modelos / f"agente_o_final_{self.ambiente.dimensao}x{self.ambiente.dimensao}.pkl"
                self.agente_o = AgenteQLearning.carregar(str(caminho_o), jogador=2)
            
            vitorias_x, vitorias_o, empates = 0, 0, 0

            # --- LÓGICA DE INTERFACE ---
            if RICH_DISPONIVEL:
                progresso = Progress(TextColumn("[bold blue]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), TimeRemainingColumn())
                id_tarefa = progresso.add_task("Avaliando", total=numero_de_partidas)

                def gerar_painel_estatisticas_avaliacao() -> Panel:
                    tabela = Table.grid(expand=True)
                    tabela.add_column(justify="left"); tabela.add_column(justify="right")
                    total_partidas = vitorias_x + vitorias_o + empates or 1
                    
                    tabela.add_row("Vitórias X", f"[bold green]{vitorias_x}[/]")
                    tabela.add_row("Vitórias O", f"[bold yellow]{vitorias_o}[/]")
                    tabela.add_row("Empates", f"{empates}")
                    tabela.add_row("-" * 20, "-" * 20)
                    tabela.add_row("Taxa de Empate %", f"{(empates / total_partidas) * 100:.2f}%")
                    tabela.add_row("Estados Conhecidos X", f"{len(self.agente_x.tabela_q):,}")
                    tabela.add_row("Estados Conhecidos O", f"{len(self.agente_o.tabela_q):,}")
                    
                    return Panel(tabela, title="[bold]Estatísticas em Tempo Real[/]", border_style="blue")

                layout = Table.grid(expand=True)
                layout.add_row(Panel(progresso, title="[bold]Progresso da Avaliação[/]", border_style="green"), gerar_painel_estatisticas_avaliacao())

                with Live(layout, refresh_per_second=10) as live:
                    for i in range(numero_de_partidas):
                        self.ambiente.reiniciar_partida()
                        while not self.ambiente.partida_finalizada:
                            agente_da_vez = self.agente_x if self.ambiente.jogador_atual == 1 else self.agente_o
                            estado = self.ambiente.obter_estado_como_tupla()
                            acoes = self.ambiente.obter_acoes_validas()
                            acao = agente_da_vez.escolher_acao(estado, acoes, em_treinamento=False)
                            self.ambiente.executar_jogada(acao)

                        if self.ambiente.vencedor == 1: vitorias_x += 1
                        elif self.ambiente.vencedor == 2: vitorias_o += 1
                        else: empates += 1
                        
                        progresso.update(id_tarefa, advance=1)
                        
                        # Atualiza o painel de estatísticas periodicamente para não sobrecarregar
                        if i % 250 == 0:
                            layout.columns[1]._cells[0] = gerar_painel_estatisticas_avaliacao()
                    
                    # Garante que a estatística final seja a mais atualizada
                    layout.columns[1]._cells[0] = gerar_painel_estatisticas_avaliacao()

            else:
                # Fallback para TQDM
                for _ in tqdm(range(numero_de_partidas), desc="Avaliando Performance"):
                    # ... (lógica do TQDM permanece a mesma) ...
                    self.ambiente.reiniciar_partida()
                    while not self.ambiente.partida_finalizada:
                        agente_da_vez = self.agente_x if self.ambiente.jogador_atual == 1 else self.agente_o
                        estado = self.ambiente.obter_estado_como_tupla()
                        acoes = self.ambiente.obter_acoes_validas()
                        acao = agente_da_vez.escolher_acao(estado, acoes, em_treinamento=False)
                        self.ambiente.executar_jogada(acao)

                    if self.ambiente.vencedor == 1: vitorias_x += 1
                    elif self.ambiente.vencedor == 2: vitorias_o += 1
                    else: empates += 1

            print("\n--- RESULTADO FINAL DA AVALIAÇÃO ---")
            print(f"Partidas Jogadas: {numero_de_partidas}")
            print(f"Vitórias de X: {vitorias_x} ({(vitorias_x/numero_de_partidas)*100:.1f}%)")
            print(f"Vitórias de O: {vitorias_o} ({(vitorias_o/numero_de_partidas)*100:.1f}%)")
            print(f"Empates: {empates} ({(empates/numero_de_partidas)*100:.1f}%)")
            print("="*50 + "\n")

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    # Opção 1: Treinamento Padrão (3x3, 50.000 partidas)
    # Roda um treinamento completo e salva os modelos.
    ambiente_padrao = AmbienteJogoDaVelha(dimensao=3)
    agente_x_padrao = AgenteQLearning(jogador=1)
    agente_o_padrao = AgenteQLearning(jogador=2)
    
    treinador_padrao = Treinador(agente_x_padrao, agente_o_padrao, ambiente_padrao)
    treinador_padrao.treinar(numero_de_partidas=800000, intervalo_log=5000, intervalo_checkpoint=200000)
    
    treinador_padrao.avaliar_agentes()

    # Opção 2: Treinamento Customizado (ex: 4x4, 100.000 partidas)
    # Descomente as linhas abaixo para rodar um treino diferente.
    # print("\n--- INICIANDO TREINAMENTO CUSTOMIZADO 4x4 ---")
    # ambiente_4x4 = AmbienteJogoDaVelha(dimensao=4)
    # agente_x_4x4 = AgenteQLearning(jogador=1, taxa_decaimento_epsilon=0.9999)
    # agente_o_4x4 = AgenteQLearning(jogador=2, taxa_decaimento_epsilon=0.9999)
    #
    # treinador_4x4 = Treinador(agente_x_4x4, agente_o_4x4, ambiente_4x4)
    # treinador_4x4.treinar(numero_de_partidas=100000, intervalo_log=10000)