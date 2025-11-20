#!/bin/bash

echo "��� Iniciando a criação dos commits..."

# --- Bloco 1: Reorganização de Pastas (Refactor) ---
echo "♻️ Organizando estrutura de pastas (fase-x -> fase_x)..."
# Stage deletions of old folders (fase-1, fase-2, fase-3)
git add -u
# Stage new folders (fase_1, fase_2, fase_3)
git add fase_1 fase_2 fase_3
git commit -m "♻️ :recycle: refactor: Reorganiza estrutura de pastas (fase-x -> fase_x)"

# --- Bloco 2: Adição dos Agentes ---
echo "✨ Adicionando estrutura de agentes..."
git add agentes
git commit -m "✨ :sparkles: feat: Adiciona estrutura inicial de agentes (Q-Learning)"

echo "✅ Processo de commit finalizado!"
echo "-------------------------------------"
echo "Verifique o status final com 'git status' e suba as mudanças com 'git push'"
