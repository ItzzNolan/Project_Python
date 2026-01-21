# frontend/vue_pygame.py

import pygame
from frontend.iso import grid_to_iso
from assets.loader import load_sprite

class VuePygame:
    def __init__(self, largeur_carte, hauteur_carte):
        pygame.init()
        
        # Dimensions écran
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("MedievAIl BAIttle GenerAIl")
        
        # Dimensions des tiles isométriques
        self.TILE_WIDTH = 64
        self.TILE_HEIGHT = 32
        
        # Caméra / scroll
        self.camera_x = self.SCREEN_WIDTH // 2
        self.camera_y = 100
        
        # Couleur de fond style AoE2 (vert foncé)
        self.BG_COLOR = (20, 50, 20)
        
        # Chargement des sprites
        self.sprites = {}
        self._charger_sprites()
        
        # Dimensions carte
        self.largeur_carte = largeur_carte
        self.hauteur_carte = hauteur_carte
        
        # État du jeu
        self.paused = False
        self.fullscreen = False
        
        # Police pour l'UI
        self.font = pygame.font.Font(None, 28)

    def _charger_sprites(self):
        """Charge tous les sprites nécessaires."""
        # Tiles
        self.sprites['grass'] = load_sprite('assets/tile_grass.png', upscale_factor=2)
        self.sprites['gold'] = load_sprite('assets/tile_gold.png', upscale_factor=2)
        self.sprites['tree'] = load_sprite('assets/tile_tree.png', upscale_factor=2)
        
        # Unités
        self.sprites['pikeman'] = load_sprite('assets/pikeman.png', upscale_factor=2)
        
        # Sprite de fallback si une image manque
        self.fallback_sprite = self._creer_fallback_sprite()

    def _creer_fallback_sprite(self):
        """Crée un sprite de remplacement (carré rouge) si une image manque."""
        surf = pygame.Surface((self.TILE_WIDTH, self.TILE_HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(surf, (255, 0, 0), [
            (self.TILE_WIDTH // 2, 0),
            (self.TILE_WIDTH, self.TILE_HEIGHT // 2),
            (self.TILE_WIDTH // 2, self.TILE_HEIGHT),
            (0, self.TILE_HEIGHT // 2)
        ])
        return surf

    def _dessiner_fond_etendu(self):
        """
        Dessine des tiles au-delà de la map pour éliminer les zones noires.
        Style AoE2 : on remplit tout l'écran avec des tiles "vides" (herbe sombre ou eau).
        """
        # D'abord, remplir le fond avec une couleur unie
        self.screen.fill(self.BG_COLOR)
        

        marge = 5  # tiles supplémentaires de chaque côté
        
        for grid_y in range(-marge, self.hauteur_carte + marge):
            for grid_x in range(-marge, self.largeur_carte + marge):
                # Sauter les tiles qui sont dans la map (on les dessine après)
                if 0 <= grid_x < self.largeur_carte and 0 <= grid_y < self.hauteur_carte:
                    continue
                
                iso_x, iso_y = grid_to_iso(grid_x, grid_y, self.TILE_WIDTH, self.TILE_HEIGHT)
                screen_x = iso_x + self.camera_x
                screen_y = iso_y + self.camera_y
                
                # Dessiner une tile sombre (bordure de map)
                self._dessiner_tile_bordure(screen_x, screen_y)

    def _dessiner_tile_bordure(self, x, y):
        """Dessine une tile de bordure (herbe sombre ou eau)."""
        # Forme losange sombre
        points = [
            (x + self.TILE_WIDTH // 2, y),
            (x + self.TILE_WIDTH, y + self.TILE_HEIGHT // 2),
            (x + self.TILE_WIDTH // 2, y + self.TILE_HEIGHT),
            (x, y + self.TILE_HEIGHT // 2)
        ]
        pygame.draw.polygon(self.screen, (15, 35, 15), points)  # Vert très foncé
        pygame.draw.polygon(self.screen, (10, 25, 10), points, 1)  # Contour

    def _dessiner_tilemap(self, carte):
        """Dessine toutes les tiles de la carte."""
        grass_sprite = self.sprites.get('grass', self.fallback_sprite)
        
        for grid_y in range(carte.hauteur):
            for grid_x in range(carte.largeur):
                iso_x, iso_y = grid_to_iso(grid_x, grid_y, self.TILE_WIDTH, self.TILE_HEIGHT)
                screen_x = iso_x + self.camera_x
                screen_y = iso_y + self.camera_y
                
                # Dessiner le tile d'herbe
                if grass_sprite:
                    # Centrer le sprite sur la position isométrique
                    blit_x = screen_x - grass_sprite.get_width() // 2 + self.TILE_WIDTH // 2
                    blit_y = screen_y
                    self.screen.blit(grass_sprite, (blit_x, blit_y))

    def _dessiner_unites(self, jeu):
        """Dessine toutes les unités vivantes."""
        for unite in jeu.unites:
            if not unite.alive or unite.coords is None:
                continue
            
            grid_x, grid_y = unite.coords
            iso_x, iso_y = grid_to_iso(grid_x, grid_y, self.TILE_WIDTH, self.TILE_HEIGHT)
            screen_x = iso_x + self.camera_x
            screen_y = iso_y + self.camera_y
            
            # Récupérer le sprite approprié
            sprite_key = unite.Unit.lower() if hasattr(unite, 'Unit') else 'pikeman'
            sprite = self.sprites.get(sprite_key, self.sprites.get('pikeman', self.fallback_sprite))
            
            if sprite:
                # Centrer le sprite sur la tile
                blit_x = screen_x + self.TILE_WIDTH // 2 - sprite.get_width() // 2
                blit_y = screen_y - sprite.get_height() + self.TILE_HEIGHT
                self.screen.blit(sprite, (blit_x, blit_y))
            
            # Dessiner la barre de vie
            self._dessiner_barre_vie(unite, screen_x, screen_y)
            
            # Dessiner le cercle de sélection sous l'unité
            self._dessiner_cercle_equipe(unite, screen_x, screen_y)

    def _dessiner_barre_vie(self, unite, x, y):
        """Dessine la barre de vie au-dessus de l'unité."""
        max_hp = unite.HPmax if hasattr(unite, 'HPmax') else 100
        current_hp = max(0, unite.HP)
        ratio = current_hp / max_hp
        
        bar_width = 40
        bar_height = 5
        bar_x = x + self.TILE_WIDTH // 2 - bar_width // 2
        bar_y = y - 20
        
        # Fond (rouge)
        pygame.draw.rect(self.screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        # Vie (vert)
        pygame.draw.rect(self.screen, (0, 200, 0), (bar_x, bar_y, int(bar_width * ratio), bar_height))
        # Contour
        pygame.draw.rect(self.screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    def _dessiner_cercle_equipe(self, unite, x, y):
        """Dessine un cercle sous l'unité pour indiquer son équipe."""
        couleur = (100, 150, 255) if unite.equipe == 0 else (255, 100, 100)
        center_x = x + self.TILE_WIDTH // 2
        center_y = y + self.TILE_HEIGHT // 2
        pygame.draw.ellipse(self.screen, couleur, (center_x - 15, center_y - 5, 30, 10), 2)

    def _dessiner_ui(self, jeu):
        """Dessine l'interface utilisateur."""
        # Barre du haut
        status = "|| PAUSE" if self.paused else "▶ EN JEU"
        nb_unites = len([u for u in jeu.unites if u.alive])
        
        ui_text = f"{status}  | Vue: Pygame | Unités: {nb_unites} | F9: Vue | F11: Plein écran | P: Pause"
        text_surface = self.font.render(ui_text, True, (255, 255, 255))
        
        # Fond semi-transparent pour le texte
        pygame.draw.rect(self.screen, (0, 0, 0, 180), (0, 0, self.SCREEN_WIDTH, 35))
        self.screen.blit(text_surface, (10, 8))

    def _dessiner_minimap(self, jeu):
        """Dessine une minimap dans le coin inférieur droit."""
        minimap_w, minimap_h = 150, 100
        minimap_x = self.SCREEN_WIDTH - minimap_w - 10
        minimap_y = self.SCREEN_HEIGHT - minimap_h - 10
        
        # Fond de la minimap
        pygame.draw.rect(self.screen, (20, 40, 20), (minimap_x, minimap_y, minimap_w, minimap_h))
        pygame.draw.rect(self.screen, (100, 100, 100), (minimap_x, minimap_y, minimap_w, minimap_h), 2)
        
        # Dessiner les unités sur la minimap
        scale_x = minimap_w / self.largeur_carte
        scale_y = minimap_h / self.hauteur_carte
        
        for unite in jeu.unites:
            if not unite.alive or unite.coords is None:
                continue
            
            gx, gy = unite.coords
            px = minimap_x + int(gx * scale_x)
            py = minimap_y + int(gy * scale_y)
            couleur = (100, 150, 255) if unite.equipe == 0 else (255, 100, 100)
            pygame.draw.circle(self.screen, couleur, (px, py), 3)

    def afficher(self, jeu):
        """Méthode principale d'affichage."""
        # 1. Fond étendu (élimine les zones noires)
        self._dessiner_fond_etendu()
        
        # 2. Tilemap principale
        self._dessiner_tilemap(jeu.carte)
        
        # 3. Unités
        self._dessiner_unites(jeu)
        
        # 4. Interface utilisateur
        self._dessiner_ui(jeu)
        
        # 5. Minimap
        self._dessiner_minimap(jeu)
        
        # 6. Mise à jour de l'écran
        pygame.display.flip()

    def gerer_camera(self, keys):
        
        vitesse = 10
        if keys[pygame.K_LEFT]:
            self.camera_x += vitesse
        if keys[pygame.K_RIGHT]:
            self.camera_x -= vitesse
        if keys[pygame.K_UP]:
            self.camera_y += vitesse
        if keys[pygame.K_DOWN]:
            self.camera_y -= vitesse
