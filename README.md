# 🧠 AI Game Learning — Do Zero à IA Jogadora

## 🎯 Objetivo

Aprender **Inteligência Artificial** do zero absoluto até criar uma IA capaz de **jogar Ragnarok Online Brasil (bRO)**.
O foco é na prática — construir, testar, errar e evoluir — entendendo a teoria enquanto aplicamos cada conceito.

## 🚀 Metodologia

Aprendizado incremental, baseado em projetos reais:

- 🧩 Conceito antes de código
- 🔁 Cada fase constrói sobre a anterior
- 🤖 Ênfase em **Aprendizado por Reforço (Reinforcement Learning)**
- 🧪 Código primeiro, teoria aplicada
- 🌐 Todo o código será posteriormente **reescrito em JavaScript** como reforço de aprendizado

## 🧭 Fases do Projeto

| Fase                                     | Descrição                                                                      | Status                    |
| ---------------------------------------- | ------------------------------------------------------------------------------ | ------------------------- |
| **0. Preparação do Ambiente**            | Configuração de Python, Git e dependências                                     | ✅ Concluída (26/10/2025) |
| **1. Fundamentos de IA**                 | Conceitos essenciais de IA, ML, DL e RL                                         | ⏳ Em andamento           |
| **2. Jogo da Velha (Q-Learning)**        | Implementação do algoritmo Q-Learning com self-play em um ambiente de lógica   | 🔜 Próxima                |
| **3. Labirinto Simples (RL)**            | Agente aprendendo a encontrar a saída de um labirinto (ambiente de grade)        | 🔜 Planejada              |
| **4. Dino do Chrome (Visão)**            | IA reativa que joga o Dino do Chrome usando captura de tela com OpenCV         | 🔜 Planejada              |
| **5. Flappy Bird (Visão + Física)**      | IA que joga Flappy Bird, exigindo timing e previsão simples                      | 🔜 Planejada              |
| **6. Breakout/Pong (Gymnasium + DQN)**   | Treinando um agente com Deep Q-Networks em um ambiente de simulação pronto     | 🔜 Planejada              |
| **7. Ragnarok Online (Projeto Final)**   | Projeto final: IA jogando Ragnarok com Visão Computacional e integração AHK    | 🔜 Futura                 |

## 🧰 Tecnologias Utilizadas

**Linguagem Principal:** Python 3.x
**Reforço de Estudo:** JavaScript (versões reescritas dos projetos)

**Ferramentas e Bibliotecas:**

- 🧮 **NumPy** – Computação numérica e manipulação de matrizes
- 📊 **Matplotlib** – Visualização e análise dos resultados
- 👁️ **OpenCV** – Visão computacional (captura e processamento de tela)
- 🧠 **TensorFlow / PyTorch** - Implementação de redes neurais (futuro)
- 🖱️ **PyAutoGUI / AutoHotkey (AHK)** – Automação de interface e comandos no jogo
- 🎮 **Gymnasium** – Ambientes de simulação e treinamento (futuro)

**Controle de Versão:** Git + GitHub

## 📅 Progresso Atual

```md
- [x] **Fase 0: Ambiente Configurado**
  - Python + ambiente virtual
  - Dependências básicas instaladas
  - Estrutura de pastas definida
  - Diretrizes de código e commits documentadas

- [ ] **Fase 1: Fundamentos Teóricos**
  - Conceitos de IA, ML, DL e RL
  - Componentes: Agente, Ambiente, Estado, Ação, Recompensa

- [ ] **Fase 2: Jogo da Velha (Q-Learning)**
  - Implementação do algoritmo do zero
  - Treinamento com autoaprendizado (self-play)
  - Visualização da evolução do agente

- [ ] **Fase 3: Labirinto Simples (RL)**
  - Desenvolvimento do ambiente de grade
  - Lógica do agente para explorar o ambiente

- [ ] **Fase 4: Dino do Chrome (Visão)**
  - Captura e interpretação de tela em tempo real
  - Detecção de obstáculos e tomada de decisão

- [ ] **Fase 5: Flappy Bird (Visão + Física)**
  - Detecção de canos e do personagem
  - Lógica de decisão baseada em timing

- [ ] **Fase 6: Breakout/Pong (Gymnasium + DQN)**
  - Implementação de uma Rede Neural Profunda
  - Treinamento do agente usando Deep Q-Learning

- [ ] **Fase 7: Ragnarok Online**
  - Leitura visual de HP, monstros e itens
  - Máquina de estados (andar, atacar, curar, fugir)
  - Integração entre Python e AutoHotkey
```

## 🗂️ Estrutura do Projeto

```bash
ai-game-learning/
├── README.md              # Este arquivo
├── diretrizes.md          # Padrões de código e commits
├── requirements.txt       # Dependências Python
├── .gitignore             # Arquivos ignorados pelo Git
├── venv/                  # Ambiente virtual (não versionado)
├── fase1_fundamentos/     # Conceitos teóricos e exemplos simples
├── fase2_jogo_velha/      # Q-Learning e self-play
├── fase3_labirinto/       # Agente em ambiente de grade
├── fase4_dino_chrome/     # Visão computacional com OpenCV
├── fase5_flappy_bird/     # Visão e timing
├── fase6_gymnasium/       # Deep Q-Networks
└── fase7_ragnarok/        # Projeto final com integração AHK
```

## 🧩 Como Executar

1.  Clone este repositório:
    ```bash
     git clone https://github.com/seuusuario/ai-game-learning.git
     cd ai-game-learning
    ```
2.  Crie e ative o ambiente virtual:
    ```bash
     python -m venv venv
     source venv/Scripts/activate  # Windows (Git Bash)
    ```
3.  Instale as dependências:
    ```bash
     pip install -r requirements.txt
    ```

## 👤 Autor

**Lucas Ferreira (LKS)**
📅 Início do projeto: **26 de outubro de 2025**

> “A melhor forma de aprender IA é ensinando a máquina a aprender.”

## 🔮 Próximos Passos

```md
- [ ] Criar e documentar exemplos práticos na Fase 1
- [ ] Implementar ambiente de treino do Jogo da Velha
- [ ] Explorar integração entre Python e AHK
- [ ] Iniciar primeiros experimentos de visão computacional
```