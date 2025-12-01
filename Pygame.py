"""
    Initialiser la fenêtre PyGame.<br>
    2. Créer un système de Caméra : variables offset_x, offset_y qui changent avec les touches ZQSD pour scroller la carte.<br>
    3. Convertir les coordonnées souris (écran) en coordonnées grille (logique) pour savoir sur quelle case on clique.
"""
import pygame
import sys
import random
import math

pygame.init()

# -------------------------
# CONFIG
# -------------------------
TILE_SIZE = 32

ZOOM_STEP = 1   # combien on augmente/diminue à chaque zoom
MIN_TILE = 8
MAX_TILE = 64

MAP_W = 50     
MAP_H = 50

SCREEN_W = 1000
SCREEN_H = 700

center_w = MAP_W//3
center_h = MAP_H//3

start_x = (MAP_W - center_w) // 2
end_x = start_x + center_w

start_y = (MAP_H - center_h) // 2
end_y = start_y + center_h


screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Camera / Mouse → Grid")

clock = pygame.time.Clock()

#pour la caméra
offset_x = 0
offset_y = 0
CAMERA_SPEED = 10

#génerer la map avec des valeurs aléatoires
def generate_map():
    grid = []
    for y in range(MAP_H):
        row = []
        for x in range(MAP_W):
            # Probabilités simples
            r = random.random()
            if r < 0.1:
                row.append("W")  # bois
            elif r < 0.15:
                row.append("G")  # or
            elif r < 0.2:
                row.append("F")  # ferme
            else:
                row.append(".")  # vide
        grid.append(row)
    return grid

def generate_map_gold():
    grid = []
    for y in range(MAP_H):
        row = []
        for x in range(MAP_W):
            # Probabilités simples
            r = random.random()
            
            if (start_x < x < end_x) and (start_y < y < end_y):
                if r<0.7:
                    row.append("G")
                elif r < 0.8:
                    row.append("F")  # ferme
                elif r < 0.9:
                     row.append("W")  # bois
                else:
                    row.append(".")  # vide

            else:
                if r < 0.1:
                    row.append("W")  # bois
                elif r < 0.2:
                    row.append("F")  # ferme
                else:
                    row.append(".")  # vide
        grid.append(row)
    return grid



grid = generate_map_gold()

def draw_map():
    for y in range(MAP_H):
        for x in range(MAP_W):
            tile = grid[y][x]

            if tile == "W":
                color = (34, 139, 34)  # vert foncé 
            elif tile == "F":
                color = (194, 178, 128)  # beige 
            elif tile == "G":
                color = (218, 165, 32)  # or
            else:
                color = (50, 205, 50)  # vert clair

            pygame.draw.rect(screen, color,
                pygame.Rect(
                    x * TILE_SIZE - offset_x,
                    y * TILE_SIZE - offset_y,
                    TILE_SIZE,
                    TILE_SIZE
                )
            )

#boucle principale 
while True:
    dt = clock.tick(60)

    # a chaque events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # click gauche : montrer tile coord
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()

            # conversion pixel écran en coord de grille
            gx = (mx + offset_x) // TILE_SIZE
            gy = (my + offset_y) // TILE_SIZE
            if 0 <= gx < MAP_W and 0 <= gy < MAP_H:
                print(f"Clicked tile: ({gx}, {gy}) = {grid[gy][gx]}")

            if event.type == pygame.MOUSEWHEEL:
                 # zoom avec molette
                old_tile_size = TILE_SIZE
                TILE_SIZE += event.y * ZOOM_STEP
                TILE_SIZE = max(MIN_TILE, min(MAX_TILE, TILE_SIZE))

                # Ajuste offset pour que la souris reste sur la même tile après zoom
                mx, my = pygame.mouse.get_pos()
                offset_x = int((offset_x + mx) * TILE_SIZE / old_tile_size - mx)
                offset_y = int((offset_y + my) * TILE_SIZE / old_tile_size - my)

    # touche pour controler la camera
    keys = pygame.key.get_pressed()

    if keys[pygame.K_z]:
        offset_y -= CAMERA_SPEED
    if keys[pygame.K_s]:
        offset_y += CAMERA_SPEED
    if keys[pygame.K_q]:
        offset_x -= CAMERA_SPEED
    if keys[pygame.K_d]:
        offset_x += CAMERA_SPEED

    #Zoom avec le clavier
    if keys[pygame.K_p]:
        old_tile_size = TILE_SIZE
        TILE_SIZE += ZOOM_STEP
        TILE_SIZE = min(TILE_SIZE, MAX_TILE)
        mx, my = SCREEN_W//2, SCREEN_H//2  # zoom centrée sur le centre de l'écran
        offset_x = int((offset_x + mx) * TILE_SIZE / old_tile_size - mx)
        offset_y = int((offset_y + my) * TILE_SIZE / old_tile_size - my)
    if keys[pygame.K_m]:
        old_tile_size = TILE_SIZE
        TILE_SIZE -= ZOOM_STEP
        TILE_SIZE = max(TILE_SIZE, MIN_TILE)
        mx, my = SCREEN_W//2, SCREEN_H//2
        offset_x = int((offset_x + mx) * TILE_SIZE / old_tile_size - mx)
        offset_y = int((offset_y + my) * TILE_SIZE / old_tile_size - my)


    #limite de la caméra
    max_offset_x = max(MAP_W * TILE_SIZE - SCREEN_W, 0)
    max_offset_y = max(MAP_H * TILE_SIZE - SCREEN_H, 0)
    offset_x = max(0, min(offset_x, max_offset_x))
    offset_y = max(0, min(offset_y, max_offset_y))

    # draw
    screen.fill((0,0,0))
    draw_map()
    pygame.display.flip()