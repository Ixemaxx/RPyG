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


    def get_animation_frame(self, id, dt):

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
        rect = pygame.Rect((sprite % 4) * (width // 4), (sprite // 4) * (width // 4), width // 4, width // 4)
        self.sprite = pygame.transform.scale(self.sprite_sheet.subsurface(rect), (64 * self.coeff, 80 * self.coeff))

    def update(self, keys, dt):
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
                    self.x += dx * 2/3
                    self.y += dy * 2/3
                    if dy >0:
                        self.dir = 'u'
                    else:
                        self.dir = 'd'
                else:
                    self.x += dx
                    self.y += dy

                id = f"walk_{self.dir}"
                self.get_animation_frame(id, dt)
            else:
                self.moving = False
                id = f"idle_{self.dir}"
                self.get_animation_frame(id, dt)

            
                


# Création des deux personnages
Dresseur = Player(sprite_sheet=pygame.transform.scale(pygame.image.load("sprites/persos/11.png"), (100,100)), username="Ixemax") 
#on met la texture en carré comme ça on a pas de problème pour piocher un sprite (largeur != hauteur sur l'originale)
