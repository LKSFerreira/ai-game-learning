#!/bin/bash

echo "🚀 Iniciando a organização dos commits..."

# --- Bloco 1: Melhorias no Processo de Treinamento ---
# Agrupamos as melhorias lógicas que fizemos no ambiente e no agente.
# A principal mudança foi a aleatorização do jogador inicial.
echo "♻️ Adicionando e commitando as melhorias no ambiente e agente..."
git add fase-2/jogo_da_velha/ambiente.py fase-2/jogo_da_velha/agente.py
git commit -m "♻️ refactor: Aleatoriza jogador inicial e aprimora lógica do agente"

# --- Bloco 2: Implementação do Treinador e Avaliador ---
# Adicionamos a funcionalidade de avaliação e a interface rica ao treinador.
echo "✨ Adicionando e commitando as funcionalidades do treinador e avaliador..."
git add fase-2/jogo_da_velha/treinador.py
git commit -m "✨ feat: Implementa avaliação pós-treino e interface rica com 'rich'"

# --- Bloco 3: Adição de Novas Ferramentas ---
# Adicionamos o script para mesclar modelos e o teste para o treinador.
echo "✨ Adicionando e commitando novas ferramentas (mesclar_modelos, test_treinador)..."
git add fase-2/jogo_da_velha/mesclar_modelos.py fase-2/jogo_da_velha/test/test_treinador.py
git commit -m "✨ feat: Adiciona script para mesclar modelos e teste de integração do treinador"

# --- Bloco 4: Limpeza de Arquivos Gerados ---
# Removemos todos os arquivos de modelos, estatísticas e gráficos que foram gerados
# durante os testes e não devem ser versionados.
echo "🧹 Adicionando e commitando a limpeza de arquivos gerados..."
git add fase-2/jogo_da_velha/estatisticas/ fase-2/jogo_da_velha/estatisticas_jogador/ fase-2/jogo_da_velha/graficos/ fase-2/jogo_da_velha/modelos/
git commit -m "🧹 cleanup: Remove arquivos de modelos e estatísticas gerados"

# --- Bloco 5: Atualização do .gitignore ---
# Atualizamos o .gitignore para que o Git ignore essas pastas no futuro.
echo "🧱 Adicionando e commitando a atualização do .gitignore..."
git add .gitignore
git commit -m "🧱 build: Atualiza .gitignore para ignorar pastas de modelos e estatísticas"


echo "✅ Processo de commit finalizado!"
echo "-------------------------------------"
echo "Verifique o status final com 'git status' e suba as mudanças com 'git push'"