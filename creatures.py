import pygame
import random

# moves = [nom, dégats, pp, précision, type]
moves = {"charge": ["Charge", 20, 30, 100, "normal"],
         "dracom": ["Draco Météores", 130, 5, 90, "dragon"],
         }

class Creature:
    def __init__(self, name, hp, attack, defense, sprite, moveset, type, lvl, req_xp, map):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sprite = sprite
        self.moveset = moveset # liste contenant le moveset [m1, m2, m3, m4] un move est une clé définie dans le dictionnaire moves
        self.type = type # str du nom du type
        self.lvl = lvl
        self.xp = 0
        self.req_xp = req_xp

    def atk(self, move, opponent):
        precision = moves[move][3]
        efficacite = self.efficacite(move, opponent.type) # renvoie None si inneficace, sinon renvoie un coeff multiplicateur de dégâts

        if efficacite > 1:
            msg = ["C'est super efficace !"]
        elif efficacite < 0:
            msg = ["Ce n'est pas très efficace..."]
        else:
            msg = ["C'est efficace"]

        if efficacite != None: # si l'attaque affecte l'adversaire
            if precision > random.randint(0,100): # attaque réussie
                opponent.hp -= move[1] * efficacite
                if opponent.hp > 0:
                    return msg
                else:
                    return [msg, f"Le {opponent.name} est K.O !"] # la liste permet d'afficher les infos sur 2 lignes différentes dans la boite de texte
            else: # attaque esquivée
                pass
        else:
            return [f"{moves[move][0]} n'affecte pas le {opponent.name} adverse"]

    def efficacite(self, move, type):
        pass


punkromatides = Creature("Punkromatides", 50, 20, 20, [pygame.image.load("sprites/creatures/kackaburr_front.png"), pygame.image.load("sprites/creatures/kackaburr_back.png")], [moves["charge"],None,None,None], "normal", random.randint(2, 5), 20 , "lil_garden")

