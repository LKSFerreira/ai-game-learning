## 🎮 Fase 2: Visão Geral do Projeto

### O que vamos construir?

Uma IA que aprende a jogar **Jogo da Velha** (Tic-Tac-Toe) do zero usando **Q-Learning**. A IA vai:

1. Começar sem saber nada (jogando aleatoriamente)
2. Jogar **milhares de partidas** contra ela mesma (Self-Play)
3. Aprender com cada vitória, derrota e empate
4. Após o treino, **nunca mais perder** uma partida!

### Por que Jogo da Velha?

É perfeito para aprender RL porque:

* **Simples:** Tabuleiro 3x3, apenas 2 jogadores
* **Finito:** Número limitado de estados possíveis (~5.478 estados únicos)
* **Rápido de treinar:** Leva segundos, não horas
* **Demonstra tudo:** Você verá o aprendizado acontecendo visualmente

---

## 📚 O que é Q-Learning?

Agora vou explicar o algoritmo que usaremos. Preste bastante atenção!

### A Ideia Central

**Q-Learning** é um dos algoritmos de RL mais famosos e simples. O nome "Q" vem de "**Quality**" (qualidade).

O algoritmo cria uma **Q-Table** (Tabela Q) que funciona como uma "**folha de cola**" gigante para o agente:

```
┌─────────────────────────────────────────────────┐
│  Q-TABLE = "Quanto vale fazer X em Y?"         │
│                                                 │
│  Estado → | Ação 1 | Ação 2 | Ação 3 | ...     │
│  ────────────────────────────────────────────   │
│  Estado A |  0.5   |  0.2   |  0.9   | ...     │
│  Estado B | -0.3   |  0.8   |  0.1   | ...     │
│  Estado C |  0.7   |  0.4   | -0.2   | ...     │
│                                                 │
└─────────────────────────────────────────────────┘
```

Cada célula guarda um **valor Q**: quanto aquela ação vale naquele estado.

### Analogia: Mapa do Tesouro

Imagine que você está em uma ilha procurando tesouros:

* Cada local da ilha = um **Estado**
* Cada direção (norte, sul...) = uma **Ação**
* A Q-Table é seu **mapa** com anotações que vão melhorando com o tempo

---

## 🔢 A Equação de Bellman

Q-Learning usa uma fórmula matemática chamada **Equação de Bellman** para atualizar a Q-Table:

$$
Q(s, a) \leftarrow Q(s, a) + \alpha \times [r + \gamma \times \max Q(s', a') - Q(s, a)]
$$

### Tradução dos símbolos

| Símbolo | Significa                   |
| ------- | --------------------------- |
| Q(s, a) | Valor da ação a no estado s |
| s       | Estado atual                |
| a       | Ação tomada                 |
| r       | Recompensa                  |
| s'      | Próximo estado              |
| α       | Taxa de aprendizado         |
| γ       | Fator de desconto           |

### Em Português Claro

> Ajuste o valor Q baseado na diferença entre o que você **esperava** e o que realmente **aconteceu**.

---

## 🎯 Q-Learning no Jogo da Velha

### Estados (s)

Cada configuração possível do tabuleiro:

```
X | O | X
---------
  | X | O
---------
  |   |  
```

Representaremos como uma tupla:
`('X','O','X','','X','O','','','')`

### Ações (a)

Escolher uma posição vazia:

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

### Recompensas (r)

| Situação          | Recompensa |
| ----------------- | ---------- |
| Vitória           | +1         |
| Derrota           | -1         |
| Empate            | 0          |
| Jogo em andamento | 0          |

---

## 📋 Estrutura do Projeto - Fase 2

```
ai-game-learning/
├── fase2_jogo_velha/
│   ├── __init__.py
│   ├── ambiente.py
│   ├── agente.py
│   ├── treinador.py
│   ├── jogar.py
│   └── visualizador.py
```

* **ambiente.py**: lógica do jogo
* **agente.py**: Q-Learning
* **treinador.py**: self-play
* **jogar.py**: jogar contra a IA treinada
* **visualizador.py**: gráficos

---

## 🚀 O Processo de Treinamento

### Exemplo do começo do treino:

* Muitos movimentos aleatórios
* IA ganhando ou perdendo por sorte
* Q-Table começa com tudo **0**

### Final do treino:

* Jogadas sempre ótimas
* A IA fica praticamente **imbatível**

---

## 🎓 Conceitos Novos: Epsilon-Greedy

Usamos o parâmetro **ε (epsilon)** para equilibrar:

| Estratégia         | O que faz               |
| ------------------ | ----------------------- |
| Explorar           | Tentar movimentos novos |
| Explorar (Exploit) | Usar a Q-Table          |

Pseudocódigo:

```python
if random() < epsilon:
    ação = escolher_aleatoriamente()
else:
    ação = ação_com_maior_Q()
```

* No início: **epsilon alto → muita exploração**
* No final: **epsilon baixo → comportamento ótimo**

---

## 📝 Resumo da Fase 2

Você vai aprender:

✅ Q-Learning do zero
✅ Criar um ambiente de jogo
✅ Treinar via Self-Play
✅ Epsilon-Greedy
✅ Visualizar resultados

### Hiperparâmetros que usaremos:

| Parâmetro               | Valor  |
| ----------------------- | ------ |
| α (Taxa de aprendizado) | 0.5    |
| γ (Desconto)            | 0.9    |
| Episódios               | 20.000 |
| ε inicial               | 0.8    |
| ε final                 | 0.1    |

---