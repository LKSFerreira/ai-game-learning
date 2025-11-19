# fase_2/labirinto/jogar.py

"""
Módulo principal para jogar o labirinto de forma interativa e gráfica.

Este arquivo combina a geração do labirinto, o ambiente e a visualização
com Pygame para criar uma experiência de jogo completa para um usuário humano.
"""

import pygame
try:
    # quando importado como parte do pacote (pytest)
    from .ambiente import Labirinto
    from .gerador_labirinto import gerar_labirinto
except Exception:
    # quando executado diretamente (python jogar.py)
    from ambiente import Labirinto
    from gerador_labirinto import gerar_labirinto

# --- PENSAMENTO 1: Definir Constantes e Configurações do Jogo ---
# Centralizar as configurações aqui facilita ajustes futuros.
# Adicionamos constantes para o rastro e para o controle de movimento.

# Cores (em padrão RGB)
COR_FUNDO = (20, 20, 40)
COR_PAREDE = (130, 130, 150)
COR_CAMINHO = (40, 40, 60)
COR_AGENTE = (255, 100, 100)
COR_SAIDA = (100, 255, 100)
COR_RASTRO = (210, 210, 210, 100)  # Branco com transparência (alpha)

# Dimensões e Velocidade
TAMANHO_CELULA_BASE = 10  # O tamanho mínimo que consideramos visualmente agradável.
INTERVALO_MOVIMENTO = 100  # Intervalo em milissegundos entre os movimentos (10 movimentos por segundo)

# Mapeamento de teclas do Pygame para as ações do nosso ambiente
MAPEAMENTO_TECLAS_PYGAME = {
    pygame.K_w: "W", pygame.K_UP: "W",
    pygame.K_s: "S", pygame.K_DOWN: "S",
    pygame.K_a: "A", pygame.K_LEFT: "A",
    pygame.K_d: "D", pygame.K_RIGHT: "D",
}


# --- PENSAMENTO 2: A Classe Principal do Jogo ---
# Renomeamos a classe para 'JogoGrafico' para refletir melhor seu propósito.
# Ela agora gerencia não apenas a tela, mas todo o estado do jogo interativo.
class JogoGrafico:
    """
    Gerencia a janela, o loop de jogo, a renderização e a interação do usuário.
    """

    def __init__(self, labirinto: Labirinto, tamanho_celula: int):
        """
        Inicializa o Pygame e a janela do jogo.

        Args:
            labirinto (Labirinto): A instância do labirinto a ser jogada.
            tamanho_celula (int): O tamanho em pixels de cada célula do labirinto.
        """
        pygame.init()

        self.labirinto = labirinto
        self.tamanho_celula = tamanho_celula

        # A janela é calculada dinamicamente com base no tamanho do labirinto e da célula.
        largura_janela = len(labirinto._matriz[0]) * self.tamanho_celula
        altura_janela = len(labirinto._matriz) * self.tamanho_celula
        titulo = "Jogo do Labirinto - Use WASD ou Setas para Mover"

        self.tela = pygame.display.set_mode((largura_janela, altura_janela))
        pygame.display.set_caption(titulo)
        self.relogio = pygame.time.Clock()

        # --- MELHORIA 1: Controle de tempo para movimento contínuo ---
        self.ultimo_movimento = 0  # Armazena o tempo do último movimento

    def executar(self) -> None:
        """
        Inicia o loop principal do jogo.

        Este é o coração pulsante do jogo, responsável por capturar eventos,
        atualizar o estado e desenhar tudo na tela a cada frame.
        """
        rodando = True
        while rodando:
            # 1. Processar Eventos (como fechar a janela)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

            # --- MELHORIA 1: Lógica de movimento contínuo ---
            # Em vez de reagir apenas a `KEYDOWN`, verificamos o estado de todas
            # as teclas a cada frame. Isso permite o movimento contínuo.
            self.processar_movimento_continuo()

            # 2. Desenhar tudo na Tela
            self.tela.fill(COR_FUNDO)
            self.desenhar_labirinto()
            pygame.display.flip()

            # 3. Controlar a velocidade do jogo
            self.relogio.tick(60)  # Limita o jogo a 60 frames por segundo

        # --- PENSAMENTO 4: Finalização Limpa ---
        pygame.quit()

    def processar_movimento_continuo(self) -> None:
        """
        Verifica as teclas pressionadas e move o agente de forma contínua e controlada.
        """
        # Pega o estado de todas as teclas do teclado.
        teclas_pressionadas = pygame.key.get_pressed()
        
        # Pega o tempo atual em milissegundos.
        tempo_atual = pygame.time.get_ticks()

        # Verifica se já passou tempo suficiente desde o último movimento.
        if tempo_atual - self.ultimo_movimento > INTERVALO_MOVIMENTO:
            acao_executada = False
            for tecla, acao in MAPEAMENTO_TECLAS_PYGAME.items():
                if teclas_pressionadas[tecla]:
                    _, _, terminou = self.labirinto.executar_acao(acao)
                    acao_executada = True
                    if terminou:
                        print("🎉 Parabéns, você encontrou a saída! 🎉")
                        pygame.time.wait(1000) # Pausa por 1 segundo para o jogador ver a vitória
                        pygame.event.post(pygame.event.Event(pygame.QUIT)) # Envia um evento para fechar o jogo
                    break # Executa apenas uma ação por vez

            # Se uma ação foi executada, atualiza o tempo do último movimento.
            if acao_executada:
                self.ultimo_movimento = tempo_atual

    def desenhar_labirinto(self) -> None:
        """
        Desenha o estado atual do labirinto na tela, incluindo o rastro.
        """
        for indice_linha, linha in enumerate(self.labirinto._matriz):
            for indice_coluna, tipo_celula in enumerate(linha):
                pos_x = indice_coluna * self.tamanho_celula
                pos_y = indice_linha * self.tamanho_celula
                retangulo = pygame.Rect(pos_x, pos_y, self.tamanho_celula, self.tamanho_celula)

                cor = COR_CAMINHO
                if tipo_celula == "#":
                    cor = COR_PAREDE
                
                pygame.draw.rect(self.tela, cor, retangulo)

                # --- MELHORIA 3: Desenhar o rastro (pegadas) ---
                # Se a célula for um caminho já visitado ('•'), desenhamos a pegada.
                if tipo_celula == "•":
                    # Desenhamos um pequeno círculo no centro da célula para ser a "pegada".
                    centro_x = pos_x + self.tamanho_celula // 2
                    centro_y = pos_y + self.tamanho_celula // 2
                    raio_pegada = self.tamanho_celula // 5 # A pegada terá 1/5 do tamanho da célula
                    pygame.draw.circle(self.tela, COR_RASTRO, (centro_x, centro_y), raio_pegada)

        # Desenha a saída e o agente por cima de tudo
        pos_saida_y, pos_saida_x = self.labirinto.ponto_final
        retangulo_saida = pygame.Rect(pos_saida_x * self.tamanho_celula, pos_saida_y * self.tamanho_celula, self.tamanho_celula, self.tamanho_celula)
        pygame.draw.rect(self.tela, COR_SAIDA, retangulo_saida)

        pos_agente_y, pos_agente_x = self.labirinto.posicao_agente
        retangulo_agente = pygame.Rect(pos_agente_x * self.tamanho_celula, pos_agente_y * self.tamanho_celula, self.tamanho_celula, self.tamanho_celula)
        pygame.draw.rect(self.tela, COR_AGENTE, retangulo_agente)


def calcular_dimensoes_ideais(
    largura_tela: int, altura_tela: int, tamanho_celula: int
) -> tuple[int, int]:
    """
    Calcula as dimensões ideais (em células) para um labirinto caber na tela.

    Args:
        largura_tela (int): Largura disponível da tela em pixels.
        altura_tela (int): Altura disponível da tela em pixels.
        tamanho_celula (int): O tamanho de cada célula em pixels.

    Returns:
        tuple[int, int]: Uma tupla contendo (altura_ideal_em_celulas, largura_ideal_em_celulas).
    """
    margem = 100
    largura_maxima_jogo = largura_tela - margem
    altura_maxima_jogo = altura_tela - margem

    max_celulas_largura = (largura_maxima_jogo // tamanho_celula - 1) // 2
    max_celulas_altura = (altura_maxima_jogo // tamanho_celula - 1) // 2

    # Define um tamanho desejado, mas o limita ao máximo permitido pela tela.
    altura_ideal = min(30, max_celulas_altura)
    largura_ideal = min(40, max_celulas_largura)

    return altura_ideal, largura_ideal


# --- PENSAMENTO 5: Ponto de Entrada e Lógica de Geração ---
# O bloco `if __name__ == '__main__':` agora contém a lógica inteligente
# para ajustar o tamanho do labirinto à tela do usuário.
if __name__ == '__main__':
    print("Iniciando o jogo do labirinto...")
    try:
        # --- MELHORIA 2: Ajuste automático ao tamanho da tela ---
        pygame.init()
        info_tela = pygame.display.Info()
        largura_tela_disponivel = info_tela.current_w
        altura_tela_disponivel = info_tela.current_h
        pygame.quit() # Quitamos o pygame só para pegar a info, vamos iniciar de novo na classe.

        print(f"Detectado tamanho da tela: {largura_tela_disponivel}x{altura_tela_disponivel} pixels.")

        # Chama a nova função testável para obter as dimensões
        ALTURA_CELULAS, LARGURA_CELULAS = calcular_dimensoes_ideais(
            largura_tela_disponivel, altura_tela_disponivel, TAMANHO_CELULA_BASE
        )
        
        print(f"Gerando um labirinto de {ALTURA_CELULAS}x{LARGURA_CELULAS} células.")

        # 1. Gerar o labirinto
        matriz = gerar_labirinto(ALTURA_CELULAS, LARGURA_CELULAS)
        ponto_inicial = (1, 1)
        ponto_final = (ALTURA_CELULAS * 2 - 1, LARGURA_CELULAS * 2 - 1)

        # 2. Criar a instância do ambiente
        ambiente = Labirinto(matriz, ponto_inicial, ponto_final)

        # 3. Criar a instância do jogo, passando o ambiente e o tamanho da célula
        jogo = JogoGrafico(ambiente, TAMANHO_CELULA_BASE)

        # 4. Executar o loop principal
        jogo.executar()

        print("Jogo fechado com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao executar o jogo: {e}")
        import traceback
        traceback.print_exc()