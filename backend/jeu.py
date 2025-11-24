# fichier : jeu.py

from backend.carte import Carte

class Jeu:
    def __init__(self, m: int = 10, n: int = 10):
        # Instance de Carte
        self.carte = Carte(m , n)  # m et n sont les dimensions de la carte
        # Liste de toutes les unités dans le jeu
        self.unites = []
        # Liste des joueurs (chaque joueur a un général et ses unités)
        self.joueurs = []

    def est_termine(self):
        """
        Détermine si la partie est terminée.
        Exemple : le jeu s’arrête s’il reste 0 ou 1 joueur.
        """
        return len(self.joueurs) <= 1

    def lancer(self):
        """
        Boucle principale du jeu.
        """
        print("=== Début du jeu ===")

        # Tant que la partie n’est pas terminée
        tour = 1
        while not self.est_termine():
            print(f"\n--- Tour {tour} ---")

            for joueur in self.joueurs:
                general = joueur["general"]
                unites_alliees = joueur["unites"]

                # Le général décide quoi faire
                general.decider_actions(unites_alliees, self)

                # Ici, on exécuterait les actions (déplacements, attaques)
                print(f"{general.__class__.__name__} a fini ses actions.")

            tour += 1

        print("\n=== Partie terminée ===")


