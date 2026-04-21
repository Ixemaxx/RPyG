import pygame
import random

# moves = [nom, dégats, pp, précision, type]
moves = {"charge": ["Charge", 20, 30, 100, "normal", "charge"],
         "dracom": ["Draco-Météores", 70, 5, 90, "dragon", "dracom"],
         }

class Creature:
    def __init__(self, name, hp, attack, defense, sprite, moveset, type, lvl, req_xp, map):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.sprite = [s.copy() for s in sprite] # sprite est une liste [texture de face et de dos]
        self.moveset = moveset # liste contenant le moveset [m1, m2, m3, m4] un move est une clé définie dans le dictionnaire moves
        self.pps = []
        for move in self.moveset:
            self.pps.append(move[2])
        self.type = type # str du nom du type
        self.lvl = lvl
        self.xp = 0
        self.req_xp = req_xp
        for i in range(len(self.sprite)):
            self.sprite[i] = pygame.transform.scale(self.sprite[i],(self.sprite[i].get_width() * 5, self.sprite[i].get_height() * 5))

    def lvlup(self):
        self.lvl += 1
        self.xp = 0
        self.max_hp += 20
        self.hp += 20
        self.req_xp *= 1.1
        self.attack += 20
        self.defense += 20


    def atk(self, move, opponent):
        precision = moves[move][3]
        efficacite = self.efficacite(move, opponent.type) # renvoie None si inneficace, sinon renvoie un coeff multiplicateur de dégâts

        if efficacite == None:
            return [f"{moves[move][0]} n'affecte pas le {opponent.name} adverse"]
        else:
            if efficacite > 1:
                msg = ["C'est super efficace !"]
            elif efficacite == 0.5:
                msg = ["Ce n'est pas très efficace..."]
            else:
                msg = ["C'est efficace"]

            if precision > random.randint(0,100): # attaque réussie
                opponent.hp -= (moves[move][1] * efficacite)
                if opponent.hp > 0:
                    return msg
                else:
                    return [msg, f"Le {opponent.name} est K.O !"] # la liste permet d'afficher les infos sur 2 lignes différentes dans la boite de texte
            else: # attaque esquivée
                return f"Le {opponent.name} a esquivé l'attaque !"
            

    def efficacite(self, move, type): # l'efficacité est aléatoire pour la démo, ça rajoute du peps on va dire
        value = random.choice([None, 0.5, 1, 1.5])
        return value


def copy(creature_name):
    if creature_name in bookmark:
        params = bookmark[creature_name]
        # On déballe la liste avec *params
        return Creature(*params)
    return None

bookmark = {"punkromatides": ["Punkromatides", 50, 20, 20, [pygame.image.load("sprites/creatures/kackaburr_front.png"), pygame.image.load("sprites/creatures/kackaburr_back.png")], [moves["charge"],moves["dracom"],moves["charge"],moves["dracom"]], "normal", random.randint(2, 5), 20 , "lil_garden"]}

