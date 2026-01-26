#Ce code sert à créer la map 2.5D. Pour cela on créer une classe 


import pygame
import sys
from game_state import GameState

class PygameView:
    def __init__(self, game_state):
        self.gs = game_state
        self.running = True

        pygame.init()

        # parametre

        #taille des tuiles
        self.TILE_SIZE = 32
        self.MIN_TILE = 8
        self.MAX_TILE = 64

        #taille de la map
        self.MAP_W = len(game_state.grid[0])
        self.MAP_H = len(game_state.grid)

        #taille de la fenetre
        self.SCREEN_W = 1000
        self.SCREEN_H = 700
        

        self.screen = pygame.display.set_mode(      #créer la fenêtre
            (self.SCREEN_W, self.SCREEN_H)
        )
        pygame.display.set_caption("2.5D View")   #titre

        self.clock = pygame.time.Clock()

        #sprite d'une tuile
        self.GRASS_TILE = pygame.image.load(
            "assets/grass.png"                  #image a changer
        ).convert_alpha()

        class Camera:
            def __init__(self):
                self.x = 0
                self.y = 0
                self.speed = 15

        self.camera = Camera()

        #paramètre MINIMAP
        self.MINIMAP_SCALE = 2
        self.MINIMAP_PADDING = 10
        self.minimap_rect = None   

   
    #coordonnées grilles en iso
    def grid_to_iso(self, x, y):
        iso_x = (x - y) * (self.TILE_SIZE // 2)
        iso_y = (x + y) * (self.TILE_SIZE // 4)
        return iso_x, iso_y

    #déssine 1 tuile
    def draw_tile_iso(self, iso_x, iso_y):
        tile = pygame.transform.scale(
            self.GRASS_TILE,
            (self.TILE_SIZE, self.TILE_SIZE // 2)
        )

        cx = iso_x - self.camera.x + self.SCREEN_W // 2
        cy = iso_y - self.camera.y + 50

        self.screen.blit(
            tile,
            (cx - self.TILE_SIZE // 2, cy - self.TILE_SIZE // 4)
        )

    #dessine toute la map
    def draw_map_iso(self):
        for y in range(self.MAP_H):
            for x in range(self.MAP_W):
                iso_x, iso_y = self.grid_to_iso(x, y)
                self.draw_tile_iso(iso_x, iso_y)

    #trace la minimap
    def draw_minimap(self):
        
        mini_w = int(self.MAP_W * self.MINIMAP_SCALE)
        mini_h = int(self.MAP_H * self.MINIMAP_SCALE)

        # position : en bas à droite
        x0 = self.SCREEN_W - mini_w - self.MINIMAP_PADDING
        y0 = self.SCREEN_H - mini_h - self.MINIMAP_PADDING

        # Cadre
        pygame.draw.rect(
            self.screen, (0, 0, 0),
            (x0 - 2, y0 - 2, mini_w + 4, mini_h + 4)
        )
        GREEN = (34, 139, 34)

        # Map (verte)
        for y in range(self.MAP_H):
            for x in range(self.MAP_W):
                px = x0 + x * self.MINIMAP_SCALE
                py = y0 + y * self.MINIMAP_SCALE
                self.screen.set_at((int(px), int(py)),GREEN)

        # Caméra (rouge)
        cam_x = int(self.camera.x / self.TILE_SIZE * self.MINIMAP_SCALE)
        cam_y = int(self.camera.y / self.TILE_SIZE * self.MINIMAP_SCALE)
        cam_w = int(self.SCREEN_W / self.TILE_SIZE * self.MINIMAP_SCALE)
        cam_h = int(self.SCREEN_H / self.TILE_SIZE * self.MINIMAP_SCALE)

        pygame.draw.rect(
            self.screen, (255, 0, 0),
            (x0 + cam_x, y0 + cam_y, cam_w, cam_h),
            1
        )

        self.minimap_rect = (x0, y0, mini_w, mini_h)


        #self.minimap_rect = (,,px,py)
    
    # boucle PYGAME
    
    def run(self):
        while self.running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.gs.paused = not self.gs.paused

                    if event.key == pygame.K_F9:
                        return "SWITCH"
                    
                 # clic minimap
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.minimap_rect:
                        mx, my = pygame.mouse.get_pos()
                        x0, y0, w, h = self.minimap_rect
                        if x0 <= mx <= x0 + w and y0 <= my <= y0 + h:
                            self.camera.x = int(
                                (mx - x0) * self.TILE_SIZE - self.SCREEN_W / 2
                            )
                            self.camera.y = int(
                                (my - y0) * self.TILE_SIZE - self.SCREEN_H / 2
                            )

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                self.camera.y -= self.camera.speed
            if keys[pygame.K_s]:
                self.camera.y += self.camera.speed
            if keys[pygame.K_q]:
                self.camera.x -= self.camera.speed
            if keys[pygame.K_d]:
                self.camera.x += self.camera.speed

            self.screen.fill((0, 0, 0))
            self.draw_map_iso()
            self.draw_minimap()
            pygame.display.flip()