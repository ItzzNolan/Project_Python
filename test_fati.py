# test_fati.py

import pygame
import sys
import os
import random

from backend.jeu import Jeu
from frontend.iso import grid_to_iso
from assets.loader import load_sprite

# --- CONFIG ---
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 750
MAP_SIZE = 30

TILE_GRASS = 0
TILE_TREE = 1
TILE_GOLD = 2


def initialiser_partie():
    partie = Jeu()
    # Equipe bleue
    partie.ajouter_unite("Knight", 5, 6, equipe=0)
    partie.ajouter_unite("Knight", 6, 7, equipe=0)
    partie.ajouter_unite("Pikeman", 4, 8, equipe=0)
    partie.ajouter_unite("Pikeman", 5, 9, equipe=0)
    partie.ajouter_unite("Crossbowman", 3, 7, equipe=0)
    partie.ajouter_unite("Crossbowman", 4, 6, equipe=0)
    
    # Equipe rouge
    partie.ajouter_unite("Knight", 24, 22, equipe=1)
    partie.ajouter_unite("Knight", 25, 23, equipe=1)
    partie.ajouter_unite("Pikeman", 23, 24, equipe=1)
    partie.ajouter_unite("Pikeman", 24, 25, equipe=1)
    partie.ajouter_unite("Crossbowman", 26, 23, equipe=1)
    partie.ajouter_unite("Crossbowman", 25, 24, equipe=1)
    return partie


def main():
    pygame.init()
    
    fullscreen = False
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("MedievAIl BAIttle GenerAIl")
    clock = pygame.time.Clock()

    mon_jeu = initialiser_partie()
    mode_actuel = "PYGAME"
    paused = True
    game_tick = 0
    
    partie_terminee = False
    gagnant = None

    # --- SPRITES ---
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        grass_sprite = load_sprite(os.path.join(base_dir, "assets/tile_grass.png"), upscale_factor=1).convert_alpha()
        tree_sprite = load_sprite(os.path.join(base_dir, "assets/tile_tree.png"), upscale_factor=1).convert_alpha()
        gold_sprite = load_sprite(os.path.join(base_dir, "assets/tile_gold.png"), upscale_factor=1).convert_alpha()
        
        crossbow_sprite = load_sprite(os.path.join(base_dir, "assets/Crossbowman.png"), upscale_factor=1).convert_alpha()
        knight_sprite = load_sprite(os.path.join(base_dir, "assets/Knight.png"), upscale_factor=1).convert_alpha()
        pikeman_sprite = load_sprite(os.path.join(base_dir, "assets/Pikeman.png"), upscale_factor=1).convert_alpha()
        
        tree_sprite = pygame.transform.smoothscale(tree_sprite, 
            (int(tree_sprite.get_width() * 0.5), int(tree_sprite.get_height() * 0.5)))
        gold_sprite = pygame.transform.smoothscale(gold_sprite, 
            (int(gold_sprite.get_width() * 0.7), int(gold_sprite.get_height() * 0.7)))
        
        crossbow_sprite = pygame.transform.smoothscale(crossbow_sprite, 
            (int(crossbow_sprite.get_width() * 1.3), int(crossbow_sprite.get_height() * 1.3)))
        knight_sprite = pygame.transform.smoothscale(knight_sprite, 
            (int(knight_sprite.get_width() * 1.3), int(knight_sprite.get_height() * 1.3)))
        pikeman_sprite = pygame.transform.smoothscale(pikeman_sprite, 
            (int(pikeman_sprite.get_width() * 1.3), int(pikeman_sprite.get_height() * 1.3)))
        
        unit_sprites = {
            "Crossbowman": crossbow_sprite,
            "Knight": knight_sprite,
            "Pikeman": pikeman_sprite
        }
    except Exception as e:
        print(f"ERREUR: {e}")
        sys.exit()

    TILE_W = grass_sprite.get_width()
    TILE_H = grass_sprite.get_height()

    # --- CARTE ---
    world_map = [[TILE_GRASS for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]
    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            r = random.random()
            if r < 0.10:
                world_map[y][x] = TILE_TREE
            elif r < 0.13:
                world_map[y][x] = TILE_GOLD

    # --- PRE-RENDU CARTE ---
    surface_w = MAP_SIZE * TILE_W + TILE_W
    surface_h = MAP_SIZE * TILE_H + TILE_H
    
    map_surface = pygame.Surface((surface_w, surface_h), pygame.SRCALPHA).convert_alpha()
    
    origin_x = surface_w // 2
    origin_y = TILE_H // 2
    
    for gy in range(MAP_SIZE):
        for gx in range(MAP_SIZE):
            iso_x, iso_y = grid_to_iso(gx, gy, TILE_W, TILE_H)
            draw_x = origin_x + iso_x - TILE_W // 2
            draw_y = origin_y + iso_y
            
            map_surface.blit(grass_sprite, (draw_x, draw_y))
            
            tile = world_map[gy][gx]
            if tile == TILE_TREE:
                map_surface.blit(tree_sprite, (draw_x + TILE_W // 2 - tree_sprite.get_width() // 2,
                                               draw_y + TILE_H - tree_sprite.get_height()))
            elif tile == TILE_GOLD:
                map_surface.blit(gold_sprite, (draw_x + TILE_W // 2 - gold_sprite.get_width() // 2,
                                               draw_y + TILE_H - gold_sprite.get_height()))

    # --- MINIMAP ---
    MINIMAP_SIZE = 120
    minimap_scale = MINIMAP_SIZE / MAP_SIZE
    
    minimap_base = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))
    for y in range(MAP_SIZE):
        for x in range(MAP_SIZE):
            tile = world_map[y][x]
            if tile == TILE_TREE:
                color = (0, 80, 0)
            elif tile == TILE_GOLD:
                color = (255, 200, 0)
            else:
                color = (50, 120, 50)
            px = int(x * minimap_scale)
            py = int(y * minimap_scale)
            pygame.draw.rect(minimap_base, color, (px, py, max(1, int(minimap_scale)), max(1, int(minimap_scale))))

    # --- FONTS ---
    font_hud = pygame.font.SysFont("Segoe UI", 18, bold=True)
    font_title = pygame.font.SysFont("Segoe UI", 28, bold=True)
    font_subtitle = pygame.font.SysFont("Segoe UI", 18)
    font_mono = pygame.font.SysFont("Consolas", 15)
    font_grid = pygame.font.SysFont("Consolas", 12, bold=True)
    font_victory = pygame.font.SysFont("Segoe UI", 50, bold=True)

    # --- CAMERA ---
    cam_x = -surface_w // 2 + SCREEN_WIDTH // 2
    cam_y = -surface_h // 4
    speed = 20

    # ========== BOUCLE ==========
    running = True
    
    while running:
        current_w, current_h = screen.get_size()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F9:
                    mode_actuel = "TERMINAL" if mode_actuel == "PYGAME" else "PYGAME"
                elif event.key == pygame.K_p:
                    if not partie_terminee:
                        paused = not paused
                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                elif event.key == pygame.K_r:
                    mon_jeu = initialiser_partie()
                    partie_terminee = False
                    gagnant = None
                    paused = True

        # Camera avec limites
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: cam_x += speed
        if keys[pygame.K_RIGHT]: cam_x -= speed
        if keys[pygame.K_UP]: cam_y += speed
        if keys[pygame.K_DOWN]: cam_y -= speed
        
        cam_x_min = -surface_w + current_w
        cam_x_max = 0
        cam_y_min = -surface_h + current_h
        cam_y_max = 0
        
        cam_x = max(cam_x_min, min(cam_x_max, cam_x))
        cam_y = max(cam_y_min, min(cam_y_max, cam_y))

        # --- UPDATE ---
        if not paused and not partie_terminee:
            game_tick += 1
            if game_tick >= 10:
                game_tick = 0
                mon_jeu.mettre_a_jour()
                
                bleus = [u for u in mon_jeu.unites if u.alive and u.equipe == 0]
                rouges = [u for u in mon_jeu.unites if u.alive and u.equipe == 1]
                
                if len(bleus) == 0 and len(rouges) > 0:
                    partie_terminee = True
                    gagnant = "ROUGE"
                elif len(rouges) == 0 and len(bleus) > 0:
                    partie_terminee = True
                    gagnant = "BLEU"
                elif len(bleus) == 0 and len(rouges) == 0:
                    partie_terminee = True
                    gagnant = "EGALITE"

        # ========== RENDU ==========
        screen.fill((121, 127, 58))
        
        if mode_actuel == "PYGAME":
            # === VUE PYGAME ===
            screen.blit(map_surface, (cam_x, cam_y))

            for u in mon_jeu.unites:
                if not u.alive or not u.coords:
                    continue
                ux, uy = u.coords
                iso_x, iso_y = grid_to_iso(ux, uy, TILE_W, TILE_H)
                dx = cam_x + origin_x + iso_x
                dy = cam_y + origin_y + iso_y + TILE_H // 2

                color = (70, 130, 255) if u.equipe == 0 else (255, 70, 70)
                pygame.draw.ellipse(screen, color, (dx - 18, dy - 8, 36, 16), 2)

                sprite = unit_sprites.get(u.Unit, crossbow_sprite)
                sx = dx - sprite.get_width() // 2
                sy = dy - sprite.get_height() + 8
                screen.blit(sprite, (sx, sy))

                hp_ratio = max(0, min(1, u.HP / 35))
                pygame.draw.rect(screen, (40, 40, 40), (dx - 18, sy - 8, 36, 5))
                pygame.draw.rect(screen, (50, 220, 50) if hp_ratio > 0.3 else (255, 100, 50), 
                               (dx - 18, sy - 8, int(36 * hp_ratio), 5))

            # Minimap
            minimap = minimap_base.copy()
            for u in mon_jeu.unites:
                if u.alive and u.coords:
                    color = (70, 130, 255) if u.equipe == 0 else (255, 70, 70)
                    px = int(u.coords[0] * minimap_scale)
                    py = int(u.coords[1] * minimap_scale)
                    pygame.draw.rect(minimap, color, (px - 2, py - 2, 5, 5))
            
            mm_x = current_w - MINIMAP_SIZE - 15
            mm_y = current_h - MINIMAP_SIZE - 15
            pygame.draw.rect(screen, (80, 80, 80), (mm_x - 2, mm_y - 2, MINIMAP_SIZE + 4, MINIMAP_SIZE + 4), 2)
            screen.blit(minimap, (mm_x, mm_y))

        else:
            # === VUE TERMINAL ===
            screen.fill((10, 15, 20))
            
            title = font_title.render("ETAT DU CHAMP DE BATAILLE - Tour " + str(mon_jeu._tour), True, (80, 200, 140))
            screen.blit(title, (current_w // 2 - title.get_width() // 2, 70))
            
            cell = min(20, (current_w - 80) // MAP_SIZE, (current_h - 300) // MAP_SIZE)
            grid_w = MAP_SIZE * cell
            grid_h = MAP_SIZE * cell
            grid_x = (current_w - grid_w) // 2
            grid_y = 120
            
            pygame.draw.rect(screen, (20, 28, 35), (grid_x - 2, grid_y - 2, grid_w + 4, grid_h + 4))
            
            for gy in range(MAP_SIZE):
                for gx in range(MAP_SIZE):
                    pygame.draw.rect(screen, (28, 38, 32), (grid_x + gx * cell, grid_y + gy * cell, cell - 1, cell - 1))
            
            for u in mon_jeu.unites:
                if not u.alive or not u.coords:
                    continue
                rx = grid_x + int(u.coords[0]) * cell
                ry = grid_y + int(u.coords[1]) * cell
                
                bg = (40, 70, 120) if u.equipe == 0 else (120, 40, 40)
                fg = (180, 220, 255) if u.equipe == 0 else (255, 180, 180)
                
                pygame.draw.rect(screen, bg, (rx, ry, cell - 1, cell - 1))
                letter = font_grid.render(u.Unit[0], True, fg)
                screen.blit(letter, (rx + cell // 2 - letter.get_width() // 2, 
                                     ry + cell // 2 - letter.get_height() // 2))
            
            info_y = grid_y + grid_h + 15
            bleus = [u for u in mon_jeu.unites if u.alive and u.equipe == 0]
            rouges = [u for u in mon_jeu.unites if u.alive and u.equipe == 1]
            
            screen.blit(font_subtitle.render(f"BLEU: {len(bleus)}", True, (100, 180, 255)), (current_w // 2 - 120, info_y))
            screen.blit(font_subtitle.render(f"ROUGE: {len(rouges)}", True, (255, 130, 130)), (current_w // 2 + 40, info_y))
            
            info_y += 30
            for u in mon_jeu.unites:
                if not u.alive:
                    continue
                color = (100, 180, 255) if u.equipe == 0 else (255, 130, 130)
                txt = f"[{'B' if u.equipe == 0 else 'R'}] {u.Unit} HP:{u.HP:.0f} ({u.coords[0]:.1f},{u.coords[1]:.1f})"
                screen.blit(font_mono.render(txt, True, color), (current_w // 2 - 150, info_y))
                info_y += 20

        # === VICTOIRE ===
        if partie_terminee:
            overlay = pygame.Surface((current_w, current_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            if gagnant == "BLEU":
                color, text = (70, 130, 255), "VICTOIRE BLEUE"
            elif gagnant == "ROUGE":
                color, text = (255, 70, 70), "VICTOIRE ROUGE"
            else:
                color, text = (200, 200, 200), "EGALITE"
            
            box_w, box_h = 400, 150
            box_x, box_y = (current_w - box_w) // 2, (current_h - box_h) // 2
            pygame.draw.rect(screen, (20, 20, 30), (box_x, box_y, box_w, box_h))
            pygame.draw.rect(screen, color, (box_x, box_y, box_w, box_h), 3)
            
            txt = font_victory.render(text, True, color)
            screen.blit(txt, (current_w // 2 - txt.get_width() // 2, box_y + 35))
            txt2 = font_subtitle.render("R = Restart   ESC = Quit", True, (150, 150, 150))
            screen.blit(txt2, (current_w // 2 - txt2.get_width() // 2, box_y + 100))

        # === HUD ===
        pygame.draw.rect(screen, (15, 20, 28), (0, 0, current_w, 50))
        pygame.draw.line(screen, (50, 55, 65), (0, 49), (current_w, 49), 2)
        
        status = "TERMINE" if partie_terminee else ("PAUSE" if paused else "EN JEU")
        status_color = (255, 215, 0) if partie_terminee else ((255, 200, 100) if paused else (100, 255, 150))
        
        screen.blit(font_hud.render(f"|| {status}", True, status_color), (20, 14))
        screen.blit(font_hud.render(f"| Vue: {mode_actuel}  |  Unites: {len([u for u in mon_jeu.unites if u.alive])}  |  F9/F11/P/R", 
                                    True, (150, 150, 150)), (150, 14))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()