# Ce fichier teste le fonctionnement de la classe Carte.

from backend.carte import Carte

def test_creation_carte():
    carte_test = Carte(20, 10)
    assert carte_test.largeur == 20
    assert carte_test.hauteur == 10
    assert len(carte_test.grille) == 10
    assert len(carte_test.grille[0]) == 20

def test_est_dans_grille():
    carte_test = Carte(20, 10)
    assert carte_test.est_dans_grille(0, 0) is True
    assert carte_test.est_dans_grille(19, 9) is True
    assert carte_test.est_dans_grille(20, 9) is False
    assert carte_test.est_dans_grille(19, 10) is False

def test_get_unite_a():
    carte_test = Carte(5, 5)
    assert carte_test.get_unite_a(2, 2) is None
    
    # On simule la présence d'une unité pour le test
    carte_test.grille[2][2] = "Mon Chevalier"
    assert carte_test.get_unite_a(2, 2) == "Mon Chevalier"
    assert carte_test.get_unite_a(10, 10) is None