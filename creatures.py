import pygame
import random

# moves = [nom, dégats, pp, précision, type]
moves = {"charge": ["Charge", 20, 30, 100, "normal", "charge"],
         "dracom": ["Draco-Météores", 70, 5, 90, "dragon", "dracom"],
         "trempette": ["Trempette", 0, 40, 0, "eau", "trempette"]
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
        self.req_xp *= 1.3
        self.attack += 20
        self.defense += 20


    def atk(self, move, opponent, origin):
        precision = moves[move][3]
        efficacite = self.efficacite(move, opponent.type) # renvoie None si inneficace, sinon renvoie un coeff multiplicateur de dégâts
        print(efficacite, move, opponent.type, moves[move][4])

        if origin == "player":
                lanceur = f"{self.name} utilise {moves[move][0]} !"
                cible = f"le {opponent.name} adverse."
        else:
            lanceur = f"Le {opponent.name} adverse utilise {moves[move][0]} !"
            cible = f"votre {self.name}."

        if moves[move][0] == "Trempette": #trempette bypass l'efficacité et la précision
                return [lanceur, "Cela n'a aucun effet."]

        if efficacite == 0:
            return [lanceur, "Cela n'affecte pas", cible]      
        else:
            if efficacite > 1:
                msg = [lanceur, "C'est super efficace sur", cible]
            elif efficacite == 0.5:
                msg = [lanceur, "Ce n'est pas très efficace sur", cible]
            else:
                msg = [lanceur, "C'est efficace sur", cible]

            if precision > random.randint(0,100): # attaque réussie
                opponent.hp -= int(abs(moves[move][1] * efficacite))
                if opponent.hp < 0: 
                    opponent.hp = 0
                return msg
            else: # attaque esquivée
                return [lanceur, cible, "a esquivé l'Attaque !"]
            

    def efficacite(self, move, type_adv): # l'efficacité est aléatoire pour la démo, ça rajoute du peps on va dire
        move_type = moves[move][4]
        for type in types[move_type]:
            if type == type_adv:
                return types[type]
            
        return 1


def copy(creature_name):
    if creature_name in bookmark:
        params = bookmark[creature_name]
        # On déballe la liste avec *params
        return Creature(*params)
    return None

bookmark = {"punkromatides": ["Punkromatides", 50, 20, 20, [pygame.image.load("sprites/creatures/kackaburr_front.png"), pygame.image.load("sprites/creatures/kackaburr_back.png")], [moves["charge"],moves["dracom"],moves["trempette"],moves["dracom"]], "normal", random.randint(2, 5), 20 , "lil_garden"]}

types = {
    "normal": {"roche": 0.5, "spectre": 0, "acier": 0.5},
    "feu": {"feu": 0.5, "eau": 0.5, "plante": 2, "glace": 2, "insecte": 2, "roche": 0.5, "dragon": 0.5, "acier": 2},
    "eau": {"feu": 2, "eau": 0.5, "plante": 0.5, "sol": 2, "roche": 2, "dragon": 0.5},
    "plante": {"feu": 0.5, "eau": 2, "plante": 0.5, "poison": 0.5, "sol": 2, "vol": 0.5, "insecte": 0.5, "roche": 2, "dragon": 0.5, "acier": 0.5},
    "electrik": {"eau": 2, "plante": 0.5, "electrik": 0.5, "sol": 0, "vol": 2, "dragon": 0.5},
    "glace": {"feu": 0.5, "eau": 0.5, "plante": 2, "glace": 0.5, "sol": 2, "vol": 2, "dragon": 2, "acier": 0.5},
    "combat": {"normal": 2, "glace": 2, "poison": 0.5, "vol": 0.5, "psy": 0.5, "insecte": 0.5, "roche": 2, "spectre": 0, "tenebres": 2, "acier": 2, "fee": 0.5},
    "poison": {"plante": 2, "poison": 0.5, "sol": 0.5, "roche": 0.5, "spectre": 0.5, "acier": 0, "fee": 2},
    "sol": {"feu": 2, "plante": 0.5, "electrik": 2, "poison": 2, "vol": 0, "insecte": 0.5, "acier": 2},
    "vol": {"plante": 2, "electrik": 0.5, "combat": 2, "insecte": 2, "roche": 0.5, "acier": 0.5},
    "psy": {"combat": 2, "poison": 2, "psy": 0.5, "tenebres": 0, "acier": 0.5},
    "insecte": {"feu": 0.5, "plante": 2, "combat": 0.5, "poison": 0.5, "vol": 0.5, "spectre": 0.5, "acier": 0.5, "fee": 0.5, "psy": 2, "tenebres": 2},
    "roche": {"feu": 2, "glace": 2, "combat": 0.5, "sol": 0.5, "vol": 2, "insecte": 2, "acier": 0.5},
    "spectre": {"normal": 0, "psy": 2, "spectre": 2, "tenebres": 0.5},
    "dragon": {"dragon": 2, "acier": 0.5, "fee": 0},
    "tenebres": {"combat": 0.5, "psy": 2, "spectre": 2, "tenebres": 0.5, "fee": 0.5},
    "acier": {"feu": 0.5, "eau": 0.5, "electrik": 0.5, "glace": 2, "roche": 2, "acier": 0.5, "fee": 2},
    "fee": {"feu": 0.5, "combat": 2, "poison": 0.5, "dragon": 2, "tenebres": 2, "acier": 0.5}
}