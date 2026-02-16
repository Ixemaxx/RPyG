import pygame
import os
import dresseur
import maps
import entity_manager as entity_mgr
import creatures as pkmns

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
pykfont = pygame.font.Font("fonts/PixeloidSans.ttf", 27)


# États
phase = "menu"

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (243, 87, 87) # background
DARK_RED = (179, 13, 13)
YELLOW = (243, 181, 87) # menu sac
DARK_YELLOW = (179, 176, 13)
GREEN = (91, 223, 87) # menu pokemon
DARK_GREEN = (13, 179, 30)
BLUE = (87, 181, 243) # pokédex
DARK_BLUE = (13, 152, 179)
PURPLE = (169, 87, 243) # sauvegarde
DARK_PURPLE = (113, 13, 179)
PINK = (243, 87, 202)
DARK_PINK = (179, 13, 130)
HOVER = (100, 100, 100)
close_tab_color = DARK_RED
menu_color2 = RED


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

GlobalDialog = [] # variable de dialogue non reliée au joueur, en combat par exemple

# vars menu

menu = "None"
menus = ["None","pause","pykemon","sac","pykedex","settings","online","save"]
btn_specs = {"save":"SAUVEGARDER",
            "settings":"PARAMETRES",
            "sac": "SAC",
            "pykemon": "EQUIPE",
            "pykedex":"PYKEDEX",
            "online": "Multijoueur"}

# vars combat

fight_bg = pygame.image.load("sprites/battle/battle_intro.png")
fight_intro = []
intro = True
for i in range(8): # animation de lancement de combat
    surface = pygame.Rect(0,i * 1272 / 8,159,1272 / 8)
    portion = pygame.transform.scale(fight_bg.subsurface(surface), (WIDTH,HEIGHT))
    fight_intro.append(portion)

fight_bg = fight_intro[0]
frame = 0

# images combat

pbar = pygame.image.load("sprites/battle/hp_player.png")
advbar = pygame.image.load("sprites/battle/hp_adv.png")
pbar = pygame.transform.scale(pbar, (pbar.get_width() * 4, pbar.get_height() * 4))
advbar = pygame.transform.scale(advbar, (advbar.get_width() * 4, advbar.get_height() * 4))



# Image de fond
#bg = pygame.image.load("sprites/x.png").convert()
#bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
fps = 0
pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')


# CHANGEMENT DE PHASE

def set_phase(new_phase, opponent=None):
    global phase, bg_color, TabState, intro, frame, IntroDone

    phase = new_phase

    if phase == "game":
        TabState = maps.SectionName[maps.map_id]
        bg_color = RED

    elif phase == "fight":
        IntroDone = False
        intro = True
        frame = 0
        dresseur.Player.encounter = opponent
        TabState = f"Combat contre..."

def get_intro_anim(id):
    global frame, intro, fight_bg, cooldown

    fight_bg = fight_intro[id]
    frame = id + 1
    cooldown = 0.6
    if frame > len(fight_intro) - 1:
        intro = False
        frame = 0
        fight_bg = pygame.transform.scale(pygame.image.load("sprites/battle/Forest.png"),(WIDTH,HEIGHT))



def set_menu(id): # ["pykemon","sac","pykedex","settings","online","save"]
    global menu, menu_win, menu_color1, menu_color2, menu_colorh, btn_list, btn_txt_pos, menu_title_pos, menu_title, cooldown, TabState, sous_menu

    menu = menus[id]
    sous_menu = None
    cooldown = 1

    if menu == "None": # fermeture du menu
        dresseur.Player.able = True
        set_phase("game")
        
    else:
        TabState = f"Dans le menu {menu}"
        dresseur.Player.able = False
        set_phase("menu")
        btn_list = [] # btn = [rect, action] action est aussi le texte affiché pour l'instant

        if menu == "pause":
            width = WIDTH // 3
            height = 0.3 * HEIGHT
            btn_w = 0.8 * width
            btn_h = 0.7 * height

        
            menu_win = pygame.Rect(0, 0, WIDTH, HEIGHT)
            btn_list=[["pykemon"],["sac"],["pykedex"],["settings"],["online"],["save"]]
            btn_datas = [[GREEN,DARK_GREEN], [YELLOW,DARK_YELLOW], [(255,0,0),DARK_RED], [PINK, DARK_PINK], [BLUE, DARK_BLUE], [PURPLE, DARK_PURPLE]]

            menu_color1 = DARK_RED # fenetre du fond et texte dans les boutons
            menu_color2 = RED # boutons et textes hors des boutons
            menu_colorh = (255,0,0)

            menu_title = "Menu principal"
            menu_title_pos = [WIDTH * 0.01, HEIGHT * 0.015]
            
            # btns
            btn_txt_x = WIDTH / 2 - btn_w / 2
            btn_txt_y = HEIGHT * 0.3
            btn_txt_offest = HEIGHT * 0.09 # différence

            for i in range(len(btn_list)): # liste = [id, rect, texte, width, colors]
                if i < 3:
                    rect = pygame.Rect((WIDTH * 0.05 * (i + 1)) + (i * btn_w), (HEIGHT * 0.25), btn_w, btn_h) # ligne 1 menu
                else:
                    rect = pygame.Rect((WIDTH * 0.05 * (i - 2)) + ((i - 3) * btn_w), (HEIGHT * 0.55), btn_w, btn_h) # ligne 2 menu

                texte = font.render(btn_specs[btn_list[i][0]], True, WHITE)

                btn_list[i].append(rect)
                btn_list[i].append(texte)
                btn_list[i].append(texte.get_width())
                btn_list[i].append(btn_datas[i])


            txt_w = 0 # largeur d'un texte, valeur déterminée dans la boucle principale
            btn_txt_pos = [((btn_txt_x + btn_w / 2) - txt_w / 2), (btn_txt_y + btn_h / 4), btn_txt_offest]

        if menu == "pykemon":
            width = WIDTH // 3
            height = 0.3 * HEIGHT
            btn_w = 0.8 * width
            btn_h = 0.7 * height

        
            menu_win = pygame.Rect(0, 0, WIDTH, HEIGHT)
            btn_list = [[dresseur.Player.team[i]] for i in range(6)] # on récupère les infos de l'équipe du joueur (None par défaut)
            btn_datas = [[(0,255,0),DARK_GREEN]]

            menu_color1 = DARK_GREEN # fenetre du fond et texte dans les boutons
            menu_color2 = GREEN # boutons et textes hors des boutons
            menu_colorh = (0,255,0)

            menu_title = "Gestion de l'équipe"
            menu_title_pos = [WIDTH * 0.01, HEIGHT * 0.015]
            
            # btns
            btn_txt_x = WIDTH / 2 - btn_w / 2
            btn_txt_y = HEIGHT * 0.3
            btn_txt_offest = HEIGHT * 0.09 # différence

            for i in range(len(btn_list)): # liste = [id, rect, texte, width, colors]
                if i < 3:
                    rect = pygame.Rect((WIDTH * 0.05 * (i + 1)) + (i * btn_w), (HEIGHT * 0.25), btn_w, btn_h) # ligne 1 menu
                else:
                    rect = pygame.Rect((WIDTH * 0.05 * (i - 2)) + ((i - 3) * btn_w), (HEIGHT * 0.55), btn_w, btn_h) # ligne 2 menu

                try:
                    name = str(btn_list[i][0].name)
                    texte = font.render(name, True, WHITE)
                except:
                    texte = font.render("Vide", True, WHITE)

                btn_list[i].append(rect)
                btn_list[i].append(texte)
                btn_list[i].append(texte.get_width())
                btn_list[i].append(btn_datas[0])


            txt_w = 0 # largeur d'un texte, valeur déterminée dans la boucle principale
            btn_txt_pos = [((btn_txt_x + btn_w / 2) - txt_w / 2), (btn_txt_y + btn_h / 4), btn_txt_offest]
                
                    

            

def pack_map():
    global map_layer, map_blit #, entities_layer

    map_w = 1920
    map_h = 1080
    map_blit = pygame.Surface((map_w,map_h),pygame.SRCALPHA)

    map_blit.blit(maps.map_layer,(0,0))
    #map_blit.blit(entities_layer,(0,0))


# 100% par moi sans aucun tuto (petit flex donc je le précise)
def get_dialog():
    global l1, l2, l3, curr_char, curr_line, IsDialogStarted, dialog, max_diag_lines, max_line_chars, dialog_cooldown, GlobalDialog, IntroDone

    if not dialog == "done" and dresseur.Player.interact != "dialog_end": # si le dialogue n'est pas fini et si le joueur n'a pas la possibilité de fermer le dialogue

        if not IsDialogStarted:
            IsDialogStarted = True
            if GlobalDialog == []: # si c'est un dialogue du joueur (pas en combat, par ex)
                dresseur.Player.interact = None
            curr_char = 0
            curr_line = 0 # 0 ou 1 (ligne 1 ou 2)
            l1, l2, l3 = "", "", ""

            if GlobalDialog == []:
                dialog = dresseur.Player.dialog[0] # liste avec les lignes de texte
            else:
                dialog = GlobalDialog

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
                    if GlobalDialog == []:
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
            if GlobalDialog != []:
                GlobalDialog = []
                IntroDone = True
            

        if GlobalDialog == []:
            dialog_cooldown = dialog_speed
        else:
            dialog_cooldown = dialog_speed * 1.2
    


# BOUCLE PRINCIPALE

def main():
    global fps, cooldown, menu, sous_menu, TabState, GameName, GameVersion, map, map_blit, dialog_cooldown, close_tab_color, GlobalDialog, IntroDone

    clock = pygame.time.Clock()
    running = True

    #on définit la position du joueur (centre) ainsi que son sprite
    dresseur.Player.x = WIDTH // 2 - dresseur.Player.sprite.get_width() // 2
    dresseur.Player.y = HEIGHT // 2 - dresseur.Player.sprite.get_height() // 2
    dresseur.Player.selfbox = pygame.Rect(dresseur.Player.x, dresseur.Player.y, 98, 98)

    dresseur.Player.extract_anim()
    #entities_layer,current_entities = draw_entities(maps.map_id)  
    current_entities = entity_mgr.get_curr_entities(maps.map_id)

    TabState = maps.map_id
    pack_map()

    dresseur.Player.team[0] = pkmns.punkromatides # debug pour ne pas commencer à 0 pokémons

    while running:
        keys = pygame.key.get_pressed()
        dt =  clock.tick(60) / 1000  # Delta time in milliseconds.

        if keys[pygame.K_x] and cooldown <= 0:
            cooldown = 1
            if menu == "None":
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

        screen.fill(menu_color2)

        # MENU

        if phase == "tilescreen":
            pass

        if phase == "game":
            
            screen.blit(map_blit,(0, 0)) # map_blit est la surface qui regroupe la tile_map et les entités (évite de faire 2 blits successifs)
            dresseur.Player.update(keys, dt, map, current_entities) # avant il y'avait aussi current_entities
            entity_mgr.all_sprites.update()

            if dresseur.Player.encounter == "get":
                for entity in entity_mgr.entities:
                    if entity.type == "grass" and entity.map == maps.map_id:
                        set_phase("fight", opponent=entity.get_creature())

            #for entity in entity_mgr.entities:
            #    try:
            #        pygame.draw.rect(screen, GREEN, entity.npc.selfbox)
            #    except:
            #        pass
            #pygame.draw.rect(screen, RED, dresseur.Player.selfbox)
                
            try: # seuls les sprites avec une image adaptée peuvent être affichés
                entity_mgr.all_sprites.draw(screen)
            except:
                pass
                
            screen.blit(dresseur.Player.sprite,(dresseur.Player.x, dresseur.Player.y)) #round pour éviter les tp du joueur
            


        elif phase == "menu":
            color2 = RED

            # bandeau du haut des menus
            pygame.draw.rect(screen,menu_color1, (0, 0, WIDTH, HEIGHT * 0.1))
            close_tab = pygame.draw.rect(screen, close_tab_color, (0, HEIGHT * 0.9, WIDTH, HEIGHT * 0.1))
            if close_tab.collidepoint(mouse_pos):
                close_tab_color = menu_colorh
                if mouse_click and cooldown <= 0:
                    cooldown = 1
                    if menu == "pause":
                        set_menu(0)
                    else:
                        if sous_menu == None:
                            set_menu(1)
                        else:
                            if sous_menu > 1:
                                sous_menu -= 1
                            else:
                                sous_menu = None
            else:
                close_tab_color = menu_color1

            # nom du menu
            screen.blit(font2.render(menu_title, True, WHITE), (menu_title_pos[0], menu_title_pos[1]))
            screen.blit(font2.render("Retour", True, WHITE), (WIDTH * 0.45, HEIGHT * 0.92))

            if menu == "pause":

                for i, btn in enumerate(btn_list):
                    if btn[1].collidepoint(mouse_pos):
                        color2 = btn[4][0]
                        if mouse_click:
                            set_menu(i + 2)   
                    else:
                        color2 = btn[4][1]
                    pygame.draw.rect(screen, color2, btn[1]) # color2
                    screen.blit(btn[2], (btn[1].centerx - btn[3] // 2, btn[1][1] + 20)) 

            elif menu == "pykemon": # vue d'un seul pokémon de l'équipe
                if sous_menu == None: # on vérifie le sous menu => None = équiê, 1 = vue d'un pokémon
                    for i, btn in enumerate(btn_list):
                        if btn[1].collidepoint(mouse_pos):
                            color2 = btn[4][0]
                            if mouse_click and cooldown <= 0 and not btn[0] == None: # si on clique sur un pokémon de l'équipe et que ce pokémon n'est pas vide
                                cooldown = 1
                                sous_menu = i + 1 
                                name = pykfont.render(f"PyKemon: {btn[0].name}",  True, WHITE)
                                level = pykfont.render(f"Niveau: {str(btn[0].lvl)}", True, WHITE)
                                moves = pykfont.render("Attaques:", True, WHITE)
                                hp = pykfont.render(f"PVs: {btn[0].hp} / {btn[0].max_hp}", True, WHITE)
                                atk = pykfont.render(f"Dégâts: {btn[0].attack}", True, WHITE)
                                defense = pykfont.render(f"Défense: {btn[0].defense}", True, WHITE)
                                types = pykfont.render(f"Type: {btn[0].type}", True, WHITE)
                                sprite = btn[0].sprite[0] # sprite de face
                                sprite = pygame.transform.scale(sprite,(sprite.get_width() * 5,sprite.get_height() * 5))
                                view_rect = pygame.Rect(WIDTH * 0.025, HEIGHT * 0.15, WIDTH * 0.3, HEIGHT * 0.7)
                                moveset = btn[0].moveset # pour chopper les infos des attaques
                                tab_name = font.render("Infos Pykemon", WHITE, True)
                                
                        else:
                            color2 = btn[4][1]
                        pygame.draw.rect(screen, color2, btn[1]) # color2
                        screen.blit(btn[2], (btn[1].centerx - btn[3] // 2, btn[1][1] + 20)) 
                else:
                    # Menu infos du pykemon
                    pygame.draw.rect(screen, menu_color1, view_rect)
                    screen.blit(tab_name, (WIDTH * 0.04, HEIGHT * 0.17))
                    screen.blit(name, (WIDTH * 0.04, HEIGHT * 0.24))
                    screen.blit(types, (WIDTH * 0.04, HEIGHT * 0.29))
                    screen.blit(level, (WIDTH * 0.04, HEIGHT * 0.34))
                    screen.blit(hp, (WIDTH * 0.04, HEIGHT * 0.39))
                    screen.blit(types, (WIDTH * 0.04, HEIGHT * 0.44))
                    screen.blit(atk, (WIDTH * 0.04, HEIGHT * 0.49))
                    screen.blit(defense, (WIDTH * 0.04, HEIGHT * 0.54))
                    screen.blit(moves, (WIDTH * 0.04, HEIGHT * 0.59))
                    screen.blit(sprite, (WIDTH * 0.9 - sprite.get_width() // 2, HEIGHT * 0.1))
                    i = 0
                    for move in moveset: # boucle qui affiche les attaques avec leurs PPs
                        if move != None:
                            screen.blit(pykfont.render(f'- {moveset[i][0]}  [PP: ? / {moveset[i][2]}]', True, WHITE), (WIDTH * 0.05, HEIGHT * (0.64 + 0.05 * i )))
                            i += 1
            else: 
                print("menu inconnu")


        elif phase == "fight":
            if intro and cooldown <= 0:
                get_intro_anim(frame)
            elif not intro and not IntroDone:
                TabState = f"Combat contre {dresseur.Player.encounter.name}"
                GlobalDialog = [f"Un {dresseur.Player.encounter.name}","sauvage apparait !"]

            screen.blit(fight_bg,(0,0))

            if not intro: # intro désigne l'animation d'intro du combat
                screen.blit(dresseur.Player.team[0].sprite[1], (WIDTH // 8, HEIGHT * 0.5))
                screen.blit(dresseur.Player.encounter.sprite[0], (WIDTH * 0.7, HEIGHT * 0.1))
                if IntroDone: # intro Done c'est quand le texte d'intro est terminé
                    screen.blit(pbar, (0, HEIGHT * 0.45))
                    screen.blit(advbar, (WIDTH * 0.75, HEIGHT * 0.025))


        ## Lignes pour visualiser le centre de l'écran
        #pygame.draw.rect(screen, RED, pygame.Rect(WIDTH/2,0,1,HEIGHT))
        #pygame.draw.rect(screen, RED, pygame.Rect(0,HEIGHT/2,WIDTH,1))

        if dresseur.Player.dialog != [] or GlobalDialog != []: # si il y'a un dialogue en cours
                
                if GlobalDialog == []:
                    name_box = pygame.Rect(WIDTH * 0.30 , HEIGHT * 0.69, WIDTH * 0.14, HEIGHT * 0.07)

                    dialog_box = pygame.Rect(WIDTH * 0.30 , HEIGHT * 0.75, WIDTH * 0.45, HEIGHT * 0.20)
                    pygame.draw.rect(screen, BLACK, name_box)

                    screen.blit(font.render(dresseur.Player.dialog[2], True, WHITE), (WIDTH * 0.31, HEIGHT * 0.71))
                    pygame.draw.rect(screen, BLACK, dialog_box)
                else:
                    dialog_box = pygame.Rect(WIDTH * 0.30 , HEIGHT * 0.75, WIDTH * 0.45, HEIGHT * 0.20)
                    pygame.draw.rect(screen, BLACK, dialog_box)



                if dialog_cooldown <= 0:
                    get_dialog()
                else:
                    dialog_cooldown -= 0.1

                screen.blit(dia_font.render(l1, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.77))
                screen.blit(dia_font.render(l2, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.83))
                screen.blit(dia_font.render(l3, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.89))
                if GlobalDialog == []:
                    if dresseur.Player.interact == "dialog_end":
                        screen.blit(font.render("...", True, WHITE), (WIDTH * 0.70, HEIGHT * 0.89))

        fps = int(clock.get_fps())
        pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')

        pygame.display.flip()

    pygame.quit()


set_phase("game")

if __name__ == "__main__":
    main()
    