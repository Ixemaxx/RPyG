import pygame

pygame.init()

tilemap = []
sprite_sheet = pygame.image.load("sprites/tilemap/Tileset.png")
sh_width = sprite_sheet.get_width() # = la hauteur car carré
maplist = []

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

def draw_map():

    map_w = 1920
    map_h = 1080
    map_surface = pygame.Surface((map_w,map_h))


    for y, line in enumerate(map):
        for x, case in enumerate(line):
            # On récupère la surface pré-découpée
            tile_image = get_tile(case) 
            # Calcul de la position à l'écran
            map_surface.blit(tile_image, (x * tile_size , y * tile_size ))

    return map_surface

def change_map(new_map,name):
    global map, map_name, map_layer

    map = new_map
    map_name = name
    map_layer = draw_map()


def get_tile(tile): #récupérer une tile dans la tilemap (liste)
    return tilemap[tile]

lil_garden = [[67, 67, 67, 67, 67, 67, 67, 1, 67, 67, 67, 67 , 130, 130, 130, 130],\
             [130, 130, 130, 130, 130, 130, 130, 1, 130, 130, 130, 130 , 23, 24, 25, 0],\
             [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0 ,0 , 87, 88, 89, 0],\
             [0, 0, 2, 3, 0, 0, 0, 1, 0, 0, 0 ,0 , 151, 152, 153, 0],\
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1 , 215, 216, 217, 0],\
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,1 , 279, 282, 281, 0],\
             [0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0 ,1 , 1, 1, 1, 1],\
             [0, 70, 70, 70, 70, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0],\
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0]]


lil_house = [[67, 67, 67, 67, 67, 67, 67, 1, 67, 67, 67, 67 , 130, 130, 130, 130],\
                    [130, 130, 130, 130, 130, 130, 130, 1, 130, 130, 130, 130 , 0, 0, 0, 0],\
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0 ,0 , 0, 0, 0, 0],\
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0 ,0 , 0, 0, 0, 0],\
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ,1 , 0, 0, 0, 0],\
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,1 , 0, 0, 0, 0],\
                    [0, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0 ,1 , 1, 1, 1, 1],\
                    [0, 70, 70, 70, 70, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0],\
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0]]

maplist.append(lil_garden) # la maplist sert à gérer les entités




tile_size = 1920 // 16 # 16 = len(world_map[0])
tilemap_manager() #pour créer la liste qui découpe la tilemap en petites sections
change_map(lil_garden,"lil_garden")

#notes pour les maps:
# 2 et 3 = banc
# 280 = centre bas de la maison rouge(sans briques)
# 517 = sol uni avec le devant des maisons (routes)
