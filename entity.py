import pygame
import os
from dresseur import Dresseur
import maps

os.chdir(os.path.dirname(os.path.abspath(__file__)))

entities = []
case = 120 # côté d'une tile

class Entity:
    def __init__(self, type, x, y, map, state, npc_name=None, npc_dir=None, npc_sprite=None, npc_team=None, reward=None, npc_dialog = None, 
                 npc_action = 0, warp_dest=None, warp_tp=None, warp_name=None, warp_dir=None, req_dir=None, hitbox_w=None,hitbox_h=None):
        self.x = x
        self.y = y
        self.type = type # npc ou item
        self.reward = reward # si combat => argent, si item => l'item, si npc échange => la créature etc.
        self.state = state # 0 => item non récupéré ou npc jamais rencontré ou combat de dresseur perdu. Sinon 1
        self.map = map # map dans laquelle l'entité apparait
        self.req_dir = req_dir # direction requise pour interagir avec l'entité

        if type == "npc":
            self.npc = Dresseur(npc_sprite,npc_name,npc_team,dir=npc_dir)
            self.npc.extract_anim() 
            self.npc.update(keys=0, dt=0, map=None, entities=None)

            self.dialog = npc_dialog # le dialogue
            self.action = npc_action # dialogue 0, combat 1, échange 2, cadeau 3
    
        elif type == "warp":
            self.warp_dest = warp_dest
            self.player_pos = warp_tp
            self.warp_name = warp_name
            self.player_dir = warp_dir
            self.w = hitbox_w
            self.h = hitbox_h
            self.hitbox = pygame.Rect(self.x, self.y, self.w, self.h) # hitbox de la warp zone, à ajuster selon les besoins
            



def draw_entities(map): # on obtient les entités d'une certaine map grâce à self.map
    
    current_entities = []
    layer = pygame.Surface((1920,1080),pygame.SRCALPHA) # on crée une surface de la taille de l'écran

    for entity in entities:
        if entity.map == map:
            current_entities.append(entity)

    for entity in current_entities:
        if entity.type == "npc":
            layer.blit(entity.npc.sprite, (entity.x, entity.y))
        elif entity.type == "warp":
            pygame.draw.rect(layer, (0,255,0,100), entity.hitbox) # on dessine la hitbox de la warp zone pour la visualiser, à retirer ensuite

    return layer, current_entities

little_garden_npc_1 = Entity(type = "npc", x = case * 9 - (case * 0.87), y = case * 5 - case // 3, map = "lil_garden",\
                              state = 0, npc_name = "Bob", npc_dir = "l", npc_sprite = pygame.transform.scale(pygame.image.load("sprites/persos/10.png"),\
                             (100,100)), npc_team = None, reward = 100, npc_dialog = ["Salut ! Je suis Bob.","Bienvenue dans mon humble demeure !"], npc_action = 1)

entities.append(little_garden_npc_1)

little_garden_warp_1 = Entity(type = "warp", x = case * 13 + case // 4, y = case * 5 , map="lil_garden",\
                               state = 0, warp_dest = maps.lil_house, warp_name = "lil_house",\
                                warp_tp = (case * 8.5 - (case * 0.87), case * 8.3 - case // 3), warp_dir ="u", req_dir = "u",hitbox_h = case, hitbox_w = case // 2)

entities.append(little_garden_warp_1)

little_house_warp = Entity(type = "warp", x = case * 7, y = case * 8.95 , map = "lil_house",\
                            state = 0, warp_dest = maps.lil_garden, warp_name = "lil_garden",\
                            warp_tp=(case * 14 - (case * 0.87), case * 6 - case // 3), warp_dir = "d", hitbox_h = case, hitbox_w = case*2)

entities.append(little_house_warp)
