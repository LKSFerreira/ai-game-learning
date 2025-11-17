#!/bin/bash

echo "🚀 Iniciando a organização dos commits da Fase 2: Labirinto..."

# --- Bloco 1: Adição do Gerador de Labirintos ---
# Introduzimos a capacidade de criar labirintos aleatórios.
# Esta é uma funcionalidade fundamental e merece seu próprio commit,
# junto com os testes que garantem sua corretude.
echo "✨ Adicionando e commitando o gerador de labirintos e seus testes..."
git add fase_2/labirinto/gerador_labirinto.py fase_2/labirinto/test/test_gerador_labirinto.py
git commit -m "✨ feat: Adiciona gerador de labirintos aleatórios com testes

- Implementa 'gerador_labirinto.py' usando o algoritmo Recursive Backtracking
  para criar labirintos perfeitos (sem loops e totalmente conectados).
- A função 'gerar_labirinto' produz uma matriz compatível com a classe Labirinto.

- Adiciona 'test_gerador_labirinto.py' para validar as propriedades do gerador:
  - Verifica as dimensões corretas da matriz resultante.
  - Garante que as bordas externas são sempre paredes.
  - Confirma que o labirinto gerado é totalmente conectado (sem ilhas)."

# --- Bloco 2: Consolidação dos Scripts de Demonstração ---
# Refatoramos os scripts de execução, unificando `main.py` e `run.py`
# no novo e mais completo `demonstracao_terminal.py`.
echo "♻️ Adicionando e commitando a refatoração dos scripts de demonstração..."
git add fase_2/labirinto/demonstracao_terminal.py fase_2/labirinto/main.py
git commit -m "♻️ refactor: Unifica scripts de execução em 'demonstracao_terminal.py'

- Cria 'demonstracao_terminal.py' que integra a geração dinâmica do
  labirinto com um modo de jogo interativo no terminal.
- Adiciona a classe 'EstatisticasJogo' para rastrear movimentos e tempo.
- Implementa comandos como 'stats' e 'limpar' para melhor UX.
- Remove o antigo 'main.py', cuja funcionalidade foi absorvida."

# --- Bloco 3: Implementação do Jogo Gráfico Interativo ---
# Este é o grande salto: a criação do jogo gráfico com Pygame.
# Inclui o próprio jogo e os testes que validam sua lógica.
echo "✨ Adicionando e commitando o jogo gráfico interativo com Pygame..."
git add fase_2/labirinto/jogar.py fase_2/labirinto/test/test_jogar.py
git commit -m "✨ feat: Implementa jogo gráfico interativo com Pygame em 'jogar.py'

- Cria a classe 'JogoGrafico' para gerenciar a janela e o loop de jogo.
- Renderiza o labirinto, agente e saída na tela.
- Implementa movimento contínuo do jogador ao segurar as teclas (WASD/Setas).
- Adiciona um rastro visual ('pegadas') para o caminho percorrido.
- Implementa ajuste dinâmico do tamanho do labirinto para caber na tela do usuário.

- Adiciona 'test_jogar.py' com testes para a lógica do jogo:
  - Testa a função de cálculo de dimensões ideais.
  - Utiliza 'pytest-mock' para simular o Pygame e testar a lógica de
    movimento sem depender de uma interface gráfica."

# --- Bloco 4: Atualização de Dependências e Correções de Importação ---
# Um commit de manutenção que agrupa as mudanças de configuração e as
# correções de importação que fizemos para garantir a compatibilidade com pytest.
echo "🧱 Adicionando e commitando atualização de dependências e correções..."
git add requirements.txt fase_2/labirinto/jogar.py fase_2/labirinto/test/test_jogar.py
git commit -m "🧱 build: Atualiza dependências e corrige importações relativas

- Adiciona 'pygame' e 'pytest-mock' ao 'requirements.txt'.
- Corrige as importações em 'jogar.py' e 'test_jogar.py' para usar
  importações relativas explícitas (com '.') e absolutas, garantindo
  que os módulos funcionem tanto na execução direta quanto via pytest."

# --- Bloco 5: Limpeza do Script de Commit Antigo ---
# Finalmente, atualizamos o próprio script de commit.
echo "🧹 Adicionando e commitando a limpeza do script de commit..."
git add commit.sh
git commit -m "🧹 cleanup: Simplifica e atualiza o script de commit"


echo "✅ Processo de commit finalizado!"
echo "-------------------------------------"
echo "Verifique o status final com 'git status' e suba as mudanças com 'git push'"