#!/bin/bash

echo "🚀 Iniciando a organização dos commits das melhorias didáticas..."

# --- Bloco 1: Melhorias Didáticas no Agente ---
# Melhorias de documentação, renomeação de métodos e melhorias de legibilidade
# no módulo principal do agente e seu teste.
echo "💡 Adicionando e commitando melhorias didáticas no agente..."
git add fase-2/jogo_da_velha/agente.py fase-2/jogo_da_velha/test/test_agente.py
git commit -m "💡 docs: Melhora documentação e legibilidade do agente e seus testes

- Adiciona docstrings completas no padrão Google
- Renomeia métodos para nomes mais descritivos:
  * aprender() -> atualizar_valor_q()
  * iniciar_nova_partida() -> limpar_historico_partida()
  * registrar_jogada() -> adicionar_jogada_ao_historico()
  * aprender_com_fim_de_partida() -> processar_aprendizado_monte_carlo()
  * _obter_melhor_valor_q_do_estado() -> _obter_melhor_valor_q_futuro()
- Melhora comentários explicativos e didáticos
- Atualiza testes para refletir novos nomes de métodos"

# --- Bloco 2: Melhorias Didáticas no Ambiente ---
# Melhorias de documentação e renomeação de métodos no ambiente e seu teste.
echo "💡 Adicionando e commitando melhorias didáticas no ambiente..."
git add fase-2/jogo_da_velha/ambiente.py fase-2/jogo_da_velha/test/test_ambiente.py
git commit -m "💡 docs: Melhora documentação e legibilidade do ambiente e seus testes

- Adiciona docstrings completas no padrão Google
- Renomeia método _trocar_jogador() -> _alternar_jogador()
- Melhora comentários explicativos sobre o funcionamento
- Adiciona explicações didáticas sobre Reinforcement Learning
- Melhora nomes de variáveis para maior clareza
- Atualiza testes com melhor documentação e nomes mais descritivos"

# --- Bloco 3: Melhorias Didáticas no Treinador ---
# Melhorias de documentação no treinador e seu teste.
echo "💡 Adicionando e commitando melhorias didáticas no treinador..."
git add fase-2/jogo_da_velha/treinador.py fase-2/jogo_da_velha/test/test_treinador.py
git commit -m "💡 docs: Melhora documentação e legibilidade do treinador e seus testes

- Adiciona docstrings completas no padrão Google
- Melhora nomes de variáveis (agente_da_vez -> agente_atual, i -> indice_partida)
- Adiciona comentários explicativos sobre self-play
- Melhora explicações sobre interfaces Rich vs TQDM
- Documenta melhor o processo de treinamento e checkpoints
- Atualiza testes com melhor documentação e explicações didáticas"

# --- Bloco 4: Melhorias Didáticas em Ferramentas Auxiliares ---
# Melhorias de documentação em mesclar_modelos e jogar.
echo "💡 Adicionando e commitando melhorias didáticas em ferramentas auxiliares..."
git add fase-2/jogo_da_velha/mesclar_modelos.py fase-2/jogo_da_velha/jogar.py
git commit -m "💡 docs: Melhora documentação e legibilidade de ferramentas auxiliares

- Adiciona docstrings completas no padrão Google para mesclar_modelos.py
- Melhora explicações sobre o processo de mesclagem de agentes
- Adiciona documentação completa para jogar.py
- Explica sistema de regras dinâmicas de escolha do jogador inicial
- Melhora comentários explicativos sobre a experiência do usuário
- Adiciona type hints onde faltavam"

echo "✅ Processo de commit finalizado!"
echo "-------------------------------------"
echo "Verifique o status final com 'git status' e suba as mudanças com 'git push'"
