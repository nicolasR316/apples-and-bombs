# Copyright (c) 2023 Nicolas Javier Ramirez Beltran
# This software is released under the MIT License
# https://opensource.org/licenses/MIT

# Importar las bibliotecas necesarias
import pygame
import random
import sys

# Definir constantes para valores que no cambiarán
# Es una buena práctica definir estas cosas como constantes en lugar de hard-codearlas
WIDTH = 480
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEEDY_MIN = 1
SPEEDY_MAX = 4
SCORE_LOSS = -2

# Inicializar Pygame y crear la ventana del juego
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de atrapar frutas")
clock = pygame.time.Clock()

# Cargar imágenes y otros recursos aquí, en lugar de en las clases o funciones
# Esto significa que los recursos sólo se cargarán una vez, en lugar de cada vez que se crea un objeto
fondo = pygame.image.load('fondo.jpg').convert()
img_cesta = pygame.image.load('cesta.png').convert_alpha()
img_fruta = pygame.image.load('fruta.png').convert_alpha()
img_bomba = pygame.image.load('bomb.png').convert_alpha()

# Crear el objeto de fuente aquí, para que sólo se cree una vez
font = pygame.font.Font(None, 36)

# Definir las clases de los sprites
# Hemos hecho que todas hereden de un objeto móvil base para evitar repetición de código
class ObjetoMovil(pygame.sprite.Sprite):
    def __init__(self, image):
        super(ObjetoMovil, self).__init__()
        self.image = pygame.transform.scale(image, (50, 50))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(SPEEDY_MIN, SPEEDY_MAX)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.reset()

class Jugador(ObjetoMovil):
    def __init__(self):
        super(Jugador, self).__init__(img_cesta)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -4
        if keystate[pygame.K_RIGHT]:
            self.speedx = 4
        self.rect.x += self.speedx

class Fruta(ObjetoMovil):
    def __init__(self):
        super(Fruta, self).__init__(img_fruta)

class Enemigo(ObjetoMovil):
    def __init__(self):
        super(Enemigo, self).__init__(img_bomba)

# Definir las funciones de juego y menú
# Estas funciones manejan la lógica principal del juego y el menú, respectivamente
def game_loop():
    jugador = Jugador()
    all_sprites = pygame.sprite.Group(jugador)
    frutas = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()

    for i in range(8):
        f = Fruta()
        all_sprites.add(f)
        frutas.add(f)
    for i in range(5):
        e = Enemigo()
        all_sprites.add(e)
        enemigos.add(e)

    score = 0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        hits = pygame.sprite.spritecollide(jugador, frutas, True)
        for hit in hits:
            score += 1
            hit.reset()

        hits = pygame.sprite.spritecollide(jugador, enemigos, True)
        for hit in hits:
            score += SCORE_LOSS
            hit.reset()

        if score <= SCORE_LOSS:
            running = False
            menu()

        screen.blit(fondo, (0, 0))
        all_sprites.draw(screen)

        text = font.render('Puntuación: ' + str(score), True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.flip()

def menu():
    title = font.render("Juego de Atrapar Frutas", True, WHITE)
    instructions = font.render("Presiona espacio para comenzar", True, WHITE)

    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 2 - title.get_height() / 2))
        screen.blit(instructions, (WIDTH / 2 - instructions.get_width() / 2, HEIGHT / 2 + title.get_height()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_loop()

        pygame.display.flip()

# Comienza con el menú del juego
menu()

# Limpia y sale cuando el juego ha terminado
pygame.quit()
