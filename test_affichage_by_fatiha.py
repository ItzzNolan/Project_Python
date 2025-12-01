# test_affichage.py
# On importe les briques nécessaires pour notre test
from backend.carte import Carte
from frontend.vue_terminal import afficher_jeu, FausseUnite

def lancer_test_affichage():
    """Crée un faux scénario et l'affiche."""
    
    carte_de_test = Carte(largeur=30, hauteur=15)

    # 2. On crée une fausse liste d'unités
    liste_unites_test = [
        # Équipe 1 (Bleu)
        FausseUnite(nom="Chevalier", pv=100, equipe=1, x=5, y=7),
        FausseUnite(nom="Piquier", pv=50, equipe=1, x=4, y=6),
        FausseUnite(nom="Piquier", pv=45, equipe=1, x=4, y=8),
        
        # Équipe 2 (Rouge)
        FausseUnite(nom="Chevalier", pv=90, equipe=2, x=24, y=7),
        FausseUnite(nom="Piquier", pv=50, equipe=2, x=25, y=6),
        FausseUnite(nom="Piquier", pv=50, equipe=2, x=25, y=8),
    ]

    # 3. On appelle ta fonction avec la vraie carte et la fausse liste d'unités
    afficher_jeu(carte_de_test, liste_unites_test)


# Cette ligne permet d'exécuter la fonction quand on lance "python test_affichage.py"
if __name__ == "__main__":
    lancer_test_affichage()