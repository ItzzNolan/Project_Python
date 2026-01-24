# frontend/vue_terminal.py

import pygame


class VueTerminal:
    """Vue terminal affichee dans la fenetre Pygame."""
    
    def __init__(self):
        self.font_title = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.font_subtitle = pygame.font.SysFont("Segoe UI", 18)
        self.font_mono = pygame.font.SysFont("Consolas", 15)
        self.font_grid = pygame.font.SysFont("Consolas", 12, bold=True)
        self.font_hud = pygame.font.SysFont("Segoe UI", 18, bold=True)
        
        self.scroll_x = 0
        self.scroll_y = 0
    
    def afficher(self, screen, jeu, partie_terminee=False, gagnant=None):
        """Affiche la vue terminal sur l'ecran pygame."""
        current_w, current_h = screen.get_size()
        MAP_SIZE = jeu.carte.largeur
        
        screen.fill((10, 15, 20))
        
        pygame.draw.rect(screen, (15, 20, 28), (0, 0, current_w, 50))
        pygame.draw.line(screen, (50, 55, 65), (0, 49), (current_w, 49), 2)
        
        screen.blit(self.font_hud.render("|| Vue: Terminal", True, (150, 200, 150)), (20, 14))
        screen.blit(self.font_hud.render(f"|  Tour: {jeu._tour}  |  Unites: {len([u for u in jeu.unites if u.alive])}", 
                                         True, (150, 150, 150)), (180, 14))
        
        shortcuts = self.font_mono.render("F9:Vue | F10:Fullscreen | F11:Save | F12:Load", True, (100, 100, 100))
        screen.blit(shortcuts, (current_w - shortcuts.get_width() - 15, 16))
        
        bleus = [u for u in jeu.unites if u.alive and u.equipe == 0]
        rouges = [u for u in jeu.unites if u.alive and u.equipe == 1]
        nom_bleu = jeu.generaux[0].name if hasattr(jeu, 'generaux') and 0 in jeu.generaux else "JOUEUR 1"
        nom_rouge = jeu.generaux[1].name if hasattr(jeu, 'generaux') and 1 in jeu.generaux else "JOUEUR 2"
        
        box_w = 180
        box_h = 60
        margin = 15
        top_y = 60
        
        pygame.draw.rect(screen, (20, 30, 50), (margin, top_y, box_w, box_h))
        pygame.draw.rect(screen, (70, 130, 255), (margin, top_y, box_w, box_h), 2)
        pygame.draw.rect(screen, (70, 130, 255), (margin, top_y, box_w, 18))
        screen.blit(self.font_grid.render("EQUIPE 1 - BLEU", True, (255, 255, 255)), (margin + 8, top_y + 2))
        screen.blit(self.font_mono.render(nom_bleu, True, (100, 180, 255)), (margin + 8, top_y + 22))
        screen.blit(self.font_mono.render(f"Unites: {len(bleus)}", True, (150, 150, 150)), (margin + 8, top_y + 40))
        
        box_x_rouge = current_w - box_w - margin
        pygame.draw.rect(screen, (50, 20, 20), (box_x_rouge, top_y, box_w, box_h))
        pygame.draw.rect(screen, (255, 70, 70), (box_x_rouge, top_y, box_w, box_h), 2)
        pygame.draw.rect(screen, (255, 70, 70), (box_x_rouge, top_y, box_w, 18))
        screen.blit(self.font_grid.render("EQUIPE 2 - ROUGE", True, (255, 255, 255)), (box_x_rouge + 8, top_y + 2))
        screen.blit(self.font_mono.render(nom_rouge, True, (255, 150, 150)), (box_x_rouge + 8, top_y + 22))
        screen.blit(self.font_mono.render(f"Unites: {len(rouges)}", True, (150, 150, 150)), (box_x_rouge + 8, top_y + 40))
        
        cell = min(20, (current_w - 80) // 25, (current_h - 250) // 20)
        visible_cols = min(MAP_SIZE - self.scroll_x, (current_w - 80) // cell)
        visible_rows = min(MAP_SIZE - self.scroll_y, (current_h - 250) // cell)
        
        grid_w = visible_cols * cell
        grid_h = visible_rows * cell
        grid_x = (current_w - grid_w) // 2
        grid_y = 135
        
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
        
        if partie_terminee:
            self._dessiner_victoire(screen, jeu, current_w, current_h, gagnant)

    def _dessiner_victoire(self, screen, jeu, current_w, current_h, gagnant):
        """Dessine l'ecran de victoire."""
        overlay = pygame.Surface((current_w, current_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        if gagnant == "BLEU":
            nom = jeu.generaux[0].name if hasattr(jeu, 'generaux') and 0 in jeu.generaux else "BLEU"
            color = (70, 130, 255)
            text = f"VICTOIRE {nom}!"
        elif gagnant == "ROUGE":
            nom = jeu.generaux[1].name if hasattr(jeu, 'generaux') and 1 in jeu.generaux else "ROUGE"
            color = (255, 70, 70)
            text = f"VICTOIRE {nom}!"
        else:
            color = (200, 200, 200)
            text = "EGALITE!"
        
        font_victory = pygame.font.SysFont("Segoe UI", 40, bold=True)
        font_sub = pygame.font.SysFont("Segoe UI", 18)
        
        box_w, box_h = 500, 150
        box_x = (current_w - box_w) // 2
        box_y = (current_h - box_h) // 2
        
        pygame.draw.rect(screen, (20, 20, 30), (box_x, box_y, box_w, box_h))
        pygame.draw.rect(screen, color, (box_x, box_y, box_w, box_h), 3)
        
        txt = font_victory.render(text, True, color)
        screen.blit(txt, (current_w // 2 - txt.get_width() // 2, box_y + 35))
        
        txt2 = font_sub.render("R = Recommencer   ESC = Quitter", True, (150, 150, 150))
        screen.blit(txt2, (current_w // 2 - txt2.get_width() // 2, box_y + 100))


def afficher(jeu):
    """Affiche l'etat du jeu dans le terminal (console)."""
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
