from ambiente import Labirinto
# import copy # Não é necessário se a classe Labirinto for bem feita,
             # mas pode ser útil se tiver problemas.


# Exemplo de uso do ambiente
# TODO O CÓDIGO EXECUTÁVEL DEVE FICAR AQUI DENTRO
if __name__ == "__main__":
    
    # Define a matriz do labirinto
    matriz_exemplo = [
        [' ',' ','#',' ',' ',' '],
        ['#',' ',' ',' ','#',' '],
        ['#','#','#','#',' ',' '],
        [' ','#',' ',' ',' ',' '],
        [' ',' ',' ','#','#','#'],
        [' ','#',' ',' ',' ',' ']
    ]
    ponto_inicial_exemplo = (0, 0)
    ponto_final_exemplo = (5, 5) # O 'F' será desenhado aqui

    # Cria uma instância do labirinto
    ambiente_jogo = Labirinto(matriz_exemplo, ponto_inicial_exemplo, ponto_final_exemplo)

    print("--- Labirinto Inicial ---")
    ambiente_jogo.imprimir_labirinto() # Usando a nova função!
    print(f"Posição inicial do agente: {ambiente_jogo.posicao_agente}")
    print(f"Ponto final: {ambiente_jogo.ponto_final}\n")

    # Simulação de algumas ações
    print("--- Executando Ações (Simulação Padrão) ---")
    acoes = ["baixo", "direita", "direita", "baixo", "esquerda", "baixo", "direita", "direita"]

    terminou_simulacao = False
    for i, acao in enumerate(acoes):
        print(f"Ação {i+1}: '{acao}'")
        
        try:
            novo_estado, recompensa, terminou = ambiente_jogo.executar_acao(acao)
            
            ambiente_jogo.imprimir_labirinto() # Visualização após a ação
            
            print(f" ⁠ Novo Estado (Posição): {novo_estado}")
            print(f" ⁠ Recompensa: {recompensa}")
            print(f" ⁠ Terminou: {terminou}")
            print("-" * 20)

            if terminou:
                print("🎉 Agente chegou ao ponto final!")
                terminou_simulacao = True
                break
        
        except ValueError as e:
            # Captura ações inválidas como "pular"
            print(f"Erro ao executar ação: {e}")
            ambiente_jogo.imprimir_labirinto() # Mostra estado atual
            print("-" * 20)
        except Exception as e:
            # Captura outros erros inesperados
            print(f"Erro inesperado durante a ação '{acao}': {e}")
            break # Interrompe a simulação se algo grave ocorrer

    if not terminou_simulacao:
        print("Simulação terminada sem chegar ao objetivo.\n")

    # Reinicia o ambiente
    print("\n--- Reiniciando o Ambiente ---")
    ambiente_jogo.reiniciar()
    ambiente_jogo.imprimir_labirinto()
    print(f"Posição do agente após reiniciar: {ambiente_jogo.posicao_agente}\n")

    # Exemplo de ação inválida (nome)
    print("--- Tentando Ação Inválida (Nome) ---")
    try:
        ambiente_jogo.executar_acao("pular")
    except ValueError as e:
        print(f"Erro capturado com sucesso: {e}\n")

    # Exemplo de ação inválida (movimento para parede)
    print("--- Tentando Andar na Parede ---")
    print(f"Posição atual: {ambiente_jogo.posicao_agente}")
    print("Executando 'cima' (deve bater na borda/parede imaginária)")
    novo_estado, recompensa, terminou = ambiente_jogo.executar_acao("cima")
    ambiente_jogo.imprimir_labirinto()
    print(f" ⁠ Novo Estado: {novo_estado} (provavelmente o mesmo)")
    print(f" ⁠ Recompensa: {recompensa} (provavelmente negativa)")
    
    print("\n" + "="*30 + "\n") # Separador
    
    # --- NOVO BLOCO: TESTE DA SOLUÇÃO COMPLETA ---
    print("--- 🎯 Teste de Solução Completa (Labirinto Principal) ---")
    
    # Reinicia o ambiente principal para o teste de vitória
    ambiente_jogo.reiniciar()
    print("Labirinto principal reiniciado.")
    ambiente_jogo.imprimir_labirinto()
    
    # Sequência de ações que resolve o labirinto 6x6
    acoes_vitoria_completa = [
        "direita", "baixo", "direita", "direita", "cima", "direita", 
        "direita", "baixo", "baixo", "baixo", "esquerda", "esquerda", 
        "esquerda", "baixo", "baixo", "direita", "direita", "direita"
    ]
    
    print(f"Executando sequência de {len(acoes_vitoria_completa)} ações para vencer...")

    recompensa_final = 0
    terminou_final = False
    
    for i, acao in enumerate(acoes_vitoria_completa):
        print(f"Passo {i+1}: '{acao}'")
        try:
            # Captura o estado da *última* ação
            novo_estado, recompensa_final, terminou_final = ambiente_jogo.executar_acao(acao)
            
            ambiente_jogo.imprimir_labirinto()
            print(f" ⁠ Posição: {novo_estado}")
            print(f" ⁠ Recompensa nesta ação: {recompensa_final}")
            
            if terminou_final:
                print("\n🎉🎉🎉 AGENTE CHEGOU AO OBJETIVO (5, 5)! 🎉🎉🎉")
                break
        except Exception as e:
            print(f"Erro inesperado no teste final: {e}")
            break
            
    # 3. Mostrar a recompensa final
    print("\n--- Resultado do Teste de Vitória Completo ---")
    print(f"O agente terminou? {terminou_final}")
    print(f"**Recompensa da Ação Final (Vitória): {recompensa_final}**")

    if not terminou_final:
        print("ALERTA: O teste de vitória falhou. A sequência de ações ou a lógica do labirinto pode estar incorreta.")