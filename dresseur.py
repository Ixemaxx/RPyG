import pygame
import maps

pygame.init()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (43, 251, 47)
ORANGE = (251, 161, 43)
DARK_ORANGE = (251, 133, 43)
DARK_RED = (166, 23, 23)

keymap = {"left": pygame.K_q, "right": pygame.K_d, "up": pygame.K_z, "down": pygame.K_s, "e": pygame.K_e}
speed = 300

allowed_tile = [0,1,5,70,102] # id de cases où le joueur peut marcher (pas de collisions)
special_tile = [2,3] # cases spéciales (bancs, hautes herbes)
sp_tile_events = {2: ["banc",None], 3: ["banc",None]} # si l'event s'exécute sans la touche E, mettre comme 3e argument "now"

tile_size = 1920 // 16

dialog = False

anims = {
            "idle_d": [0],
            "idle_l": [8],
            "idle_r": [12],
            "idle_u": [4],
            "walk_d": [1,3],
            "walk_l": [8,9],
            "walk_r": [12,13],
            "walk_u": [5,7]
        }

class Dresseur:
    def __init__(self, sprite_sheet, username = "Red", team = None, inv = None,dir="d"):
        global width

        self.sprite_sheet = pygame.transform.scale(sprite_sheet, (100,100)) #alpha pour retirer le fond blanc
        self.sprite = sprite_sheet #provisoire, le temps d'appeler get_sprite()
        self.username = username
        self.able = True #able définit la capacité du joueur à interagir avec son perso (bouger, parler aux pnj...)
        #création de l'équipe
        self.team = []
        #animations
        self.anim = ""
        self.frames = 1 #nb de frames de l'anim
        self.curr_frame = 0 
        self.dir = dir #direction du sprite
        self.anim_timer = 0
        self.coeff = 1.3 #coeff de taille de sprite
        self.moving = False
        self.anim_list = [] #liste d'animations du joueur, pour éviter le lag. Les PNJ utilisent la fonction get_animation_frame pour l'instant
        self.interact = None
        self.cooldown = 0
        self.state = None

        width = self.sprite_sheet.get_width()

        for i in range(6):
            self.team.append(None)

    def extract_anim(self):

        for i in range(16):
            rect = pygame.Rect((i % 4) * (width // 4), (i // 4) * (width // 4), width // 4, width // 4)
            self.anim_list.append(pygame.transform.scale(self.sprite_sheet.subsurface(rect), (64 * self.coeff, 80 * self.coeff)))


    def animate_dresseur(self, id): # pour un dresseur (anim_list) pour éviter le transform.scale à chaque frame (des fps benef) 

        if self.anim != id:
            self.anim = id
            self.frames = anims[id]
            self.curr_frame = 0
            self.anim_timer = 0

        self.anim_timer += 0.07
        if self.anim_timer >= 1:
            self.anim_timer = 0
            self.curr_frame += 1
        
        if self.curr_frame > (len(self.frames) - 1): #si l'animation change 
            self.curr_frame = 0

        sprite = self.frames[self.curr_frame]
        self.sprite = self.anim_list[sprite]

    # IA
    def IsFuturePosAllowed(self, dx, dy, world_map, entities): 
        global tile_size, special_tile, allowed_tile, sp_tile_events

        sprite_w = 64 * self.coeff
        sprite_h = 80 * self.coeff

        # On calcule la position future du "bas" du personnage (ses pieds)

        feet_x = self.x + dx + (sprite_w / 4) # pied gauche
        feet_x2 = self.x + dx + (sprite_w * 3/4) # pied droit
        feet_y = self.y + dy + sprite_h

        # Conversion en indices de map
        col = int(feet_x // tile_size) # col pied gauche
        col2 = int(feet_x2 // tile_size) # col pied droit
        row = int(feet_y // tile_size)

        # Vérification des limites
        if 0 <= row < len(world_map) and 0 <= col <= col2 < len(world_map[0]):
            
            tile_left = world_map[row][col]
            tile_right = world_map[row][col2]

            sp_tile = None # pas de case spéciale déclarée au début

            # Pas IA, dans le bloc IA
            for entity in entities: # vérif si il y'a une entité sur le chemin

                if entity.req_dir != None: # on vérifie si la direction et autorisée
                    if entity.req_dir != self.dir:
                        direction_check = False
                else:
                    direction_check = True
                
                if entity.type == "npc":
                    if ((feet_x > entity.x - 30) and (feet_x < entity.x + sprite_w)) and ((feet_y < entity.y + sprite_h + 30) and (feet_y > entity.y + 10)) and direction_check:
                        self.interact = ["npc",entity]
                        return False
                elif entity.type == "warp":
                    if ((feet_x2 > entity.x) and (feet_x < entity.x + entity.w)) and ((feet_y < entity.y + entity.h) and (feet_y > entity.y)) and direction_check:
                        self.interact = ["warp",entity,"now"]
                        self.get_interaction()
                
            self.interact = None
                
            # vérifie si on est sur une case spéciale
            for tile in special_tile:
                if tile == tile_left and tile == tile_right:
                    sp_tile = tile

            if sp_tile != None:
                event = sp_tile_events[sp_tile]
                self.interact = [event[0],event[1]]
                if len(event) == 3:
                    if event[2] == "now":
                        self.get_interaction()

            # Autorisé SEULEMENT si les DEUX pieds sont sur du sol (0 ou 1)
            if (tile_left in allowed_tile) and (tile_right in allowed_tile):
                return True
        
        return False
    

    def get_interaction(self): # interact est une liste de type  [type,interaction] interaction contient les infos de l'interaction

        type = self.interact[0] #juste le type qui détermine si c'est un item, dialogue, banc, warpzone...
        interact = self.interact[1]
        self.cooldown = 2.5

        if self.able and not dialog:
            if type == "npc":
                print(interact.dialog)
            
            elif type == "banc" and self.dir == "u": # il faut être devant le banc pour pouvoir s'asseoir
                self.state = "banc"
                self.y -= 20
                self.dir = "d"
                
            elif type == "warp": # à compléter
                # interact[1] c'est l'entité warp, qui contient les infos nécessaires pour le changement de map
                map = interact.warp_dest 
                map_name = interact.warp_name
                self.x, self.y = interact.player_pos[0], interact.player_pos[1]
                self.dir = interact.player_dir
                maps.change_map(map,map_name)
        else:
            if self.state == "banc":
                self.y += 30
            self.state = None
            self.able = True

        self.get_state()

    def get_state(self):
        if not dialog:
            if self.state == "banc":
                self.able = False

        

    def update(self, keys, dt, map, entities):
        global speed

        dx, dy = 0, 0
        if self.cooldown >= 0:
            self.cooldown -= 0.1

        if self.able:
            if keys != 0:
                if keys[keymap["left"]]:
                    dx -= speed * dt
                    self.dir = "l"
                if keys[keymap["right"]]:
                    dx += speed * dt
                    self.dir = 'r'
                if keys[keymap["up"]]:
                    dy -= speed * dt
                    self.dir = 'u'
                if keys[keymap["down"]]:
                    dy += speed * dt
                    self.dir = 'd'


        if dx != 0 or dy != 0: #définit si le joueur bouge ou pas
            self.moving = True
            if dx != 0 and dy != 0: #si on se déplace en diagonale, on réduit la vitesse pour éviter d'aller plus vite
                if self.IsFuturePosAllowed(dx, dy, maps.map, entities):
                    self.x += dx * 2/3
                    self.y += dy * 2/3
                if dy >0:
                    self.dir = 'd' # dire que si on bouge gauche/droite + haut/bas c'est l'anim haut/bas qui se joue
                else:
                    self.dir = 'u'
            else:
                if self.IsFuturePosAllowed(dx, dy, maps.map, entities):
                    self.x += dx
                    self.y += dy

            id = f"walk_{self.dir}"
            self.animate_dresseur(id)
        else:
            self.moving = False
            id = f"idle_{self.dir}"
            self.animate_dresseur(id)

        
        if keys != 0 and self.cooldown <= 0:
            if keys[keymap["e"]]: # à part, ça permet d'interagir avec des pnj, des boites de dialogue...
                if self.interact != None:
                    self.get_interaction()



            

# Création des deux personnages
Player = Dresseur(sprite_sheet=pygame.transform.scale(pygame.image.load("sprites/persos/11.png"), (100,100)), username="Ixemax") 
#on met la texture en carré comme ça on a pas de problème pour piocher un sprite (largeur != hauteur sur l'originale)