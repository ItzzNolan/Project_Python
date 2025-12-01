

# On importe les VRAIES classes que l'on veut tester ensemble.
from backend.carte import Carte
from backend.Units import Unit

NOM_UNITE_POUR_TEST = "Knight"



# --- DÉBUT DES TESTS ---

def test_creation_carte():
    """Vérifie que la carte est créée avec les bonnes dimensions."""
    carte_test = Carte(20, 10)
    assert carte_test.largeur == 20
    assert carte_test.hauteur == 10
    assert len(carte_test.grille) == 10
    assert len(carte_test.grille[0]) == 20

def test_est_dans_grille():
    """Vérifie la détection des coordonnées valides et invalides."""
    carte_test = Carte(20, 10)
    assert carte_test.est_dans_grille(0, 0) is True     # Coin en haut à gauche
    assert carte_test.est_dans_grille(19, 9) is True    # Coin en bas à droite
    assert carte_test.est_dans_grille(20, 9) is False   # Hors limites en largeur
    assert carte_test.est_dans_grille(19, 10) is False  # Hors limites en hauteur

def test_get_unite_a():
    """Vérifie la récupération d'une VRAIE unité sur la carte."""
    # ARRANGE
    carte_test = Carte(5, 5)
    # On crée une VRAIE instance de Unit.
    vraie_unite = Unit(nomUnite=NOM_UNITE_POUR_TEST)
    
    carte_test.placer_unite(vraie_unite, 2, 2)
    
    # ACT & ASSERT
    assert carte_test.get_unite_a(0, 0) is None  # Case vide
    assert carte_test.get_unite_a(2, 2) is vraie_unite # Case avec notre unité
    assert carte_test.get_unite_a(10, 10) is None # Case hors de la carte

def test_placer_unite_succes_et_echecs():
    """Teste les différents scénarios de placement avec de VRAIES unités."""
    # ARRANGE
    carte = Carte(5, 5)
    # On crée deux instances distinctes de la VRAIE classe Unit.
    unite1 = Unit(nomUnite=NOM_UNITE_POUR_TEST)
    unite2 = Unit(nomUnite=NOM_UNITE_POUR_TEST)
    
    # ACT (Success) & ASSERT
    succes_placement_1 = carte.placer_unite(unite1, 1, 1)
    assert succes_placement_1 is True
    assert carte.get_unite_a(1, 1) is unite1
    
    # ACT (Failure - Occupied) & ASSERT
    succes_placement_2 = carte.placer_unite(unite2, 1, 1)
    assert succes_placement_2 is False
    assert carte.get_unite_a(1, 1) is unite1 # C'est toujours unite1 qui est sur la case
    
    # ACT (Failure - Out of bounds) & ASSERT
    succes_placement_3 = carte.placer_unite(unite2, -1, 5)
    assert succes_placement_3 is False

def test_retirer_unite_succes_et_echec():
    """Teste les scénarios de retrait avec de VRAIES unités."""
    # ARRANGE
    carte = Carte(5, 5)
    unite_a_retirer = Unit(nomUnite=NOM_UNITE_POUR_TEST)
    unite_inexistante = Unit(nomUnite=NOM_UNITE_POUR_TEST)
    carte.placer_unite(unite_a_retirer, 3, 3)
    
    # ACT (Failure - Not on map) & ASSERT
    # On essaie de retirer une unité qui n'a jamais été placée sur la carte.
    echec_retrait = carte.retirer_unite(unite_inexistante)
    assert echec_retrait is False
    assert carte.get_unite_a(3, 3) is unite_a_retirer # L'autre unité est toujours là
    
    # ACT (Success) & ASSERT
    succes_retrait = carte.retirer_unite(unite_a_retirer)
    assert succes_retrait is True
    assert carte.get_unite_a(3, 3) is None # La case est maintenant vide