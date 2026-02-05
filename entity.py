import pygame
import os
from dresseur import Dresseur

os.chdir(os.path.dirname(os.path.abspath(__file__)))

entities = []
case = 120 # côté d'une tile

class Entity:
    def __init__(self, type, x, y, map, state, npc_name=None, npc_dir=None, npc_sprite=None, npc_team=None, reward=None, npc_dialog = None, npc_action = 0):
        self.x = x
        self.y = y
        self.type = type # npc ou item
        self.reward = reward # si combat => argent, si item => l'item, si npc échange => la créature etc.
        self.state = state # 0 => item non récupéré ou npc jamais rencontré ou combat de dresseur perdu. Sinon 1
        self.map = map # map dans laquelle l'entité apparait

        if type == "npc":
            self.npc = Dresseur(npc_sprite,npc_name,npc_team,dir=npc_dir)
            self.npc.extract_anim()       # bug quand je le fais, ça applique le changement au joueur
            self.npc.update(keys=0, dt=0, map=None, entities=None)

            self.dialog = npc_dialog # le dialogue
            self.action = npc_action # dialogue 0, combat 1, échange 2, cadeau 3



def draw_entities(map): # on obtient les entités d'une certaine map grâce à self.map
    
    current_entities = []
    layer = pygame.Surface((1920,1080),pygame.SRCALPHA) # on crée une surface de la taille de l'écran

    for entity in entities:
        if entity.map == map:
            current_entities.append(entity)

    for entity in current_entities:
        layer.blit(entity.npc.sprite, (entity.x, entity.y))

    return layer, current_entities

little_house_npc_1 = Entity(type = "npc", x = case * 9 - (case * 0.87), y = case * 5 - case // 3, map="lil_garden", state=0, npc_name="Bob", npc_dir="l", npc_sprite = pygame.transform.scale(pygame.image.load("sprites/persos/10.png"), (100,100)), npc_team=None, reward=100, npc_dialog=["Salut ! Je suis Bob.","Bienvenue dans mon humble demeure !"], npc_action=1)
entities.append(little_house_npc_1)