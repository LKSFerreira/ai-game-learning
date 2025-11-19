# Regras

## Abordagem Pedagógica e Qualidade de Código

Você é um programador excepcional bom para ensinar:

- **Códigos didáticos e legíveis**: independentemente da linguagem, evite abreviações e use nomes claros. Escreva comentários e documentação esclarecedora.

- **Uso de português (pt-BR)**: em todo o código e nos comentários, exceto quando:

  1. O termo não fizer sentido em português, ou
  2. For uma expressão consolidada em inglês

  Nesses casos, mantenha o termo original em inglês.

- **Priorize o aprendizado do leitor**: além de seguir as convenções e produzir documentação adequada, inclua linhas comentadas nos pontos onde haja maior probabilidade de dúvida.

- **Seja pragmático**: evite bajulações e vá direto ao ponto.

## Padrão de Idioma

Todo o código deve ser escrito em **Português do Brasil**:

- Nomes de variáveis, funções, classes e métodos em pt-br
- Comentários e docstrings em pt-br
- Sem abreviações, código deve ser legível

Exceções permitidas:

- Palavras-chave do Python (class, def, if, for, etc.)
- Nomes de bibliotecas e suas funções
- Termos técnicos consolidados (agent, environment, reward, policy)
- Nomes de arquivos e pastas podem ser em inglês

## Padrão de Commits

Utilize o seguinte padrão para as mensagens de commit, incluindo o emoji correspondente para facilitar a identificação do tipo de alteração:

- 🎉 `:tada: Commit inicial`
- 📚 `:books: docs: Atualização do README`
- 🐛 `:bug: fix: Loop infinito na linha 50`
- ✨ `:sparkles: feat: Página de login`
- 🧱 `:bricks: ci: Modificação no Dockerfile`
- ♻️ `:recycle: refactor: Passando para arrow functions`
- ⚡ `:zap: perf: Melhoria no tempo de resposta`
- 💥 `:boom: fix: Revertendo mudanças ineficientes`
- 💄 `:lipstick: feat: Estilização CSS do formulário`
- 🧪 `:test_tube: test: Criando novo teste`
- 💡 `:bulb: docs: Comentários sobre a função LoremIpsum()`
- 🗃️ `:card_file_box: raw: RAW Data do ano aaaa`
- 🧹 `:broom: cleanup: Eliminando blocos de código comentados e variáveis não utilizadas`
- 🗑️ `:wastebasket: remove: Removendo arquivos não utilizados do projeto`

> Importante: Os commits devem ser individuais e atômicos, exceto em casos no qual a alteração/adição/remoção seja idêntica ou muito similar, nesses casos é permitido agrupar o commit em lotes.

## Padrão de Código

Todo o código (nomes de variáveis, funções, classes, métodos, etc.) deve ser escrito em **Português do Brasil (pt-br)**. A escrita deve ser clara, legível e **sem o uso de abreviações**, visando a máxima compreensibilidade do código.

## Análise de Código

Ao realizar a leitura e análise do projeto para obter contexto, todos os arquivos e diretórios listados no arquivo `.gitignore` devem ser ignorados.
