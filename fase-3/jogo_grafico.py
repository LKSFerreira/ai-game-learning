"""
Módulo responsável pela interface gráfica do jogo do Labirinto usando Pygame.

Este módulo contém apenas a lógica de visualização e interação com o usuário.
Ele não sabe nada sobre geração de labirintos ou treinamento de IA.
"""

import pygame
from ambiente import Labirinto

# --- PENSAMENTO 1: Constantes de Configuração Visual ---
# Centralizamos todas as cores e configurações visuais aqui para facilitar
# ajustes futuros. Se quisermos mudar o tema visual, basta alterar essas constantes.

# Paleta de Cores (RGB)
COR_FUNDO = (20, 20, 40)           # Azul escuro para o fundo
COR_PAREDE = (130, 130, 150)        # Cinza para as paredes
COR_CAMINHO = (40, 40, 60)          # Azul bem escuro para o caminho
COR_AGENTE = (255, 100, 100)        # Vermelho para o agente
COR_SAIDA = (100, 255, 100)         # Verde para a saída (fixo, conforme solicitado)
COR_RASTRO = (210, 210, 210, 100)   # Branco translúcido para o rastro

# Configurações de Jogo
INTERVALO_MOVIMENTO_MS = 100        # Milissegundos entre movimentos (controla velocidade)

# --- PENSAMENTO 2: Mapeamento de Teclas ---
# O Pygame usa constantes específicas para teclas (pygame.K_w, pygame.K_UP, etc).
# Mapeamos essas teclas para as ações que nosso ambiente entende ("W", "A", "S", "D").
# Isso permite que o jogador use tanto WASD quanto as setas direcionais.
MAPEAMENTO_TECLAS = {
    pygame.K_w: "W",
    pygame.K_UP: "W",
    pygame.K_s: "S",
    pygame.K_DOWN: "S",
    pygame.K_a: "A",
    pygame.K_LEFT: "A",
    pygame.K_d: "D",
    pygame.K_RIGHT: "D",
}


class JogoGrafico:
    """
    Gerencia a janela do jogo, renderização e interação com o usuário.
    
    Esta classe é responsável apenas pela camada de apresentação (UI).
    Ela recebe um ambiente de Labirinto já criado e apenas o exibe e permite
    interação humana.
    """

    def __init__(
        self,
        labirinto: Labirinto,
        seed_usada: int | None = None,
        tamanho_celula: int = 20
    ):
        """
        Inicializa a interface gráfica do jogo.
        
        Args:
            labirinto (Labirinto): O ambiente do labirinto já inicializado.
            seed_usada (int | None): A seed usada para gerar o labirinto (apenas para exibição).
            tamanho_celula (int): Tamanho em pixels de cada célula. Padrão: 20.
        """
        # --- PENSAMENTO 3: Inicialização do Pygame ---
        # Precisamos inicializar o Pygame antes de criar janelas ou usar suas funcionalidades.
        pygame.init()

        self.labirinto = labirinto
        self.seed = seed_usada
        self.tamanho_celula = tamanho_celula

        # --- PENSAMENTO 4: Cálculo Dinâmico do Tamanho da Janela ---
        # O tamanho da janela depende do tamanho do labirinto. Não queremos valores
        # fixos, mas sim calcular com base na matriz recebida.
        num_linhas = len(labirinto._matriz)
        num_colunas = len(labirinto._matriz[0])
        
        largura_janela = num_colunas * self.tamanho_celula
        altura_janela = num_linhas * self.tamanho_celula

        # --- PENSAMENTO 5: Criação da Janela e Configurações ---
        self.tela = pygame.display.set_mode((largura_janela, altura_janela))
        
        # O título mostra a seed para o usuário saber qual mapa está jogando
        titulo = f"Labirinto - Mapa {seed_usada if seed_usada else 'Aleatório'}"
        pygame.display.set_caption(titulo)
        
        self.relogio = pygame.time.Clock()  # Controla o FPS
        self.ultimo_movimento = 0  # Timestamp do último movimento (em ms)

    def executar(self) -> None:
        """
        Inicia o loop principal do jogo.
        
        Este é o coração do jogo. Ele roda continuamente até o usuário
        fechar a janela ou completar o labirinto.
        """
        rodando = True
        while rodando:
            # --- PENSAMENTO 6: Processar Eventos ---
            # O Pygame acumula eventos (cliques, teclas, fechar janela) em uma fila.
            # Precisamos processá-los a cada frame.
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:  # Usuário clicou no X da janela
                    rodando = False

            # --- PENSAMENTO 7: Lógica de Movimento ---
            # Separamos a lógica de movimento em uma função própria para manter
            # o código organizado e legível.
            self._processar_movimento()

            # --- PENSAMENTO 8: Renderização ---
            # Primeiro limpamos a tela, depois desenhamos tudo, depois exibimos.
            self.tela.fill(COR_FUNDO)
            self._desenhar_labirinto()
            pygame.display.flip()  # Atualiza a tela com o que foi desenhado

            # --- PENSAMENTO 9: Controle de FPS ---
            # Limita o jogo a 60 frames por segundo para não consumir CPU desnecessariamente
            self.relogio.tick(60)

        # --- PENSAMENTO 10: Limpeza ao Sair ---
        pygame.quit()

    def _processar_movimento(self) -> None:
        """
        Verifica as teclas pressionadas e executa o movimento no ambiente.
        
        Usamos um sistema de "cooldown" para evitar que o agente se mova
        rápido demais quando o usuário segura uma tecla.
        """
        # Pega o estado atual de TODAS as teclas (pressionadas ou não)
        teclas = pygame.key.get_pressed()
        tempo_atual = pygame.time.get_ticks()

        # --- PENSAMENTO 11: Sistema de Cooldown ---
        # Só permitimos um movimento se já passou tempo suficiente desde o último.
        # Isso cria um movimento "suave" e controlado.
        if tempo_atual - self.ultimo_movimento < INTERVALO_MOVIMENTO_MS:
            return  # Ainda em cooldown, não faz nada

        # --- PENSAMENTO 12: Detecção de Tecla e Execução ---
        # Percorremos o mapeamento de teclas e verificamos se alguma está pressionada.
        for tecla_pygame, acao_ambiente in MAPEAMENTO_TECLAS.items():
            if teclas[tecla_pygame]:
                # Executa a ação no ambiente
                _, _, terminou = self.labirinto.executar_acao(acao_ambiente)
                
                # Atualiza o timestamp
                self.ultimo_movimento = tempo_atual
                
                # --- PENSAMENTO 13: Verificar Vitória ---
                if terminou:
                    print("🎉 Parabéns! Você encontrou a saída! 🎉")
                    pygame.time.wait(1500)  # Pausa 1.5s para o jogador ver
                    pygame.event.post(pygame.event.Event(pygame.QUIT))  # Fecha o jogo
                
                break  # Só processa uma ação por vez

    def _desenhar_labirinto(self) -> None:
        """
        Renderiza o estado atual do labirinto na tela.
        
        Desenha: paredes, caminhos, rastro, saída e agente.
        """
        # --- PENSAMENTO 14: Renderizar a Grade Base ---
        # Percorremos toda a matriz e desenhamos cada célula.
        for linha_idx, linha in enumerate(self.labirinto._matriz):
            for coluna_idx, tipo_celula in enumerate(linha):
                # Calcula a posição em pixels
                x = coluna_idx * self.tamanho_celula
                y = linha_idx * self.tamanho_celula
                retangulo = pygame.Rect(x, y, self.tamanho_celula, self.tamanho_celula)

                # Escolhe a cor baseada no tipo de célula
                if tipo_celula == "#":  # Parede
                    cor = COR_PAREDE
                else:  # Caminho
                    cor = COR_CAMINHO
                
                pygame.draw.rect(self.tela, cor, retangulo)

                # --- PENSAMENTO 15: Desenhar o Rastro ---
                # Se a célula tem o marcador de "caminho visitado" (•),
                # desenhamos um círculo pequeno para indicar que o agente passou ali.
                if tipo_celula == "•":
                    centro_x = x + self.tamanho_celula // 2
                    centro_y = y + self.tamanho_celula // 2
                    raio = self.tamanho_celula // 5
                    pygame.draw.circle(self.tela, COR_RASTRO, (centro_x, centro_y), raio)

        # --- PENSAMENTO 16: Desenhar a Saída (por cima da grade) ---
        saida_y, saida_x = self.labirinto.ponto_final
        rect_saida = pygame.Rect(
            saida_x * self.tamanho_celula,
            saida_y * self.tamanho_celula,
            self.tamanho_celula,
            self.tamanho_celula
        )
        pygame.draw.rect(self.tela, COR_SAIDA, rect_saida)

        # --- PENSAMENTO 17: Desenhar o Agente (por cima de tudo) ---
        agente_y, agente_x = self.labirinto.posicao_agente
        rect_agente = pygame.Rect(
            agente_x * self.tamanho_celula,
            agente_y * self.tamanho_celula,
            self.tamanho_celula,
            self.tamanho_celula
        )
        pygame.draw.rect(self.tela, COR_AGENTE, rect_agente)
