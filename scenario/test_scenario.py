import unittest
from scenario.scenario_chevalier_piquier import scenario_piquiers_vs_chevaliers
from backend.jeu import Jeu
from backend.carte import Carte
from backend.Units import Unit

class TestScenario(unittest.TestCase):
    def test_creation(self):
        jeu = scenario_piquiers_vs_chevaliers()
        self.assertIsInstance(jeu, Jeu)
        self.assertIsNotNone(jeu.carte)
        self.assertEqual(len(jeu.joueurs), 2)
        self.assertGreater(len(jeu.carte.liste_unites), 0)

if __name__ == "__main__":
    unittest.main()
