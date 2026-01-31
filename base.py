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

posX = WIDTH // 2 - Dresseur.sprite.get_width() // 2
posY = HEIGHT // 2 - Dresseur.sprite.get_height() // 2

map = world_map

tile_size = WIDTH // len(map[0])

# variables anim (déplacement joueur)
dresseur_anim = [i for i in range(16)]
print(dresseur_anim)


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
            # On récupère la surface pré-découpée
            tile_image = get_tile(case) 
            # Calcul de la position à l'écran
            screen.blit(tile_image, (x * tile_size, y * tile_size))


def get_sprite(sprite_sheet, case):
    global dresseur_anim, posX, posY

    width = sprite_sheet.get_width()
    coeff = 1.3 #coeff multiplicateur de taille
    sized_sheet = pygame.transform.scale(sprite_sheet, (100,100)) # fait en sorte que la grille soit carrée

    rect = pygame.Rect(case // 4 * width // 4, case // 4 * width // 4, width // 4, width // 4) 
    portion = pygame.transform.scale(sized_sheet.subsurface(rect), (64 * coeff, 80 * coeff))
    return portion



# BOUCLE PRINCIPALE

def main():
    global fps

    clock = pygame.time.Clock()
    running = True

    #on définit la position du joueur (centre) ainsi que son sprite
    Dresseur.sprite = get_sprite(Dresseur.sprite,0)
    posX = WIDTH // 2 - Dresseur.sprite.get_width() // 2
    posY = HEIGHT // 2 - Dresseur.sprite.get_height() // 2
    Dresseur.x = posX
    Dresseur.y = posY

    while running:
        keys = pygame.key.get_pressed()
        dt =  clock.tick(60) / 1000  # Delta time in milliseconds.

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
            Dresseur.update(keys, dt)
            screen.blit(Dresseur.sprite,(round(Dresseur.x), round(Dresseur.y))) #round pour éviter les tp du joueur

        elif phase == "lapemon":
            pass

        ## Lignes pour visualiser le centre de l'écran
        #pygame.draw.rect(screen, RED, pygame.Rect(WIDTH/2,0,1,HEIGHT))
        #pygame.draw.rect(screen, RED, pygame.Rect(0,HEIGHT/2,WIDTH,1))

        # Affichage des FPS
        pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')
        fps = int(clock.get_fps())

        pygame.display.flip()

    pygame.quit()



set_phase("game")

if __name__ == "__main__":
    main()
    