import pygame


class VueTerminal:
    
    def __init__(self):
        self.font_title = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.font_subtitle = pygame.font.SysFont("Segoe UI", 18)
        self.font_mono = pygame.font.SysFont("Consolas", 15)
        self.font_grid = pygame.font.SysFont("Consolas", 12, bold=True)
        self.font_hud = pygame.font.SysFont("Segoe UI", 18, bold=True)
        self.scroll_x = 0
        self.scroll_y = 0
    
    def afficher(self, screen, jeu):
        current_w, current_h = screen.get_size()
        MAP_SIZE = jeu.carte.largeur
        screen.fill((10, 15, 20))

        title = self.font_title.render(f"ETAT DU CHAMP DE BATAILLE - Tour {jeu._tour}", True, (80, 200, 140))
        screen.blit(title, (current_w // 2 - title.get_width() // 2, 70))
        scroll_info = self.font_mono.render(f"Scroll: ({self.scroll_x}, {self.scroll_y}) | ZQSD+Shift", True, (100, 100, 100))
        screen.blit(scroll_info, (current_w // 2 - scroll_info.get_width() // 2, 100))
        cell = min(20, (current_w - 80) // 25, (current_h - 300) // 20)
        visible_cols = min(MAP_SIZE - self.scroll_x, (current_w - 80) // cell)
        visible_rows = min(MAP_SIZE - self.scroll_y, (current_h - 300) // cell)
        
        grid_w = visible_cols * cell
        grid_h = visible_rows * cell
        grid_x = (current_w - grid_w) // 2
        grid_y = 125
        pygame.draw.rect(screen, (20, 28, 35), (grid_x - 2, grid_y - 2, grid_w + 4, grid_h + 4))
        for row in range(visible_rows):
            for col in range(visible_cols):
                gx = col + self.scroll_x
                gy = row + self.scroll_y
                if 0 <= gx < MAP_SIZE and 0 <= gy < MAP_SIZE:
                    pygame.draw.rect(screen, (28, 38, 32), (grid_x + col * cell, grid_y + row * cell, cell - 1, cell - 1))
        for u in jeu.unites:
            if not u.alive or not u.coords:
                continue
            
            col = int(u.coords[0]) - self.scroll_x
            row = int(u.coords[1]) - self.scroll_y
            
            if 0 <= col < visible_cols and 0 <= row < visible_rows:
                rx = grid_x + col * cell
                ry = grid_y + row * cell
                
                bg = (40, 70, 120) if u.equipe == 0 else (120, 40, 40)
                fg = (180, 220, 255) if u.equipe == 0 else (255, 180, 180)
                
                pygame.draw.rect(screen, bg, (rx, ry, cell - 1, cell - 1))
                letter = self.font_grid.render(u.Unit[0], True, fg)
                screen.blit(letter, (rx + cell // 2 - letter.get_width() // 2, 
                                     ry + cell // 2 - letter.get_height() // 2))
        info_y = grid_y + grid_h + 15
        bleus = [u for u in jeu.unites if u.alive and u.equipe == 0]
        rouges = [u for u in jeu.unites if u.alive and u.equipe == 1]
        
        screen.blit(self.font_subtitle.render(f"BLEU: {len(bleus)}", True, (100, 180, 255)), (current_w // 2 - 120, info_y))
        screen.blit(self.font_subtitle.render(f"ROUGE: {len(rouges)}", True, (255, 130, 130)), (current_w // 2 + 40, info_y))
        
        info_y += 30
        for u in jeu.unites:
            if not u.alive:
                continue
            color = (100, 180, 255) if u.equipe == 0 else (255, 130, 130)
            txt = f"[{'B' if u.equipe == 0 else 'R'}] {u.Unit} HP:{u.HP:.0f} ({u.coords[0]:.1f},{u.coords[1]:.1f})"
            screen.blit(self.font_mono.render(txt, True, color), (current_w // 2 - 150, info_y))
            info_y += 20
        pygame.draw.rect(screen, (15, 20, 28), (0, 0, current_w, 50))
        pygame.draw.line(screen, (50, 55, 65), (0, 49), (current_w, 49), 2)
        
        screen.blit(self.font_hud.render("|| Vue: Terminal", True, (150, 200, 150)), (20, 14))
        screen.blit(self.font_hud.render(f"|  Tour: {jeu._tour}  |  Unites: {len([u for u in jeu.unites if u.alive])}", 
                                         True, (150, 150, 150)), (180, 14))
        
        shortcuts = self.font_mono.render("F9:Vue | F10:Fullscreen | F11:Save | F12:Load | TAB:Stats", True, (100, 100, 100))
        screen.blit(shortcuts, (current_w - shortcuts.get_width() - 15, 16))

def afficher(jeu):
    print("\n" + "="*50)
    print(f"  Tour: {jeu._tour}")
    print("="*50)
    
    bleus = [u for u in jeu.unites if u.alive and u.equipe == 0]
    rouges = [u for u in jeu.unites if u.alive and u.equipe == 1]
    
    print(f"  Bleus: {len(bleus)}  |  Rouges: {len(rouges)}")
    print("-"*50)
    
    for u in jeu.unites:
        if not u.alive:
            continue
        equipe = "BLEU" if u.equipe == 0 else "ROUGE"
        print(f"  [{equipe}] {u.Unit} HP:{u.HP:.0f} @ ({u.coords[0]:.1f}, {u.coords[1]:.1f})")
    
    print("="*50 + "\n")
