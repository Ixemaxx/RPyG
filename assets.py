import pygame

pygame.init()
pygame.mixer.init()
pygame.display.set_mode((1920, 1080))

# sounds
grass_snd = pygame.mixer.Sound("sounds/grass.mp3")
wild_snd = pygame.mixer.Sound("sounds/wild.mp3")
atk_snd = pygame.mixer.Sound("sounds/atk.mp3")
atk2_snd = pygame.mixer.Sound("sounds/atk2.mp3")
heal_snd = pygame.mixer.Sound("sounds/heal.mp3")
throw_snd = pygame.mixer.Sound("sounds/throw.mp3")
shaking_snd = pygame.mixer.Sound("sounds/ball1.mp3")
caught_snd = pygame.mixer.Sound("sounds/caught.mp3")
warp_snd = pygame.mixer.Sound("sounds/door.mp3")
shiny_snd = pygame.mixer.Sound("sounds/shiny.wav")
item_snd = pygame.mixer.Sound("sounds/item.wav")
fuite_snd = pygame.mixer.Sound("sounds/fuite.wav")
collision_snd = pygame.mixer.Sound("sounds/wallhit.wav")
super_eff_snd = pygame.mixer.Sound("sounds/supereff.wav")
effective_snd = pygame.mixer.Sound("sounds/eff.wav")
not_eff_snd = pygame.mixer.Sound("sounds/noteff.wav")
exp_snd = pygame.mixer.Sound("sounds/expgrind.wav")
exp_max_snd = pygame.mixer.Sound("sounds/expmax.wav")
lvlup_snd = pygame.mixer.Sound("sounds/lvlup.wav")
dialog_snd = pygame.mixer.Sound("sounds/message.wav")
bicycle_snd = pygame.mixer.Sound("sounds/bicycle.wav")
low_hp_snd = pygame.mixer.Sound("sounds/lowhp.wav")
menu_1_snd = pygame.mixer.Sound("sounds/menu1.wav")
menu_2_snd = pygame.mixer.Sound("sounds/menu2.wav")
menu_open_snd = pygame.mixer.Sound("sounds/menuopen.wav")
pykemon_caught_snd = pygame.mixer.Sound("sounds/pykeget.wav")
ball_enter_snd = pygame.mixer.Sound("sounds/ball_enter.wav")

init = False # pour déterminer si la save a chargée


# génération des animations de balls
balls_tex = pygame.image.load("sprites/items/balls.png").convert_alpha()
items_tex = pygame.image.load("sprites/items/items.png").convert_alpha()
balls = {}

def get_ball(col, name):
    ball_frames = []
    grid_size = 17
    tex_width = balls_tex.get_width()
    tex_height = balls_tex.get_height()

    # Utilisation de la division entière pour éviter les flottants
    case_w = tex_width // grid_size
    case_h = tex_height // grid_size

    pos_x = col * case_w

    for y in range(grid_size):
        # On calcule pos_y précisément
        pos_y = y * case_h
        
        # Sécurité pour ne pas dépasser d'un pixel à cause des arrondis
        rect = pygame.Rect(pos_x, pos_y, case_w, case_h)
        
        try:
            frame = balls_tex.subsurface(rect)
            ball_frames.append(pygame.transform.scale(frame, (98, 98)))
        except ValueError:
            # Au cas où le rectangle dépasse de l'image source
            print(f"Erreur de découpe à l'index y={y}")

    balls[name] = ball_frames

    
get_ball(3, "pykeball") # colonnes de 0 à 16 (17 en tout)
get_ball(2, "superball") # colonnes de 0 à 16 (17 en tout)
get_ball(1, "hyperball") # colonnes de 0 à 16 (17 en tout)
get_ball(0, "masterball") # colonnes de 0 à 16 (17 en tout)

def get_item(case_x, case_y): # on commence en (1,1) ici
    width = 16
    height = 35
    # On s'assure que case_size est un entier pour Pygame
    case_w = items_tex.get_width() / width
    case_h = items_tex.get_height() / height

    # On calcule la position X une seule fois (colonne * taille d'une case)
    pos_x = (case_x - 1) * case_w
    pos_y = (case_y - 1)* case_h

    
    rect = pygame.Rect(pos_x, pos_y, case_w, case_h)
    # subsurface extrait la zone, scale la redimensionne
    frame = items_tex.subsurface(rect)
    return pygame.transform.scale(frame, (98, 98))



# inventaire
sac_parts = ["heals","balls","unique"]
traduction_part = {'heals': 'Soins', 'balls': 'Balls', 'unique': 'Objets Clés'}
inventory = {
    # balls
    "pykeball": {'type': 'balls', 'tex': get_item(4, 1), 'alias': "PyKeball", 'desc': ["Un objet qui permet d'attraper", "des PyKemons sauvages."]},
    "superball": {'type': 'balls', 'tex': get_item(3, 1), 'alias': "Superball", 'desc': ["Un objet qui permet d'attraper", "des PyKemons sauvages avec", "une meilleure efficacité", "que la PyKeball"]},
    "hyperball": {'type': 'balls', 'tex': get_item(2, 1), 'alias': "Hyperball", 'desc': ["Un objet qui permet d'attraper", "des PyKemons sauvages avec", "une excellente efficacité."]},
    "masterball": {'type': 'balls', 'tex': get_item(1, 1), 'alias': "Masterball", 'desc': ["Un objet extrêmement rare", "et convoité qui permet", "d'attraper un PyKemon à", "coup sûr."]},
    # heals
    "potion": {'type': 'heals', 'tex': get_item(11, 1), "alias": "Potion", 'desc': ["Permet de gagner 20PV"]},
    "rappel": {'type': 'heals', 'tex': get_item(11, 2), 'alias': 'Rappel', 'desc': ["Permet de réanimer un PyKemon K.O", "à hauteur de la moitié de ses PV"]},
    "rappel_max": {'type': 'heals', 'tex': get_item(6, 2), 'alias': 'Rappel Max', 'desc': ["Permet de réanimer un PyKemon K.O", "à hauteur de tous ses PV"]},
    "total_soin": {'type': 'heals', 'tex': get_item(5, 2), 'alias': 'Total Soin', 'desc': ["De la morphine, pour faire", "oublier à vos pykemons", "qu'ils sont brûlés, gelés", "endormis, paralysés...", "Espèce de monstre."]},
    "guerison": {'type': 'heals', 'tex': get_item(1, 2), 'alias': 'Guérison', 'desc': ["De la magie noire en flacon","je vois que ça.","Redonne tous les pvs."]},
    # unique
    "dex": {'type': 'unique', 'tex': get_item(3, 27), 'alias': 'PyKedex', 'desc': ["Un genre d'appareil photo made in", "China qui enregistre les infos", "des PyKemons attrapés"]},
    "bike": {'type': 'unique', 'tex': get_item(3, 27), 'alias': 'Vélo', 'desc': ["Un vélo Décathlon premier prix", "que vous avez eu pour vos 8 ans.", "Malgré son usure globale, la sonette", "marche encore;"]}
    
}

