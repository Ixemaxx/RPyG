from cmath import rect
import pygame
import os
import random # pour la rotation aléatoire
import assets


pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.display.set_mode((1920, 1080))

tilemap = []
sprite_sheet = pygame.image.load("sprites/tilemap/Tileset.png").convert()
sh_width = sprite_sheet.get_width() # = la hauteur car carré
maplist = []
isNewMap = False
rotating_tiles = [0,1]
rotating_surface = [] # la version surface des tiles 
rotation = [0, 90, 180, 270] # rotation en degrés à appliquer

SectionName = {"lil_garden": "Route 1", "lil_house": "Ma Maison"}


def tilemap_manager():
    global tilemap, sprite_sheet

    # On parcourt par ligne (row) puis par colonne (col)
    for row in range(64):
        for col in range(64):
            # On définit la zone (x, y, largeur, hauteur)
            rect = pygame.Rect(col * sh_width // 64, row * sh_width // 64, sh_width // 64, sh_width // 64)
            
            # On crée une référence à cette portion de l'image
            portion = pygame.transform.scale(sprite_sheet.subsurface(rect), (tile_size,tile_size))
            
            tilemap.append(portion)
            if row * 64 + col in rotating_tiles: # si dans rotating tiles, on ajoute la surface dans rotating_surface
                rotating_surface.append(portion)

def draw_map():

    map_w = 1920
    map_h = 1080
    map_surface = pygame.Surface((map_w,map_h),pygame.SRCALPHA)


    for y, line in enumerate(map):
        for x, case in enumerate(line):
            # On récupère la surface pré-découpée
            tile_image = get_tile(case) 
            # Calcul de la position à l'écran
            if tile_image in rotating_surface: 
                map_surface.blit(pygame.transform.rotate(tile_image,random.choice(rotation)), (x * tile_size , y * tile_size ))
            else:
                map_surface.blit(tile_image, (x * tile_size , y * tile_size ))

    return map_surface

def change_map(new_map,new_name):
    global map, map_id, map_layer, isNewMap

    map = new_map
    map_id = new_name
    map_layer = draw_map()
    isNewMap = True


def get_tile(tile): #récupérer une tile dans la tilemap (liste)
    return tilemap[tile]


lil_garden = [[67, 67, 67, 67, 67, 67, 67, 257, 67, 67, 67, 67 , 130, 130, 130, 130],\
             [130, 130, 130, 130, 130, 130, 130, 257, 130, 130, 130, 130 , 23, 24, 25, 0],\
             [0, 0, 0, 0, 0, 0, 0, 257, 0, 0, 0 ,0 , 87, 88, 89, 0],\
             [0, 0, 2, 3, 0, 0, 0, 257, 0, 0, 0 ,0 , 151, 152, 153, 0],\
             [262, 262, 262, 262, 262, 262, 262, 258, 262, 262, 262 ,260 , 215, 216, 217, 0],\
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,257 , 279, 282, 281, 0],\
             [0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0 ,263 , 262, 258, 262, 262],\
             [0, 70, 70, 70, 70, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0],\
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0]]


lil_house = [[131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131 , 131, 131, 131, 131],\
                    [131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131, 131 , 131, 131, 131, 131],\
                    [131, 131, 131, 131, 34, 34, 34, 34, 102, 102, 102 ,102 , 131, 131, 131, 131],\
                    [131, 131, 131, 131, 102, 102, 102, 102, 102, 102, 102 ,102 , 131, 131, 131, 131],\
                    [131, 131, 131, 131, 102, 102, 102, 102, 102, 102, 102 ,102 , 131, 131, 131, 131],\
                    [131, 131, 131, 131, 102, 102, 102, 102, 102, 102, 102 ,102 , 131, 131, 131, 131],\
                    [131, 131, 131, 131, 102, 102, 102, 102, 102, 102, 102 ,102 , 131, 131, 131, 131],\
                    [131, 131, 131, 131, 131, 131, 131, 102, 102, 131, 131 ,131 , 131, 131, 131, 131],\
                    [131, 131, 131, 131, 131, 131, 131, 102, 102, 131, 131 ,131 , 131, 131, 131, 131]]

maplist.append(lil_garden) # la maplist sert à gérer les entités
maplist.append(lil_house)



tile_size = 1920 // 16 # 16 = len(world_map[0])
tilemap_manager() #pour créer la liste qui découpe la tilemap en petites sections
change_map(lil_garden,"lil_garden")

#notes pour les maps:
# 2 et 3 = banc
# 280 = centre bas de la maison rouge(sans briques)
# 517 = sol uni avec le devant des maisons (routes)
