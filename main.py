import pygame
import os
import dresseur
import maps
import entity_manager as entity_mgr

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))


font = pygame.font.Font("fonts/dogicapixelbold.otf", 40)
dia_font = pygame.font.Font("fonts/dogicapixelbold.otf", 30)
font2 = pygame.font.Font("fonts/PixeloidSans.ttf", 55)


# États
phase = "menu"

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (243, 87, 87) # background
DARK_RED = (179, 13, 13)
YELLOW = (243, 181, 87) # menu sac
DARK_YELLOW = (179, 176, 13)
GREEN = (91, 243, 87) # menu pokemon
DARK_GREEN = (13, 179, 30)
BLUE = (87, 181, 243) # pokédex
DARK_BLUE = (13, 152, 179)
PURPLE = (169, 87, 243) # sauvegarde
DARK_PURPLE = (113, 13, 179)
PINK = (243, 87, 202)
DARK_PINK = (179, 13, 130)
HOVER = (100, 100, 100)
close_tab_color = DARK_RED


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
btn_specs = {"resume":"REPRENDRE",
            "settings":"PARAMETRES",
            "sac": "SAC",
            "pykemon": "EQUIPE",
            "pykedex":"PYKEDEX"}


# Image de fond
#bg = pygame.image.load("sprites/x.png").convert()
#bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
fps = 0
pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')


# CHANGEMENT DE PHASE

def set_phase(new_phase):
    global phase, bg_color

    phase = new_phase

    if phase == "game":
        bg_color = RED


def set_menu(id): # [None,"pause","settings","sac","pykemon","pykedex"]
    global menu, menu_win, menu_color1, menu_color2, menu_colorh, btn_list, btn_txt_pos, menu_title_pos, menu_title

    menu = menus[id]

    if menu == None: # fermeture du menu
        dresseur.Player.able = True
        set_phase("game")
        
    else:
        dresseur.Player.able = False
        set_phase("menu")
        btn_list = [] # btn = [rect, action] action est aussi le texte affiché pour l'instant

        if menu == "pause":
            width = WIDTH // 3
            height = 0.3 * HEIGHT
            btn_w = 0.8 * width
            btn_h = 0.7 * height

        
            menu_win = pygame.Rect(0, 0, WIDTH, HEIGHT)
            btn_list=[["resume"],["settings"],["sac"],["pykemon"],["pykedex"]]
            

            menu_color1 = DARK_RED # fenetre du fond et texte dans les boutons
            menu_color2 = RED # boutons et textes hors des boutons
            menu_colorh = (255,0,0)

            menu_title_pos = [WIDTH * 0.01, HEIGHT * 0.015]
            
            # btns
            btn_txt_x = WIDTH / 2 - btn_w / 2
            btn_txt_y = HEIGHT * 0.3
            btn_txt_offest = HEIGHT * 0.09 # différence

            for i in range(len(btn_list)):
                if i < 3:
                    rect = pygame.Rect((WIDTH * 0.05 * (i + 1)) + (i * btn_w), (HEIGHT * 0.25), btn_w, btn_h) # ligne 1 menu
                else:
                    rect = pygame.Rect((WIDTH * 0.05 * (i - 2)) + ((i - 3) * btn_w), (HEIGHT * 0.55), btn_w, btn_h) # ligne 2 menu

                btn_list[i].append(rect)


            txt_w = 0 # largeur d'un texte, valeur déterminée dans la boucle principale
            btn_txt_pos = [((btn_txt_x + btn_w / 2) - txt_w / 2), (btn_txt_y + btn_h / 4), btn_txt_offest]

            # btn_list = [id, rect, texte affiché, largeur du texte]
            
            for btn in btn_list: # gestion améliorée de la liste pour mieux lire 
                texte = font.render(btn_specs[btn[0]], True, WHITE)
                btn.append(texte)
                btn.append(texte.get_width())

        elif menu == "ex-pause":
            width = 0.25 * WIDTH
            height = 0.5 * HEIGHT
            btn_w = 0.9 * width
            btn_h = 0.15 * height
        
            menu_win = pygame.Rect(WIDTH / 2 - width / 2, HEIGHT * 0.25, width, height)

            menu_color1 = DARK_RED # fenetre du fond et texte dans les boutons
            menu_color2 = RED # boutons et textes hors des boutons
            menu_colorh = HOVER

            menu_title_pos = [WIDTH * 0.01, HEIGHT * 0.015]
            
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
                texte = font.render(btn_specs[btn[1]], True, menu_color1)
                btn.append(texte)
                btn.append(texte.get_width())

            

def pack_map():
    global map_layer, map_blit #, entities_layer

    map_w = 1920
    map_h = 1080
    map_blit = pygame.Surface((map_w,map_h),pygame.SRCALPHA)

    map_blit.blit(maps.map_layer,(0,0))
    #map_blit.blit(entities_layer,(0,0))


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
    global fps, cooldown, menu, TabState, GameName, GameVersion, map, map_blit, dialog_cooldown, close_tab_color

    clock = pygame.time.Clock()
    running = True

    #on définit la position du joueur (centre) ainsi que son sprite
    dresseur.Player.x = WIDTH // 2 - dresseur.Player.sprite.get_width() // 2
    dresseur.Player.y = HEIGHT // 2 - dresseur.Player.sprite.get_height() // 2

    dresseur.Player.extract_anim()
    #entities_layer,current_entities = draw_entities(maps.map_id)  
    current_entities = entity_mgr.get_curr_entities(maps.map_id)

    TabState = maps.map_id
    pack_map()

    while running:
        keys = pygame.key.get_pressed()
        dt =  clock.tick(60) / 1000  # Delta time in milliseconds.

        if keys[pygame.K_x] and cooldown <= 0:
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
            #entities_layer, current_entities = draw_entities(maps.map_id)  
            # 2. On reconstruit map_blit pour que screen.blit(map_blit) affiche le nouveau décor
            pack_map()
            current_entities = entity_mgr.get_curr_entities(maps.map_id)
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(bg_color)

        # MENU

        if phase == "tilescreen":
            pass

        if phase == "game":
            
            screen.blit(map_blit,(0, 0)) # map_blit est la surface qui regroupe la tile_map et les entités (évite de faire 2 blits successifs)
            dresseur.Player.update(keys, dt, map, current_entities) # avant il y'avait aussi current_entities
            entity_mgr.all_sprites.update()
                
            try: # seuls les sprites avec une image adaptée peuvent être affichés
                entity_mgr.all_sprites.draw(screen)
            except:
                pass
                
            screen.blit(dresseur.Player.sprite,(dresseur.Player.x, dresseur.Player.y)) #round pour éviter les tp du joueur

            if dresseur.Player.dialog != []: # si il y'a un dialogue en cours
                
                name_box = pygame.Rect(WIDTH * 0.30 , HEIGHT * 0.69, WIDTH * 0.14, HEIGHT * 0.07)

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


        elif phase == "menu":
            if menu == "pause":
                pygame.draw.rect(screen, DARK_RED, (0, 0, WIDTH, HEIGHT * 0.1))
                close_tab = pygame.draw.rect(screen, close_tab_color, (0, HEIGHT * 0.9, WIDTH, HEIGHT * 0.1))
                if close_tab.collidepoint(mouse_pos):
                    close_tab_color = menu_colorh
                    if mouse_click:
                            set_menu(0)
                else:
                    close_tab_color = DARK_RED
                screen.blit(font2.render("Menu principal", True, menu_color2), (menu_title_pos[0], menu_title_pos[1]))
                screen.blit(font2.render("Retour", True, WHITE), (WIDTH * 0.45, HEIGHT * 0.92))

                for i, btn in enumerate(btn_list):
                    if btn[1].collidepoint(mouse_pos):
                        color2 = menu_colorh
                        if mouse_click:
                            set_menu(i)
                    else:
                        color2 = menu_color1
                    pygame.draw.rect(screen, color2, btn[1]) # color2
                    screen.blit(btn[2], (btn[1].centerx - btn[3] // 2, btn[1][1] + 20)) 


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
    