"""
Módulo: 🧪 test_treinador.py
Projeto: 📘 AI Game Learning

Este arquivo realiza um teste de integração rápido para a classe Treinador.
Ele verifica se o ciclo completo de treinamento (partida -> aprendizado)
funciona sem erros para um número pequeno de partidas.

Para executar, use o comando no terminal:
python fase-2_jogo_velha/test_treinador.py
"""

from ambiente import AmbienteJogoDaVelha
from agente import AgenteQLearning
from treinador import Treinador

def testar_ciclo_de_treinamento_rapido():
    """
    Verifica se o treinador consegue executar um ciclo de treinamento
    curto sem levantar exceções.
    """
    print("--- INICIANDO TESTE 1: CICLO DE TREINAMENTO RÁPIDO ---")
    
    # 1. Configuração do cenário de teste
    ambiente_teste = AmbienteJogoDaVelha(dimensao=3)
    agente_x_teste = AgenteQLearning(jogador=1)
    agente_o_teste = AgenteQLearning(jogador=2)
    
    treinador_teste = Treinador(agente_x_teste, agente_o_teste, ambiente_teste)
    
    numero_de_partidas_teste = 100
    
    print(f"Executando um mini-treinamento de {numero_de_partidas_teste} partidas...")
    
    # 2. Execução do método a ser testado
    # (Usamos um try/except para capturar qualquer erro inesperado)
    try:
        treinador_teste.treinar(numero_de_partidas=numero_de_partidas_teste, intervalo_log=50)
    except Exception as e:
        # Se qualquer erro ocorrer, o teste falha
        assert False, f"O treinamento falhou com um erro: {e}"
        
    # 3. Verificação dos resultados
    # Verificamos se os agentes realmente aprenderam algo (suas memórias não estão vazias)
    assert len(agente_x_teste.tabela_q) > 0, "A Tabela Q do Agente X não deveria estar vazia."
    assert len(agente_o_teste.tabela_q) > 0, "A Tabela Q do Agente O não deveria estar vazia."
    
    # Verificamos se o número de partidas treinadas foi registrado corretamente
    assert agente_x_teste.partidas_treinadas == numero_de_partidas_teste
    assert agente_o_teste.partidas_treinadas == numero_de_partidas_teste
    
    print(f"\n✅ O Agente X conhece {len(agente_x_teste.tabela_q)} situações.")
    print(f"✅ O Agente O conhece {len(agente_o_teste.tabela_q)} situações.")
    print("✅ O ciclo de treinamento rápido foi concluído com sucesso!")
    print("--- TESTE 1 FINALIZADO ---\n")

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🧪 INICIANDO BATERIA DE TESTES DO TREINADOR 🧪")
    print("="*50 + "\n")
    
    testar_ciclo_de_treinamento_rapido()
    
    print("="*50)
    print("✅ TODOS OS TESTES DO TREINADOR CONCLUÍDOS COM SUCESSO!")
    print("="*50 + "\n")