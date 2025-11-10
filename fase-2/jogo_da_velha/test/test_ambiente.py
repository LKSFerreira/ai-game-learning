"""
Módulo: 🧪 test_ambiente.py
Projeto: 📘 AI Game Learning

Este arquivo contém todos os testes para a classe AmbienteJogoDaVelha.
Ele é projetado para ser executado diretamente do terminal para verificar
se o ambiente do jogo está funcionando corretamente.

Para executar, use o comando no terminal:
python fase-2_jogo_velha/test_ambiente.py
"""

# 1. Importamos a "cozinha" (o ambiente) para que o "inspetor" (este script) possa usá-la.
from ambiente import AmbienteJogoDaVelha

def simular_partida(jogo: AmbienteJogoDaVelha, titulo: str, jogadas: list[int]):
    """
    Função auxiliar para simular uma partida completa e exibir os resultados.
    
    Args:
        jogo (AmbienteJogoDaVelha): A instância do ambiente do jogo.
        titulo (str): O título do cenário de teste.
        jogadas (list[int]): Uma lista com a sequência de jogadas a serem executadas.
    """
    print("=" * 50)
    print(f"➡️  Cenário: {titulo}")
    print("=" * 50)

    jogo.reiniciar_partida()
    print("Tabuleiro Inicial:")
    jogo.exibir_tabuleiro()

    for i, acao in enumerate(jogadas):
        jogador = 'X' if jogo.jogador_atual == 1 else 'O'
        print(f"Turno {i + 1}: Jogador '{jogador}' joga na posição {acao}.")
        
        try:
            _, _, fim = jogo.executar_jogada(acao)
            jogo.exibir_tabuleiro()

            if fim:
                if jogo.vencedor == 0:
                    print(f"🏁 Partida finalizada! Resultado: Empate (Velha)!\n")
                else:
                    simbolo_vencedor = 'X' if jogo.vencedor == 1 else 'O'
                    print(f"🏁 Partida finalizada! Vencedor: Jogador '{simbolo_vencedor}'\n")
                return # Termina a simulação para este cenário
                
        except ValueError as e:
            print(f"❌ ERRO AO EXECUTAR JOGADA: {e}")
            return
            
    print("⚠️  A sequência de jogadas terminou antes do fim da partida.")


# --- INÍCIO DA EXECUÇÃO DOS TESTES ---
# Este bloco só é executado quando o arquivo é rodado diretamente.
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🧪 INICIANDO BATERIA DE TESTES DO AMBIENTE 🧪")

    # Testes para o tabuleiro 3x3
    jogo_3x3 = AmbienteJogoDaVelha()
    print("\n✅ Jogo 3x3 criado com sucesso!")
    simular_partida(jogo_3x3, "X vence na primeira linha", [0, 4, 1, 5, 2])
    simular_partida(jogo_3x3, "Empate (Velha)", [0, 4, 8, 2, 6, 3, 5, 7, 1])
    simular_partida(jogo_3x3, "O vence na coluna do meio", [0, 4, 2, 1, 3, 7])

    # Testes para o tabuleiro 4x4
    jogo_4x4 = AmbienteJogoDaVelha(4)
    print("\n✅ Jogo 4x4 criado com sucesso!")
    simular_partida(jogo_4x4, "X vence na diagonal principal (4x4)", [0, 1, 5, 2, 10, 3, 15])

    print("\n" + "=" * 50)
    print("✅ BATERIA DE TESTES CONCLUÍDA!")
    print("=" * 50 + "\n")