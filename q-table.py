import matplotlib.pyplot as plt
import numpy as np

def desenhar_qtable(tabuleiro, q_values, titulo="Visualização da Q-Table", salvar=False, nome_arquivo="qtable_visual.png"):
    """
    Desenha um tabuleiro 3x3 do Jogo da Velha com os valores de Q (Q-values) sobrepostos nas células.

    Parâmetros:
    - tabuleiro: lista de 9 elementos representando o estado atual ("X", "O" ou "_")
    - q_values: lista de 9 valores numéricos correspondentes aos Q-values das ações
    - titulo: título do gráfico (opcional)
    - salvar: se True, salva o gráfico como imagem PNG
    - nome_arquivo: nome do arquivo a ser salvo (opcional)
    """

    # Verificações básicas
    if len(tabuleiro) != 9 or len(q_values) != 9:
        raise ValueError("O tabuleiro e os Q-values devem ter exatamente 9 elementos.")

    # Converter para array 3x3
    tabuleiro_2d = np.array(tabuleiro).reshape(3, 3)
    q_values_2d = np.array(q_values).reshape(3, 3)

    # Cria o heatmap (cores de acordo com magnitude do Q)
    fig, ax = plt.subplots(figsize=(5, 5))
    im = ax.imshow(q_values_2d, cmap='RdYlGn', vmin=min(q_values), vmax=max(q_values))

    # Títulos e ajustes visuais
    plt.title(titulo, fontsize=14, pad=15)
    ax.set_xticks([])
    ax.set_yticks([])

    # Desenhar linhas do tabuleiro
    for i in range(1, 3):
        ax.axhline(i - 0.5, color='black', linewidth=2)
        ax.axvline(i - 0.5, color='black', linewidth=2)

    # Inserir texto (Q-values e símbolos do tabuleiro)
    for i in range(3):
        for j in range(3):
            simbolo = tabuleiro_2d[i, j]
            valor_q = q_values_2d[i, j]
            texto = f"{simbolo if simbolo != '_' else ''}\n{valor_q:.2f}" if np.isfinite(valor_q) else f"{simbolo}\n—"
            ax.text(j, i, texto, ha='center', va='center', color='black', fontsize=12, fontweight='bold')

    # Barra de cores
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Valor Q', rotation=270, labelpad=15)

    plt.tight_layout()

    # Salvar imagem se desejado
    if salvar:
        plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')

    plt.show()

# Exemplo de uso:
if __name__ == "__main__":
    tabuleiro = [
        '_', '_', '_',
        '_', '_', '_',
        '_', '_', '_'
    ]

    q_values = [
        float('-inf'), 0.12, 0.05,
        -0.03, float('-inf'), 0.08,
        float('-inf'), 0.02, 0.15
    ]

    desenhar_qtable(tabuleiro, q_values, titulo="Q-Table - Estado Parcial do Jogo")
