import pygame

tilemap = None

def tilemap_manager():
    global tilemap

    tilemap = []
    for col in range(64):
        for line in range(64):
            tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            tilemap.append(tile)
            #tile.blit(self.sprite_sheet, (0, 0), (col * tile_size, line * tile_size, tile_size, tile_size))

    print(tilemap)

def get_tile(tile): #récupérer une tile dans la tilemap (liste)
    return tilemap[tile]

world_map = [[0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0],\
             [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0],\
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0],\
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 , 0, 0, 0, 0],\
             [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0 ,0 , 0, 0, 0, 0],\
             [0, 0, 0, 0, 0, 1, 1, 1, 3, 0, 0 ,0 , 1, 0, 0, 0],\
             [0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0 ,0 , 2, 0, 0, 0],\
             [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0 ,2 , 2, 2, 0, 0],\
             [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0 ,0 , 2, 0, 0, 0]]


tile_size = 1920 // len(world_map[0]) #16 ? 
tilemap_manager() #pour créer la liste qui découpe la tilemap en petites sections

