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

class Player:
    def __init__(self, sprite, username = "Red", team = None, inv = None):

        self.sprite = sprite #alpha pour retirer le fond blanc
        self.username = username
        self.able = True #able définit la capacité du joueur à interagir avec son perso (bouger, parler aux pnj...)
        #création de l'équipe
        self.team = []
        for i in range(6):
            self.team.append(None)

    def update(self, keys):

        if self.able:
            if keys[self.left]:
                pass
            elif keys[self.right]:
                pass


# Création des deux personnages
Dresseur = Player(sprite=pygame.transform.scale(pygame.image.load("sprites/persos/11.png"), (100,100)), username="Ixemax") 
#on met la texture en carré comme ça on a pas de problème pour piocher un sprite (largeur != hauteur sur l'originale)
