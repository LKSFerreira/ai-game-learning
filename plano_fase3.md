# Implementação do Agente Q-Learning para Labirinto (Fase 3)

## 🎯 Objetivo

Implementar um agente de Aprendizado por Reforço (Q-Learning) capaz de resolver o ambiente do Labirinto (`fase-3`). O agente deve aprender a navegar do ponto inicial até a saída, evitando paredes e otimizando o caminho.

## 📝 Contexto

Já temos:

- **Ambiente (`ambiente.py`):** Define o labirinto, estados (posições), ações (movimentos) e recompensas.
- **Jogo Manual (`jogar.py`):** Permite jogar manualmente e visualizar o labirinto.

Precisamos criar:

- **Agente (`agente.py`):** O "cérebro" que aprenderá a jogar.
- **Treinador (`treinador.py`):** Script para rodar múltiplos episódios de treinamento (sem interface gráfica) para o agente aprender.

## 🛠️ Alterações Propostas

### 1. Criar `fase-3/agente.py`

Baseado no `agente.py` do Jogo da Velha, mas adaptado:

- **Estado:** Em vez de uma tupla de 9 números (tabuleiro), o estado será uma tupla `(linha, coluna)` representando a posição do agente.
- **Ações:** Em vez de índices 0-8, as ações serão strings: `['cima', 'baixo', 'esquerda', 'direita']` (ou índices mapeados para essas strings).
- **Q-Table:** Dicionário mapeando `(linha, coluna) -> {acao: valor_q}`.

### 2. Criar `fase-3/treinador.py`

Script para gerenciar o ciclo de vida do treinamento:

- Instanciar Ambiente e Agente.
- Loop de Episódios (ex: 1000 partidas).
- Loop de Passos (dentro de cada episódio):
  - Agente escolhe ação.
  - Ambiente executa.
  - Agente recebe recompensa e atualiza Q-Table.
- Exibir estatísticas de evolução (recompensa média, passos até a saída).

### 3. Atualizar `fase-3/jogar.py` (Opcional/Futuro)

- Adicionar modo para assistir a IA jogando (carregar modelo treinado).

## ⚠️ Pontos de Atenção

- **Exploração vs Exploração:** Manter epsilon-greedy.
- **Recompensas:** O ambiente já penaliza passos (-0.1) e premia a saída. Isso deve ser suficiente para buscar o caminho mais curto.
- **Loop Infinito:** No início, o agente pode ficar andando em círculos. Precisamos limitar o número máximo de passos por episódio.

## 📋 Plano de Execução

1.  [ ] Criar `fase-3/agente.py`
2.  [ ] Criar `fase-3/treinador.py`
3.  [ ] Rodar treinamento e validar aprendizado.
