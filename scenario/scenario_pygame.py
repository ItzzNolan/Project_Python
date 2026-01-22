# scenario/scenario_pygame.py

import pygame
from backend.carte import Carte
from backend.Units import Unit  
from backend.jeu import Jeu
from ia.general import CaptainBraindead, MajorDAFT
from frontend.vue_pygame import VuePygame

def scenario_MajorDAFT_vs_CaptainBraindead_pygame():  

    # 1. Créer le jeu et la carte
    jeu = Jeu(10, 10)

    # 2. Créer les généraux
    general_joueur1 = MajorDAFT(0)
    general_joueur2 = CaptainBraindead(1)

    # 3. Ajouter les unités sur la carte
    # --- MajorDAFT (joueur 1) BLEU
    for x in range(3):
        for y in range(10):
            jeu.ajouter_unite("Pikeman",x,y,0)  

    # --- CaptainBraindead (joueur 2) ROUGE
    for x in range(7, 10):
        for y in range(10):
            jeu.ajouter_unite("Pikeman",x,y,1)

    # 4. Lancer le jeu avec l'interface Pygame
    vue = VuePygame(10, 10)
    clock = pygame.time.Clock()
    running = True
    while running and not jeu.est_termine():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        jeu.mettre_a_jour()
        vue.afficher(jeu)
        clock.tick(30)  # Limiter à 30 FPS
    pygame.quit()


if __name__ == "__main__":
    scenario_MajorDAFT_vs_CaptainBraindead_pygame()
    


