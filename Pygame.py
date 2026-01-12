"""
    Initialiser la fenêtre PyGame.<br>
    2. Créer un système de Caméra : variables offset_x, offset_y qui changent avec les touches ZQSD pour scroller la carte.<br>
    3. Convertir les coordonnées souris (écran) en coordonnées grille (logique) pour savoir sur quelle case on clique.


     grid to iso pour passer à 2.5D

    Première version /obsolète
"""
import pygame
import sys
from game_state import Gamestate

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

GRASS_TILE = pygame.image.load("assets/grass.png").convert_alpha() #image a changer

clock = pygame.time.Clock()


# -------------------------
# CAMERA
# -------------------------
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 15

camera = Camera()



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




grid = generate_map()

""""
def draw_map():
    for y in range(MAP_H):
        for x in range(MAP_W):
            tile = grid[y][x]

            if tile == "W":
                color = (42, 97, 55)  # vert foncé 
            elif tile == "F":
                color = (194, 178, 128)  # marron
            elif tile == "G":
                color = (237, 179, 35)  # or
            else:
                color = (50, 200, 37)  # vert clair

            pygame.draw.rect(screen, color,
                pygame.Rect(
                    x * TILE_SIZE - offset_x,
                    y * TILE_SIZE - offset_y,
                    TILE_SIZE,
                    TILE_SIZE
                )
            )
"""

def grid_to_iso(x,y):
    iso_x = (x - y) * (TILE_SIZE // 2)
    iso_y = (x + y) * (TILE_SIZE // 4)
    return iso_x, iso_y

def draw_tile_iso(iso_x, iso_y):
    """ Dessine une tuile losange isométrique """
    tile = pygame.transform.scale(
        GRASS_TILE,
        (TILE_SIZE, TILE_SIZE // 2)
    )

    cx = iso_x - camera.x + SCREEN_W // 2
    cy = iso_y - camera.y + 50

    screen.blit(
        tile,
        (cx - TILE_SIZE // 2, cy - TILE_SIZE // 4)
    )

# -------------------------
# DRAW MAP
# -------------------------

def draw_map_iso():
    """ Dessine la map entière en isométrique """
    for y in range(MAP_H):
        for x in range(MAP_W):
            iso_x, iso_y = grid_to_iso(x, y)
            draw_tile_iso(iso_x, iso_y)

def iso_to_grid(mx, my):
    """ Convertit position souris → coord grille isométrique """

    # Remet dans l'espace isométrique
    iso_x = mx + camera.x - SCREEN_W//2
    iso_y = my + camera.y - 50

    gx = (iso_y / (TILE_SIZE//4) + iso_x / (TILE_SIZE//2)) / 2
    gy = (iso_y / (TILE_SIZE//4) - iso_x / (TILE_SIZE//2)) / 2

    return int(gx), int(gy)

#parametre de la minimap
MINIMAP_SCALE = 1  # pour modifier la taille
MINIMAP_PADDING = 10  # marge depuis le bord
# minimap_fullscreen = False utile si on fait version minimap global

#fonction pour créer la minimap
def draw_minimap():
    # Taille en pixels de la minimap
    mini_w = int(MAP_W * MINIMAP_SCALE)
    mini_h = int(MAP_H * MINIMAP_SCALE)

    # Position dans le coin inférieur droit
    x0 = SCREEN_W - mini_w - MINIMAP_PADDING
    y0 = SCREEN_H - mini_h - MINIMAP_PADDING

    # Fond noir
    pygame.draw.rect(screen, (0, 0, 0), (x0 - 2, y0 - 2, mini_w + 4, mini_h + 4))

    # Génération pixel par pixel
    for gy in range(MAP_H):
        for gx in range(MAP_W):
            tile = grid[gy][gx]
            if tile == "W":
                col = (34, 139, 34)
            elif tile == "G":
                col = (218, 165, 32)
            elif tile == "F":
                col = (194, 178, 128)
            else:
                col = (50, 205, 50)
                        
            px = int(x0 + gx * MINIMAP_SCALE)
            py = int(y0 + gy * MINIMAP_SCALE)
            
            screen.set_at((px, py), col)

    # Rectangle représentant la caméra
    cam_x = int(camera.x / TILE_SIZE * MINIMAP_SCALE)
    cam_y = int(camera.y / TILE_SIZE * MINIMAP_SCALE)
    cam_w = int(SCREEN_W / TILE_SIZE * MINIMAP_SCALE)
    cam_h = int(SCREEN_H / TILE_SIZE * MINIMAP_SCALE)

    pygame.draw.rect(
        screen, (255, 0, 0),   # rouge
        (x0 + cam_x, y0 + cam_y, cam_w, cam_h),
        1
    )

    return (x0, y0, mini_w, mini_h)


#boucle principale 
while True:
    dt = clock.tick(60)

    # a chaque events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            gx, gy = iso_to_grid(mx, my)
            if 0 <= gx < MAP_W and 0 <= gy < MAP_H:
                print(f"Clicked tile ({gx},{gy}) = {grid[gy][gx]}")

            mini = draw_minimap()
            if mini:
                mx0, my0, mw, mh = mini
                if mx0 <= mx <= mx0 + mw and my0 <= my <= my0 + mh:
                    camera.x = int((mx - mx0) * TILE_SIZE - SCREEN_W / 2)
                    camera.y = int((my - my0) * TILE_SIZE - SCREEN_H / 2)

        # Mouse wheel zoom
        if event.type == pygame.MOUSEWHEEL:
            old = TILE_SIZE
            TILE_SIZE += event.y * ZOOM_STEP
            TILE_SIZE = max(MIN_TILE, min(MAX_TILE, TILE_SIZE))
            mx, my = pygame.mouse.get_pos()
            camera.x = int((camera.x + mx) * TILE_SIZE / old - mx)
            camera.y = int((camera.y + my) * TILE_SIZE / old - my)


    # touche pour controler la camera
    keys = pygame.key.get_pressed()

    if keys[pygame.K_z]:
        offset_y -= camera.speed
    if keys[pygame.K_s]:
        offset_y += camera.speed
    if keys[pygame.K_q]:
        offset_x -= camera.speed
    if keys[pygame.K_d]:
        offset_x += camera.speed

    #Zoom avec le clavier
    if keys[pygame.K_g]:
        old_tile_size = TILE_SIZE
        TILE_SIZE += ZOOM_STEP
        TILE_SIZE = min(TILE_SIZE, MAX_TILE)
        mx, my = SCREEN_W//2, SCREEN_H//2  # zoom centrée sur le centre de l'écran
        offset_x = int((offset_x + mx) * TILE_SIZE / old_tile_size - mx)
        offset_y = int((offset_y + my) * TILE_SIZE / old_tile_size - my)
    if keys[pygame.K_n]:
        old_tile_size = TILE_SIZE
        TILE_SIZE -= ZOOM_STEP
        TILE_SIZE = max(TILE_SIZE, MIN_TILE)
        mx, my = SCREEN_W//2, SCREEN_H//2
        offset_x = int((offset_x + mx) * TILE_SIZE / old_tile_size - mx)
        offset_y = int((offset_y + my) * TILE_SIZE / old_tile_size - my)



    #limite de la caméra
    camera.x = max(-MAP_W * TILE_SIZE, min(camera.x, MAP_W * TILE_SIZE))
    camera.y = max(-MAP_H * TILE_SIZE, min(camera.y, MAP_H * TILE_SIZE))

    # draw
    screen.fill((0,0,0))
    draw_map_iso()
    minimap_rect =draw_minimap()
    pygame.display.flip()