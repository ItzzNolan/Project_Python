# Ce fichier teste le fonctionnement de la classe Carte.

from backend.carte import Carte


# --- FAUSSE CLASSE UNITE POUR NOS TESTS ---
class FakeUnite:
    def __init__(self, nom="TestUnit"):
        self.nom = nom
    # On ajoute cette méthode pour que pytest affiche des noms plus clairs en cas d'erreur
    def __repr__(self):
        return f"<FakeUnite {self.nom}>"

def test_creation_carte():
    carte_test = Carte(20, 10)
    assert carte_test.largeur == 20
    assert carte_test.hauteur == 10
    assert len(carte_test.grille) == 10
    assert len(carte_test.grille[0]) == 20

def test_est_dans_grille():
    carte_test = Carte(20, 10)
    assert carte_test.est_dans_grille(0, 0) is True     #coin en haut à gauche
    assert carte_test.est_dans_grille(19, 9) is True    #coin en bas à droite
    assert carte_test.est_dans_grille(20, 9) is False   #hors limites en largeur (trop à droite)
    assert carte_test.est_dans_grille(19, 10) is False  #hors limites en hauteur (trop en bas)

def test_get_unite_a():
    carte_test = Carte(5, 5)
    assert carte_test.get_unite_a(2, 2) is None  #case vide car au début tout est est Vide --None--
    
    # On simule la présence d'une unité pour le test
    carte_test.grille[2][2] = "Mon Chevalier"
    assert carte_test.get_unite_a(2, 2) == "Mon Chevalier"
    assert carte_test.get_unite_a(10, 10) is None

def test_placer_unite_succes_et_echecs():
    """Teste les différents scénarios de placement d'unité."""
    # ARRANGE
    carte = Carte(5, 5)
    unite1 = FakeUnite(nom="Aragorn")
    unite2 = FakeUnite(nom="Legolas")
    
    # ACT (Success) & ASSERT
    succes_placement_1 = carte.placer_unite(unite1, 1, 1)
    assert succes_placement_1 is True
    assert carte.get_unite_a(1, 1) == unite1
    
    # ACT (Failure - Occupied) & ASSERT
    succes_placement_2 = carte.placer_unite(unite2, 1, 1)
    assert succes_placement_2 is False
    assert carte.get_unite_a(1, 1) == unite1 # C'est toujours unite1 qui est sur la case
    
    # ACT (Failure - Out of bounds) & ASSERT
    succes_placement_3 = carte.placer_unite(unite2, -1, 5)
    assert succes_placement_3 is False

def test_retirer_unite_succes_et_echec():
    """Teste les scénarios de retrait d'unité."""

    carte = Carte(5, 5)
    unite_a_retirer = FakeUnite(nom="Gimli")
    unite_inexistante = FakeUnite(nom="Sauron")
    carte.placer_unite(unite_a_retirer, 3, 3)
    
    # ACT (Failure - Not on map) & ASSERT
    echec_retrait = carte.retirer_unite(unite_inexistante)
    assert echec_retrait is False
    assert carte.get_unite_a(3, 3) == unite_a_retirer # L'unité est toujours là
    
    # ACT (Success) & ASSERT
    succes_retrait = carte.retirer_unite(unite_a_retirer)
    assert succes_retrait is True
    assert carte.get_unite_a(3, 3) is None # La case est maintenant vide