import pygame
import sys
import time

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO, ALTO = 800, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Colisión de Carritos")

# Colores
VERDE = (0, 128, 0)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (192, 192, 192)

# Clase base para las entidades del juego
class Entidad:
    def __init__(self, x, y, ancho, alto, color):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        self.vivo = True

    def dibujar(self):
        if self.vivo:
            pygame.draw.rect(screen, self.color, self.rect)

# Clase para el movimiento
class Movimiento:
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy

    def mover(self, paredes):
        if hasattr(self, 'vivo') and self.vivo:
            nueva_pos = self.rect.move(self.dx, self.dy)
            if not any(nueva_pos.colliderect(pared) for pared in paredes):
                self.rect = nueva_pos
            else:
                self.dx = -self.dx
                self.dy = -self.dy

# Clase para los carritos que hereda de Entidad y Movimiento
class Carrito(Entidad, Movimiento):
    def __init__(self, x, y, color, dx=0, dy=0):
        Entidad.__init__(self, x, y, 50, 50, color)
        Movimiento.__init__(self, dx, dy)

# Clase para los rayos que hereda de Entidad y Movimiento
class Rayo(Entidad, Movimiento):
    def __init__(self, x, y, dx, dy, color):
        Entidad.__init__(self, x, y, 5, 5, color)
        Movimiento.__init__(self, dx, dy)

    def mover(self, paredes):
        nueva_pos = self.rect.move(self.dx, self.dy)
        if not any(nueva_pos.colliderect(pared) for pared in paredes):
            self.rect = nueva_pos
            return True
        return False

# Función para mostrar "Game Over"
def mostrar_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, NEGRO)
    screen.blit(text, (ANCHO // 2 - text.get_width() // 2, ALTO // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    sys.exit()

# Función para mostrar el menú de dificultad
def mostrar_menu():
    font = pygame.font.Font(None, 74)
    text = font.render("Selecciona Dificultad", True, NEGRO)
    screen.fill(VERDE)
    screen.blit(text, (ANCHO // 2 - text.get_width() // 2, ALTO // 4))

    opciones = ["1. Fácil", "2. Medio", "3. Difícil"]
    for i, opcion in enumerate(opciones):
        text = font.render(opcion, True, NEGRO)
        screen.blit(text, (ANCHO // 2 - text.get_width() // 2, ALTO // 2 + i * 100))

    pygame.display.flip()
    seleccionando = True
    while seleccionando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "Fácil"
                elif event.key == pygame.K_2:
                    return "Medio"
                elif event.key == pygame.K_3:
                    return "Difícil"

# Función principal del juego
def juego(dificultad):
    # Crear los carritos según la dificultad
    if dificultad == "Fácil":
        carrito1 = Carrito(100, 100, ROJO)
        carrito2 = Carrito(600, 400, AZUL, dx=2, dy=2)
    elif dificultad == "Medio":
        carrito1 = Carrito(100, 100, ROJO)
        carrito2 = Carrito(600, 400, AZUL, dx=4, dy=4)
    elif dificultad == "Difícil":
        carrito1 = Carrito(100, 100, ROJO)
        carrito2 = Carrito(600, 400, AZUL, dx=5, dy=5)
        carrito3 = Carrito(350, 280, AZUL, dx=-5, dy=-5)

    # Lista de rayos disparados
    rayos = []

    # Definir el laberinto como una lista de rectángulos
    paredes = [
        pygame.Rect(50, 50, 700, 10),
        pygame.Rect(50, 50, 10, 500),
        pygame.Rect(50, 540, 700, 10),
        pygame.Rect(740, 50, 10, 500),
        pygame.Rect(200, 50, 10, 300),
        pygame.Rect(400, 200, 10, 340),
        pygame.Rect(600, 50, 10, 300),
    ]

    # Reloj para controlar la velocidad de fotogramas
    clock = pygame.time.Clock()

    # Bucle principal del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Disparar rayos con espacio para carrito1 y LSHIFT para carrito2
                if event.key == pygame.K_SPACE:
                    rayos.append(Rayo(carrito1.rect.centerx, carrito1.rect.centery, 10, 0, ROJO))
                elif event.key == pygame.K_LSHIFT:
                    rayos.append(Rayo(carrito2.rect.centerx, carrito2.rect.centery, -10, 0, AZUL))
                if dificultad == "Difícil" and event.key == pygame.K_LSHIFT:
                    rayos.append(Rayo(carrito3.rect.centerx, carrito3.rect.centery, -10, 0, AZUL))

        # Fondo verde
        screen.fill(VERDE)

        # Dibujar paredes del laberinto
        for pared in paredes:
            pygame.draw.rect(screen, GRIS, pared)

        # Movimiento del carrito rojo (controlado por las teclas WASD)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            carrito1.dx = -5
            carrito1.dy = 0
        elif keys[pygame.K_d]:
            carrito1.dx = 5
            carrito1.dy = 0
        elif keys[pygame.K_w]:
            carrito1.dx = 0
            carrito1.dy = -5
        elif keys[pygame.K_s]:
            carrito1.dx = 0
            carrito1.dy = 5

        carrito1.mover(paredes)

        # Movimiento automático de los carritos azules
        carrito2.mover(paredes)
        if dificultad == "Difícil":
            carrito3.mover(paredes)

        # Mover y dibujar los rayos
        for rayo in rayos[:]:
            if not rayo.mover(paredes):
                rayos.remove(rayo)
            rayo.dibujar()

        # Colisión de rayos con carritos
        for rayo in rayos:
            if rayo.color == ROJO and rayo.rect.colliderect(carrito2.rect):
                carrito2.vivo = False
            if rayo.color == AZUL and rayo.rect.colliderect(carrito1.rect):
                carrito1.vivo = False
                mostrar_game_over()
            if dificultad == "Difícil" and rayo.color == ROJO and rayo.rect.colliderect(carrito3.rect):
                carrito3.vivo = False

        # Verificar si los carritos azules están destruidos
        if dificultad == "Difícil" and not carrito2.vivo and not carrito3.vivo:
            mostrar_game_over()

        # Dibujar los carritos
        carrito1.dibujar()
        carrito2.dibujar()
        if dificultad == "Difícil":
            carrito3.dibujar()

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(30)

# Mostrar el menú de selección de dificultad
dificultad_seleccionada = mostrar_menu()

# Iniciar el juego con la dificultad seleccionada
if dificultad_seleccionada is not None:
    juego(dificultad_seleccionada)
else:
    print("No se seleccionó ninguna dificultad.")
    pygame.quit()
    sys.exit()
