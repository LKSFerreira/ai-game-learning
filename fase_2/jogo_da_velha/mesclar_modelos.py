"""
Módulo: 💎 mesclar_modelos.py
Projeto: 📘 AI Game Learning

Este módulo implementa uma ferramenta para criar um "Superagente" combinando
o conhecimento de dois agentes previamente treinados (um que joga como 'X'
e outro que joga como 'O').

A mesclagem funciona combinando as Tabelas Q de ambos os agentes, criando um
agente mais forte que possui o conhecimento de ambos. O processo resolve
conflitos (quando ambos os agentes conhecem o mesmo estado) mantendo sempre
o maior valor Q, assumindo que valores maiores representam conhecimento melhor.

Por que mesclar agentes?
- Cada agente aprende perspectivas diferentes (jogando como X ou O)
- O agente X pode conhecer estratégias que o O não conhece, e vice-versa
- Combinando ambos, criamos um agente mais completo e versátil
- O Superagente resultante pode jogar bem tanto como X quanto como O

Este módulo é tipicamente executado após o treinamento completo dos agentes,
criando o modelo final que será usado no jogo contra humanos.
"""

import pickle
from pathlib import Path
import copy
from typing import Dict, Tuple


def mesclar_tabelas_q(caminho_agente_x: str, caminho_agente_o: str, caminho_saida: str):
    """
    Mescla as Tabelas Q de dois agentes treinados para criar um Superagente.

    Este processo combina o conhecimento de ambos os agentes de forma inteligente:
    1. Carrega as Tabelas Q de ambos os agentes
    2. Começa com a tabela do Agente X como base
    3. Adiciona estados que só o Agente O conhece
    4. Para estados compartilhados, mantém o maior valor Q (melhor conhecimento)
    5. Salva o resultado como um novo modelo (Superagente)

    A estratégia de resolução de conflitos é simples mas eficaz: quando ambos
    os agentes conhecem o mesmo estado e ação, mantemos o maior valor Q, assumindo
    que valores maiores indicam melhor conhecimento sobre aquela situação.

    Args:
        caminho_agente_x: Caminho do arquivo .pkl contendo a Tabela Q do Agente X.
            Exemplo: "modelos_treinados/agente_x_final_3x3.pkl"
        caminho_agente_o: Caminho do arquivo .pkl contendo a Tabela Q do Agente O.
            Exemplo: "modelos_treinados/agente_o_final_3x3.pkl"
        caminho_saida: Caminho onde o Superagente mesclado será salvo.
            Exemplo: "modelos_treinados/superagente_final_3x3.pkl"

    Note:
        - Se os arquivos não existirem, o processo será interrompido com mensagem de erro
        - O diretório de saída será criado automaticamente se não existir
        - O processo exibe estatísticas detalhadas sobre a mesclagem

    Example:
        >>> mesclar_tabelas_q(
        ...     "modelos_treinados/agente_x_final_3x3.pkl",
        ...     "modelos_treinados/agente_o_final_3x3.pkl",
        ...     "modelos_treinados/superagente_final_3x3.pkl"
        ... )
    """
    print("\n" + "="*50)
    print("💎 INICIANDO A FUSÃO DE CONHECIMENTO DOS AGENTES 💎")
    print("="*50)

    # --- FASE 1: CARREGAR AS MEMÓRIAS (TABELAS Q) ---
    try:
        # Carrega a Tabela Q do Agente X
        with open(caminho_agente_x, 'rb') as arquivo:
            dados_x = pickle.load(arquivo)
            # Verifica se os dados estão em um formato especial (dicionário com chave 'q_table')
            # ou se são diretamente a tabela Q. Isso garante compatibilidade com diferentes formatos.
            tabela_q_x = dados_x.get('q_table', dados_x) if isinstance(dados_x, dict) else dados_x
        print(f"✅ Memória do Agente X carregada: {len(tabela_q_x):,} estados conhecidos.")

        # Carrega a Tabela Q do Agente O
        with open(caminho_agente_o, 'rb') as arquivo:
            dados_o = pickle.load(arquivo)
            # Mesma verificação de formato para o Agente O
            tabela_q_o = dados_o.get('q_table', dados_o) if isinstance(dados_o, dict) else dados_o
        print(f"✅ Memória do Agente O carregada: {len(tabela_q_o):,} estados conhecidos.")

    except FileNotFoundError as erro:
        print(f"❌ ERRO: Arquivo de modelo não encontrado: {erro}.")
        print("   Verifique se os caminhos dos arquivos estão corretos.")
        return
    except (KeyError, TypeError) as erro:
        print(f"❌ ERRO: O formato dos arquivos .pkl é inesperado: {erro}")
        print("   Verifique como os dados foram salvos pelos agentes.")
        return

    # --- FASE 2: PROCESSO DE MESCLAGEM ---
    print("\nIniciando o processo de mesclagem...")
    
    # Começa com uma cópia profunda da tabela do Agente X como base
    # Isso preserva todo o conhecimento do Agente X
    tabela_q_mesclada: Dict[Tuple, Dict[int, float]] = copy.deepcopy(tabela_q_x)
    
    # Contadores para estatísticas da mesclagem
    conflitos_resolvidos = 0
    estados_novos_adicionados = 0
    acoes_novas_adicionadas = 0

    # Itera sobre todos os estados conhecidos pelo Agente O
    for estado_o, acoes_o in tabela_q_o.items():
        # Caso 1: Estado novo (só o Agente O conhece)
        # Adiciona o estado completo com todas suas ações
        if estado_o not in tabela_q_mesclada:
            tabela_q_mesclada[estado_o] = acoes_o
            estados_novos_adicionados += 1
        else:
            # Caso 2: Estado compartilhado (ambos conhecem)
            # Precisamos mesclar as ações individualmente
            for acao_o, valor_q_o in acoes_o.items():
                # Caso 2a: Ação nova (só o Agente O conhece esta ação neste estado)
                if acao_o not in tabela_q_mesclada[estado_o]:
                    tabela_q_mesclada[estado_o][acao_o] = valor_q_o
                    acoes_novas_adicionadas += 1
                else:
                    # Caso 2b: Conflito (ambos conhecem esta ação)
                    # Resolve mantendo o maior valor Q (assumindo que é melhor conhecimento)
                    valor_q_existente = tabela_q_mesclada[estado_o][acao_o]
                    if valor_q_o > valor_q_existente:
                        tabela_q_mesclada[estado_o][acao_o] = valor_q_o
                        conflitos_resolvidos += 1
    
    print("✅ Fusão concluída!")

    # --- FASE 3: EXIBIR ESTATÍSTICAS DA MESCLAGEM ---
    print("\n--- ESTATÍSTICAS DA FUSÃO ---")
    print(f"Estados únicos no Agente X: {len(tabela_q_x):,}")
    print(f"Estados únicos no Agente O: {len(tabela_q_o):,}")
    print("-" * 30)
    print(f"Estados que só o Agente O conhecia: {estados_novos_adicionados:,}")
    print(f"Ações novas aprendidas em estados compartilhados: {acoes_novas_adicionadas:,}")
    print(f"Conflitos de opinião resolvidos (mantendo a melhor nota): {conflitos_resolvidos:,}")
    print("-" * 30)
    print(f"Total de estados no Superagente final: {len(tabela_q_mesclada):,}")

    # --- FASE 4: SALVAR O SUPERAGENTE ---
    caminho_arquivo_saida = Path(caminho_saida)
    # Cria o diretório se não existir
    caminho_arquivo_saida.parent.mkdir(parents=True, exist_ok=True)
    
    # Salva a tabela Q mesclada em formato pickle
    with open(caminho_arquivo_saida, 'wb') as arquivo:
        pickle.dump(tabela_q_mesclada, arquivo)

    print(f"\n💾 Superagente salvo com sucesso em: {caminho_arquivo_saida}")
    print("="*50 + "\n")


# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    """
    Ponto de entrada do módulo quando executado diretamente.

    Quando executado como script, mescla automaticamente os modelos finais
    dos agentes X e O para criar o Superagente final.
    """
    # Define os caminhos dos arquivos de modelo
    pasta_modelos = Path("modelos_treinados")
    dimensao = 3  # Dimensão do tabuleiro (3x3)
    
    caminho_x = pasta_modelos / f"agente_x_final_{dimensao}x{dimensao}.pkl"
    caminho_o = pasta_modelos / f"agente_o_final_{dimensao}x{dimensao}.pkl"
    caminho_final = pasta_modelos / f"superagente_final_{dimensao}x{dimensao}.pkl"
    
    # Executa a mesclagem
    mesclar_tabelas_q(str(caminho_x), str(caminho_o), str(caminho_final))
