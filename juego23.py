import pygame
import sys
import random

pygame.init()

ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Animación del Tanque - Metal Slug")

# Colores
GREEN = (34, 177, 76)
DARK_GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar las imágenes
background = pygame.image.load("fondo para juego.png").convert()
background = pygame.transform.scale(background, (ANCHO, ALTO))

# Imagen de fondo para el menú de selección de dificultad
menu_background = pygame.image.load("WhatsApp Image 2024-12-01 at 18.54.15.jpeg").convert()
menu_background = pygame.transform.scale(menu_background, (ANCHO, ALTO))

# Cargar el sprite sheet del tanque
tank_sprite_sheet = pygame.image.load("00232.png").convert()
tank_sprite_sheet.set_colorkey(BLACK)

# Cargar el sprite sheet del rayo
laser_sprite_sheet = pygame.image.load("Capture001 - copia-Photoroom.png").convert()
laser_sprite_sheet.set_colorkey(BLACK)

# Cargar el sprite sheet del soldado
soldado_sprite_sheet = pygame.image.load("Capture001 - copia (2)-Photoroom.png").convert()
soldado_sprite_sheet.set_colorkey(BLACK)

# Dimensiones del sprite sheet del tanque
tank_sprite_sheet_ancho, tank_sprite_sheet_alto = 1472, 94
NUM_FRAMES_TANK = 19
FRAME_ANCHO_TANK = tank_sprite_sheet_ancho // NUM_FRAMES_TANK
FRAME_ALTO_TANK = tank_sprite_sheet_alto

# Extraer frames del sprite sheet del tanque
tank_frames = [
    tank_sprite_sheet.subsurface((i * FRAME_ANCHO_TANK, 0, FRAME_ANCHO_TANK, FRAME_ALTO_TANK))
    for i in range(NUM_FRAMES_TANK)
]

# Dimensiones del sprite sheet del rayo
laser_sprite_sheet_ancho, laser_sprite_sheet_alto = 228, 50
NUM_FRAMES_LASER = 6
FRAME_ANCHO_LASER = laser_sprite_sheet_ancho // NUM_FRAMES_LASER
FRAME_ALTO_LASER = laser_sprite_sheet_alto

# Extraer frames del sprite sheet del rayo
laser_frames = [
    laser_sprite_sheet.subsurface((i * FRAME_ANCHO_LASER, 0, FRAME_ANCHO_LASER, FRAME_ALTO_LASER))
    for i in range(NUM_FRAMES_LASER)
]

# Dimensiones del sprite sheet del soldado
soldado_sprite_sheet_ancho, soldado_sprite_sheet_alto = 639, 42
NUM_FRAMES_SOLDIER = 24  
FRAME_ANCHO_SOLDIER = soldado_sprite_sheet_ancho // NUM_FRAMES_SOLDIER
FRAME_ALTO_SOLDIER = soldado_sprite_sheet_alto

# Extraer frames del sprite sheet del soldado
soldado_frames = [
    soldado_sprite_sheet.subsurface((i * FRAME_ANCHO_SOLDIER, 0, FRAME_ANCHO_SOLDIER, FRAME_ALTO_SOLDIER)).convert()
    for i in range(NUM_FRAMES_SOLDIER)
]

# Clases para el tanque, el láser y el soldado
class Tanque(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = tank_frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (50, 575)  
        self.frame_index = 0
        self.animation_time = 0.1
        self.current_time = 0
        self.dx = 0

    def update(self, dt):
        self.current_time += dt
        if self.dx != 0:
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.frame_index = (self.frame_index + 1) % NUM_FRAMES_TANK
                self.image = self.frames[self.frame_index]

        self.rect.x += self.dx

        # Mantener al tanque dentro de los límites
        if self.rect.left < 50:
            self.rect.left = 50
        if self.rect.right > 730:
            self.rect.right = 730

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = laser_frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame_index = 0
        self.animation_time = 0.05
        self.current_time = 0
        self.speed = 500  

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.frame_index = (self.frame_index + 1) % NUM_FRAMES_LASER
            self.image = self.frames[self.frame_index]

        self.rect.x += self.speed * dt  

        # Verificar colisiones del láser con los soldados
        colisionados = pygame.sprite.spritecollide(self, soldado_group, False)
        if colisionados:
            colisionados[0].kill_and_respawn()
            self.kill()
            global score
            score += 10

class Soldado(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = soldado_frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.frame_index = 0
        self.animation_time = 0.1
        self.current_time = 0
        self.respawn_count = 3  

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.frame_index = (self.frame_index + 1) % NUM_FRAMES_SOLDIER
            self.image = self.frames[self.frame_index]

    def kill_and_respawn(self):
        if self.respawn_count > 0:
            self.respawn_count -= 1
            self.rect.topleft = (random.randint(350, 750), 525)
        else:
            self.kill()

def mostrar_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, WHITE)
    text_rect = text.get_rect(center=(ANCHO // 2, ALTO // 2))
    screen.blit(text, text_rect)

def mostrar_puntaje():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Puntaje: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def mostrar_tiempo():
    font = pygame.font.Font(None, 36)
    text = font.render(f"Tiempo: {int(time_left)}", True, WHITE)
    screen.blit(text, (ANCHO - 150, 10))

def mostrar_selector_dificultad():
    font = pygame.font.Font(None, 74)
    title_text = font.render("Selecciona Dificultad", True, GREEN)
    title_rect = title_text.get_rect(center=(ANCHO // 2, ALTO // 4))
    screen.blit(title_text, title_rect)

    font = pygame.font.Font(None, 36)
    easy_text = font.render("1 - Facil", True, WHITE)
    medium_text = font.render("2 - Medio", True, WHITE)
    hard_text = font.render("3 - Dificil", True, WHITE)

    easy_rect = easy_text.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
    medium_rect = medium_text.get_rect(center=(ANCHO // 2, ALTO // 2))
    hard_rect = hard_text.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))

    screen.blit(menu_background, (0, 0))  # Dibujar el fondo del menú
    screen.blit(easy_text, easy_rect)
    screen.blit(medium_text, medium_rect)
    screen.blit(hard_text, hard_rect)

    pygame.display.flip()

    return easy_rect, medium_rect, hard_rect

# Variables del puntaje y temporizador
score = 0
time_left = 0  # Inicializar en 0 hasta que se seleccione dificultad

# Crear instancia del tanque y de los soldados
tanque = Tanque()
soldado1 = Soldado(360, 525)  # Posición del primer soldado
soldado2 = Soldado(480, 525)  
all_sprites = pygame.sprite.Group(tanque, soldado1, soldado2)
laser_group = pygame.sprite.Group()
soldado_group = pygame.sprite.Group(soldado1, soldado2)

# Reloj para controlar la velocidad de fotogramas
clock = pygame.time.Clock()

# Bucle principal de selección de dificultad
dificultad_seleccionada = False
while not dificultad_seleccionada:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dificultad_seleccionada = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:  # Facil
        time_left = 30
        dificultad_seleccionada = True
    elif keys[pygame.K_2]:  # Medio
        time_left = 15
        dificultad_seleccionada = True
    elif keys[pygame.K_3]:  # Dificil
        time_left = 10
        dificultad_seleccionada = True

    easy_rect, medium_rect, hard_rect = mostrar_selector_dificultad()

    pygame.display.flip()
    clock.tick(60)

# Bucle principal del juego
running = True
while running:
    dt = clock.tick(60) / 1000  # Segundos por frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser = Laser(tanque.rect.right, tanque.rect.centery)
                laser_group.add(laser)
                all_sprites.add(laser)

    keys = pygame.key.get_pressed()
    tanque.dx = (keys[pygame.K_d] - keys[pygame.K_a]) * 5
    all_sprites.update(dt)

    if len(soldado_group) == 0 or time_left <= 0:
        mostrar_game_over()
    else:
        # Reducir tiempo
        time_left -= dt

        # Dibujar fondo y elementos en la pantalla
        screen.blit(background, (0, 0)) 
        pygame.draw.rect(screen, GREEN, (300, 500, 300, 65)) 
        pygame.draw.polygon(screen, GREEN, [(300, 500), (400, 450), (500, 500)]) 
        pygame.draw.rect(screen, DARK_GREEN, (360, 471, 60, 30)) 

        # Dibujar el suelo negro
        pygame.draw.rect(screen, BLACK, (0, ALTO - 50, ANCHO, 50)) 

        # Dibujar las rayas blancas en el suelo
        for i in range(0, ANCHO, 50):
            pygame.draw.line(screen, WHITE, (i, ALTO - 25), (i + 25, ALTO - 25), 5)

        # Dibujar otros elementos como el tanque y los soldados
        all_sprites.draw(screen)
        mostrar_puntaje()
        mostrar_tiempo()

    pygame.display.flip()  # Actualizar la pantalla

pygame.quit()
sys.exit()
