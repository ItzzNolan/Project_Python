# frontend/manager_vue.py

import pygame
from frontend.vue_pygame import VuePygame
from frontend.vue_terminal import afficher as afficher_terminal

class ManagerVue:
    def __init__(self, jeu):
        self.jeu = jeu
        
        # On initialise les deux vues
        self.vue_pygame = VuePygame(jeu.carte.largeur, jeu.carte.hauteur)
        
        # Le mode initial est Pygame
        self.mode_actuel = "PYGAME"

    def changer_mode(self):
        """Bascule entre le mode PYGAME et le mode TERMINAL."""
        if self.mode_actuel == "PYGAME":
            self.mode_actuel = "TERMINAL"
            print("\n" * 50)  # Effacer l'écran du terminal
            print("--- Passage en Vue Terminal ---")
        else:
            self.mode_actuel = "PYGAME"
            print("--- Passage en Vue Pygame ---")

    def afficher(self):
        """Appelle la fonction d'affichage du mode actuel."""
        if self.mode_actuel == "PYGAME":
            self.vue_pygame.afficher(self.jeu)
        else:  # Mode TERMINAL
            # On affiche un écran noir dans Pygame pour garder le focus clavier
            self.vue_pygame.screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 36)
            text = font.render("Mode Terminal (F9 pour revenir)", True, (255, 255, 255))
            self.vue_pygame.screen.blit(text, (50, 50))
            # Et on affiche dans le terminal
            afficher_terminal(self.jeu)
