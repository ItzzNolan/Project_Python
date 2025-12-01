# test_simple.py

from backend.jeu import Jeu
import time

def test_partie_simple():
    """
    Test simple avec quelques unités pour vérifier le combat.
    """
    partie = Jeu()
    print("Instance de Jeu créée.")
    
    # Ajoute quelques unités des deux camps
    partie.ajouter_unite("Knight", 5, 5, equipe=0)
    partie.ajouter_unite("Knight", 6, 5, equipe=0)
    
    partie.ajouter_unite("Pikeman", 20, 10, equipe=1)
    partie.ajouter_unite("Crossbowman", 22, 12, equipe=1)
    
    return partie


if __name__ == "__main__":
    mon_jeu = test_partie_simple()
    
    tour = 0
    while not mon_jeu.est_termine():
        tour += 1
        mon_jeu.mettre_a_jour()
        
        # Limite optionnelle pour éviter les boucles infinies
        if tour > 100:
            print("Limite de tours atteinte !")
            break
    
    print("\n=== Test terminé ===")