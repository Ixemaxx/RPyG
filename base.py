import pygame
import os
from player import * 

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

GameName = "PyKemon"
GameVersion = 0
TabState = "Loading"


# Image de fond
#bg = pygame.image.load("sprites/x.png").convert()
#bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
pygame.display.set_caption(f'{GameName} v{GameVersion} - {TabState}')


# CHANGEMENT DE PHASE

def set_phase(new_phase):
    global phase

    phase = new_phase

    if phase == "game":
        pass

# BOUCLE PRINCIPALE

def main():
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

        # MENU

        if phase == "menu":
            pass

        if phase == "game":
            screen.blit(x,y)

        elif phase == "lapemon":
            pass


        pygame.display.flip()

    pygame.quit()



set_phase("menu")

if __name__ == "__main__":
    main()
