# 🧠 Fase 3: O agente no Labirinto — Navegação em Grid World

Bem-vindo à Fase 3! Se na fase anterior nossa IA aprendeu a jogar um jogo de tabuleiro estático, agora ela vai aprender a **andar**.

### O que vamos construir?

Uma Inteligência Artificial que aprende a navegar em um **Labirinto** (Grid World) para encontrar a saída o mais rápido possível, evitando paredes e becos sem saída.

1.  **O Agente:** Um "agente virtual" que pode se mover para Cima, Baixo, Esquerda e Direita.
2.  **O Ambiente:** Um labirinto 10x10 com paredes e uma saída.
3.  **O Objetivo:** Encontrar o caminho mais curto até a saída.

---

## 🗺️ O Mundo em Grade (Grid World)

Este é o "Hello World" da navegação em robótica e jogos. Diferente do Jogo da Velha, onde o estado era a configuração das peças, aqui o estado é **onde você/agente está**.

### 1. O Estado: "Onde estou?"

No Jogo da Velha, o estado era complexo (uma `tupla` de 9 itens). Aqui, é muito mais simples e visual.
O estado é apenas a **coordenada (Linha, Coluna)** do nosso agente.

```
  0 1 2 3
0 . . . .
1 . A . .  <-- O Agente (A) está na linha 1, coluna 1.
2 . . . .      Estado = (1, 1)
3 . . S .
```

Tupla:  É como uma "lista" de itens que não pode ser alterada depois de criada. Pense nela como um pacote fechado de informações. Por exemplo, a coordenada `(1, 1)` é uma tupla que agrupa a linha `1` e a coluna `1` em uma única unidade. Uma vez que você define `(1, 1)`, você não pode mudar o `1` da linha para `2` dentro da mesma tupla; você teria que criar uma nova tupla `(2, 1)`.

### 2. As Ações: "Para onde vou?"

Em vez de "marcar X na posição 5", nossas ações agora são movimentos físicos:

- ⬆️ **Cima** (Up)
- ⬇️ **Baixo** (Down)
- ⬅️ **Esquerda** (Left)
- ➡️ **Direita** (Right)

### 3. A Recompensa: O Segredo da Preguiça Inteligente 🦥

Aqui entra um conceito crucial do Aprendizado por Reforço: **Recompensas Negativas (Penalidades)**.

Imagine que você quer ensinar seu cachorro a vir até você.

- Se ele chegar em você: **Ganha um biscoito (+10)**.
- Mas se ele ficar dando voltas no jardim antes de vir: **Não acontece nada (0)**.

O cachorro pode aprender a dar 50 voltas no jardim e só depois ir até você, porque o resultado final é o mesmo: biscoito. Ele não tem pressa.

Para a nossa IA, queremos o **caminho mais curto**. Como ensinamos pressa? **Cobrando "energia" por cada passo.**

- **Chegar na Saída:** +10.0 (O Biscoito 🍪)
- **Bater na Parede:** -0.5 (A Dor de Cabeça 🤕)
- **Dar um Passo:** -0.1 (O Cansaço 😮‍💨)

> **A Lógica da IA:** "Cada passo que eu dou me custa 0.1 pontos. Se eu demorar 100 passos, vou perder 10 pontos! Eu preciso correr para a saída para parar de perder pontos e ganhar logo meu biscoito."

Isso força a IA a encontrar o **caminho ótimo**.

---

## 🧠 A Q-Table do Labirinto

Nossa "cola" (Q-Table) agora vai mapear cada **quadrado do chão** para as 4 direções possíveis.

Imagine que o chão do labirinto tem setas desenhadas, indicando qual a melhor direção a seguir naquele quadrado. A Q-Table é quem desenha essas setas.

**Exemplo de uma linha da Q-Table para o Estado (1, 1):**

| Estado (Posição) | Cima ⬆️ | Baixo ⬇️ | Esquerda ⬅️ | Direita ➡️ |
| :--------------- | :-----: | :------: | :---------: | :--------: |
| **(1, 1)**       |  -0.5   |   -0.1   |    -0.5     |  **0.8**   |

- **Cima (-0.5):** Parede! Ruim.
- **Esquerda (-0.5):** Parede! Ruim.
- **Baixo (-0.1):** Caminho livre, mas leva para longe da saída.
- **Direita (0.8):** Caminho livre e aproxima da saída! **Melhor Ação.**

---

## 🎮 Do Tabuleiro para o Mapa

A grande mudança mental desta fase é perceber que **RL serve para qualquer coisa**.

- No Jogo da Velha, "navegávamos" por estados de um tabuleiro.
- No Labirinto, navegamos por posições físicas.
- No Ragnarok (futuro), navegaremos por mapas reais do jogo.

A matemática (Q-Learning, Bellman) é **exatamente a mesma**. Só mudamos o que chamamos de "Estado" e "Ação".

## 🚀 O que vamos construir?

| Arquivo        | Responsabilidade                                                          |
| :------------- | :------------------------------------------------------------------------ |
| `ambiente.py`  | (Já existe) Cria o labirinto, desenha paredes e define as regras.         |
| `agente.py`    | (Sua Missão) O cérebro que decide para onde andar.                        |
| `treinador.py` | O "gym" onde o agente vai correr milhares de vezes até decorar o caminho. |
| `jogar.py`     | (Já existe) Para vermos o resultado visualmente.                          |

Preparado para guiar nosso rato virtual? Vamos para o código!
