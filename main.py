import pygame
import os
from dresseur import * 
from maps import *
from entity import *

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

menu = None
cooldown = 0
map = lil_garden
map_name = "lil_garden"
map_entities = [] # une entité = un npc ou un item, représenté par sa classe Entity

tile_size = WIDTH // 16
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


def change_tab(State):
    TabState = State
    pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')

def set_menu(id):
    global menu

    if id == 0: # fermeture du menu
        menu = None
        Player.able = True
    else:
        menu = id
        Player.able = False
        

# BOUCLE PRINCIPALE

def main():
    global fps, cooldown, menu, TabState, GameName, GameVersion

    clock = pygame.time.Clock()
    running = True

    #on définit la position du joueur (centre) ainsi que son sprite
    Player.x = WIDTH // 2 - Player.sprite.get_width() // 2
    Player.y = HEIGHT // 2 - Player.sprite.get_height() // 2

    Player.extract_anim()
    
    map_layer = draw_map()
    entities_layer,current_entities = draw_entities(map_name)  

    change_tab(map_name)

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
            screen.blit(map_layer,(0, 0))
            screen.blit(entities_layer,(0,0))
            Player.update(keys, dt, map, current_entities)
            screen.blit(Player.sprite,(round(Player.x), round(Player.y))) #round pour éviter les tp du joueur

        elif phase == "lapemon":
            pass

        ## Lignes pour visualiser le centre de l'écran
        #pygame.draw.rect(screen, RED, pygame.Rect(WIDTH/2,0,1,HEIGHT))
        #pygame.draw.rect(screen, RED, pygame.Rect(0,HEIGHT/2,WIDTH,1))


        pygame.display.flip()

    pygame.quit()



set_phase("game")

if __name__ == "__main__":
    main()
    