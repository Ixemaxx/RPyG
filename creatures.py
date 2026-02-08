import pygame
import random

# moves = [nom, dégats, pp, précision, type]
moves = {"charge": ["Charge", 20, 30, 100, "normal"],
         "dracom": ["Draco Météores", 130, 5, 90, "dragon"],
         }

class Creature:
    def __init__(self, name, hp, attack, defense, sprite, moveset, type):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sprite = sprite
        self.moveset = moveset # liste contenant le moveset [m1, m2, m3, m4] un move est une clé définie dans le dictionnaire moves
        self.type = type # str du nom du type

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


