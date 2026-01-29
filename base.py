import pygame
import os
from player import * 
from maps import *

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 38)

# États
phase = "menu"

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
HOVER = (100, 100, 100)

fps = 0
GameName = "PyKemon"
GameVersion = 0
TabState = "Loading"

posX = WIDTH // 2 - Dresseur.texture.get_width() // 2
posY = HEIGHT // 2 - Dresseur.texture.get_height() // 2

map = world_map

tile_size = WIDTH // len(map[0])


# Image de fond
#bg = pygame.image.load("sprites/x.png").convert()
#bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')


# CHANGEMENT DE PHASE

def set_phase(new_phase):
    global phase

    phase = new_phase

    if phase == "game":
        pass


# À faire AVANT la boucle while

def draw_map():
    for y, line in enumerate(map):
        for x, case in enumerate(line):
            # On utilise l'image déjà chargée et redimensionnée
            screen.blit(get_tile(case), (x * tile_size, y * tile_size))

# BOUCLE PRINCIPALE

def main():
    global fps

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_map()

        # MENU

        if phase == "menu":
            pass

        if phase == "game":
            screen.blit(Dresseur.texture,(posX, posY))

        elif phase == "lapemon":
            pass

        ## Lignes pour visualiser le centre de l'écran
        pygame.draw.rect(screen, RED, pygame.Rect(WIDTH/2,0,1,HEIGHT))
        pygame.draw.rect(screen, RED, pygame.Rect(0,HEIGHT/2,WIDTH,1))

        # Affichage des FPS
        pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')
        fps = int(clock.get_fps())

        pygame.display.flip()

    pygame.quit()



set_phase("game")

if __name__ == "__main__":
    main()
