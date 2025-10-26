# 🧠 Fase 1: Fundamentos de Inteligência Artificial

## 🎯 O que é Inteligência Artificial?

### A Definição Mais Simples

**Inteligência Artificial (IA)** é fazer computadores realizarem tarefas que normalmente requerem inteligência humana. Coisas como:[4][5]
- Reconhecer rostos em fotos
- Entender quando você fala com a Alexa
- Jogar xadrez
- Dirigir um carro (carros autônomos)

Pense na IA como o **conceito geral**: "máquinas que pensam".[6][1]

---

## 📦 IA, Machine Learning e Deep Learning: A Hierarquia

Aqui está a parte que confunde todo mundo! Vou usar uma analogia visual:

### 🪆 A Boneca Russa

Imagine bonecas russas (aquelas que ficam uma dentro da outra):[2][4]

```
┌─────────────────────────────────────────┐
│  INTELIGÊNCIA ARTIFICIAL (IA)          │  ← A boneca maior (conceito geral)
│  ┌─────────────────────────────────┐   │
│  │  MACHINE LEARNING (ML)          │   │  ← Boneca do meio (subcampo da IA)
│  │  ┌─────────────────────────┐    │   │
│  │  │  DEEP LEARNING (DL)     │    │   │  ← Boneca menor (subcampo do ML)
│  │  │                         │    │   │
│  │  │  (Redes Neurais)        │    │   │
│  │  └─────────────────────────┘    │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Traduzindo:**
- **IA** = O todo (fazer máquinas pensarem)
- **ML** = Uma forma de fazer IA (fazer máquinas **aprenderem** com dados)
- **DL** = Uma forma avançada de ML (usar **redes neurais** inspiradas no cérebro humano)[7][2]

### 🔍 As Diferenças na Prática

| Conceito | O que é? | Exemplo no Mundo Real |
|----------|----------|----------------------|
| **IA** | Máquinas que simulam inteligência | Um robô que joga xadrez usando regras programadas[4] |
| **Machine Learning** | Máquinas que **aprendem** com exemplos | Netflix sugere filmes baseado no que você assistiu[7][8] |
| **Deep Learning** | ML usando redes neurais complexas | Reconhecimento facial do seu celular[7][4] |

***

## 🎓 Machine Learning: O Aprendizado com Dados

### Como Funciona?

Imagine ensinar uma criança a diferenciar gatos de cachorros:[2][7]

**Método Tradicional (Programação):**
- Você teria que escrever milhares de regras: "Se tem orelhas pontudas E bigodes E mia = gato"
- Impossível cobrir todos os casos!

**Método Machine Learning:**
- Você mostra **milhares de fotos** de gatos e cachorros
- O computador **aprende sozinho** os padrões que diferenciam um do outro
- Depois, consegue identificar animais que nunca viu antes![4][2]

### Os 3 Tipos de ML

1. **Supervisionado:** Você dá as respostas (fotos com etiquetas "gato" ou "cachorro")
2. **Não-Supervisionado:** O computador encontra padrões sozinho
3. **Aprendizado por Reforço (RL):** O que vamos usar! Explicarei já já[3][8]

***

## 🧬 Deep Learning: Imitando o Cérebro

**Deep Learning** usa **Redes Neurais Artificiais**, inspiradas nos neurônios do cérebro humano.[2][4]

### Por que "Deep" (Profundo)?

Porque tem **muitas camadas** de neurônios artificiais processando informações:[7][2]

```
Imagem → [Camada 1: detecta bordas] → [Camada 2: detecta formas] → 
        [Camada 3: detecta partes] → [Camada 4: reconhece o objeto]
```

**Diferenças do ML "normal":**
- Precisa de **muito mais dados** (milhões de exemplos)
- Precisa de **mais poder computacional** (GPUs)
- Aprende de forma **mais autônoma** (menos intervenção humana)[9][7][2]

**Usaremos Deep Learning na Fase 4** (Ragnarok), quando precisarmos reconhecer monstros na tela.[7][4]

---

## 🎮 Reinforcement Learning: O Coração do Nosso Projeto

Agora a parte **mais importante** para nós! **Reinforcement Learning (RL)** ou **Aprendizado por Reforço**.[8][3]

### 🐕 A Analogia Perfeita: Adestramento de Cachorro

Imagine que você quer ensinar um cachorro a sentar:[10][8]

1. **Você dá um comando:** "Senta!"
2. **O cachorro tenta algo:** Ele pode sentar, deitar ou ignorar
3. **Você dá feedback:**
   - ✅ Sentou? **BISCOITO!** (recompensa)
   - ❌ Não sentou? **Nada** (sem recompensa ou leve repreensão)
4. **O cachorro aprende:** Após muitas tentativas, ele associa "sentar" com "ganhar biscoito"
5. **Resultado:** O cachorro aprende a sentar sempre que você pede![3][8]

**Reinforcement Learning funciona EXATAMENTE assim!**[10][3]

### 🎯 RL em uma Frase

> **"Aprendizado através de tentativa e erro, guiado por recompensas e punições"**[8][3]

Não damos respostas prontas à IA. Ela **tenta, erra, acerta, e aprende sozinha** qual estratégia maximiza as recompensas![11][8]

***

## 🧩 Os 5 Componentes Fundamentais do RL

Todo sistema de RL tem exatamente 5 elementos:[12][11][8]

### 1️⃣ Agente (Agent)

**O que é:** O "cérebro" da IA. Quem toma as decisões.[11][8]

**No nosso caso:**
- **Fase 2:** O algoritmo que decide onde jogar no Jogo da Velha
- **Fase 4:** A IA que decide se deve atacar, curar ou fugir no Ragnarok

### 2️⃣ Ambiente (Environment)

**O que é:** O "mundo" onde o agente vive e age.[11][8]

**No nosso caso:**
- **Fase 2:** O tabuleiro do Jogo da Velha (9 casas)
- **Fase 4:** O jogo Ragnarok (mapa, monstros, personagem)

### 3️⃣ Estado (State)

**O que é:** A "foto" da situação atual do ambiente.[12][11]

**No nosso caso:**
- **Fase 2:** Posição das peças X e O no tabuleiro
- **Fase 4:** HP do personagem, posição dos monstros, localização no mapa

### 4️⃣ Ação (Action)

**O que é:** O que o agente pode **fazer** em resposta ao estado.[8][11]

**No nosso caso:**
- **Fase 2:** Escolher uma casa vazia (1-9) para jogar
- **Fase 4:** Atacar, mover, usar poção, usar habilidade

### 5️⃣ Recompensa (Reward)

**O que é:** O "feedback" que o agente recebe após cada ação. Pode ser positivo (+) ou negativo (-).[10][11][8]

**No nosso caso:**
- **Fase 2:** 
  - +10 se ganhou o jogo
  - -10 se perdeu
  - 0 se empatou ou o jogo continua
- **Fase 4:**
  - +50 se matou um monstro
  - -100 se morreu
  - +5 se coletou um item

***

## 🔄 O Ciclo do Reinforcement Learning

Aqui está como tudo se conecta:[12][11][8]

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  1. AGENTE observa o ESTADO do AMBIENTE        │
│         ↓                                       │
│  2. AGENTE escolhe uma AÇÃO                    │
│         ↓                                       │
│  3. AMBIENTE muda para um novo ESTADO          │
│         ↓                                       │
│  4. AMBIENTE dá uma RECOMPENSA ao AGENTE       │
│         ↓                                       │
│  5. AGENTE aprende e volta ao passo 1          │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Esse ciclo se repete milhares ou milhões de vezes!** A cada repetição, o agente aprende um pouquinho mais sobre quais ações levam às melhores recompensas.[3][11][8][10]

***

## 🎲 O que é "Treinar" uma IA?

Você perguntou sobre o que é um **algoritmo de treinamento**. Vou explicar de forma super simples:

### Sem Treinamento

Imagine um bebê recém-nascido tentando andar:
- Ele não sabe qual músculo mover
- Cai, tropeça, não vai a lugar nenhum
- **Resultado:** Aleatório, caótico[3]

### Com Treinamento

O bebê tenta andar **milhares de vezes**:
- Cada vez que cai, o cérebro dele aprende: "Isso não funcionou"
- Cada vez que dá um passo, o cérebro reforça: "Isso funcionou!"
- Após meses, ele anda perfeitamente[8][10]

### No RL

**Treinar** significa fazer o agente **repetir o ciclo** (estado → ação → recompensa) muitas vezes até que ele descubra a **melhor estratégia** (chamada de **Política**):[13][11][8]

- **Início:** A IA joga aleatoriamente (igual o bebê)
- **Durante o treino:** A IA experimenta tudo, ganha e perde muito
- **Final:** A IA sabe exatamente o que fazer em cada situação para maximizar as recompensas[3][8]

**Analogia:** É como jogar um videogame 1 milhão de vezes até decorar todos os segredos e virar o melhor jogador do mundo![11][12]

***

## 🎯 Conceitos Extras Importantes

### Política (Policy)

É o "manual de instruções" que o agente desenvolve:[13][11][8]
- **Política:** "Se meu HP estiver abaixo de 30%, use poção"
- **Política:** "Se há um monstro fraco à esquerda, ataque-o"

O objetivo do treinamento é descobrir a **política ótima**.[11][8]

### Exploração vs. Exploração (Exploration vs. Exploitation)

Dilema que o agente enfrenta:[10][8]
- **Exploração:** Testar ações novas para descobrir recompensas desconhecidas
- **Exploração (Exploitation):** Usar ações conhecidas que já dão boas recompensas

É como escolher restaurante: arriscar um novo ou ir no seu favorito?[8]

***

## 📝 Resumo da Fase 1

### Você aprendeu:

✅ **IA** = Máquinas que simulam inteligência  
✅ **ML** = Subcampo da IA que aprende com dados  
✅ **DL** = Subcampo do ML que usa redes neurais profundas  
✅ **RL** = Tipo de ML que aprende por tentativa e erro com recompensas  

### Os 5 Pilares do RL:
1. **Agente:** Quem decide
2. **Ambiente:** Onde acontece tudo
3. **Estado:** A situação atual
4. **Ação:** O que o agente faz
5. **Recompensa:** O feedback (+ ou -)

### O Processo:
**Treinar** = Repetir o ciclo (observar → agir → receber recompensa) até descobrir a melhor estratégia![3][11][8]

***

# Vídeo aula: Fundamentos de Inteligência Artificial

<a href="https://youtu.be/Z4S0Cz2qJjk">
  <img src="https://media.discordapp.net/attachments/1085266518151016468/1432108754224152776/image.png?ex=68ffdab6&is=68fe8936&hm=d762a1518c857adf97954c7641c465cb7d218bf54afcfc456355f8efcf1cbc8b" width="400" height="200" />
</a>


**Referencias:**

[1 - IBM: AI vs Machine Learning vs Deep Learning vs Neural Networks](https://www.ibm.com/think/topics/ai-vs-machine-learning-vs-deep-learning-vs-neural-networks/)

[2 - AWS: Diferença entre Machine Learning e Deep Learning](https://aws.amazon.com/compare/the-difference-between-machine-learning-and-deep-learning/)

[3 - Zendesk: O que é Reinforcement Learning?](https://www.zendesk.com.br/blog/reinforcement-learning/)

[4 - Coursera: Guia para iniciantes sobre IA vs ML vs Deep Learning](https://www.coursera.org/articles/ai-vs-deep-learning-vs-machine-learning-beginners-guide)

[5 - Columbia Engineering: AI vs Machine Learning](https://ai.engineering.columbia.edu/ai-vs-machine-learning/)

[6 - TechTarget: Diferenças entre AI, Machine Learning e Deep Learning](https://www.techtarget.com/searchenterpriseai/tip/AI-vs-machine-learning-vs-deep-learning-Key-differences)

[7 - PUCPR: Machine Learning x Deep Learning](https://posdigital.pucpr.br/blog/machine-learning-deep-learning)

[8 - AWS: O que é Reinforcement Learning?](https://aws.amazon.com/pt/what-is/reinforcement-learning/)

[9 - Google Cloud: Deep Learning vs Machine Learning](https://cloud.google.com/discover/deep-learning-vs-machine-learning)

[10 - OVHcloud: O que é Reinforcement Learning?](https://www.ovhcloud.com/pt/learn/what-is-reinforcement-learning/)

[11 - DataCamp: Reinforcement Learning com Python](https://www.datacamp.com/pt/tutorial/reinforcement-learning-with-gymnasium)

[12 - Ultralytics: Glossário de Reinforcement Learning](https://www.ultralytics.com/pt/glossary/reinforcement-learning)

[13 - DSAcademy: Aplicações de IA com Reinforcement Learning](https://blog.dsacademy.com.br/aplicacoes-de-inteligencia-artificial-com-reinforcement-learning/)

[14 - LinkedIn Pulse: Conceitos básicos de Reinforcement Learning](https://pt.linkedin.com/pulse/conceitos-basicos-de-reinforcement-learning-christiano-faig)

[15 - UFSC: Apostila sobre Reinforcement Learning (PDF)](http://www.inf.ufsc.br/~mauro.roisenberg/ine5377/Cursos-ICA/TAIC-apostila_RL.pdf)

[16 - NVIDIA: Diferenças entre IA, ML e Deep Learning](https://blog.nvidia.com.br/blog/qual-e-a-diferenca-entre-inteligencia-artificial-machine-learning-e-deep-learning/)

[17 - DSAcademy: IA x ML x Deep Learning x LLM](https://blog.dsacademy.com.br/ia-x-machine-learning-x-deep-learning-x-llm/)

[18 - UFSC: Introdução ao Reinforcement Learning (PDF)](http://www.inf.ufsc.br/~mauro.roisenberg/ine5377/Cursos-ICA/TAIC-RL-Introducao%20(1aula)%20.pdf)

[19 - IBM Brasil: Reinforcement Learning](https://www.ibm.com/br-pt/think/topics/reinforcement-learning)

[20 - Dataside: Diferença entre IA, ML e DL](https://www.dataside.com.br/post/diferenca-ia-ml-dl)
