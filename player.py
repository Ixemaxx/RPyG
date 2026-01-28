import pygame

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (43, 251, 47)
ORANGE = (251, 161, 43)
DARK_ORANGE = (251, 133, 43)
LOW_HP = (166, 23, 23)

class Player:
    def __init__(self, username = "Red", team = [], inv = {}, sprite):

        self.texture = sprite.convert_alpha() #alpha pour retirer le fond blanc
        self.username = username
        self.able = True #able définit la capacité du joueur à interagir avec son perso (bouger, parler aux pnj...)
        for i in range(6):
            team.append(None)
        print(self.team)

    def update(self, keys):

        if self.able:
            if keys[self.left]:
                pass
            elif keys[self.right]:
                pass


# Création des deux personnages
Dresseur = Player("Ixemax",sprite=pygame.image.load("sprites/humans/player.png"))
