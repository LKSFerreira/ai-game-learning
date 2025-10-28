"""
Visualizador de Estatísticas de Treinamento

Este módulo cria gráficos e visualizações dos dados de treinamento
dos agentes Q-Learning.

Funcionalidades:
- Ler arquivos JSON de estatísticas
- Criar gráficos de progresso do treinamento
- Mostrar evolução do epsilon, vitórias, empates
- Comparar múltiplos treinamentos
- Salvar visualizações em alta qualidade

Métricas visualizadas:
- Taxa de vitórias/derrotas/empates por janela
- Evolução do epsilon (exploração → exploração)
- Crescimento da Q-Table (estados conhecidos)
- Média móvel para suavizar curvas
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np
from datetime import datetime


class VisualizadorTreinamento:
    """
    Classe para visualizar estatísticas de treinamento de agentes RL.
    
    Cria gráficos profissionais mostrando a evolução do aprendizado:
    - Desempenho (vitórias, derrotas, empates)
    - Exploração (epsilon decay)
    - Conhecimento adquirido (tamanho Q-Table)
    """
    
    def __init__(self, pasta_estatisticas: str = "estatisticas"):
        """
        Inicializa o visualizador.
        
        Args:
            pasta_estatisticas: Pasta contendo arquivos JSON de treino
        """
        self.pasta_estatisticas = Path(pasta_estatisticas)
        self.pasta_graficos = Path("graficos")
        self.pasta_graficos.mkdir(exist_ok=True)
        
        # Configurações de estilo
        self._configurar_estilo()
    
    def _configurar_estilo(self):
        """Configura o estilo visual dos gráficos."""
        # Estilo geral
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Configurações globais
        plt.rcParams['figure.figsize'] = (16, 10)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 11
        plt.rcParams['axes.titlesize'] = 13
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 16
        
        # Cores personalizadas
        self.cores = {
            'x_vitoria': '#2E86AB',  # Azul
            'o_vitoria': '#A23B72',  # Roxo
            'empate': '#F18F01',     # Laranja
            'epsilon': '#C73E1D',    # Vermelho
            'qtable_x': '#06A77D',   # Verde
            'qtable_o': '#005377',   # Azul escuro
            'media_movel': '#555555' # Cinza
        }
    
    def listar_estatisticas_disponiveis(self) -> List[Path]:
        """
        Lista todos os arquivos de estatísticas disponíveis.
        
        Returns:
            Lista de caminhos para arquivos JSON
        """
        if not self.pasta_estatisticas.exists():
            print(f"⚠️  Pasta '{self.pasta_estatisticas}' não encontrada!")
            return []
        
        arquivos = sorted(self.pasta_estatisticas.glob("treino_*.json"))
        return arquivos
    
    def carregar_estatisticas(self, caminho: Path) -> Optional[Dict]:
        """
        Carrega estatísticas de um arquivo JSON.
        
        Args:
            caminho: Caminho do arquivo JSON
        
        Returns:
            Dicionário com dados de treinamento ou None se erro
        """
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            return dados
        except Exception as e:
            print(f"❌ Erro ao carregar {caminho.name}: {e}")
            return None
    
    def calcular_media_movel(
        self,
        dados: List[float],
        janela: int = 5
    ) -> List[float]:
        """
        Calcula média móvel para suavizar curvas.
        
        Args:
            dados: Lista de valores
            janela: Tamanho da janela de média
        
        Returns:
            Lista com médias móveis
        """
        if len(dados) < janela:
            return dados
        
        medias = []
        for i in range(len(dados)):
            inicio = max(0, i - janela + 1)
            fim = i + 1
            media = np.mean(dados[inicio:fim])
            medias.append(media)
        
        return medias
    
    def criar_grafico_completo(
        self,
        caminho_json: Path,
        salvar: bool = True,
        mostrar: bool = True
    ):
        """
        Cria visualização completa com todos os gráficos.
        
        Args:
            caminho_json: Arquivo JSON com estatísticas
            salvar: Se deve salvar o gráfico
            mostrar: Se deve mostrar o gráfico na tela
        """
        print(f"\n📊 Carregando estatísticas de: {caminho_json.name}")
        
        dados = self.carregar_estatisticas(caminho_json)
        if not dados:
            return
        
        # Extrai informações
        historico = dados.get('historico', {})
        config = dados.get('configuracao', {})
        episodios_totais = dados.get('episodios_totais', 0)
        
        # Prepara dados
        vitorias_x = historico.get('vitorias_x', [])
        vitorias_o = historico.get('vitorias_o', [])
        empates = historico.get('empates', [])
        epsilon_x = historico.get('epsilon_x', [])
        epsilon_o = historico.get('epsilon_o', [])
        
        # Cria figura com subplots
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle(
            f'Análise de Treinamento - {episodios_totais:,} Episódios\n'
            f'Alpha: {config["agente_x"]["alpha"]} | '
            f'Gamma: {config["agente_x"]["gamma"]}',
            fontsize=16,
            fontweight='bold'
        )
        
        # Define grid de subplots
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.25)
        
        # 1. Taxa de Resultados (3 linhas)
        ax1 = fig.add_subplot(gs[0, :])
        self._plotar_resultados(ax1, vitorias_x, vitorias_o, empates)
        
        # 2. Taxa de Empates (foco no objetivo)
        ax2 = fig.add_subplot(gs[1, 0])
        self._plotar_taxa_empates(ax2, vitorias_x, vitorias_o, empates)
        
        # 3. Evolução do Epsilon
        ax3 = fig.add_subplot(gs[1, 1])
        self._plotar_epsilon(ax3, epsilon_x, epsilon_o)
        
        # 4. Distribuição Final de Resultados (Pizza)
        ax4 = fig.add_subplot(gs[2, 0])
        self._plotar_distribuicao_final(ax4, vitorias_x, vitorias_o, empates)
        
        # 5. Convergência (últimas janelas)
        ax5 = fig.add_subplot(gs[2, 1])
        self._plotar_convergencia(ax5, vitorias_x, vitorias_o, empates)
        
        # Adiciona informações adicionais
        self._adicionar_info_texto(fig, dados)
        
        # Salva ou mostra
        if salvar:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"analise_treino_{episodios_totais}_eps_{timestamp}.png"
            caminho_saida = self.pasta_graficos / nome_arquivo
            
            plt.savefig(
                caminho_saida,
                dpi=300,
                bbox_inches='tight',
                facecolor='white'
            )
            print(f"✅ Gráfico salvo em: {caminho_saida}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()
    
    def _plotar_resultados(
        self,
        ax,
        vitorias_x: List[int],
        vitorias_o: List[int],
        empates: List[int]
    ):
        """Plota evolução de vitórias X, O e empates."""
        janelas = range(1, len(vitorias_x) + 1)
        
        # Calcula médias móveis
        media_x = self.calcular_media_movel(vitorias_x, janela=3)
        media_o = self.calcular_media_movel(vitorias_o, janela=3)
        media_emp = self.calcular_media_movel(empates, janela=3)
        
        # Plota linhas
        ax.plot(
            janelas, vitorias_x,
            color=self.cores['x_vitoria'], alpha=0.3, linewidth=1
        )
        ax.plot(
            janelas, media_x,
            color=self.cores['x_vitoria'], linewidth=2.5, label='Vitórias X'
        )
        
        ax.plot(
            janelas, vitorias_o,
            color=self.cores['o_vitoria'], alpha=0.3, linewidth=1
        )
        ax.plot(
            janelas, media_o,
            color=self.cores['o_vitoria'], linewidth=2.5, label='Vitórias O'
        )
        
        ax.plot(
            janelas, empates,
            color=self.cores['empate'], alpha=0.3, linewidth=1
        )
        ax.plot(
            janelas, media_emp,
            color=self.cores['empate'], linewidth=2.5, label='Empates'
        )
        
        ax.set_xlabel('Janela de Treinamento')
        ax.set_ylabel('Quantidade de Resultados')
        ax.set_title('Evolução dos Resultados ao Longo do Treinamento', fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
    
    def _plotar_taxa_empates(
        self,
        ax,
        vitorias_x: List[int],
        vitorias_o: List[int],
        empates: List[int]
    ):
        """Plota taxa de empate (métrica principal de sucesso)."""
        janelas = range(1, len(empates) + 1)
        
        # Calcula taxa de empate por janela
        taxas_empate = []
        for vx, vo, emp in zip(vitorias_x, vitorias_o, empates):
            total = vx + vo + emp
            taxa = (emp / total * 100) if total > 0 else 0
            taxas_empate.append(taxa)
        
        # Média móvel
        media_taxa = self.calcular_media_movel(taxas_empate, janela=5)
        
        # Plota
        ax.plot(
            janelas, taxas_empate,
            color=self.cores['empate'], alpha=0.3, linewidth=1
        )
        ax.plot(
            janelas, media_taxa,
            color=self.cores['empate'], linewidth=2.5, label='Taxa de Empate'
        )
        
        # Linha de referência (objetivo: >80%)
        ax.axhline(y=80, color='green', linestyle='--', linewidth=2, alpha=0.5, label='Objetivo (80%)')
        ax.axhline(y=95, color='gold', linestyle='--', linewidth=2, alpha=0.5, label='Excelente (95%)')
        
        ax.set_xlabel('Janela de Treinamento')
        ax.set_ylabel('Taxa de Empate (%)')
        ax.set_title('Taxa de Empate (Indicador de Aprendizado Ótimo)', fontweight='bold')
        ax.set_ylim([0, 105])
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Adiciona zona de sucesso
        ax.fill_between(janelas, 80, 100, alpha=0.1, color='green')
    
    def _plotar_epsilon(
        self,
        ax,
        epsilon_x: List[float],
        epsilon_o: List[float]
    ):
        """Plota evolução do epsilon (exploração → exploração)."""
        janelas = range(1, len(epsilon_x) + 1)
        
        ax.plot(
            janelas, epsilon_x,
            color=self.cores['epsilon'], linewidth=2.5, label='Epsilon X', marker='o', markersize=3
        )
        ax.plot(
            janelas, epsilon_o,
            color=self.cores['epsilon'], linewidth=2.5, linestyle='--', label='Epsilon O', marker='s', markersize=3
        )
        
        # Linha de epsilon mínimo (geralmente 0.01)
        epsilon_min = min(min(epsilon_x), min(epsilon_o))
        ax.axhline(y=epsilon_min, color='gray', linestyle=':', linewidth=1.5, alpha=0.5, label=f'Mínimo ({epsilon_min:.4f})')
        
        ax.set_xlabel('Janela de Treinamento')
        ax.set_ylabel('Epsilon (Taxa de Exploração)')
        ax.set_title('Decaimento do Epsilon (Exploração → Exploração)', fontweight='bold')
        ax.set_yscale('log')  # Escala logarítmica para visualizar melhor
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, which='both')
    
    def _plotar_distribuicao_final(
        self,
        ax,
        vitorias_x: List[int],
        vitorias_o: List[int],
        empates: List[int]
    ):
        """Plota distribuição final de resultados (gráfico de pizza)."""
        # Soma total dos últimos resultados
        total_x = sum(vitorias_x[-10:]) if len(vitorias_x) >= 10 else sum(vitorias_x)
        total_o = sum(vitorias_o[-10:]) if len(vitorias_o) >= 10 else sum(vitorias_o)
        total_emp = sum(empates[-10:]) if len(empates) >= 10 else sum(empates)
        
        total_geral = total_x + total_o + total_emp
        
        # Dados
        labels = [f'X Venceu\n({total_x})', f'O Venceu\n({total_o})', f'Empates\n({total_emp})']
        sizes = [total_x, total_o, total_emp]
        colors = [self.cores['x_vitoria'], self.cores['o_vitoria'], self.cores['empate']]
        explode = (0.05, 0.05, 0.1)  # Destaca empates
        
        ax.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90,
            textprops={'fontsize': 11, 'weight': 'bold'}
        )
        
        num_janelas = 10 if len(vitorias_x) >= 10 else len(vitorias_x)
        ax.set_title(f'Distribuição de Resultados\n(Últimas {num_janelas} Janelas)', fontweight='bold')
    
    def _plotar_convergencia(
        self,
        ax,
        vitorias_x: List[int],
        vitorias_o: List[int],
        empates: List[int]
    ):
        """Plota convergência (últimas 20 janelas) para ver estabilidade."""
        ultimas_n = 20
        
        if len(empates) < ultimas_n:
            ultimas_n = len(empates)
        
        vx_ult = vitorias_x[-ultimas_n:]
        vo_ult = vitorias_o[-ultimas_n:]
        emp_ult = empates[-ultimas_n:]
        
        janelas_ult = range(len(empates) - ultimas_n + 1, len(empates) + 1)
        
        # Empilhado (stacked bar)
        ax.bar(janelas_ult, vx_ult, color=self.cores['x_vitoria'], label='X Venceu')
        ax.bar(janelas_ult, vo_ult, bottom=vx_ult, color=self.cores['o_vitoria'], label='O Venceu')
        
        bottoms = [x + o for x, o in zip(vx_ult, vo_ult)]
        ax.bar(janelas_ult, emp_ult, bottom=bottoms, color=self.cores['empate'], label='Empates')
        
        ax.set_xlabel('Janela de Treinamento')
        ax.set_ylabel('Quantidade de Jogos')
        ax.set_title(f'Convergência (Últimas {ultimas_n} Janelas)', fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3, axis='y')
    
    def _adicionar_info_texto(self, fig, dados: Dict):
        """Adiciona caixa de texto com informações resumidas."""
        resultados_x = dados['resultados']['agente_x']
        resultados_o = dados['resultados']['agente_o']
        
        info_texto = (
            f"Estados Conhecidos:\n"
            f"  X: {resultados_x['estados_conhecidos']:,}\n"
            f"  O: {resultados_o['estados_conhecidos']:,}\n\n"
            f"Taxa Final:\n"
            f"  X: {resultados_x['taxa_vitoria']*100:.1f}% vitórias\n"
            f"  O: {resultados_o['taxa_vitoria']*100:.1f}% vitórias\n"
            f"  Empates: {resultados_x['taxa_empate']*100:.1f}%"
        )
        
        fig.text(
            0.02, 0.02, info_texto,
            fontsize=9,
            verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3)
        )
    
    def criar_comparacao(
        self,
        caminhos_json: List[Path],
        metrica: str = 'empates',
        salvar: bool = True,
        mostrar: bool = True
    ):
        """
        Compara múltiplos treinamentos lado a lado.
        
        Args:
            caminhos_json: Lista de arquivos JSON para comparar
            metrica: 'empates', 'vitorias_x', 'vitorias_o', 'epsilon'
            salvar: Se deve salvar o gráfico
            mostrar: Se deve mostrar o gráfico
        """
        print(f"\n📊 Comparando {len(caminhos_json)} treinamentos...")
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        for caminho in caminhos_json:
            dados = self.carregar_estatisticas(caminho)
            if not dados:
                continue
            
            historico = dados.get('historico', {})
            episodios = dados.get('episodios_totais', 0)
            
            if metrica == 'empates':
                valores = historico.get('empates', [])
            elif metrica == 'vitorias_x':
                valores = historico.get('vitorias_x', [])
            elif metrica == 'vitorias_o':
                valores = historico.get('vitorias_o', [])
            elif metrica == 'epsilon':
                valores = historico.get('epsilon_x', [])
            else:
                valores = []
            
            media_movel = self.calcular_media_movel(valores, janela=5)
            janelas = range(1, len(media_movel) + 1)
            
            ax.plot(
                janelas, media_movel,
                linewidth=2, label=f'{episodios:,} episódios', marker='o', markersize=4
            )
        
        ax.set_xlabel('Janela de Treinamento')
        ax.set_ylabel(metrica.replace('_', ' ').title())
        ax.set_title(f'Comparação de Treinamentos - {metrica.replace("_", " ").title()}', fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        if salvar:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"comparacao_{metrica}_{timestamp}.png"
            caminho_saida = self.pasta_graficos / nome_arquivo
            plt.savefig(caminho_saida, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"✅ Comparação salva em: {caminho_saida}")
        
        if mostrar:
            plt.show()
        else:
            plt.close()


# ===== INTERFACE DE MENU =====

def menu_principal():
    """Interface de menu para o visualizador."""
    print("\n" + "="*70)
    print("📊 VISUALIZADOR DE ESTATÍSTICAS DE TREINAMENTO")
    print("="*70)
    
    visualizador = VisualizadorTreinamento()
    arquivos = visualizador.listar_estatisticas_disponiveis()
    
    if not arquivos:
        print("\n❌ Nenhum arquivo de estatísticas encontrado!")
        print("   Execute o treinamento primeiro (treinador.py)")
        return
    
    print(f"\n📂 Encontrados {len(arquivos)} arquivo(s) de estatísticas:\n")
    
    for i, arquivo in enumerate(arquivos, 1):
        print(f"  {i}. {arquivo.name}")
    
    print(f"\n  {len(arquivos) + 1}. Comparar múltiplos treinamentos")
    print("  0. Sair\n")
    
    try:
        escolha = int(input("Digite o número da opção: "))
        
        if escolha == 0:
            print("👋 Até logo!")
            return
        
        if escolha == len(arquivos) + 1:
            # Modo comparação
            print("\nSelecione os arquivos para comparar (separados por vírgula):")
            indices = input("Ex: 1,2,3: ").strip().split(',')
            
            arquivos_comparar = []
            for idx in indices:
                try:
                    arquivos_comparar.append(arquivos[int(idx) - 1])
                except (ValueError, IndexError):
                    print(f"⚠️  Índice inválido: {idx}")
            
            if len(arquivos_comparar) < 2:
                print("❌ Selecione pelo menos 2 arquivos para comparar!")
                return
            
            print("\nQual métrica comparar?")
            print("  1. Empates")
            print("  2. Vitórias X")
            print("  3. Vitórias O")
            print("  4. Epsilon")
            
            metrica_escolha = int(input("\nEscolha: "))
            metricas = {1: 'empates', 2: 'vitorias_x', 3: 'vitorias_o', 4: 'epsilon'}
            metrica = metricas.get(metrica_escolha, 'empates')
            
            visualizador.criar_comparacao(arquivos_comparar, metrica=metrica)
        
        elif 1 <= escolha <= len(arquivos):
            arquivo_selecionado = arquivos[escolha - 1]
            visualizador.criar_grafico_completo(arquivo_selecionado)
        
        else:
            print("⚠️  Opção inválida!")
    
    except ValueError:
        print("⚠️  Digite um número válido!")
    except KeyboardInterrupt:
        print("\n\n👋 Interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    menu_principal()
