import pygame
import random
import math

# inicializa o Pygame
pygame.init()

# Define as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Variáveis para o estado do jogo
game_over = False
foguete_pousou = False

# cria a tela 800x600
infoObject = pygame.display.Info()
screen_width, screen_height = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((screen_width, screen_height - 50))

# Carrega a imagem de fundo
background_image = pygame.image.load('assets/fundo.jpg')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Redimensiona para se ajustar à tela

# Carrega a imagem da plataforma
plataform_image = pygame.image.load('assets/pa.png')
platform_width, platform_height = 400, 25
platform_pos = [(screen_width - platform_width) // 2, screen_height - 300]  # Posição da plataforma

# Configurações do foguete
rocket_width, rocket_height = 10, 100
rocket_pos = [random.randint(50, screen_width - 50), 50]  # Posição inicial aleatória na parte de cima
rocket_vel = [0, 0]  # Velocidade inicial
rocket_angle = 0  # Ângulo inicial
rocket_image_original = pygame.image.load('assets/foguete1.png')
rocket_image_original = pygame.transform.scale(rocket_image_original, (rocket_width, rocket_height))  # Redimensiona para se ajustar à tela


# Carrega a imagem do fogo do foguete
fire_image_original = pygame.image.load('assets/fogo2.png')
fire_image_original = pygame.transform.scale(fire_image_original, (5, 5))  # Redimensiona para se ajustar à tela
show_fire = False  # Variável para controlar a exibição do fogo

# Carrega a imagem do jato de estabilização do foguete
jet_left_image_original = pygame.image.load('assets/jet_left.png')
jet_left_image_original = pygame.transform.scale(jet_left_image_original, (50, 15))
show_jet_left = False  # Variável para controlar a exibição do jet


jet_right_image_original = pygame.image.load('assets/jet_right.png')
jet_right_image_original = pygame.transform.scale(jet_right_image_original, (50, 15))
show_jet_right = False  # Variável para controlar a exibição do jet


# Gravidade e controle
gravity = 0.05
thrust = -0.1  # Empuxo para cima
rotation_speed = 0.5  # Velocidade de rotação

# Configurações de fonte
font_info = pygame.font.SysFont(None, 25)  # None para usar a fonte padrão, 55 para o tamanho
font_countdown = pygame.font.SysFont(None, 100)  # None para usar a fonte padrão, 55 para o tamanho


# Relógio para controlar o FPS
clock = pygame.time.Clock()

# Inicio do Jogo
start_game = False

# Função para exibir a contagem regressiva
def countdown():
    for i in range(3, -1, -1):
        screen.fill(BLACK)
        text = font_countdown.render(str(i), True, WHITE)
        text_rect = text.get_rect(center=(screen_width / 2, (screen_height - 100) / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)  # Espera 1000 milissegundos (1 segundo)
    return False

# Main loop
running = True
while running:
    # Mantém o loop rodando na velocidade certa
    clock.tick(60)

    # Exibe a contagem regressiva antes de iniciar o jogo
    if start_game: 
        start_game = countdown()

    for i in range(5): 
        start_text = font_info.render(f'{i}', True, WHITE)
        screen.blit(start_text, (screen_width/2, screen_height/2))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Controles do usuário
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        # Aplica o empuxo para cima
        rocket_vel[1] += thrust * math.cos(math.radians(rocket_angle))
        rocket_vel[0] += thrust * math.sin(math.radians(rocket_angle))
        show_fire = True
    else:
        show_fire = False

    if keys[pygame.K_LEFT]:
        
        # Aplica o empuxo para cima
        rocket_vel[1] += -0.005 * math.cos(math.radians(rocket_angle))
        rocket_vel[0] += -0.005 * math.sin(math.radians(rocket_angle))

        # Rotaciona para a esquerda
        rocket_angle -= rotation_speed
        show_jet_left = True
    else:
        show_jet_left = False
        
    if keys[pygame.K_RIGHT]:
        # Aplica o empuxo para cima
        rocket_vel[1] += -0.05 * math.cos(math.radians(rocket_angle))
        rocket_vel[0] += -0.05 * math.sin(math.radians(rocket_angle))

        # Rotaciona para a direita
        rocket_angle += rotation_speed
        show_jet_right = True
    else:
        show_jet_right = False
        

    # Aplica gravidade
  
    rocket_vel[1] += gravity


    # Atualiza a posição do foguete
    rocket_pos[0] += rocket_vel[0]
    rocket_pos[1] += rocket_vel[1]


    # Verifica se o foguete está na altura da plataforma
    if rocket_pos[1]  > platform_pos[1] + 30:
        # Verifica se está alinhado horizontalmente com a plataforma
        if platform_pos[0] <= rocket_pos[0] <= platform_pos[0] + platform_width:
            foguete_pousou = True
            rocket_vel = [0, 0]  # Para o foguete
            rocket_pos[1] = platform_pos[1] + 30
            # Se não, foguete cai na água
            #game_over = True

    # Preenche a tela com a cor de fundo
    screen.fill(BLACK)

    # Desenha a imagem de fundo
    screen.blit(background_image, (0, 0))

    # Desenha a plataforma de pouso
    screen.blit(plataform_image, platform_pos)

    # Rotaciona o foguete
    rocket = pygame.transform.rotate(rocket_image_original, rocket_angle)
    rocket_rect = rocket.get_rect(center=(rocket_pos[0], rocket_pos[1]))

    # Desenha o foguete
    screen.blit(rocket, rocket_rect)

  
        # Desenha o fogo na base do foguete, se necessário
    if show_fire:
        fire_image = pygame.transform.rotate(fire_image_original, rocket_angle)
        # Ajusta a posição do fogo para que esteja na base do foguete
        # Calcula a posição da base do foguete considerando a rotação em torno do centro
        offset_x = -rocket_height / 2 * math.sin(math.radians(rocket_angle))
        offset_y = rocket_height / 2 * math.cos(math.radians(rocket_angle))
        fire_pos = (rocket_rect.centerx - offset_x, rocket_rect.centery + offset_y)
        fire_rect = fire_image.get_rect(center=fire_pos)
        screen.blit(fire_image, fire_rect)

    if show_jet_left:
        # Rotaciona a imagem do jato em torno do ponto de rotação do foguete
        jet_left_image = pygame.transform.rotate(jet_left_image_original, rocket_angle + 45)
        # Calcula a posição do jato esquerdo em relação ao topo do foguete
        jet_left_offset_x = (-rocket_height / 2 + 50) * math.sin(math.radians(rocket_angle))
        jet_left_offset_y = (-rocket_height / 2 + 50) * math.cos(math.radians(rocket_angle))
        jet_left_pos = ((rocket_rect.centerx) + jet_left_offset_x - 20, (rocket_rect.centery) + jet_left_offset_y)
        jet_left_rect = jet_left_image.get_rect(center=jet_left_pos)
        screen.blit(jet_left_image, jet_left_rect)

    if show_jet_right:
        # Rotaciona a imagem do jato em torno do ponto de rotação do foguete
        jet_right_image = pygame.transform.rotate(jet_right_image_original, rocket_angle - 45)
        # Calcula a posição do jato direito em relação ao topo do foguete
        jet_right_offset_x = (-rocket_height / 2 + 50) * math.sin(math.radians(rocket_angle))
        jet_right_offset_y = (-rocket_height / 2 + 50) * math.cos(math.radians(rocket_angle))
        jet_right_pos = (rocket_rect.centerx + jet_right_offset_x + 20, rocket_rect.centery + jet_right_offset_y)
        jet_right_rect = jet_right_image.get_rect(center=jet_right_pos)
        screen.blit(jet_right_image, jet_right_rect)



    # Escreve texto
    text1 = font_info.render(f'Posição do Foguete: {rocket_pos[0], rocket_pos[1]}', True, WHITE)
    text2 = font_info.render(f'Angulo do foguete: {rocket_angle}', True, WHITE)
    screen.blit(text1, (0, 5))
    screen.blit(text2, (0, 25))


    # Verifica se o jogo terminou
    if game_over:
        screen.fill(BLACK)  # Limpa a tela
        game_over_text = font_info.render("Game Over! Você caiu na água.", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        pygame.time.delay(3000)  # Mostra a mensagem por 3 segundos
        running = False  # Termina o loop do jogo

    # Atualiza o conteúdo da tela inteira
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()
