import pygame

pygame.init()
pygame.mixer.init()
pygame.display.set_mode((1920, 1080))

# sounds
grass_snd = pygame.mixer.Sound("sounds/grass.mp3")
wild_snd = pygame.mixer.Sound("sounds/wild.mp3")
atk_snd = pygame.mixer.Sound("sounds/atk.mp3")
atk2_snd = pygame.mixer.Sound("sounds/atk2.mp3")
heal_snd = pygame.mixer.Sound("sounds/heal.mp3")


# génération des animations de balls
balls_tex = pygame.image.load("sprites/items/balls.png").convert_alpha()
balls = {}

def get_ball(col, name):
    ball_frames = [] # contiendera chaque frame de la ball désirée
    grid_size = 17
    case_size = balls_tex.get_width() / 17

    for x in range(grid_size):
        if x == col:
            for y in range(grid_size):
                rect = pygame.Rect(x, y, x + case_size, y + case_size)
                ball_frames.append(pygame.transform.scale(balls_tex.subsurface(rect), (98, 98)))

            balls[name] = ball_frames
            break

    
get_ball(3, "pykeball") # colonnes de 0 à 16 (17 en tout)
get_ball(2, "superball") # colonnes de 0 à 16 (17 en tout)

# inventaire
sac_parts = ["heals","balls","unique"]
inventory = {
    # balls
    "pykeball": {'type': 'balls', 'tex': balls['pykeball']},
    "superball": {'type': 'balls', 'tex': balls['superball']},
    # heals
    "potion": {'type': 'heals', 'tex': balls['pykeball']},
    "rappel": {'type': 'heals', 'tex': balls['pykeball']},
    # unique
    "dex": {'type': 'unique', 'tex': balls['pykeball']}
}


