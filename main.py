import pygame
import os
import dresseur
import maps
import entity_manager as entity_mgr
import creatures as pkmns
import random
import assets
import copy

# Initialisation de Pygame
pygame.init()
pygame.mixer.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.mixer.music.set_volume(0.75)

WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))


font = pygame.font.Font("fonts/dogicapixelbold.otf", 40)
dia_font = pygame.font.Font("fonts/dogicapixelbold.otf", 20)
font2 = pygame.font.Font("fonts/PixeloidSans.ttf", 55)
pykfont = pygame.font.Font("fonts/PixeloidSans.ttf", 24)
font3 = pygame.font.Font("fonts/dogicapixelbold.otf", 21)
lvlfont = pygame.font.Font("fonts/dogicapixelbold.otf", 26)


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
GameVersion = 0.65
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

fight_bg = pygame.image.load("sprites/battle/battle_intro.png").convert()
fight_intro = []
intro = True
for i in range(8): # animation de lancement de combat
    surface = pygame.Rect(0,i * 1272 / 8,159,1272 / 8)
    portion = pygame.transform.scale(fight_bg.subsurface(surface), (WIDTH,HEIGHT))
    fight_intro.append(portion)

fight_bg = fight_intro[0]
frame = 0
action = False
hp_cooldown = 0

# vars balls

ball = {'type': None, 'name': 'None', 'throwing': False, 'catch_rate': 0, 'anim': 'throw', 'frame': 0, 'caught': False, 'shakes': 0, 'pos':[-98,0]}

# images combat

pbar = pygame.image.load("sprites/battle/hp_player.png").convert_alpha()
advbar = pygame.image.load("sprites/battle/hp_adv.png").convert_alpha()
pbar = pygame.transform.scale(pbar, (pbar.get_width() * 4, pbar.get_height() * 4))
advbar = pygame.transform.scale(advbar, (advbar.get_width() * 4, advbar.get_height() * 4))
hp_p = pykfont.render("-- / -- PV", True, WHITE)
hp_adv = pykfont.render("-- / -- PV", True, WHITE)
p_color = GREEN
adv_color = GREEN
stats_ui = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)



# Image de fond
#bg = pygame.image.load("sprites/x.png").convert()
#bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
fps = 0
pygame.display.set_caption(f'FPS: {fps} - {GameName} v{GameVersion} - {TabState}')


# CHANGEMENT DE PHASE

def set_phase(new_phase, encounter=None):
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
        dresseur.Player.encounter = encounter
        TabState = f"Combat contre..."
        pygame.mixer.music.stop()
        assets.wild_snd.play()
        pygame.mixer.music.load("sounds/encounter.mp3")  # Charger la musique



        

def get_intro_anim(id):
    global frame, intro, fight_bg, cooldown

    
    fight_bg = fight_intro[id]
    frame = id + 1
    cooldown = 0.6
    if frame > len(fight_intro) - 1:
        intro = False
        frame = 0
        fight_bg = pygame.transform.scale(pygame.image.load("sprites/battle/Forest.png").convert(),(WIDTH,HEIGHT))



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

        elif menu == "pykemon":
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

        elif menu == "sac":
            width = WIDTH // 3
            height = 0.3 * HEIGHT
            btn_w = 0.8 * width
            btn_h = 0.7 * height

        
            menu_win = pygame.Rect(0, 0, WIDTH, HEIGHT)
            btn_list = [[assets.sac_parts[i]] for i in range(len(assets.sac_parts))] # on récupère les infos du sac
            btn_datas = [[(122,90,0),DARK_YELLOW]]

            menu_color1 = DARK_YELLOW # fenetre du fond et texte dans les boutons
            menu_color2 = YELLOW # boutons et textes hors des boutons
            menu_colorh = (122,90,0)

            menu_title = "Sac"
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


                part = str(btn_list[i][0])
                texte = font.render(assets.traduction_part[part], True, WHITE)


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

    if not dialog == "done" and not dresseur.Player.dialog_end: # si le dialogue n'est pas fini et si le joueur n'a pas la possibilité de fermer le dialogue

        if not IsDialogStarted:
            IsDialogStarted = True
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
                        dresseur.Player.dialog_end = True
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
    global fight_menu, GlobalDialog, fuite, l1, l2, l3, fight_color, stats_ui, p_color, adv_color # blue=fuir, green=pkms, yellow=sac, red=atk

    p_ratio = dresseur.Player.curr_creature.before_hp / dresseur.Player.curr_creature.max_hp
    adv_ratio = dresseur.Player.encounter.before_hp / dresseur.Player.encounter.max_hp

    if p_ratio > 0.5:
        p_color = GREEN
    elif p_ratio > 0.15:
        p_color = YELLOW
    else:
        if p_color != (255,0,0) and dresseur.Player.curr_creature.hp > 0:
            for i in range(3):
                assets.low_hp_snd.play()
        p_color = (255,0,0)

    if adv_ratio > 0.5:
        adv_color = GREEN
    elif adv_ratio > 0.15:
        adv_color = YELLOW
    else:
        if adv_color != (255,0,0) and dresseur.Player.encounter.hp > 0:
            for i in range(3):
                assets.low_hp_snd.play()
        adv_color = (255,0,0)
    # on ajoute toutes les infos de l'ui sur une surface qui ne s'actualise pas toutes les frames
    stats_ui = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)

    stats_ui.blit(pbar, (0, HEIGHT * 0.45))
    stats_ui.blit(advbar, (WIDTH * 0.75, HEIGHT * 0.025))


    stats_ui.blit(font3.render(f"{round(dresseur.Player.curr_creature.before_hp)} / {dresseur.Player.curr_creature.max_hp} PV", True, WHITE), (20, HEIGHT * 0.505)) # hp_p = 
    stats_ui.blit(font3.render(f"{round(dresseur.Player.encounter.before_hp)} / {dresseur.Player.encounter.max_hp} PV", True, WHITE), (WIDTH * 0.87, HEIGHT * 0.08)) # hp_adv = 

    stats_ui.blit(font3.render(f"{dresseur.Player.curr_creature.nick}", True, BLACK), (20, HEIGHT * 0.45)) # name_p = 
    stats_ui.blit(font3.render(f"{dresseur.Player.curr_creature.nick}", True, WHITE), (22, HEIGHT * 0.45)) # name_p2 = 

    stats_ui.blit(font3.render(f"{dresseur.Player.encounter.nick}", True, BLACK), (WIDTH * 0.77, HEIGHT * 0.025)) # name_adv = 
    stats_ui.blit(font3.render(f"{dresseur.Player.encounter.nick}", True, WHITE), (WIDTH * 0.771, HEIGHT * 0.025)) # name_adv2 = 

    stats_ui.blit(lvlfont.render(f"{dresseur.Player.curr_creature.lvl}", True, WHITE), (383, HEIGHT * 0.452)) # lvl_p = 
    stats_ui.blit(lvlfont.render(f"{dresseur.Player.encounter.lvl}", True, WHITE), (WIDTH * 0.936, HEIGHT * 0.026)) # lvl_adv = 

    pygame.draw.rect(stats_ui, adv_color, (WIDTH * 0.75 + 224, HEIGHT * 0.05 + 9, 192 * (dresseur.Player.encounter.before_hp / dresseur.Player.encounter.max_hp), 8)) # barre de vie adversaire
    pygame.draw.rect(stats_ui, p_color, (WIDTH * 0 + 64, HEIGHT * 0.5 - 18, 192 * (dresseur.Player.curr_creature.before_hp / dresseur.Player.curr_creature.max_hp), 8)) # barre de vie joueur




    if tab == BLUE: # fuite
        if random.randint(1,100) >= 5: # 95% de chances de s'enfuir
            GlobalDialog = ["Vous prenez la fuite !"]
            fuite = True
        else:
            GlobalDialog = ["Vous n'avez pas réussi à fuir !"]

    elif tab == RED:
        rect = pygame.Rect(WIDTH * 0.7, HEIGHT * 0.5, WIDTH * 0.3, HEIGHT * 0.3)
        fight_menu = {"rect": rect,
                      "btns": [dresseur.Player.curr_creature.moveset[i] for i in range(len(dresseur.Player.curr_creature.moveset))],
                      "title": font.render("Attaques", True, WHITE),
                      "color": RED,
                      "btns-text": [pykfont.render(dresseur.Player.curr_creature.moveset[j][0], True, WHITE if dresseur.Player.curr_creature.pps[j] > 0 else RED) for j in range(len(dresseur.Player.curr_creature.moveset))],
                      #DMG, PP, Precision, type
                      "subtext": [pykfont.render(f" {dresseur.Player.curr_creature.pps[k]} / {dresseur.Player.curr_creature.moveset[k][2]} PP", True, WHITE if dresseur.Player.curr_creature.pps[k] > 0 else RED) for k in range(len(dresseur.Player.curr_creature.moveset))], 
                      "type": "fight",
                      'bag_type': None}
        
        fight_color = fight_menu["color"]
        


    elif tab == YELLOW:
        rect = pygame.Rect(WIDTH * 0.7, HEIGHT * 0.5, WIDTH * 0.3, HEIGHT * 0.3)
        if fight_menu['bag_type'] == None:
            fight_menu = {"rect": rect,
                        "btns": ["heals","balls"],
                        "title": font.render("Sac", True, WHITE),
                        "color": YELLOW,
                        "btns-text": [pykfont.render(assets.traduction_part["heals"], True, WHITE), pykfont.render(assets.traduction_part["balls"], True, WHITE)],
                        #DMG, PP, Precision, type
                        "subtext": [], 
                        "type": "bag",
                        'bag_type': None}
        else:
            btns = []
            btns_text = []
            for item in dresseur.Player.inv:
                if assets.inventory[item]['type'] == fight_menu['bag_type']:
                    if dresseur.Player.inv[item] > 0:
                        color = WHITE
                    else:
                        color = RED
                    btns.append(item)
                    btns_text.append(pykfont.render(f"x{dresseur.Player.inv[item]} - {assets.inventory[item]['alias']}", True, color))

            if btns == []:
                GlobalDialog = ["Vous n'avez pas d'objets de type", f"{assets.traduction_part[fight_menu['bag_type']]} dans votre inventaire."]
                fight_menu['bag_type'] = None
                fight_tab[YELLOW]
            else:
                fight_menu['btns'] = btns
                fight_menu['btns-text'] = btns_text

        fight_color = fight_menu["color"]

def item_effect(item, pykemon, origin):
    
    global ball, GlobalDialog
    pykemon.before_hp = copy.deepcopy(pykemon.hp)

    if origin == "p":
        lanceur = f"Votre {pykemon.name}"
        cible = f"Le {pykemon.name} adverse" # je remplacerai par le bon préfixe, car le joueur n'utilise pas dd'objet sur l'ennemi 
    else:
        lanceur = f"Le {pykemon.name} adverse"
        cible = f"votre {pykemon.name}"

    # soins
    if item == 'potion':
        pykemon.hp = min(pykemon.hp + 20, pykemon.max_hp)
        assets.heal_snd.play()
        return [f"Vous utilisez une potion sur {lanceur}", "Il regagne 20 PVs."]
    
    elif item == 'rappel':
        pykemon.hp = int(round(pykemon.max_hp / 2))
        assets.heal_snd.play()
        return [f"Vous utilisez un rappel sur {lanceur}", "Il n'est plus K.O !"]
    
    elif item == 'rappel_max' or item == 'guerison': # même action dans le code
        pykemon.hp = int(pykemon.max_hp)
        assets.heal_snd.play()
        pykemon.status = None
        return [f"Vous utilisez une guérison sur {lanceur}" if item == 'guerison' else f"Vous utilisez un rappel max sur {lanceur}", "Il regagne toute sa vie"] 
    
    if item == 'total_soin':
        pykemon.status = None
        assets.heal_snd.play()
        return [f"Vous utilisez un total soin sur {lanceur}", "Il n'a plus d'effet de status !'"]

    if item == 'pykeball':
        ball = {'type': item, 'name': f"{assets.inventory[item]['alias']}", 'throwing': True, 'catch_rate': 0.5, 'anim': 'throw', 'frame': 0, 'sprite': assets.balls[item][0], 'pos': [-98, HEIGHT * 0.65], 'caught': False, 'shakes': 0}
        return [f"Vous lancez une {assets.inventory[item]['alias']} sur", f"{cible}"]

    if item == 'superball':
        ball = {'type': item, 'name': f"{assets.inventory[item]['alias']}", 'throwing': True, 'catch_rate': 0.65, 'anim': 'throw', 'frame': 0, 'sprite': assets.balls[item][0], 'pos': [-98, HEIGHT * 0.65], 'caught': False, 'shakes': 0}
        return [f"Vous lancez une {assets.inventory[item]['alias']} sur", f"{cible}"]
    
    if item == 'hyperball':
        ball = {'type': item, 'name': f"{assets.inventory[item]['alias']}", 'throwing': True, 'catch_rate': 0.75, 'anim': 'throw', 'frame': 0, 'sprite': assets.balls[item][0], 'pos': [-98, HEIGHT * 0.65], 'caught': False, 'shakes': 0}
        return [f"Vous lancez une {assets.inventory[item]['alias']} sur", f"{cible}"]
    
    if item == 'masterball':
        ball = {'type': item, 'name': f"{assets.inventory[item]['alias']}", 'throwing': True, 'catch_rate': 1, 'anim': 'throw', 'frame': 0, 'sprite': assets.balls[item][0], 'pos': [-98, HEIGHT * 0.65], 'caught': False, 'shakes': 0}
        return [f"Vous lancez une {assets.inventory[item]['alias']} sur", f"{cible}"]


def smooth_hp(creature):
    global hp_cooldown

    if hp_cooldown <= 0:

        diff = creature.hp - creature.before_hp

        if diff != 0:
            hp_cooldown = 0.2

            if abs(diff) < 0.1:
                creature.before_hp = creature.hp
            else:
                # La barre parcourt 10% de la distance restante à chaque frame
                # Ça marche pour le soin (+) et les dégâts (-)
                creature.before_hp += diff * 0.1

            fight_tab(None)
    else:
        hp_cooldown -= 0.1

def fight_round(prefix_l, canPlay, checkup, choice):
    global GlobalDialog

    # prefix_lanceur / cible
    if prefix_l == 'p':
        lanceur = dresseur.Player.curr_creature
        cible = dresseur.Player.encounter
    else:
        lanceur = dresseur.Player.encounter
        cible = dresseur.Player.curr_creature

    
    # si le lanceur peut jouer (pps restants sur au moins 1 capacité)
    if canPlay:
        lanceur.pps[choice] -= 1
        GlobalDialog = lanceur.atk(lanceur.moveset[choice][5], cible, prefix_l)
        checkup[f"{prefix_l}_atk"] = True

        
        fight_tab(RED) # on actualise les pv etc.
    else:
        if checkup[f"{prefix_l}_pp"] == False:
            if prefix_l == "p": # on change le message en fct de qui joue
                GlobalDialog = [f"Votre {lanceur.name} n'a plus de", " capacité pour se battre."]
            else:
                GlobalDialog = [f"Le {lanceur.name} adverse n'a plus", "de capacité pour se battre."]
            checkup[f"{prefix_l}_pp"] = True

        if GlobalDialog == []:
            GlobalDialog = lanceur.atk("lutte", cible, prefix_l)
            checkup[f"{prefix_l}_atk"] = True
            
            fight_tab(RED) # on actualise les pv etc.

    return checkup # c'est pas une variable globale donc on l'actualise ici
        



# BOUCLE PRINCIPALE

def main():
    global fps, cooldown, menu, sous_menu, TabState, GameName, GameVersion, map, map_blit, dialog_cooldown, close_tab_color, GlobalDialog, IntroDone, fuite, fight_color, action, stats_ui, ball

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

    dresseur.Player.team[0] = pkmns.base_copy("punkromatides") # debug pour ne pas commencer à 0 pokémons
    for i in range(dresseur.Player.team[0].lvl - 1):
        dresseur.Player.team[0].lvlup()
    dresseur.Player.curr_creature = dresseur.Player.team[0]

    while running:
        keys = pygame.key.get_pressed()
        dt =  clock.tick(60) / 1000  # Delta time in milliseconds.

        if keys[pygame.K_x] and cooldown <= 0 and phase == "game" and dresseur.Player.able:
            assets.menu_open_snd.play()
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
                        set_phase("fight", encounter=entity.get_creature())
                        
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
                    assets.menu_2_snd.play()
                    if menu == "pause":
                        set_menu(0)
                    else:
                        if sous_menu == None:
                            set_menu(1)
                        else:
                            if sous_menu > 1:
                                sous_menu = None
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
                            assets.menu_1_snd.play()
                            set_menu(i + 2)   
                    else:
                        color2 = btn[4][1]
                    pygame.draw.rect(screen, color2, btn[1]) # color2
                    screen.blit(btn[2], (btn[1].centerx - btn[3] // 2, btn[1][1] + 20)) 

            elif menu == "pykemon": # vue d'un seul pokémon de l'équipe
                if sous_menu == None: # on vérifie le sous menu => None = équipe, 1 = vue d'un pokémon
                    for i, btn in enumerate(btn_list):
                        if btn[1].collidepoint(mouse_pos):
                            color2 = btn[4][0]
                            if mouse_click and cooldown <= 0 and not btn[0] == None: # si on clique sur un pokémon de l'équipe et que ce pokémon n'est pas vide
                                cooldown = 1
                                assets.menu_1_snd.play()
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

            elif menu == "sac":
                if sous_menu == None:
                    for i, btn in enumerate(btn_list):
                        if btn[1].collidepoint(mouse_pos):
                            color2 = btn[4][0]
                            if mouse_click and cooldown <= 0 and not btn[0] == None: # si on clique sur un pokémon de l'équipe et que ce pokémon n'est pas vide
                                cooldown = 1
                                sous_menu = i + 1 
                                desc = [pykfont.render("",  True, WHITE)]
                                view_rect = pygame.Rect(WIDTH * 0.025, HEIGHT * 0.15, WIDTH * 0.3, HEIGHT * 0.7)
                                tab_name = font.render(assets.traduction_part[btn[0]], WHITE, True)
                                sous_menu = 1
                                
                                items = {}
                                # on définit les items visibles
                                for item in dresseur.Player.inv:
                                    if assets.inventory[item]["type"] == btn[0]:
                                        # items[item] = [nom, qtté, texture, desc]
                                        items[item] = [item, font.render(f"x{str(dresseur.Player.inv[item])}", WHITE, True), assets.inventory[item]['tex'], font.render(assets.inventory[item]['alias'], WHITE, True), assets.inventory[item]['desc']]

                                
                        else:
                            color2 = btn[4][1]
                        pygame.draw.rect(screen, color2, btn[1]) # color2
                        screen.blit(btn[2], (btn[1].centerx - btn[3] // 2, btn[1][1] + 20)) 
                else:
                    i = 0
                    for item in items:
                        i += 1
                        item_rect = pygame.Rect(WIDTH / 3, (i * HEIGHT / 10) + 55, WIDTH / 3, HEIGHT * 0.09)
                        if item_rect.collidepoint(mouse_pos):
                            color2 = (251, 246, 43)
                            desc = []
                            for ligne in assets.inventory[item]['desc']:          # si ça lag trop sur loRdi, passer ça dans le click
                                desc.append(pykfont.render(ligne, WHITE, True))

                            if mouse_click and cooldown <= 0 and not btn[0] == None:
                                pass # garder ça au cas où ça lag sur loRdi
                        else:
                            color2 = DARK_YELLOW

                        # items[item] = [nom, qtté, texture, nom_render, desc]
                        pygame.draw.rect(screen, color2, item_rect) # color2
                        screen.blit(items[item][3], (WIDTH / 3 + items[item][2].get_width(),(i * HEIGHT / 10) + 85)) # texte
                        screen.blit(items[item][1], (WIDTH * 0.6,(i * HEIGHT / 10) + 85)) # qtté
                        screen.blit(items[item][2], (WIDTH / 3 + 10, (i * HEIGHT / 10) + 65)) # texture


                    # Contenu d'une partie du sac
                    pygame.draw.rect(screen, menu_color1, view_rect) # barre latérale gauche verticale
                    screen.blit(tab_name, (WIDTH * 0.04, HEIGHT * 0.17))
                    for i in range(len(desc)):
                        screen.blit(desc[i], (WIDTH * 0.04, HEIGHT * 0.24 + (i * HEIGHT * 0.03)))
                    
            else: 
                print("menu inconnu")


        elif phase == "fight":
            if intro and cooldown <= 0:
                get_intro_anim(frame)
                LeveledUp = False
                IsFightThemeStarted = False
            elif not intro and not IntroDone:
                TabState = f"Combat contre {dresseur.Player.encounter.name}"
                GlobalDialog = [f"Un {dresseur.Player.encounter.name} sauvage apparait !"]

            if not IsFightThemeStarted and not pygame.mixer.get_busy():
                    pygame.mixer.music.play(loops=-1, start=0.0)
                    IsFightThemeStarted = True

            screen.blit(fight_bg,(0,0))

            if dresseur.Player.curr_creature.xp > dresseur.Player.curr_creature.req_xp:
                if  GlobalDialog == []:
                    assets.exp_max_snd.play()
                    assets.lvlup_snd.play()
                    dresseur.Player.curr_creature.lvlup()
                    GlobalDialog = [f"{dresseur.Player.curr_creature.nick} passe au niveau {dresseur.Player.curr_creature.lvl} !"]
            else:
                LeveledUp = True



            print(f"XP: {dresseur.Player.curr_creature.xp} / {dresseur.Player.curr_creature.req_xp}")
            if (fuite or (ball['caught'] and not action and LeveledUp)) and GlobalDialog == []:
                ball = {'type': 'none', 'name': 'none', 'throwing': False, 'catch_rate': 0.5, 'anim': 'throw', 'frame': 0, 'sprite': 'none', 'pos': [200, HEIGHT], 'caught': False, 'shakes': 0}
                pygame.mixer.stop()
                if fuite:
                    assets.fuite_snd.play()
                fuite = False
                pygame.mixer.music.load("sounds/town.mp3")  # Charger la musique
                pygame.mixer.music.play(loops=-1, start=0.0)
                set_phase("game")

            if not intro and phase == "fight": # intro désigne l'animation d'intro du combat
                smooth_hp(dresseur.Player.curr_creature)
                smooth_hp(dresseur.Player.encounter)

                screen.blit(dresseur.Player.curr_creature.sprite[1], (WIDTH // 8, HEIGHT * 0.5))

                if not ((ball['anim'] == 'shaking' and ball['throwing']) or (ball['pos'][0] > WIDTH * 0.759 and ball['throwing'])):
                    screen.blit(dresseur.Player.encounter.sprite[0], (WIDTH * 0.7, HEIGHT * 0.1)) 

                if IntroDone: # intro Done c'est quand le texte d'intro est terminé

                    # Si pykemons K.O
                    if dresseur.Player.curr_creature.hp <= 0 and not fuite and GlobalDialog == []:
                        GlobalDialog = ["Vous n'avez plus de PyKemon en état de se battre. ", "Vous prenez la fuite !"]
                        fuite = True
                        action = False
                    if dresseur.Player.encounter.hp <= 0 and GlobalDialog == []:
                        exp = max(dresseur.Player.encounter.lvl - dresseur.Player.curr_creature.lvl, 1) * random.randint(20, 30)
                        GlobalDialog = [f"Le {dresseur.Player.encounter.name} adverse est K.O !", f"Vous gagnez {exp} points d'Exp."]
                        dresseur.Player.curr_creature.xp += exp
                        assets.exp_snd.play()

                        action = False
                        fuite = True
                            
                        

                    # barres d'hp
                    # pour optimiser: fusionner toutes les infos des barres en une surface
                    screen.blit(stats_ui, (0,0))

                    if not action and not fuite and GlobalDialog == []: # on cache l'interface
                        # boutons de jeu
                        for element in fight_ui:
                            rect = pygame.draw.rect(screen, element[0], element[1]) # screen, couleur, rect, titre
                            screen.blit(element[2], (rect.centerx - element[2].get_width() / 2 , rect.centery - 22))
                            if rect.collidepoint(mouse_pos) and mouse_click and GlobalDialog == []:
                                fight_tab(element[0]) # le bouton est déterminé par sa couleur, tel un identifiant

                        # menu d'attaques, sac etc.
                        pygame.draw.rect(screen, fight_menu["color"], fight_menu["rect"]) #fight_menu est un dico
                        screen.blit(fight_menu["title"],(WIDTH * 0.72, HEIGHT * 0.52))

                        
                        if fight_color == RED: #Attaques
                            for i in range(len(fight_menu["btns"])): # différents menus (fight, sac, etc.)
                                y_offset = HEIGHT * 0.58 if i < 2 else HEIGHT * 0.68
                                x_offset = WIDTH * 0.72 + (i % 2) * WIDTH * 0.127
                                btn = pygame.draw.rect(screen, BLACK, (x_offset, y_offset, WIDTH * 0.12, HEIGHT * 0.09))
                                screen.blit(fight_menu["btns-text"][i], (x_offset + 10, y_offset + 10))
                                screen.blit(fight_menu["subtext"][i], (x_offset + 10, y_offset + 40))

                                if btn.collidepoint(mouse_pos) and mouse_click and not action and cooldown <= 0:
                                    cooldown = 1
                                    action = True
                                    indice = i
                                    checkup = {"p_atk": False, "adv_atk": False, "p_pp": False, "adv_pp": False}

                        elif fight_color == YELLOW:
                            for i in range(len(fight_menu["btns"])): # différents menus (fight, sac, etc.)
                                y_offset = HEIGHT * 0.58 + (i * HEIGHT * 0.06) if i < 3 else HEIGHT * 0.58 + ((i - 3) * HEIGHT * 0.06)
                                x_offset = WIDTH * 0.72 if i < 3 else WIDTH * 0.72 + WIDTH * 0.127
                                btn = pygame.draw.rect(screen, BLACK, (x_offset, y_offset, WIDTH * 0.12, HEIGHT * 0.05))
                                screen.blit(fight_menu["btns-text"][i], (x_offset + 10, y_offset + 10))
                                #screen.blit(fight_menu["subtext"][i], (x_offset + 10, y_offset + 40))

                                if btn.collidepoint(mouse_pos) and mouse_click and not action and GlobalDialog == [] and cooldown <= 0 and not ball["throwing"]:
                                    cooldown = 1
                                    if fight_menu['bag_type'] == None:
                                        fight_menu['bag_type'] = fight_menu['btns'][i]
                                        
                                        fight_tab(YELLOW)
                                    else:
                                        if dresseur.Player.inv[fight_menu['btns'][i]] <= 0:
                                            GlobalDialog = [f"Vous n'avez plus de {assets.inventory[fight_menu['btns'][i]]['alias']}."]
                                        else:
                                            dresseur.Player.inv[fight_menu['btns'][i]] -= 1
                                            action = True
                                            checkup = {"p_atk": True, "adv_atk": False, "p_pp": False, "adv_pp": False}
                                            GlobalDialog = item_effect(fight_menu['btns'][i], dresseur.Player.curr_creature,'p')
                                            if GlobalDialog == None:
                                                GlobalDialog = ["**MESSAGE DE DEBUG**", "Objet inconnu, choisissez un autre item.", f"ID Item: {fight_menu['btns'][i]}"]
                                                action = False
                                                checkup = {"p_atk": False, "adv_atk": False, "p_pp": False, "adv_pp": False}
                                                dresseur.Player.inv[fight_menu['btns'][i]] = 0

                                            
                                            indice = 0 # on simule pour pas casser la condition suivante
                                            
                                            fight_tab(YELLOW)

                    if ball["throwing"]:
                        screen.blit(ball['sprite'], (ball['pos'][0], ball['pos'][1]))
                        if ball['anim'] == 'throw' and cooldown <= 0 and GlobalDialog == []:
                            cooldown = 0.25

                            if ball['pos'][0] == -98: # position de départ, joué une fois donc
                                assets.throw_snd.play()
                            

                            ball['sprite'] = assets.balls[ball['type']][ball['frame']]

                            if ball['pos'][0] < WIDTH * 0.76:
                                if ball['frame'] < 0:
                                    ball['frame'] = 8
                                else:
                                    ball['frame'] -= 1


                                ball['pos'][0] += 45
                                ball['pos'][1] -= 17
                                
                            else:
                                if ball['frame'] < 8:
                                    ball['frame'] += 1
                                else:
                                    ball['frame'] = 0

                                ball['pos'][1] += 7

                                if ball['pos'][1] > HEIGHT * 0.28:
                                    ball['anim'] = 'shaking'
                                    ball['frame'] = 11
                                    ball['sprite'] = assets.balls[ball['type']][ball['frame']]
                                    if random.randint(0,100) < ball['catch_rate'] * 100:
                                        ball['shakes'] = 3
                                        ball['caught'] = True
                                    else:
                                        ball['shakes'] = random.randint(1,2)
                                        ball['caught'] = False

                        elif ball['anim'] == 'shaking' and cooldown <= 0:
                            cooldown = 1
                            ball['pos'] = [WIDTH * 0.76, HEIGHT * 0.28]

                            if ball['frame'] == 14:
                                assets.shaking_snd.play()

                            if ball['frame'] < 16 and ball['shakes'] > 0:
                                ball['frame'] += 1
                            else:
                                if ball['shakes'] > 0:
                                    ball['frame'] = 11
                                    ball['shakes'] -= 1

                                if ball['shakes'] <= 0 and ball['frame'] != 9:
                                    if ball['caught']:
                                        ball['frame'] = 9
                                        assets.caught_snd.play()
                                        action = False
                                        checkup = {"p_atk": False, "adv_atk": False, "p_pp": False, "adv_pp": False}
                                        exp = max(dresseur.Player.encounter.lvl - dresseur.Player.curr_creature.lvl, 1) * random.randint(20, 30)
                                        GlobalDialog = [f'Vous avez attrapé {dresseur.Player.encounter.name} !', f"Vous gagnez {exp} pts d'Exp."]
                                        dresseur.Player.curr_creature.xp += exp
                                        assets.exp_snd.play()
                                        assets.pykemon_caught_snd.play()
            
                                        InTeam = False
                                        for i in range(len(dresseur.Player.team)):
                                            if dresseur.Player.team[i] == None and not InTeam:
                                                dresseur.Player.team[i] = dresseur.Player.encounter.copy(ball['type'])
                                                InTeam = True

                                        if not InTeam: # Si attrapé mais pas de place dans l'équipe
                                            GlobalDialog = ["Vous n'avez plus de place dans votre", "équipe. Le Pykemon à été transféré", "dans vos boites."]
                                        

                                    else:
                                        ball['frame'] = 10
                                        GlobalDialog = [f"Vous n'avez pas réussi à attraper {dresseur.Player.encounter.name}..."]
                                        ball["throwing"] = False

                            ball['sprite'] = assets.balls[ball['type']][ball['frame']]


                                        




                    elif action == True and GlobalDialog == [] and not ball['throwing']: # si action == True
                        # le checkup permet de se situer dans la boucle

                        # on vérifie si les pykemons ont encore des pp (cas de lutte)
                        PcanPlay = False
                        for pp in dresseur.Player.curr_creature.pps:
                            if pp != 0:
                                PcanPlay = True

                        AdvcanPlay = False
                        for pp in dresseur.Player.encounter.pps:
                            if pp != 0:
                                AdvcanPlay = True

                        AdvChoice = random.randint(0, len(dresseur.Player.encounter.moveset) - 1)

                        if (dresseur.Player.curr_creature.pps[indice] > 0 or not PcanPlay) or checkup["p_atk"] == True: # PP joueur > 0 mais pas incapable d'attaquer
                            
                            if dresseur.Player.curr_creature.speed > dresseur.Player.encounter.speed: # on prend en compte la vitesse de chaque pykemon

                                if checkup["p_atk"] == False:
                                    checkup = fight_round("p", PcanPlay, checkup, indice)
                                          
                                elif checkup["adv_atk"] == False and GlobalDialog == []:
                                    checkup = fight_round("adv", AdvcanPlay, checkup, AdvChoice)

                            else: #si adversaire plus rapide: 
                                               
                                if checkup["adv_atk"] == False:
                                    checkup = fight_round("adv", AdvcanPlay, checkup, AdvChoice)
                                    
                                elif checkup["p_atk"] == False and GlobalDialog == []:
                                    checkup = fight_round("p", PcanPlay, checkup, indice)

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

                    screen.blit(lvlfont.render(dresseur.Player.dialog[2], True, WHITE), (WIDTH * 0.306, HEIGHT * 0.705))
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
                    if dresseur.Player.dialog_end:
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
    