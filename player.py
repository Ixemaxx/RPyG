import pygame

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

class Player:
    def __init__(self, sprite_sheet, username = "Red", team = None, inv = None):

        self.sprite_sheet = sprite_sheet #alpha pour retirer le fond blanc
        self.sprite = sprite_sheet #provisoire, le temps d'appeler get_sprite()
        self.username = username
        self.able = True #able définit la capacité du joueur à interagir avec son perso (bouger, parler aux pnj...)
        #création de l'équipe
        self.team = []
        for i in range(6):
            self.team.append(None)

    def update(self, keys, dt):
        global speed 

        if self.able:
            if keys[keymap["left"]]:
                self.x -= speed * dt
            if keys[keymap["right"]]:
                self.x += speed * dt
            if keys[keymap["up"]]:
                self.y -= speed * dt
            if keys[keymap["down"]]:
                self.y += speed * dt
            elif keys[keymap["e"]]:
                speed = 420

            #self.x += dx
            #self.y += dy


# Création des deux personnages
Dresseur = Player(sprite_sheet=pygame.transform.scale(pygame.image.load("sprites/persos/11.png"), (100,100)), username="Ixemax") 
#on met la texture en carré comme ça on a pas de problème pour piocher un sprite (largeur != hauteur sur l'originale)
