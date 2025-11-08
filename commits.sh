#!/bin/bash

# Commit 1: Quiz Feature
echo "Criando commit para a funcionalidade de quiz..."
git add index.html script.js style.css fase-1/perguntas_fase_1.json fase-2/perguntas_fase_2.json
git commit -m "✨ :sparkles: feat: Adiciona a funcionalidade de quiz com HTML, CSS e JS"

# Commit 2: Q-Table Visualization Tool
echo "Criando commit para a ferramenta de visualização da Q-table..."
git add q-table.py
git commit -m "✨ :sparkles: feat: Adiciona script para visualização da Q-table"

# Commit 3: Project Documentation
echo "Criando commit para a documentação do projeto..."
git add README.md diretrizes.md fase-1/fase-1.md fase-2/fase-2.md
git commit -m "📚 :books: docs: Adiciona e atualiza a documentação do projeto"

# Commit 4: Project Dependencies
echo "Criando commit para as dependências do projeto..."
git add requirements.txt
git commit -m "🧱 :bricks: ci: Adiciona o arquivo de dependências requirements.txt"

# Commit 5: Tic-Tac-Toe AI - Core
echo "Criando commit para o núcleo da IA do Jogo da Velha..."
git add fase-2/jogo_da_velha/agente.py fase-2/jogo_da_velha/ambiente.py
git commit -m "✨ :sparkles: feat: Implementa o núcleo da IA para o Jogo da Velha (Agente e Ambiente)"

# Commit 6: Tic-Tac-Toe AI - Training and Interaction
echo "Criando commit para a interface de treino e jogo da IA do Jogo da Velha..."
git add fase-2/jogo_da_velha/treinador.py fase-2/jogo_da_velha/jogar.py
git commit -m "✨ :sparkles: feat: Adiciona a interface de treino e jogo para a IA do Jogo da Velha"

# Commit 7: Tic-Tac-Toe AI - Visualization
echo "Criando commit para o visualizador de estatísticas da IA do Jogo da Velha..."
git add fase-2/jogo_da_velha/visualizador.py
git commit -m "✨ :sparkles: feat: Adiciona o visualizador de estatísticas de treinamento para o Jogo da Velha"

echo "Script de commits concluído!"
