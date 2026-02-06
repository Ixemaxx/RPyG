import pygame
import os
import dresseur
import maps
from entity import *

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

try: # windows ou linux
    font = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 42)
except:
    font = pygame.font.Font("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 42)

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
map_entities = [] # une entité = un npc ou un item, représenté par sa classe Entity

tile_size = WIDTH // 16
# variables anim (déplacement joueur)
dresseur_anim = [] 

# vars dialogue

l1 = ""
l2 = ""
l3 = ""
curr_char = 0
curr_line = 0
IsDialogStarted = False
dialog = ""
max_diag_lines = 1
max_line_chars = 1
dialog_cooldown = 0
dialog_speed = 0.1

# Image de fond
#bg = pygame.image.load("sprites/x.png").convert()
#bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
fps = 0
pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')


# CHANGEMENT DE PHASE

def set_phase(new_phase):
    global phase

    phase = new_phase

    if phase == "game":
        pass


def set_menu(id):
    global menu

    if id == 0: # fermeture du menu
        menu = None
        dresseur.dresseur.Player.able = True
    else:
        menu = id
        dresseur.dresseur.Player.able = False

def pack_map():
    global map_layer, entities_layer, map_blit

    map_w = 1920
    map_h = 1080
    map_blit = pygame.Surface((map_w,map_h),pygame.SRCALPHA)

    map_blit.blit(maps.map_layer,(0,0))
    map_blit.blit(entities_layer,(0,0))


def get_dialog():
    global l1, l2, l3, curr_char, curr_line, IsDialogStarted, dialog, max_diag_lines, max_line_chars, dialog_cooldown

    if not dialog == "done" and dresseur.Player.interact != "dialog_end": # si le dialogue n'est pas fini et si le joueur n'a pas la possibilité de fermer le dialogue
        if not IsDialogStarted:
            IsDialogStarted = True
            dresseur.Player.interact = None
            curr_char = 0
            curr_line = 0 # 0 ou 1 (ligne 1 ou 2)
            l1, l2, l3 = "", "", ""

            dialog = dresseur.Player.dialog[0] # liste avec les lignes de texte

            max_diag_lines = len(dialog)

            max_line_chars = len(dialog[curr_line])
        else:
            curr_char += 1
            if curr_char >= max_line_chars:
                curr_line += 1
                if curr_line < max_diag_lines:
                    max_line_chars = len(dialog[curr_line])
                    curr_char = 0
                else:
                    dialog = "done" # état spécial pour déterminer la fin de la boucle
                    dresseur.Player.interact = "dialog_end"
                    IsDialogStarted = False
            
        if dialog != "done":        
            if curr_line == 0:
                l1 = f"{l1}{dialog[curr_line][curr_char]}"
            elif curr_line == 1:
                l2 = f"{l2}{dialog[curr_line][curr_char]}"
            else:
                l3 = f"{l3}{dialog[curr_line][curr_char]}"
        else:
            dialog = "" # reset du dialogue

        dialog_cooldown = dialog_speed

    



# BOUCLE PRINCIPALE

def main():
    global fps, cooldown, menu, TabState, GameName, GameVersion, map, map_blit, entities_layer, dialog_cooldown

    clock = pygame.time.Clock()
    running = True

    #on définit la position du joueur (centre) ainsi que son sprite
    dresseur.Player.x = WIDTH // 2 - dresseur.Player.sprite.get_width() // 2
    dresseur.Player.y = HEIGHT // 2 - dresseur.Player.sprite.get_height() // 2

    dresseur.Player.extract_anim()
    entities_layer,current_entities = draw_entities(maps.map_name)  

    TabState = maps.map_name
    pack_map()

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

        # Dans main.py, à l'intérieur de la boucle while running :

        if maps.isNewMap:
            maps.isNewMap = False
            TabState = maps.map_name
            # 1. On récupère les nouvelles entités de la nouvelle map
            entities_layer, current_entities = draw_entities(maps.map_name)  
            # 2. On reconstruit map_blit pour que screen.blit(map_blit) affiche le nouveau décor
            pack_map()
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        # MENU

        if phase == "menu":
            pass

        if phase == "game":

            screen.blit(map_blit,(0, 0)) # map_blit est la surface qui regroupe la tile_map et les entités (évite de faire 2 blits successifs)
            dresseur.Player.update(keys, dt, map, current_entities)
            screen.blit(dresseur.Player.sprite,(dresseur.Player.x, dresseur.Player.y)) #round pour éviter les tp du joueur
            #print(map_name) # attention ce print saccage les fps de loRdi
            if dresseur.Player.dialog != []: # si il y'a un dialogue en cours

                name_box = pygame.Rect(WIDTH * 0.30 , HEIGHT * 0.69, WIDTH * 0.12, HEIGHT * 0.07)

                dialog_box = pygame.Rect(WIDTH * 0.30 , HEIGHT * 0.75, WIDTH * 0.45, HEIGHT * 0.20)
                pygame.draw.rect(screen, BLACK, name_box)

                screen.blit(font.render(dresseur.Player.dialog[2], True, WHITE), (WIDTH * 0.31, HEIGHT * 0.7))
                pygame.draw.rect(screen, BLACK, dialog_box)

                if dialog_cooldown <= 0:
                    get_dialog()
                else:
                    dialog_cooldown -= 0.1

                screen.blit(font.render(l1, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.76))
                screen.blit(font.render(l2, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.82))
                screen.blit(font.render(l3, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.88))
                if dresseur.Player.interact == "dialog_end":
                    screen.blit(font.render("...", True, WHITE), (WIDTH * 0.72, HEIGHT * 0.89))
                

        elif phase == "lapemon":
            pass

        ## Lignes pour visualiser le centre de l'écran
        #pygame.draw.rect(screen, RED, pygame.Rect(WIDTH/2,0,1,HEIGHT))
        #pygame.draw.rect(screen, RED, pygame.Rect(0,HEIGHT/2,WIDTH,1))


        fps = int(clock.get_fps())
        pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')

        pygame.display.flip()

    pygame.quit()



set_phase("game")

if __name__ == "__main__":
    main()
    