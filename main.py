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


font = pygame.font.Font("fonts/dogicapixelbold.otf", 40)
dia_font = pygame.font.Font("fonts/dogicapixelbold.otf", 30)
font2 = pygame.font.Font("fonts/PixeloidSans.ttf", 40)


# États
phase = "menu"

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
HOVER = (100, 100, 100)

fps = 0
GameName = "PyKemon"
GameVersion = 0.1
TabState = "Loading"

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

# vars menu

menu = None
menus = [None,"pause","settings","sac","pykemon","pykedex"]
btn_names = {"resume":"REPRENDRE", "settings":"PARAMETRES", "sac": "SAC", "pykemon": "EQUIPE","pykedex":"PYKEDEX"}


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


def set_menu(id): # [None,"pause","settings","sac","pykemon","pykedex"]
    global menu, menu_win, menu_color1, menu_color2, menu_colorh, btn_list, btn_txt_pos, menu_title_pos, menu_title

    menu = menus[id]

    if menu == None: # fermeture du menu
        dresseur.Player.able = True
    else:
        dresseur.Player.able = False
        btn_list = [] # btn = [rect, action] action est aussi le texte affiché pour l'instant

        if menu == "pause":
            width = 0.25 * WIDTH
            height = 0.5 * HEIGHT
            btn_w = 0.9 * width
            btn_h = 0.15 * height
        
            menu_win = pygame.Rect(WIDTH / 2 - width / 2, HEIGHT * 0.25, width, height)

            menu_color1 = BLACK # fenetre du fond et texte dans les boutons
            menu_color2 = WHITE # boutons et textes hors des boutons
            menu_colorh = HOVER

            menu_title = font2.render("Pause", True, menu_color2)
            title_size = menu_title.get_width()
            menu_title_pos = [(menu_win.centerx - title_size / 2), HEIGHT * 0.252]
            
            # btns
            btn_txt_x = WIDTH / 2 - btn_w / 2
            btn_txt_y = HEIGHT * 0.3
            btn_txt_offest = HEIGHT * 0.09 # différence

            btn_pause = pygame.Rect(btn_txt_x, btn_txt_y, btn_w, btn_h) # les 2 premiers arguments du btn haut sonts utilisés pour btn_txt_pos
            btn_settings = pygame.Rect(btn_txt_x, btn_txt_y + btn_txt_offest, btn_w, btn_h)
            btn_sac = pygame.Rect(btn_txt_x, btn_txt_y + 2 * btn_txt_offest, btn_w, btn_h)
            btn_pykemon = pygame.Rect(btn_txt_x, btn_txt_y + 3 * btn_txt_offest, btn_w, btn_h)
            btn_pykedex = pygame.Rect(btn_txt_x, btn_txt_y + 4 * btn_txt_offest, btn_w, btn_h)

            txt_w = 0 # largeur d'un texte, valeur déterminée dans la boucle principale
            btn_txt_pos = [((btn_txt_x + btn_w / 2) - txt_w / 2), (btn_txt_y + btn_h / 4), btn_txt_offest]

            # btn_list = [rect, id, texte affiché, largeur du texte]
            btn_list=[[btn_pause, "resume"],[btn_settings, "settings"],[btn_sac, "sac"],[btn_pykemon, "pykemon"],[btn_pykedex, "pykedex"]]
            
            for btn in btn_list: # gestion améliorée de la liste pour mieux lire 
                texte = font.render(btn_names[btn[1]], True, menu_color1)
                btn.append(texte)
                btn.append(texte.get_width())

            

def pack_map():
    global map_layer, entities_layer, map_blit

    map_w = 1920
    map_h = 1080
    map_blit = pygame.Surface((map_w,map_h),pygame.SRCALPHA)

    map_blit.blit(maps.map_layer,(0,0))
    map_blit.blit(entities_layer,(0,0))


# 100% par moi (petit flex donc je le précise)
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
    entities_layer,current_entities = draw_entities(maps.map_id)  

    TabState = maps.map_id
    pack_map()

    while running:
        keys = pygame.key.get_pressed()
        dt =  clock.tick(60) / 1000  # Delta time in milliseconds.

        if keys[pygame.K_ESCAPE] and cooldown <= 0:
            cooldown = 1
            if menu == None:
                set_menu(1)
            else:
                set_menu(0)

        if cooldown >= 0: #cooldown utilisé pour les menus
            cooldown -= 0.1


        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        # Dans main.py, à l'intérieur de la boucle while running :

        if maps.isNewMap:
            maps.isNewMap = False
            TabState = maps.SectionName[maps.map_id] # on utilise l'id de la map pour 
            # 1. On récupère les nouvelles entités de la nouvelle map
            entities_layer, current_entities = draw_entities(maps.map_id)  
            # 2. On reconstruit map_blit pour que screen.blit(map_blit) affiche le nouveau décor
            pack_map()
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        # MENU

        if phase == "tilescreen":
            pass

        if phase == "game":

            
            screen.blit(map_blit,(0, 0)) # map_blit est la surface qui regroupe la tile_map et les entités (évite de faire 2 blits successifs)
            if menu == None: # un chouilla d'optimisation pour loRdi
                dresseur.Player.update(keys, dt, map, current_entities)
            screen.blit(dresseur.Player.sprite,(dresseur.Player.x, dresseur.Player.y)) #round pour éviter les tp du joueur

            if dresseur.Player.dialog != []: # si il y'a un dialogue en cours

                name_box = pygame.Rect(WIDTH * 0.30 , HEIGHT * 0.69, WIDTH * 0.12, HEIGHT * 0.07)

                dialog_box = pygame.Rect(WIDTH * 0.30 , HEIGHT * 0.75, WIDTH * 0.45, HEIGHT * 0.20)
                pygame.draw.rect(screen, BLACK, name_box)

                screen.blit(font.render(dresseur.Player.dialog[2], True, WHITE), (WIDTH * 0.31, HEIGHT * 0.71))
                pygame.draw.rect(screen, BLACK, dialog_box)

                if dialog_cooldown <= 0:
                    get_dialog()
                else:
                    dialog_cooldown -= 0.1

                screen.blit(dia_font.render(l1, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.77))
                screen.blit(dia_font.render(l2, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.83))
                screen.blit(dia_font.render(l3, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.89))
                if dresseur.Player.interact == "dialog_end":
                    screen.blit(font.render("...", True, WHITE), (WIDTH * 0.70, HEIGHT * 0.89))

            if menu != None:
                pygame.draw.rect(screen, menu_color1, menu_win)
                screen.blit(font2.render("Menu", True, menu_color2), (menu_title_pos[0], menu_title_pos[1]))

                for i, btn in enumerate(btn_list):
                    if btn[0].collidepoint(mouse_pos):
                        color2 = menu_colorh
                        if mouse_click:
                            set_menu(i)
                    else:
                        color2 = menu_color2
                    pygame.draw.rect(screen, color2, btn[0])
                    screen.blit(btn[2], (btn_txt_pos[0] - btn[3] / 2, btn_txt_pos[1] + (i * btn_txt_pos[2]))) # btn_txt_pos est une liste avec [x, y, y_offset]
                

        elif phase == "pykedex":
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
    