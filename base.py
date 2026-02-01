import pygame
import os
from dresseur import * 
from maps import *

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

try:
    font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 38)
except:
    font = pygame.font.Font("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 38)

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

map = world_map
menu = None
cooldown = 0

tile_size = WIDTH // len(map[0])

# variables anim (déplacement joueur)
dresseur_anim = []


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

def draw_map():
    map_w = 1920
    map_h = 1080
    map_surface = pygame.Surface((map_w,map_h))


    for y, line in enumerate(map):
        for x, case in enumerate(line):
            # On récupère la surface pré-découpée
            tile_image = get_tile(case) 
            # Calcul de la position à l'écran
            map_surface.blit(tile_image, (x * tile_size , y * tile_size ))

    return map_surface.convert()

def set_menu(id):
    global menu

    if id == 0: # fermeture du menu
        menu = None
        Dresseur.able = True
    else:
        menu = id
        Dresseur.able = False
        

# BOUCLE PRINCIPALE

def main():
    global fps, cooldown, menu

    clock = pygame.time.Clock()
    running = True

    #on définit la position du joueur (centre) ainsi que son sprite
    Dresseur.x = WIDTH // 2 - Dresseur.sprite.get_width() // 2
    Dresseur.y = HEIGHT // 2 - Dresseur.sprite.get_height() // 2

    Dresseur.extract_anim()
    old_fps = 0 # benchmark à l'arrache pour print le fps max

    current_map = draw_map()

    while running:
        keys = pygame.key.get_pressed()
        dt =  clock.tick(60) / 1000  # Delta time in milliseconds.

        if keys[pygame.K_ESCAPE] and cooldown <= 0:
            cooldown = 3
            if menu == None:
                set_menu(1)
            else:
                set_menu(menu - 1)

        if cooldown >= 0: #cooldown utilisé pour les menus
            cooldown -= 0.1


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
            screen.blit(current_map,(0, 0))
            Dresseur.update(keys, dt, map)
            screen.blit(Dresseur.sprite,(round(Dresseur.x), round(Dresseur.y))) #round pour éviter les tp du joueur

        elif phase == "lapemon":
            pass

        ## Lignes pour visualiser le centre de l'écran
        #pygame.draw.rect(screen, RED, pygame.Rect(WIDTH/2,0,1,HEIGHT))
        #pygame.draw.rect(screen, RED, pygame.Rect(0,HEIGHT/2,WIDTH,1))

        # Affichage des FPS
        pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')
        fps = int(clock.get_fps())
        if fps > old_fps:
            old_fps = fps
            print(fps)

        pygame.display.flip()

    pygame.quit()



set_phase("game")

if __name__ == "__main__":
    main()
    