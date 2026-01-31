import pygame
import math

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
speed =360
anim_list = [] #liste d'animations du joueur, pour éviter le lag. Les PNJ utilisent la fonction get_animation_frame pour l'instant

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

class Player:
    def __init__(self, sprite_sheet, username = "Red", team = None, inv = None):
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
        self.dir = "d" #direction du sprite
        self.anim_timer = 0
        self.coeff = 1.3 #coeff de taille de sprite
        self.moving = False

        width = self.sprite_sheet.get_width()

        for i in range(6):
            self.team.append(None)

    def extract_anim(self):
        global anim_list

        for i in range(16):
            rect = pygame.Rect((i % 4) * (width // 4), (i // 4) * (width // 4), width // 4, width // 4)
            anim_list.append(pygame.transform.scale(self.sprite_sheet.subsurface(rect), (64 * self.coeff, 80 * self.coeff)))


    def animate_dresseur(self, id): # pour un dresseur (anim_list) pour éviter le transform.scale à chaque frame (des fps benef)

        if self.anim != id:
            self.anim = id
            self.frames = anims[id]
            self.curr_frame = 0
            self.anim_timer = 0

        self.anim_timer += 0.1
        if self.anim_timer >= 1:
            self.anim_timer = 0
            self.curr_frame += 1
        
        if self.curr_frame > (len(self.frames) - 1): #si l'animation change 
            self.curr_frame = 0

        sprite = self.frames[self.curr_frame]
        self.sprite = anim_list[sprite]

    def IsFuturePosAllowed(self, dx, dy, world_map):
        # On définit la largeur et hauteur du sprite pour les calculs
        sprite_w = 64 * self.coeff
        sprite_h = 80 * self.coeff

        tile_size = 1920 // 16

        # On calcule la position future du "bas" du personnage (ses pieds)
        # On prend le centre horizontal (x + largeur/2) 
        # et le bas vertical (y + hauteur)
        feet_x = self.x + dx + (sprite_w / 4) # pied gauche
        feet_x2 = self.x + dx + (sprite_w * 3/4) # pied droit
        feet_y = self.y + dy + sprite_h

        # Conversion en indices de map
        col = int(feet_x // tile_size) # col pied gauche
        col2 = int(feet_x2 // tile_size) # col pied droit
        row = int(feet_y // tile_size)

        # Vérification des limites
        if 0 <= row < len(world_map) and 0 <= col <= col2 < len(world_map[0]):
            tile_value = world_map[row][col]
            
            # Liste des tiles bloquantes (à adapter selon tes besoins)
            # Par exemple, si 0 est de l'herbe et tout le reste bloque :
            tile_left = world_map[row][col]
            tile_right = world_map[row][col2]

            allowed_tile = [0,1,5,70]

            # Autorisé SEULEMENT si les DEUX pieds sont sur du sol (0 ou 1)
            if (tile_left in allowed_tile) and (tile_right in allowed_tile):
                return True
        
        return False

        

    def update(self, keys, dt, map):
        global speed

        if self.able:
            dx, dy = 0, 0
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
            elif keys[keymap["e"]]:
                speed = 420


            if dx != 0 or dy != 0: #définit si le joueur bouge ou pas
                self.moving = True
                if dx != 0 and dy != 0: #si on se déplace en diagonale, on réduit la vitesse pour éviter d'aller plus vite
                    if self.IsFuturePosAllowed(dx, dy, map):
                        self.x += dx * 2/3
                        self.y += dy * 2/3
                    if dy >0:
                        self.dir = 'd' # dire que si on bouge gauche/droite + haut/bas c'est l'anim haut/bas qui se joue
                    else:
                        self.dir = 'u'
                else:
                    if self.IsFuturePosAllowed(dx, dy, map):
                        self.x += dx
                        self.y += dy

                id = f"walk_{self.dir}"
                self.animate_dresseur(id)
            else:
                self.moving = False
                id = f"idle_{self.dir}"
                self.animate_dresseur(id)

            
                


# Création des deux personnages
Dresseur = Player(sprite_sheet=pygame.transform.scale(pygame.image.load("sprites/persos/11.png"), (100,100)), username="Ixemax") 
#on met la texture en carré comme ça on a pas de problème pour piocher un sprite (largeur != hauteur sur l'originale)
