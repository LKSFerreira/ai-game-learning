"""
Treinador de Agentes Q-Learning por Self-Play

Esta versão apresenta:
- Barra de progresso + janela de estatísticas atualizando em tempo real
  ocupando apenas o espaço mínimo necessário (compact).
- Suporte a dois modos:
  * rich (quando disponível) -> melhor experiência visual com Live.
  * fallback para tqdm quando rich não estiver instalado.

Substitua/integre este arquivo no seu projeto. Depende de:
- ambiente.JogoVelha
- agente.AgenteQLearning
"""

from __future__ import annotations

import time
import json
from pathlib import Path
from typing import Tuple, Dict, List

# Tenta importar rich para UI avançada; se não houver, usa tqdm como fallback.
try:
    from rich.live import Live
    from rich.table import Table
    from rich.console import Group
    from rich.panel import Panel
    from rich.progress import (
        Progress,
        BarColumn,
        TextColumn,
        TimeRemainingColumn,
        SpinnerColumn,
    )

    RICH_AVAILABLE = True
except Exception:
    RICH_AVAILABLE = False

from tqdm import tqdm

# Importa nossos módulos criados anteriormente (devem existir no seu projeto)
from ambiente import JogoVelha
from agente import AgenteQLearning


class TreinadorSelfPlay:
    """
    Classe responsável por treinar dois agentes jogando entre si.

    A interface foi desenhada para não imprimir linhas durante o loop de
    treinamento — tudo é atualizado em-place (sem rolagem).
    """

    def __init__(
        self,
        agente_x: AgenteQLearning,
        agente_o: AgenteQLearning,
        verbose: bool = True,
    ):
        """
        Inicializa o treinador com dois agentes.

        Args:
            agente_x: Agente que joga como X (jogador 1)
            agente_o: Agente que joga como O (jogador 2)
            verbose: Se True, mostra a interface; se False, executa silenciosamente.
        """
        self.agente_x = agente_x
        self.agente_o = agente_o
        self.ambiente = JogoVelha()
        self.verbose = verbose

        # Histórico para salvar por janelas
        self.historico_vitorias_x: List[int] = []
        self.historico_vitorias_o: List[int] = []
        self.historico_empates: List[int] = []
        self.historico_epsilon_x: List[float] = []
        self.historico_epsilon_o: List[float] = []

        # Pastas
        self.pasta_modelos = Path("modelos")
        self.pasta_estatisticas = Path("estatisticas")
        self.pasta_modelos.mkdir(exist_ok=True)
        self.pasta_estatisticas.mkdir(exist_ok=True)

        # Controle do último checkpoint salvo (apenas para exibição)
        self.ultimo_checkpoint: int | None = None

    def executar_episodio(self) -> Tuple[int, int]:
        """
        Executa um episódio (uma partida) completo.

        Returns:
            (vencedor, numero_jogadas)
            vencedor: 1 (X), 2 (O), 0 (empate)
        """
        estado = self.ambiente.resetar()
        self.agente_x.iniciar_episodio()
        self.agente_o.iniciar_episodio()

        numero_jogadas = 0

        while not self.ambiente.finalizado:
            agente_atual = (
                self.agente_x if self.ambiente.jogador_atual == 1 else self.agente_o
            )

            estado_atual = self.ambiente.obter_estado()
            acoes_validas = self.ambiente.obter_acoes_validas()

            acao = agente_atual.escolher_acao(estado_atual, acoes_validas, treino=True)
            agente_atual.registrar_jogada(estado_atual, acao)

            _, _, finalizado = self.ambiente.fazer_jogada(acao)
            numero_jogadas += 1

            if finalizado:
                if self.ambiente.vencedor == 1:
                    recompensa_x, recompensa_o = 1.0, -1.0
                elif self.ambiente.vencedor == 2:
                    recompensa_x, recompensa_o = -1.0, 1.0
                else:
                    recompensa_x, recompensa_o = 0.0, 0.0

                self.agente_x.finalizar_episodio(recompensa_x)
                self.agente_o.finalizar_episodio(recompensa_o)

        return self.ambiente.vencedor, numero_jogadas

    def treinar(
        self,
        episodios: int = 20000,
        intervalo_estatisticas: int = 1000,
        intervalo_checkpoint: int = 5000,
        salvar_final: bool = True,
    ):
        """
        Executa o treinamento completo dos agentes com UI compacta (barra + stats).
        """
        if self.verbose:
            print("\n" + "=" * 70)
            print("🎮 INICIANDO TREINAMENTO POR SELF-PLAY")
            print("=" * 70)
            print(f"Total de episódios: {episodios:,}")
            print(f"Agente X: Alpha={self.agente_x.alpha}, Gamma={self.agente_x.gamma}")
            print(f"Agente O: Alpha={self.agente_o.alpha}, Gamma={self.agente_o.gamma}")
            print(
                f"Epsilon inicial: X={self.agente_x.epsilon:.6f}, O={self.agente_o.epsilon:.6f}"
            )
            print("=" * 70 + "\n")

        # Variáveis da janela
        vitorias_x_janela = 0
        vitorias_o_janela = 0
        empates_janela = 0

        tempo_inicio = time.time()

        # ---------- Parâmetros de compactação (ajustáveis) ----------
        MAX_BAR_WIDTH = 40  # largura máxima da barra (caracteres)
        MAX_TABLE_COL_WIDTH = 18  # largura por coluna da tabela (caracteres)
        # ------------------------------------------------------------

        if RICH_AVAILABLE and self.verbose:
            # --- MODO RICH (melhor experiência, compacta) ---
            progress = Progress(
                SpinnerColumn(),
                TextColumn("{task.description}"),
                BarColumn(bar_width=MAX_BAR_WIDTH),
                TextColumn("{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
                expand=False,  # NÃO ocupar largura total
            )
            task_id = progress.add_task("Treinando", total=episodios)

            def montar_tabela_compacta(episodio_atual: int) -> Panel:
                tabela = Table.grid(expand=False)
                tabela.add_column(justify="left", width=MAX_TABLE_COL_WIDTH)
                tabela.add_column(justify="right", width=MAX_TABLE_COL_WIDTH)

                taxa_empate = (
                    empates_janela
                    / max(1, (vitorias_x_janela + vitorias_o_janela + empates_janela))
                ) * 100

                tabela.add_row("Episódio", f"{episodio_atual:,}/{episodios:,}")
                tabela.add_row("Eps X", f"{self.agente_x.epsilon:.6f}")
                tabela.add_row("Eps O", f"{self.agente_o.epsilon:.6f}")
                tabela.add_row("Janela X", f"{vitorias_x_janela}")
                tabela.add_row("Janela O", f"{vitorias_o_janela}")
                tabela.add_row("Janela Emp", f"{empates_janela}")
                tabela.add_row("Empate %", f"{taxa_empate:.1f}%")
                tabela.add_row("Q-States X", f"{len(self.agente_x.q_table):,}")
                tabela.add_row("Q-States O", f"{len(self.agente_o.q_table):,}")
                tabela.add_row(
                    "Ult. Checkpoint",
                    f"{self.ultimo_checkpoint if self.ultimo_checkpoint is not None else '-'}",
                )

                painel = Panel(
                    tabela, title="Estatísticas (janela)", expand=False, padding=(0, 1)
                )
                return painel

            # Live com layout compacto: painel do progress + painel da tabela lado a lado
            with Live(refresh_per_second=6) as live:
                live.update(
                    Group(
                        Panel(progress, expand=False, padding=(0, 1)),
                        montar_tabela_compacta(0),
                    )
                )

                for episodio in range(episodios):
                    vencedor, _ = self.executar_episodio()

                    if vencedor == 1:
                        vitorias_x_janela += 1
                    elif vencedor == 2:
                        vitorias_o_janela += 1
                    else:
                        empates_janela += 1

                    progress.update(task_id, advance=1)

                    # Checkpoint estatístico (janela)
                    if (episodio + 1) % intervalo_estatisticas == 0:
                        total_janela = intervalo_estatisticas
                        taxa_x = (vitorias_x_janela / total_janela) * 100
                        taxa_o = (vitorias_o_janela / total_janela) * 100
                        taxa_emp = (empates_janela / total_janela) * 100

                        # Salva no histórico (para persistência)
                        self.historico_vitorias_x.append(vitorias_x_janela)
                        self.historico_vitorias_o.append(vitorias_o_janela)
                        self.historico_empates.append(empates_janela)
                        self.historico_epsilon_x.append(self.agente_x.epsilon)
                        self.historico_epsilon_o.append(self.agente_o.epsilon)

                        # Reseta janela
                        vitorias_x_janela = 0
                        vitorias_o_janela = 0
                        empates_janela = 0

                    # Checkpoint de salvamento (silencioso)
                    if (episodio + 1) % intervalo_checkpoint == 0:
                        self._salvar_checkpoint(episodio + 1)
                        self.ultimo_checkpoint = episodio + 1

                    # Atualiza a Live com layout compacto (in-place)
                    live.update(
                        Group(
                            Panel(progress, expand=False, padding=(0, 1)),
                            montar_tabela_compacta(episodio + 1),
                        )
                    )

        else:
            # --- MODO TQDM (fallback) ---
            with tqdm(
                total=episodios, desc="Treinando", disable=not self.verbose
            ) as pbar:
                for episodio in range(episodios):
                    vencedor, _ = self.executar_episodio()

                    if vencedor == 1:
                        vitorias_x_janela += 1
                    elif vencedor == 2:
                        vitorias_o_janela += 1
                    else:
                        empates_janela += 1

                    total_window = (
                        vitorias_x_janela + vitorias_o_janela + empates_janela
                    )
                    taxa_empate = (
                        (empates_janela / total_window) * 100
                        if total_window > 0
                        else 0.0
                    )

                    postfix = {
                        "EpsX": f"{self.agente_x.epsilon:.4f}",
                        "EpsO": f"{self.agente_o.epsilon:.4f}",
                        "Emp%": f"{taxa_empate:.1f}%",
                        "QX": f"{len(self.agente_x.q_table):,}",
                        "QO": f"{len(self.agente_o.q_table):,}",
                        "chk": f"{self.ultimo_checkpoint if self.ultimo_checkpoint is not None else '-'}",
                    }

                    pbar.set_postfix(postfix)

                    if (episodio + 1) % intervalo_estatisticas == 0:
                        self.historico_vitorias_x.append(vitorias_x_janela)
                        self.historico_vitorias_o.append(vitorias_o_janela)
                        self.historico_empates.append(empates_janela)
                        self.historico_epsilon_x.append(self.agente_x.epsilon)
                        self.historico_epsilon_o.append(self.agente_o.epsilon)

                        # reseta
                        vitorias_x_janela = 0
                        vitorias_o_janela = 0
                        empates_janela = 0

                    if (episodio + 1) % intervalo_checkpoint == 0:
                        self._salvar_checkpoint(episodio + 1)
                        self.ultimo_checkpoint = episodio + 1
                        pbar.set_postfix(postfix)

                    pbar.update(1)

        # Finalização — prints fora do loop (apenas no fim)
        tempo_total = time.time() - tempo_inicio

        if self.verbose:
            print("\n" + "=" * 70)
            print("✅ TREINAMENTO CONCLUÍDO!")
            print("=" * 70)
            print(
                f"Tempo total: {tempo_total:.2f} segundos ({tempo_total/60:.2f} minutos)"
            )
            print(f"Velocidade: {episodios/tempo_total:.1f} episódios/segundo")
            print()

        # Estatísticas finais (métodos do agente devem existir)
        self.agente_x.imprimir_estatisticas()
        self.agente_o.imprimir_estatisticas()

        if salvar_final:
            self._salvar_modelos_finais(episodios)
            self._salvar_estatisticas(episodios)

    def _salvar_checkpoint(self, episodio: int):
        """
        Salva silenciosamente um checkpoint — sem prints nem tqdm.write.
        O objetivo é não inserir linhas no terminal durante o treinamento.
        """
        caminho_x = self.pasta_modelos / f"agente_x_checkpoint_{episodio}.pkl"
        caminho_o = self.pasta_modelos / f"agente_o_checkpoint_{episodio}.pkl"

        self.agente_x.salvar(str(caminho_x))
        self.agente_o.salvar(str(caminho_o))

    def _salvar_modelos_finais(self, episodios: int):
        if self.verbose:
            print("\n💾 Salvando modelos finais...")

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        caminho_x = (
            self.pasta_modelos / f"agente_x_final_{episodios}_eps_{timestamp}.pkl"
        )
        caminho_o = (
            self.pasta_modelos / f"agente_o_final_{episodios}_eps_{timestamp}.pkl"
        )

        self.agente_x.salvar(str(caminho_x))
        self.agente_o.salvar(str(caminho_o))

        if self.verbose:
            print(f"✅ Modelos salvos na pasta '{self.pasta_modelos}/'")

    def _salvar_estatisticas(self, episodios: int):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        caminho = self.pasta_estatisticas / f"treino_{episodios}_eps_{timestamp}.json"

        dados = {
            "episodios_totais": episodios,
            "configuracao": {
                "agente_x": {
                    "alpha": self.agente_x.alpha,
                    "gamma": self.agente_x.gamma,
                    "epsilon_inicial": 1.0,
                    "epsilon_final": self.agente_x.epsilon,
                },
                "agente_o": {
                    "alpha": self.agente_o.alpha,
                    "gamma": self.agente_o.gamma,
                    "epsilon_inicial": 1.0,
                    "epsilon_final": self.agente_o.epsilon,
                },
            },
            "resultados": {
                "agente_x": self.agente_x.obter_estatisticas(),
                "agente_o": self.agente_o.obter_estatisticas(),
            },
            "historico": {
                "vitorias_x": self.historico_vitorias_x,
                "vitorias_o": self.historico_vitorias_o,
                "empates": self.historico_empates,
                "epsilon_x": self.historico_epsilon_x,
                "epsilon_o": self.historico_epsilon_o,
            },
        }

        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False)

        if self.verbose:
            print(f"📊 Estatísticas salvas em '{caminho}'")

    def avaliar_agentes(self, num_partidas: int = 100) -> Dict:
        """
        Avalia o desempenho dos agentes sem exploração (treino=False).
        """
        print(f"\n🎯 AVALIANDO AGENTES ({num_partidas} partidas)...")

        vitorias_x = 0
        vitorias_o = 0
        empates = 0

        for _ in tqdm(range(num_partidas), desc="Avaliando"):
            estado = self.ambiente.resetar()

            while not self.ambiente.finalizado:
                agente = (
                    self.agente_x if self.ambiente.jogador_atual == 1 else self.agente_o
                )
                estado_atual = self.ambiente.obter_estado()
                acoes_validas = self.ambiente.obter_acoes_validas()
                acao = agente.escolher_acao(estado_atual, acoes_validas, treino=False)
                self.ambiente.fazer_jogada(acao)

            if self.ambiente.vencedor == 1:
                vitorias_x += 1
            elif self.ambiente.vencedor == 2:
                vitorias_o += 1
            else:
                empates += 1

        taxa_x = (vitorias_x / num_partidas) * 100
        taxa_o = (vitorias_o / num_partidas) * 100
        taxa_empate = (empates / num_partidas) * 100

        resultados = {
            "partidas": num_partidas,
            "vitorias_x": vitorias_x,
            "vitorias_o": vitorias_o,
            "empates": empates,
            "taxa_vitoria_x": taxa_x,
            "taxa_vitoria_o": taxa_o,
            "taxa_empate": taxa_empate,
        }

        print("\n📊 RESULTADOS DA AVALIAÇÃO:")
        print(f"X venceu: {vitorias_x:>3}/{num_partidas} ({taxa_x:>5.1f}%)")
        print(f"O venceu: {vitorias_o:>3}/{num_partidas} ({taxa_o:>5.1f}%)")
        print(f"Empates:  {empates:>3}/{num_partidas} ({taxa_empate:>5.1f}%)")

        if taxa_empate > 95:
            print(
                "\n🤝 PERFEITO! Os agentes atingiram o equilíbrio de Nash (ou algo muito próximo)."
            )
        elif taxa_empate > 75:
            print("\n🏆 EXCELENTE! Ambos os agentes jogam quase perfeitamente.")
        elif taxa_empate > 50:
            print(
                "\n👍 BOM! Os agentes estão jogando bem, mas ainda há espaço para melhoria."
            )
        else:
            print("\n⚠️  Os agentes precisam de mais treinamento.")

        return resultados


# ===== Funções auxiliares de conveniência =====
def treinar_novo_modelo(episodios: int = 20000, alpha: float = 0.5, gamma: float = 0.9):
    agente_x = AgenteQLearning(
        alpha=alpha,
        gamma=gamma,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.9995,
        jogador=1,
    )
    agente_o = AgenteQLearning(
        alpha=alpha,
        gamma=gamma,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.9995,
        jogador=2,
    )

    treinador = TreinadorSelfPlay(agente_x, agente_o, verbose=True)

    treinador.treinar(
        episodios=episodios,
        intervalo_estatisticas=1000,
        intervalo_checkpoint=5000,
        salvar_final=True,
    )
    treinador.avaliar_agentes(num_partidas=100)
    return treinador


def continuar_treinamento(
    caminho_agente_x: str, caminho_agente_o: str, episodios_adicionais: int = 10000
):
    agente_x = AgenteQLearning.carregar(caminho_agente_x)
    agente_o = AgenteQLearning.carregar(caminho_agente_o)
    treinador = TreinadorSelfPlay(agente_x, agente_o, verbose=True)
    treinador.treinar(
        episodios=episodios_adicionais,
        intervalo_estatisticas=1000,
        intervalo_checkpoint=5000,
        salvar_final=True,
    )
    treinador.avaliar_agentes(num_partidas=100)
    return treinador


def teste_rapido():
    print("\n" + "=" * 70)
    print("🧪 TESTE RÁPIDO DO TREINADOR")
    print("=" * 70)
    print("Treinando por apenas 1.000 episódios para testar...\n")
    treinador = treinar_novo_modelo(episodios=1000, alpha=0.5, gamma=0.9)
    print("\n✅ Teste concluído!")


if __name__ == "__main__":
    # Opção 1: Teste rápido (1.000 episódios)
    # teste_rapido()

    # Opção 2: Treinamento completo (50.000 episódios)
    treinar_novo_modelo(episodios=10000)

    # Opção 3: Treinamento custom
    # treinar_novo_modelo(episodios=20000, alpha=0.3, gamma=0.95)
