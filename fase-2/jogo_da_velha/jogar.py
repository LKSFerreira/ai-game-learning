"""
Interface para Jogar contra a IA Treinada

Este módulo permite que um humano jogue Jogo da Velha contra
os agentes treinados por Q-Learning.

Funcionalidades:
- Carregar modelos treinados
- Interface de console interativa
- Validação de jogadas
- Estatísticas de desempenho
- Modo de dicas (ver o que a IA faria)
"""

import sys
from pathlib import Path
from typing import Optional, List, Dict
import json
from datetime import datetime

from ambiente import JogoVelha
from agente import AgenteQLearning


class JogadorHumano:
    """
    Classe que representa o jogador humano.
    
    Responsável por:
    - Receber input do usuário
    - Validar jogadas
    - Mostrar informações de ajuda
    """
    
    def __init__(self, simbolo: str, jogador: int):
        """
        Inicializa o jogador humano.
        
        Args:
            simbolo: 'X' ou 'O'
            jogador: 1 ou 2
        """
        self.simbolo = simbolo
        self.jogador = jogador
        self.vitorias = 0
        self.derrotas = 0
        self.empates = 0
    
    def escolher_acao(
        self,
        ambiente: JogoVelha,
        mostrar_dica: bool = False,
        agente_dica: Optional[AgenteQLearning] = None
    ) -> int:
        """
        Solicita uma jogada do usuário.
        
        Args:
            ambiente: Estado atual do jogo
            mostrar_dica: Se deve mostrar sugestão da IA
            agente_dica: Agente para gerar a dica
        
        Returns:
            Posição escolhida (0-8)
        """
        acoes_validas = ambiente.obter_acoes_validas()
        
        # Mostra dica se solicitado
        if mostrar_dica and agente_dica:
            estado = ambiente.obter_estado()
            dica = agente_dica.escolher_acao(estado, acoes_validas, treino=False)
            print(f"💡 Dica: A IA jogaria na posição {dica}")
        
        while True:
            try:
                entrada = input(f"\n{self.simbolo} - Sua jogada (0-8, 'h' para ajuda, 'd' para dica): ").strip().lower()
                
                if entrada == 'h':
                    self._mostrar_ajuda()
                    continue
                
                if entrada == 'd':
                    if agente_dica:
                        estado = ambiente.obter_estado()
                        dica = agente_dica.escolher_acao(estado, acoes_validas, treino=False)
                        print(f"💡 Dica: A IA jogaria na posição {dica}")
                    else:
                        print("⚠️  Dica não disponível (agente não carregado)")
                    continue
                
                if entrada == 'q':
                    print("\n👋 Saindo do jogo...")
                    sys.exit(0)
                
                posicao = int(entrada)
                
                if posicao not in acoes_validas:
                    if posicao < 0 or posicao > 8:
                        print("⚠️  Posição inválida! Use números de 0 a 8.")
                    else:
                        print("⚠️  Essa posição já está ocupada!")
                    continue
                
                return posicao
                
            except ValueError:
                print("⚠️  Entrada inválida! Digite um número de 0 a 8.")
            except KeyboardInterrupt:
                print("\n\n👋 Jogo interrompido pelo usuário.")
                sys.exit(0)
    
    def _mostrar_ajuda(self):
        """Mostra ajuda sobre comandos disponíveis."""
        print("\n" + "="*50)
        print("📖 AJUDA")
        print("="*50)
        print("Comandos disponíveis:")
        print("  0-8  : Escolher posição para jogar")
        print("  h    : Mostrar esta ajuda")
        print("  d    : Pedir dica da IA")
        print("  q    : Sair do jogo")
        print("\nPosições do tabuleiro:")
        print("  0 | 1 | 2")
        print("  ---------")
        print("  3 | 4 | 5")
        print("  ---------")
        print("  6 | 7 | 8")
        print("="*50)


class InterfaceJogo:
    """
    Interface principal do jogo humano vs IA.
    
    Gerencia:
    - Carregamento de modelos
    - Loop do jogo
    - Estatísticas de partidas
    - Menu de opções
    """
    
    def __init__(self):
        """Inicializa a interface do jogo."""
        self.ambiente = JogoVelha()
        self.agente_ia: Optional[AgenteQLearning] = None
        self.jogador_humano: Optional[JogadorHumano] = None
        self.humano_joga_como: Optional[int] = None  # 1 (X) ou 2 (O)
        
        # Estatísticas da sessão
        self.historico_partidas: List[Dict] = []
    
    def iniciar(self):
        """Inicia a interface do jogo."""
        self._mostrar_banner()
        self._selecionar_oponente()
        self._escolher_lado()
        self._loop_principal()
    
    def _mostrar_banner(self):
        """Mostra o banner inicial."""
        print("\n" + "="*60)
        print("🎮 JOGO DA VELHA - HUMANO vs IA")
        print("="*60)
        print("Desafie os agentes treinados por Q-Learning!")
        print("="*60 + "\n")
    
    def _selecionar_oponente(self):
        """Permite ao usuário escolher qual modelo carregar."""
        print("📂 Selecione seu oponente:\n")
        
        pasta_modelos = Path("modelos")
        
        if not pasta_modelos.exists():
            print("❌ Pasta 'modelos/' não encontrada!")
            print("   Execute o treinamento primeiro (treinador.py)")
            sys.exit(1)
        
        # Lista todos os modelos disponíveis
        modelos = sorted(pasta_modelos.glob("*.pkl"))
        
        if not modelos:
            print("❌ Nenhum modelo treinado encontrado!")
            print("   Execute o treinamento primeiro (treinador.py)")
            sys.exit(1)
        
        # Agrupa modelos finais e checkpoints
        modelos_finais = [m for m in modelos if "final" in m.name]
        checkpoints = [m for m in modelos if "checkpoint" in m.name]
        
        opcoes = []
        contador = 1
        
        if modelos_finais:
            print("🏆 Modelos Finais:")
            for modelo in modelos_finais[:5]:  # Mostra até 5 mais recentes
                print(f"  {contador}. {modelo.name}")
                opcoes.append(modelo)
                contador += 1
            print()
        
        if checkpoints:
            print("💾 Checkpoints (últimos 3):")
            for modelo in checkpoints[-3:]:
                print(f"  {contador}. {modelo.name}")
                opcoes.append(modelo)
                contador += 1
            print()
        
        print(f"  {contador}. Caminho customizado")
        print("  0. Sair\n")
        
        while True:
            try:
                escolha = int(input("Digite o número da opção: "))
                
                if escolha == 0:
                    print("👋 Até logo!")
                    sys.exit(0)
                
                if escolha == contador:
                    caminho = input("Digite o caminho do modelo: ").strip()
                    caminho_modelo = Path(caminho)
                else:
                    caminho_modelo = opcoes[escolha - 1]
                
                if not caminho_modelo.exists():
                    print("❌ Arquivo não encontrado!")
                    continue
                
                print(f"\n📥 Carregando {caminho_modelo.name}...")
                self.agente_ia = AgenteQLearning.carregar(str(caminho_modelo))
                print("✅ Modelo carregado com sucesso!\n")
                break
                
            except (ValueError, IndexError):
                print("⚠️  Opção inválida!")
            except Exception as e:
                print(f"❌ Erro ao carregar modelo: {e}")
                sys.exit(1)
    
    def _escolher_lado(self):
        """Permite ao usuário escolher se joga como X ou O."""
        print("🎲 Escolha seu lado:\n")
        print("  1. Jogar como X (você começa)")
        print("  2. Jogar como O (IA começa)")
        print("  3. Aleatório\n")
        
        while True:
            try:
                escolha = int(input("Digite o número da opção: "))
                
                if escolha == 1:
                    self.humano_joga_como = 1
                    self.jogador_humano = JogadorHumano('X', 1)
                    print("\n✅ Você joga como X (começa primeiro)\n")
                    break
                elif escolha == 2:
                    self.humano_joga_como = 2
                    self.jogador_humano = JogadorHumano('O', 2)
                    print("\n✅ Você joga como O (IA começa)\n")
                    break
                elif escolha == 3:
                    import random
                    self.humano_joga_como = random.choice([1, 2])
                    simbolo = 'X' if self.humano_joga_como == 1 else 'O'
                    self.jogador_humano = JogadorHumano(simbolo, self.humano_joga_como)
                    quem_comeca = "você" if self.humano_joga_como == 1 else "IA"
                    print(f"\n🎲 Sorteio: Você joga como {simbolo} ({quem_comeca} começa)\n")
                    break
                else:
                    print("⚠️  Opção inválida!")
                    
            except ValueError:
                print("⚠️  Digite um número válido!")
    
    def _loop_principal(self):
        """Loop principal do jogo."""
        continuar = True
        
        while continuar:
            self._jogar_partida()
            continuar = self._perguntar_continuar()
        
        self._mostrar_estatisticas_finais()
    
    def _jogar_partida(self):
        """Executa uma partida completa."""
        self.ambiente.resetar()
        
        print("\n" + "="*60)
        print("🎮 NOVA PARTIDA")
        print("="*60)
        
        # Mostra quem começa
        if self.ambiente.jogador_atual == self.humano_joga_como:
            print(f"Você ({self.jogador_humano.simbolo}) começa!")
        else:
            simbolo_ia = 'X' if self.agente_ia.jogador == 1 else 'O'
            print(f"IA ({simbolo_ia}) começa!")
        
        # Loop da partida
        while not self.ambiente.finalizado:
            # Mostra o tabuleiro
            print()
            self.ambiente.renderizar_com_indices()
            
            # Determina quem joga
            if self.ambiente.jogador_atual == self.humano_joga_como:
                # Turno do humano
                acao = self.jogador_humano.escolher_acao(
                    self.ambiente,
                    agente_dica=self.agente_ia
                )
            else:
                # Turno da IA
                estado = self.ambiente.obter_estado()
                acoes_validas = self.ambiente.obter_acoes_validas()
                acao = self.agente_ia.escolher_acao(estado, acoes_validas, treino=False)
                simbolo_ia = 'X' if self.agente_ia.jogador == 1 else 'O'
                print(f"\n🤖 IA ({simbolo_ia}) jogou na posição {acao}")
            
            # Executa a jogada
            self.ambiente.fazer_jogada(acao)
        
        # Mostra resultado final
        print()
        self.ambiente.renderizar()
        self._mostrar_resultado()
        self._registrar_partida()
    
    def _mostrar_resultado(self):
        """Mostra o resultado da partida."""
        print("="*60)
        
        if self.ambiente.vencedor == 0:
            print("🤝 EMPATE!")
            self.jogador_humano.empates += 1
        elif self.ambiente.vencedor == self.humano_joga_como:
            print("🎉 VOCÊ VENCEU! Parabéns!")
            self.jogador_humano.vitorias += 1
        else:
            print("😔 IA VENCEU! Tente novamente.")
            self.jogador_humano.derrotas += 1
        
        print("="*60)
        
        # Mostra estatísticas da sessão
        total = self.jogador_humano.vitorias + self.jogador_humano.derrotas + self.jogador_humano.empates
        print(f"\n📊 Estatísticas da Sessão:")
        print(f"   Vitórias:  {self.jogador_humano.vitorias}/{total}")
        print(f"   Derrotas:  {self.jogador_humano.derrotas}/{total}")
        print(f"   Empates:   {self.jogador_humano.empates}/{total}")
    
    def _registrar_partida(self):
        """Registra dados da partida para estatísticas."""
        resultado = None
        if self.ambiente.vencedor == 0:
            resultado = "empate"
        elif self.ambiente.vencedor == self.humano_joga_como:
            resultado = "vitoria"
        else:
            resultado = "derrota"
        
        self.historico_partidas.append({
            'timestamp': datetime.now().isoformat(),
            'humano_simbolo': self.jogador_humano.simbolo,
            'resultado': resultado,
            'vencedor': self.ambiente.vencedor
        })
    
    def _perguntar_continuar(self) -> bool:
        """Pergunta se o usuário quer continuar jogando."""
        while True:
            resposta = input("\n🎮 Jogar novamente? (s/n): ").strip().lower()
            if resposta in ['s', 'sim', 'y', 'yes']:
                return True
            elif resposta in ['n', 'não', 'nao', 'no']:
                return False
            else:
                print("⚠️  Responda 's' para sim ou 'n' para não.")
    
    def _mostrar_estatisticas_finais(self):
        """Mostra estatísticas finais da sessão."""
        print("\n" + "="*60)
        print("📊 ESTATÍSTICAS FINAIS DA SESSÃO")
        print("="*60)
        
        total = len(self.historico_partidas)
        vitorias = self.jogador_humano.vitorias
        derrotas = self.jogador_humano.derrotas
        empates = self.jogador_humano.empates
        
        if total > 0:
            taxa_vitoria = (vitorias / total) * 100
            taxa_empate = (empates / total) * 100
            
            print(f"Partidas jogadas:  {total}")
            print(f"Vitórias:          {vitorias} ({taxa_vitoria:.1f}%)")
            print(f"Derrotas:          {derrotas} ({(derrotas/total)*100:.1f}%)")
            print(f"Empates:           {empates} ({taxa_empate:.1f}%)")
            print()
            
            # Análise de desempenho
            if taxa_vitoria > 40:
                print("🏆 EXCELENTE! Você está jogando muito bem contra a IA!")
            elif taxa_empate > 60:
                print("🤝 ÓTIMO! Você está no nível da IA (muitos empates).")
            elif taxa_vitoria + taxa_empate > 50:
                print("👍 BOM! Continue praticando para melhorar ainda mais.")
            else:
                print("💪 Continue treinando! A IA é forte, mas você pode vencê-la.")
            
            # Salva estatísticas
            self._salvar_estatisticas()
        
        print("\n👋 Obrigado por jogar! Até a próxima.")
    
    def _salvar_estatisticas(self):
        """Salva estatísticas da sessão em arquivo."""
        pasta_stats = Path("estatisticas_jogador")
        pasta_stats.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = pasta_stats / f"sessao_{timestamp}.json"
        
        dados = {
            'timestamp_inicio': self.historico_partidas[0]['timestamp'],
            'timestamp_fim': self.historico_partidas[-1]['timestamp'],
            'total_partidas': len(self.historico_partidas),
            'vitorias': self.jogador_humano.vitorias,
            'derrotas': self.jogador_humano.derrotas,
            'empates': self.jogador_humano.empates,
            'modelo_ia': str(self.agente_ia.obter_estatisticas()['episodios']),
            'historico': self.historico_partidas
        }
        
        with open(caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(dados, arquivo, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Estatísticas salvas em '{caminho}'")


# ===== FUNÇÃO PRINCIPAL =====

def main():
    """Função principal para executar o jogo."""
    try:
        interface = InterfaceJogo()
        interface.iniciar()
    except KeyboardInterrupt:
        print("\n\n👋 Jogo interrompido. Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
