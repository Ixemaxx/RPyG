import pygame
import random
import assets
import copy

pygame.mixer.init()
pygame.display.set_mode((1920, 1080))


# moves = [nom, dégats, pp, précision, type]
moves = {"charge": ["Charge", 20, 40, 100, "normal", "charge", "atk"],
         "dracom": ["Draco-Météores", 130, 5, 90, "dragon", "dracom", "atk2"],
         "trempette": ["Trempette", 0, 1, 35, "eau", "trempette", None],
         "heal": ["Soin", 0, 5, 100, "normal", "heal", "heal"],
         "lutte": ["Lutte", 50, 1, 100, "normal", "lutte", "lutte"]
         }

class Creature:
    def __init__(self, name, hp, attack, defense, sprite, moveset, type, lvl, req_xp, map, speed, ball='pykeball'):
        self.name = name
        self.hp = hp # pour ajouter un peu de variété dans les stats des créatures 
        self.shiny = random.randint(0,3)
        self.nick = copy.deepcopy(self.name)
        self.max_hp = hp
        self.before_hp = hp # utilisé pour faire l'effet d'animation de la barre de vie
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.status = None
        self.ball = 'pykeball'
        self.sprite = [s.copy() for s in sprite] # sprite est une liste [texture de face et de dos]
        self.moveset = moveset # liste contenant le moveset [m1, m2, m3, m4] un move est une clé définie dans le dictionnaire moves
        self.pps = []
        self.usable_mvs = []
        for move in self.moveset:
            self.pps.append(move[2])
            self.usable_mvs.append(move[5])
        self.type = type # str du nom du type
        self.lvl = lvl
        self.xp = 0
        self.req_xp = req_xp
        if map != 'ball': # map est un argument inutilisé, il sert ici à empêcher le sprite de regrossir après une capture de pykemon
            for i in range(len(self.sprite)):
                self.sprite[i] = pygame.transform.scale(self.sprite[i],(self.sprite[i].get_width() * 5, self.sprite[i].get_height() * 5))

    def lvlup(self):
        self.lvl += 1
        self.xp = max(self.xp - self.req_xp, 0)
        self.max_hp += 2
        self.hp += 2
        self.req_xp *= 1.2
        self.attack += 2
        self.defense += 2
        self.speed += 2
        self.before_hp = self.hp

    def nick(self, nickname): # renommer le Pykemon
        self.nick = nickname

    def get_sound(self, snd):
        if snd == "atk":
            return assets.atk_snd
        if snd == "atk2":
            return assets.atk2_snd
        if snd == "heal":
            return assets.heal_snd
        

    def copy(self, caught_ball):
        creature = Creature(self.name, self.max_hp, self.attack, self.defense, self.sprite, self.moveset, self.type, self.lvl, self.req_xp, 'ball', self.speed, ball=caught_ball)

        creature.pps = copy.deepcopy(self.pps)
        creature.usable_mvs = copy.deepcopy(self.usable_mvs)
        creature.xp = copy.deepcopy(self.xp)
        creature.hp = copy.deepcopy(self.hp)
        creature.shiny = copy.deepcopy(self.shiny)
        creature.nick = copy.deepcopy(self.nick)
        creature.status = copy.deepcopy(self.status)
        return creature



    def atk(self, move, opponent, origin):
        precision = moves[move][3]
        efficacite = self.efficacite(move, opponent.type) # renvoie None si inneficace, sinon renvoie un coeff multiplicateur de dégâts

        self.before_hp = copy.deepcopy(self.hp)
        opponent.before_hp = copy.deepcopy(opponent.hp)

        # on vérifie que le move est pas épuisé en PPs chez le bot (il pick au hasard puis par élimination)
        if origin == "adv" and move != "lutte": # lutte n'est pas un move du pykemon, ça foutrait en l'air ce bout de code de le vérifier
            for i in range(len(self.pps)):
                if self.pps[i] <= 0:
                    self.usable_mvs[i] = None

            if not move in self.usable_mvs:
                choice = random.choice(self.usable_mvs)
                while choice == None:
                    choice = random.choice(self.usable_mvs)
                move = str(choice)

            for i in range(len(self.usable_mvs)):
                if self.usable_mvs[i] == move:
                    BotPos = i
            
            self.pps[BotPos] -= 1 # on retire les pps du bot ici

        # on définit le lanceur et la cible
        if origin == "p":
                lanceur = f"{self.name} utilise {moves[move][0]} !"
                cible = f"le {opponent.name} adverse."
        else:
            lanceur = f"Le {opponent.name} adverse utilise {moves[move][0]} !"
            cible = f"votre {self.name}."

        # attaques particulières
        if moves[move][0] == "Trempette": #trempette bypass l'efficacité et la précision
            return [lanceur, "Cela n'a aucun effet."]
        
        if moves[move][0] == "Soin": # soin bypass aussi le reste
            self.hp = int(round(min(self.max_hp, self.hp + self.max_hp /2)))
            assets.heal_snd.play()
            return [lanceur, "Il regagne des PV."]
        
        if moves[move][0] == "Lutte": # soin bypass aussi le reste
            self.hp = int(max(0, self.hp - self.max_hp /4))
            opponent.hp = round(max(opponent.hp - (((((opponent.lvl * 0.4 + 2) * self.attack * moves[move][1])/opponent.defense) / 50) + 2) * efficacite, 0))
            assets.atk_snd.play()
            
            return [lanceur, "Il se blesse dans son attaque."]


        # efficacité
        if efficacite == 0:
            return [lanceur, "Cela n'affecte pas", cible]      
        else:
            if efficacite > 1:
                msg = [lanceur, f"C'est super efficace sur {cible}"]
                snd = assets.super_eff_snd

            elif efficacite == 0.5:
                msg = [lanceur, f"Ce n'est pas très efficace sur {cible}"]
                snd = assets.not_eff_snd
            else:
                msg = [lanceur, f"C'est efficace sur {cible}"]
                snd = assets.effective_snd

            # précision de l'attaque
            if precision > random.randint(0,100): # attaque réussie
                opponent.hp = int(round(max(opponent.hp - (((((opponent.lvl * 0.4 + 2) * self.attack * moves[move][1])/opponent.defense) / 50) + 2) * efficacite, 0))) # vraie formule de pokemon
                
                self.get_sound(moves[move][6]).play()
                snd.play()
                return msg
            else: # attaque esquivée
                return [lanceur, cible, "a esquivé l'Attaque !"]
            

    def efficacite(self, move, type_adv): # l'efficacité est aléatoire pour la démo, ça rajoute du peps on va dire
        move_type = moves[move][4]
        for type in types[move_type]:
            if type == type_adv:
                return types[type]
            
        return 1


def base_copy(creature_name):
    if creature_name in bookmark:
        params = bookmark[creature_name]
        # On déballe la liste avec *params
        return Creature(*params)
    return None

bookmark = {"Punkromatides": ["Punkromatides", 12, 6, 6, [pygame.image.load("sprites/creatures/kackaburr_front.png").convert_alpha(), pygame.image.load("sprites/creatures/kackaburr_back.png").convert_alpha()], [moves["charge"], moves["dracom"]], "normal", 2, 20 , "lil_garden", 6]}

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