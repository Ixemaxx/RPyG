import pygame
import os
from dresseur import Dresseur
import maps

os.chdir(os.path.dirname(os.path.abspath(__file__)))

entities = []
case = 120 # côté d'une tile
all_sprites = pygame.sprite.Group()

class Entity(pygame.sprite.Sprite):
    def __init__(self, type, x, y, map, state, npc_name=None, npc_dir=None, npc_sprite=None, npc_team=None, reward=None, npc_dialog = None, 
                 npc_action = 0, warp_dest=None, warp_tp=None, warp_name=None, warp_dir=None, req_dir=None, hitbox_w=None,hitbox_h=None):
        
        super().__init__() # on initialise pygame.sprite.Sprite, pour créer un groupe de sprites
        self.x = x
        self.y = y
        self.type = type # npc ou item
        self.reward = reward # si combat => argent, si item => l'item, si npc échange => la créature etc.
        self.state = state # 0 => item non récupéré ou npc jamais rencontré ou combat de dresseur perdu. Sinon 1
        self.map = map # map dans laquelle l'entité apparait
        self.req_dir = req_dir # direction requise pour interagir avec l'entité
        

        if type == "npc":
            self.npc = Dresseur(npc_sprite,npc_name,npc_team,dir=npc_dir, x=self.x, y=self.y)
            self.npc.extract_anim() 
            self.npc.update(keys=0, dt=0, map=None, entities=None)

            # pour le spritegroup
            self.image = self.npc.sprite
            self.rect = self.image.get_rect(topleft=(x, y))

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

    def update(self): # mise à jour du sprite dynamiquement
        if self.type == "npc":
            self.image = self.npc.sprite  # Met à jour l'image pour l'animation
            self.rect.topleft = (self.x, self.y) # Met à jour la position
        elif self.type == "warp":
            self.hitbox.topleft = (self.x, self.y) # Met à jour la position de la hitbox





def get_curr_entities(map):
    global all_sprites 

    all_sprites = pygame.sprite.Group()

    for entity in entities:
        if entity.map == map:
            all_sprites.add(entity)

    return all_sprites


little_garden_npc_1 = Entity(type = "npc", x = case * 9 - (case * 0.87), y = case * 5 - case // 3, map = "lil_house",\
                              state = 0, npc_name = "Maman", npc_dir = "d", npc_sprite = pygame.transform.scale(pygame.image.load("sprites/persos/mom.png"),\
                             (100,100)), npc_team = None, reward = 100, npc_dialog = ["Fais attention dehors","il y a des PyKemons sauvages !"], npc_action = 1)

entities.append(little_garden_npc_1)

little_garden_warp_1 = Entity(type = "warp", x = case * 13 + case // 4, y = case * 5 , map="lil_garden",\
                               state = 0, warp_dest = maps.lil_house, warp_name = "lil_house",\
                                warp_tp = (case * 8.5 - (case * 0.87), case * 8 - case // 3), warp_dir ="u", req_dir = "u",hitbox_h = case, hitbox_w = case // 2)

entities.append(little_garden_warp_1)

little_house_warp = Entity(type = "warp", x = case * 7, y = case * 8.95 , map = "lil_house",\
                            state = 0, warp_dest = maps.lil_garden, warp_name = "lil_garden",\
                            warp_tp=(case * 14 - (case * 0.87), case * 6 - case // 3), warp_dir = "d", hitbox_h = case, hitbox_w = case*2)

entities.append(little_house_warp)

all_sprites = get_curr_entities(maps.map_id)