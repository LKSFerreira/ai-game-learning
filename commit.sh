#!/bin/bash

echo "🚀 Iniciando a organização dos commits..."

# --- Bloco 1: Implementação do Ambiente do Jogo ---
# Refatoramos e implementamos a classe Ambiente, que define as regras do nosso mundo.
echo "✨ Adicionando e commitando o ambiente do jogo (ambiente.py)..."
git add fase-2/jogo_da_velha/ambiente.py
git commit -m "✨ feat: Implementa a classe Ambiente modular e didática com suporte a N x N"

# --- Bloco 2: Implementação do Agente Q-Learning ---
# Implementamos a classe Agente, o cérebro da nossa IA, com toda a lógica de aprendizado.
echo "✨ Adicionando e commitando o cérebro da IA (agente.py)..."
git add fase-2/jogo_da_velha/agente.py
git commit -m "✨ feat: Implementa a classe AgenteQLearning com lógica de aprendizado"

# --- Bloco 3: Adição dos Testes de Unidade ---
# Criamos os testes que validam o funcionamento isolado do Ambiente e do Agente.
echo "🧪 Adicionando e commitando os testes de unidade..."
git add fase-2/jogo_da_velha/test/
git commit -m "🧪 test: Adiciona testes de unidade para Ambiente e Agente"

# --- Bloco 4: Arquivos de Estrutura e Automação ---
# Adicionamos arquivos que ajudam na organização e automação do projeto.
echo "🧱 Adicionando e commitando arquivos de estrutura e automação..."
git add fase-2/jogo_da_velha/__init__.py
git add commit.sh
git commit -m "🧱 build: Adiciona __init__.py e script de automação de commits"


echo "✅ Processo de commit finalizado!"
echo "-------------------------------------"
echo "Verifique o status final com 'git status' e suba as mudanças com 'git push'"