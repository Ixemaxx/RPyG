import pygame
import os
import dresseur
import maps
import entity_manager as entity_mgr
import creatures as pkmns
import random

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))


font = pygame.font.Font("fonts/dogicapixelbold.otf", 40)
dia_font = pygame.font.Font("fonts/dogicapixelbold.otf", 20)
font2 = pygame.font.Font("fonts/PixeloidSans.ttf", 55)
pykfont = pygame.font.Font("fonts/PixeloidSans.ttf", 24)
font3 = pygame.font.Font("fonts/dogicapixelbold.otf", 21)
lvlfont = pygame.font.Font("fonts/dogicapixelbold.otf", 26)

# musiques
wild_snd = pygame.mixer.Sound("sounds/wild.mp3")


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

# vars fight
temp_width = WIDTH / 4

fight_ui = [[BLUE, (0, HEIGHT * 0.9, temp_width, HEIGHT * 0.08), font.render("Fuir", True, WHITE)],
            [GREEN, (temp_width, HEIGHT * 0.9, temp_width, HEIGHT * 0.08), font.render("PyKemons", True, WHITE)],
            [YELLOW, (2 * temp_width, HEIGHT * 0.9, temp_width, HEIGHT * 0.08), font.render("Objets", True, WHITE)],
            [RED, (3 * temp_width, HEIGHT * 0.9, temp_width, HEIGHT * 0.08), font.render("Attaques", True, WHITE)]]
fuite = False




fps = 0
GameName = "PyKemon"
GameVersion = 0.3
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
end_cooldown = 1

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
action = False

# images combat

pbar = pygame.image.load("sprites/battle/hp_player.png")
advbar = pygame.image.load("sprites/battle/hp_adv.png")
pbar = pygame.transform.scale(pbar, (pbar.get_width() * 4, pbar.get_height() * 4))
advbar = pygame.transform.scale(advbar, (advbar.get_width() * 4, advbar.get_height() * 4))
hp_p = pykfont.render("-- / -- PV", True, WHITE)
hp_adv = pykfont.render("-- / -- PV", True, WHITE)
p_color = GREEN
adv_color = GREEN



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
        # le son est appelé à certains set_phase("game"), donc pas ici

    elif phase == "fight":
        IntroDone = False
        intro = True
        frame = 0
        dresseur.Player.encounter = opponent
        TabState = f"Combat contre..."
        pygame.mixer.music.stop()
        wild_snd.play()
        pygame.mixer.music.load("sounds/encounter.mp3")  # Charger la musique



        

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
    global menu, menu_win, menu_color1, menu_color2, menu_colorh, btn_list, btn_txt_pos, menu_title_pos, menu_title, cooldown, TabState, sous_menu, action, hp_p, hp_adv

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
    global l1, l2, l3, curr_char, curr_line, IsDialogStarted, dialog, max_diag_lines, max_line_chars, dialog_cooldown, GlobalDialog, IntroDone, end_cooldown

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
                if end_cooldown <= 0:
                    GlobalDialog = []
                    IntroDone = True
                    IsDialogStarted = False
                    end_cooldown = 1
                else:
                    end_cooldown -= 0.05
            

        if GlobalDialog == []:
            dialog_cooldown = dialog_speed
        else:
            dialog_cooldown = dialog_speed * 0.5
    
def fight_tab(tab):
    global fight_menu, GlobalDialog, fuite, l1, l2, l3, fight_color, hp_p, hp_adv, p_color, adv_color, name_p, name_adv, lvl_p, lvl_adv, name_p2 # blue=fuir, green=pkms, yellow=sac, red=atk

    p_ratio = dresseur.Player.team[0].hp / dresseur.Player.team[0].max_hp
    adv_ratio = dresseur.Player.encounter.hp / dresseur.Player.encounter.max_hp

    if p_ratio > 0.5:
        p_color = GREEN
    elif p_ratio > 0.15:
        p_color = YELLOW
    else:
        p_color = (255,0,0)

    if adv_ratio > 0.5:
        adv_color = GREEN
    elif adv_ratio > 0.15:
        adv_color = YELLOW
    else:
        adv_color = (255,0,0)

    hp_p = font3.render(f"{dresseur.Player.team[0].hp} / {dresseur.Player.team[0].max_hp} PV", True, WHITE)
    hp_adv = font3.render(f"{dresseur.Player.encounter.hp} / {dresseur.Player.encounter.max_hp} PV", True, WHITE)

    name_p = font3.render(f"{dresseur.Player.team[0].name}", True, WHITE)
    name_p2 = font3.render(f"{dresseur.Player.team[0].name}", True, BLACK)
    name_adv = font3.render(f"{dresseur.Player.team[0].name}", True, WHITE)

    lvl_p = lvlfont.render(f"{dresseur.Player.team[0].lvl}", True, WHITE)
    lvl_adv = lvlfont.render(f"{dresseur.Player.encounter.lvl}", True, WHITE)

    if tab == BLUE: # fuite
        if random.randint(1,100) >= 5: # 95% de chances de s'enfuir
            GlobalDialog = ["Vous prenez la fuite !"]
            fuite = True
        else:
            GlobalDialog = ["Vous n'avez pas réussi à fuir !"]
    elif tab == RED:
        rect = pygame.Rect(WIDTH * 0.7, HEIGHT * 0.5, WIDTH * 0.3, HEIGHT * 0.3)
        fight_menu = {"rect": rect,
                      "btns": [dresseur.Player.team[0].moveset[0], dresseur.Player.team[0].moveset[1], dresseur.Player.team[0].moveset[2], dresseur.Player.team[0].moveset[3]],
                      "title": font.render("Attaques", True, WHITE),
                      "color": RED,
                      "btns-text": [pykfont.render(dresseur.Player.team[0].moveset[0][0], True, WHITE), pykfont.render(dresseur.Player.team[0].moveset[1][0], True, WHITE), pykfont.render(dresseur.Player.team[0].moveset[2][0], True, WHITE), pykfont.render(dresseur.Player.team[0].moveset[3][0], True, WHITE)],
                      #DMG, PP, Precision, type
                      "subtext": [pykfont.render(f" {dresseur.Player.team[0].pps[0]} / {dresseur.Player.team[0].moveset[0][2]} PP", True, WHITE),
                                   pykfont.render(f" {dresseur.Player.team[0].pps[1]} / {dresseur.Player.team[0].moveset[1][2]} PP", True, WHITE),
                                 pykfont.render(f" {dresseur.Player.team[0].pps[2]} / {dresseur.Player.team[0].moveset[2][2]} PP", True, WHITE),
                                  pykfont.render(f" {dresseur.Player.team[0].pps[3]} / {dresseur.Player.team[0].moveset[3][2]} PP", True, WHITE)], 
                      "type": "fight"}
        

        fight_color = fight_menu["color"]





# BOUCLE PRINCIPALE

def main():
    global fps, cooldown, menu, sous_menu, TabState, GameName, GameVersion, map, map_blit, dialog_cooldown, close_tab_color, GlobalDialog, IntroDone, fuite, fight_color, action, p_color, adv_color, name_p, name_adv, lvl_p, lvl_adv, name_p2

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

    dresseur.Player.team[0] = pkmns.copy("punkromatides") # debug pour ne pas commencer à 0 pokémons
    for i in range(dresseur.Player.team[0].lvl - 1):
        dresseur.Player.team[0].lvlup()

    while running:
        keys = pygame.key.get_pressed()
        dt =  clock.tick(60) / 1000  # Delta time in milliseconds.

        if keys[pygame.K_x] and cooldown <= 0 and phase == "game":
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
                        fight_tab(RED)

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
                                view_rect = pygame.Rect(WIDTH * 0.025, HEIGHT * 0.15, WIDTH * 0.3, HEIGHT * 0.7)
                                moveset = btn[0].moveset # pour chopper les infos des attaques
                                pps = btn[0].pps
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
                            screen.blit(pykfont.render(f'- {moveset[i][0]}  [PP: {pps[i]} / {moveset[i][2]}]', True, WHITE), (WIDTH * 0.05, HEIGHT * (0.64 + 0.05 * i )))
                            i += 1
            else: 
                print("menu inconnu")


        elif phase == "fight":
            if intro and cooldown <= 0:
                get_intro_anim(frame)
            elif not intro and not IntroDone:
                TabState = f"Combat contre {dresseur.Player.encounter.name}"
                GlobalDialog = [f"Un {dresseur.Player.encounter.name} sauvage apparait !"]
                pygame.mixer.music.play(loops=-1, start=0.0)

            screen.blit(fight_bg,(0,0))


            if fuite and GlobalDialog == []:
                fuite = False
                pygame.mixer.stop()
                pygame.mixer.music.load("sounds/town.mp3")  # Charger la musique
                pygame.mixer.music.play(loops=-1, start=0.0)
                set_phase("game")

            if not intro and phase == "fight": # intro désigne l'animation d'intro du combat

                screen.blit(dresseur.Player.team[0].sprite[1], (WIDTH // 8, HEIGHT * 0.5))
                screen.blit(dresseur.Player.encounter.sprite[0], (WIDTH * 0.7, HEIGHT * 0.1))
                if IntroDone: # intro Done c'est quand le texte d'intro est terminé

                    if dresseur.Player.team[0].hp <= 0 and not fuite and GlobalDialog == []: #si pykemons ko
                        GlobalDialog = ["Vous n'avez plus de PyKemon en état de se battre. ", "Vous prenez la fuite !"]
                        fuite = True

                    if dresseur.Player.encounter.hp <= 0 and GlobalDialog == []:
                        exp = max(dresseur.Player.encounter.lvl - dresseur.Player.team[0].lvl, 1) * random.randint(20, 30)
                        GlobalDialog = [f"Le {dresseur.Player.encounter.name} adverse est K.O !", f"Vous gagnez {exp} points d'Exp."]
                        dresseur.Player.team[0].xp += exp
                        while dresseur.Player.team[0].xp > dresseur.Player.team[0].req_xp:
                            dresseur.Player.team[0].lvlup()

                        fuite = True
                        action = False

                    # barres d'hp
                    screen.blit(pbar, (0, HEIGHT * 0.45))
                    screen.blit(advbar, (WIDTH * 0.75, HEIGHT * 0.025))
                    pygame.draw.rect(screen, adv_color, (WIDTH * 0.75 + 224, HEIGHT * 0.05 + 9, 192 * (dresseur.Player.encounter.hp / dresseur.Player.encounter.max_hp), 8)) # barre de vie adversaire
                    pygame.draw.rect(screen, p_color, (WIDTH * 0 + 64, HEIGHT * 0.5 - 18, 192 * (dresseur.Player.team[0].hp / dresseur.Player.team[0].max_hp), 8)) # barre de vie joueur
                    screen.blit(hp_p, (20, HEIGHT * 0.505))
                    screen.blit(hp_adv, (WIDTH * 0.87, HEIGHT * 0.08))

                    screen.blit(name_p2, (20, HEIGHT * 0.45)) # ombre pour rendre plus visible le nom du pykemon du joueur
                    screen.blit(name_p, (21, HEIGHT * 0.453))
                    screen.blit(name_adv, (WIDTH * 0.77, HEIGHT * 0.025))

                    screen.blit(lvl_p, (383, HEIGHT * 0.453))
                    screen.blit(lvl_adv, (WIDTH * 0.936, HEIGHT * 0.0275))


                    if not action and not fuite: # on cache l'interface
                        # boutons de jeu
                        for element in fight_ui:
                            rect = pygame.draw.rect(screen, element[0], element[1]) # screen, couleur, rect, titre
                            screen.blit(element[2], (rect.centerx - element[2].get_width() / 2 , rect.centery - 22))
                            if rect.collidepoint(mouse_pos) and mouse_click:
                                fight_tab(element[0]) # le bouton est déterminé par sa couleur, tel un identifiant

                        # menu d'attaques, sac etc.
                        pygame.draw.rect(screen, fight_menu["color"], fight_menu["rect"]) #fight_menu est un dico
                        screen.blit(fight_menu["title"],(WIDTH * 0.72, HEIGHT * 0.52))

                        for i in range(len(fight_menu["btns"])): # différents menus (fight, sac, etc.)
                            if fight_color == RED: #Attaques
                                y_offset = HEIGHT * 0.58 if i < 2 else HEIGHT * 0.68
                                x_offset = WIDTH * 0.72 + (i % 2) * WIDTH * 0.127
                                btn = pygame.draw.rect(screen, BLACK, (x_offset, y_offset, WIDTH * 0.12, HEIGHT * 0.09))
                                screen.blit(fight_menu["btns-text"][i], (x_offset + 10, y_offset + 10))
                                screen.blit(fight_menu["subtext"][i], (x_offset + 10, y_offset + 40))

                                if btn.collidepoint(mouse_pos) and mouse_click and not action:
                                    action = True
                                    indice = i
                                    checkup = {"p_atk": False, "adv_atk": False, "p_pp": False, "adv_pp": False}

                    elif action == True: # si action == True
                        # le checkup permet de se situer dans la boucle

                        # on vérifie si les pykemons ont encore des pp (cas de lutte)
                        PcanPlay = False
                        for pp in dresseur.Player.team[0].pps:
                            if pp != 0:
                                PcanPlay = True

                        AdvcanPlay = False
                        for pp in dresseur.Player.encounter.pps:
                            if pp != 0:
                                AdvcanPlay = True

                        AdvChoice = random.randint(0, len(dresseur.Player.encounter.moveset) - 1)

                        if (dresseur.Player.team[0].pps[indice] > 0 or not PcanPlay) or checkup["p_atk"] == True: # PP joueur > 0 mais pas incapable d'attaquer
                            
                            if dresseur.Player.team[0].speed > dresseur.Player.encounter.speed: # on prend en compte la vitesse de chaque pykemon

                                if checkup["p_atk"] == False:
                                    if PcanPlay:
                                        dresseur.Player.team[0].pps[indice] -= 1
                                        GlobalDialog = dresseur.Player.team[0].atk(dresseur.Player.team[0].moveset[indice][5], dresseur.Player.encounter, "player")
                                        checkup["p_atk"] = True
                                        fight_tab(RED) # on actualise les pv etc.
                                    else:
                                        if checkup["p_pp"] == False:
                                            GlobalDialog = [f"Votre {dresseur.Player.team[0].name} n'a plus de", " capacité pour se battre."]
                                            checkup["p_pp"] = True
                            
                                        if GlobalDialog == []:
                                            GlobalDialog = dresseur.Player.team[0].atk("lutte", dresseur.Player.encounter, "player")
                                            checkup["p_atk"] = True
                                            fight_tab(RED) # on actualise les pv etc.
                                    
                                    
                                elif checkup["adv_atk"] == False and GlobalDialog == []:
                                    if AdvcanPlay:
                                        GlobalDialog = dresseur.Player.encounter.atk(dresseur.Player.encounter.moveset[AdvChoice][5], dresseur.Player.team[0], "bot")
                                        checkup["adv_atk"] = True
                                        fight_tab(RED) # on actualise les pv etc.
                                    else:
                                        if checkup["adv_pp"] == False:
                                            GlobalDialog = [f"Le {dresseur.Player.encounter.name} adverse n'a plus", "de capacité pour se battre."]
                                            checkup["adv_pp"] = True
                            
                                        if GlobalDialog == []:
                                            GlobalDialog = dresseur.Player.encounter.atk("lutte", dresseur.Player.team[0], "bot")
                                            checkup["adv_atk"] = True
                                            fight_tab(RED) # on actualise les pv etc.

                            else: #si adversaire plus rapide: 
                                               
                                if checkup["adv_atk"] == False:
                                    if AdvcanPlay:
                                        GlobalDialog = dresseur.Player.encounter.atk(dresseur.Player.encounter.moveset[AdvChoice][5], dresseur.Player.team[0], "bot")
                                        checkup["adv_atk"] = True
                                        fight_tab(RED) # on actualise les pv etc.
                                    else:
                                        if checkup["adv_pp"] == False:
                                            GlobalDialog = [f"Le {dresseur.Player.encounter.name} adverse n'a plus", "de capacité pour se battre."]
                                            checkup["adv_pp"] = True
                            
                                        if GlobalDialog == []:
                                            GlobalDialog = dresseur.Player.encounter.atk("lutte", dresseur.Player.team[0], "bot")
                                            checkup["adv_atk"] = True
                                            fight_tab(RED) # on actualise les pv etc.

                                elif checkup["p_atk"] == False and GlobalDialog == []:
                                        if PcanPlay:
                                            dresseur.Player.team[0].pps[indice] -= 1
                                            GlobalDialog = dresseur.Player.team[0].atk(dresseur.Player.team[0].moveset[indice][5], dresseur.Player.encounter, "player")
                                            checkup["p_atk"] = True
                                            fight_tab(RED) # on actualise les pv etc.
                                        else:
                                            if checkup["p_pp"] == False:
                                                GlobalDialog = [f"Votre {dresseur.Player.team[0].name} n'a plus de", " capacité pour se battre."]
                                                checkup["p_pp"] = True
                                
                                            if GlobalDialog == []:
                                                GlobalDialog = dresseur.Player.team[0].atk("lutte", dresseur.Player.encounter, "player")
                                                checkup["p_atk"] = True
                                                fight_tab(RED) # on actualise les pv etc.

        
                            # cas d'arrêt du tour
                            if GlobalDialog == [] and checkup["p_atk"] == True and checkup["adv_atk"] == True:
                                action = False
    
                        else:
                            # cas d'arrêt du tour si plus de pp
                            if checkup["p_pp"] == False:
                                GlobalDialog = ["Plus de PP pour cette capacité"]
                                checkup["p_pp"] = True
                                
                            if GlobalDialog == []:
                                action = False
            
                            
  

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
                    dialog_box = pygame.Rect(WIDTH * 0.30 , HEIGHT * 0.75, WIDTH * 0.48, HEIGHT * 0.20)
                    pygame.draw.rect(screen, BLACK, dialog_box)



                if dialog_cooldown <= 0:
                    get_dialog()
                else:
                    dialog_cooldown -= 0.1

                screen.blit(dia_font.render(l1, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.77))
                screen.blit(dia_font.render(l2, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.83))
                screen.blit(dia_font.render(l3, True, WHITE), (WIDTH * 0.31, HEIGHT * 0.89))
                if GlobalDialog == [] :
                    if dresseur.Player.interact == "dialog_end":
                        screen.blit(font.render("...", True, WHITE), (WIDTH * 0.70, HEIGHT * 0.89))
            



        fps = int(clock.get_fps())
        pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')

        pygame.display.flip()

    pygame.quit()

pygame.mixer.music.load("sounds/town.mp3")  # Charger la musique
pygame.mixer.music.play(loops=-1, start=0.0)
set_phase("game")

if __name__ == "__main__":
    main()
    