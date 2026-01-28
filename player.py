import pygame

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

        self.texture = sprite #alpha pour retirer le fond blanc
        self.username = username
        self.able = True #able définit la capacité du joueur à interagir avec son perso (bouger, parler aux pnj...)
        #création de l'équipe
        self.team = []
        for i in range(6):
            self.team.append(None)
        print(self.team)

    def update(self, keys):

        if self.able:
            if keys[self.left]:
                pass
            elif keys[self.right]:
                pass


# Création des deux personnages
Dresseur = Player(sprite=pygame.image.load("sprites/tilemap/wood2.png"), username="Ixemax")
