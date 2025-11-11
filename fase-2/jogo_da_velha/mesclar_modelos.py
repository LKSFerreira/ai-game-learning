"""
Módulo: 💎 mesclar_modelos.py
Projeto: 📘 AI Game Learning

Esta é uma ferramenta para criar um "Superagente" a partir de dois agentes
previamente treinados (X e O).
"""

import pickle
from pathlib import Path
import copy

def mesclar_tabelas_q(caminho_agente_x: str, caminho_agente_o: str, caminho_saida: str):
    """
    Carrega, mescla e salva as Tabelas Q de dois agentes.
    """
    print("\n" + "="*50)
    print("💎 INICIANDO A FUSÃO DE CONHECIMENTO DOS AGENTES 💎")
    print("="*50)

    # --- 1. Carregar as Memórias (Tabelas Q) - LÓGICA CORRIGIDA ---
    try:
        with open(caminho_agente_x, 'rb') as f:
            dados_x = pickle.load(f)
            # Verifica se os dados estão dentro de um "contêiner" (dicionário)
            # Se for um dicionário e tiver a chave 'q_table', pegue-a. Senão, use os dados diretamente.
            tabela_q_x = dados_x.get('q_table', dados_x) if isinstance(dados_x, dict) else dados_x
        print(f"✅ Memória do Agente X carregada: {len(tabela_q_x):,} estados conhecidos.")

        with open(caminho_agente_o, 'rb') as f:
            dados_o = pickle.load(f)
            # Faz a mesma verificação para o agente O
            tabela_q_o = dados_o.get('q_table', dados_o) if isinstance(dados_o, dict) else dados_o
        print(f"✅ Memória do Agente O carregada: {len(tabela_q_o):,} estados conhecidos.")

    except FileNotFoundError as e:
        print(f"❌ ERRO: Arquivo de modelo não encontrado: {e}.")
        return
    except (KeyError, TypeError):
        print("❌ ERRO: O formato dos arquivos .pkl é inesperado. Verifique como os dados foram salvos.")
        return

    # --- 2. Iniciar a Fusão (Lógica já corrigida anteriormente) ---
    print("\nIniciando o processo de mesclagem...")
    
    tabela_q_mesclada = copy.deepcopy(tabela_q_x)
    conflitos_resolvidos, estados_novos_adicionados, acoes_novas_adicionadas = 0, 0, 0

    for estado_o, acoes_o in tabela_q_o.items():
        if estado_o not in tabela_q_mesclada:
            tabela_q_mesclada[estado_o] = acoes_o
            estados_novos_adicionados += 1
        else:
            for acao_o, valor_q_o in acoes_o.items():
                if acao_o not in tabela_q_mesclada[estado_o]:
                    tabela_q_mesclada[estado_o][acao_o] = valor_q_o
                    acoes_novas_adicionadas += 1
                else:
                    valor_q_existente = tabela_q_mesclada[estado_o][acao_o]
                    if valor_q_o > valor_q_existente:
                        tabela_q_mesclada[estado_o][acao_o] = valor_q_o
                        conflitos_resolvidos += 1
    
    print("Fusão concluída!")

    # --- 3. Exibir Estatísticas da Fusão ---
    print("\n--- ESTATÍSTICAS DA FUSÃO ---")
    print(f"Estados únicos no Agente X: {len(tabela_q_x):,}")
    print(f"Estados únicos no Agente O: {len(tabela_q_o):,}")
    print("-" * 30)
    print(f"Estados que só o Agente O conhecia: {estados_novos_adicionados:,}")
    print(f"Ações novas aprendidas em estados compartilhados: {acoes_novas_adicionadas:,}")
    print(f"Conflitos de opinião resolvidos (mantendo a melhor nota): {conflitos_resolvidos:,}")
    print("-" * 30)
    print(f"Total de estados no Superagente final: {len(tabela_q_mesclada):,}")

    # --- 4. Salvar o Novo Modelo ---
    caminho_arquivo_saida = Path(caminho_saida)
    caminho_arquivo_saida.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho_arquivo_saida, 'wb') as f:
        pickle.dump(tabela_q_mesclada, f)

    print(f"\n💾 Superagente salvo com sucesso em: {caminho_arquivo_saida}")
    print("="*50 + "\n")


if __name__ == "__main__":
    pasta_modelos = Path("modelos_treinados")
    dimensao = 3
    caminho_x = pasta_modelos / f"agente_x_final_{dimensao}x{dimensao}.pkl"
    caminho_o = pasta_modelos / f"agente_o_final_{dimensao}x{dimensao}.pkl"
    caminho_final = pasta_modelos / f"superagente_final_{dimensao}x{dimensao}.pkl"
    mesclar_tabelas_q(caminho_x, caminho_o, caminho_final)