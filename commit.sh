#!/bin/bash

echo "🚀 Iniciando a organização dos commits da Fase 2: Labirinto..."

# --- Bloco 1: Estrutura Inicial e Ambiente do Labirinto ---
# Este é o commit fundamental que introduz o novo projeto do labirinto.
# Ele inclui a primeira versão da classe `Labirinto` e a estrutura de pastas.
echo "✨ Adicionando e commitando a estrutura inicial e a classe Labirinto..."
git add fase_2/labirinto/ambiente.py fase_2/labirinto/__init__.py fase_2/labirinto/test/__init__.py
git commit -m "✨ feat: Cria estrutura inicial e ambiente base para o Labirinto

- Adiciona o diretório 'fase_2/labirinto' para o novo projeto.
- Implementa a classe 'Labirinto' em 'ambiente.py' com a lógica central:
  - Inicialização com matriz, ponto inicial e final.
  - Método 'executar_acao' para movimentação do agente.
  - Lógica de recompensas (-0.1 por passo, +10.0 por vitória).
  - Detecção de colisão com paredes e limites.
  - Método 'reiniciar' para começar um novo episódio.
- Adiciona docstrings e type hints iniciais."

# --- Bloco 2: Testes Unitários para o Ambiente ---
# Adiciona o arquivo de teste que valida o comportamento da classe Labirinto.
# É um passo separado para manter a implementação e o teste em commits distintos.
echo "🧪 Adicionando e commitando os testes unitários para o ambiente..."
git add fase_2/labirinto/test/test_ambiente.py
git commit -m "🧪 test: Adiciona testes unitários para a classe Labirinto

- Cria 'test_ambiente.py' para validar o comportamento do ambiente.
- Implementa testes para:
  - Inicialização correta do labirinto.
  - Movimentação válida do agente.
  - Colisão com paredes e limites do mapa.
  - Reinício do ambiente para o estado inicial.
  - Verificação da recompensa correta ao atingir o ponto final.
- Utiliza importações absolutas para compatibilidade com pytest."

# --- Bloco 3: Melhorias de Robustez e Flexibilidade ---
# Este commit agrupa as melhorias significativas que você implementou,
# tornando o ambiente muito mais poderoso e amigável.
echo "♻️ Adicionando e commitando as melhorias de robustez e flexibilidade..."
git add fase_2/labirinto/ambiente.py fase_2/labirinto/test/test_ambiente.py
git commit -m "♻️ refactor: Aprimora ambiente com suporte a WASD e validações

- **Flexibilidade de Ações:**
  - Adiciona suporte para teclas WASD (maiúsculas e minúsculas).
  - Implementa um sistema de normalização de ações para desacoplar a
    entrada do usuário da lógica interna.

- **Robustez:**
  - Adiciona validações no construtor para matrizes vazias/malformadas.
  - Adiciona validação em 'executar_acao' para rejeitar ações inválidas.

- **Melhorias de Design:**
  - A recompensa por vitória agora é dinâmica, escalando com o tamanho
    do labirinto.
  - O agente agora deixa um rastro ('•') para visualização do caminho.

- **Testes:**
  - Atualiza e expande os testes para cobrir as novas funcionalidades,
    incluindo testes para teclas WASD e validação de erros."

# --- Bloco 4: Adição do Script de Demonstração Visual ---
# Adiciona o arquivo `main.py` que serve como um ponto de entrada para
# testar e visualizar o ambiente de forma interativa no terminal.
echo "✨ Adicionando e commitando o script de demonstração visual..."
git add fase_2/labirinto/main.py fase_2/labirinto/ambiente.py
git commit -m "✨ feat: Adiciona script 'main.py' e visualizador de grade no terminal

- Cria o arquivo 'main.py' para servir como um exemplo executável
  e ponto de teste visual do ambiente.
- Implementa o método 'imprimir_labirinto' na classe Labirinto, que
  desenha uma grade formatada no console para melhor visualização.
- 'main.py' demonstra a inicialização, execução de uma sequência de
  ações e o reinício do ambiente, usando a nova visualização."

echo "✅ Processo de commit finalizado!"
echo "-------------------------------------"
echo "Verifique o status final com 'git status' e suba as mudanças com 'git push'"