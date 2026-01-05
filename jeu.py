# backend/jeu.py

from carte import Carte
from Units import Unit  
from vue_terminal import afficher
import matplotlib.pyplot as plt

class Jeu:
    """
    Classe principale du jeu. Gère la carte, les unités et la boucle de jeu.
    """
    def __init__(self,type='simple',m: int=25,n:int=15):
        """
        Crée une Carte et une liste d'unités.
        """
        # Instance de Carte
        self.carte = Carte(m , n)  # m et n sont les dimensions de la carte
        # Liste de toutes les unités dans le jeu
        self.unites = []
        self._tour = 1
        self.type=type
        self.death0 = [0]
        self.death1 = [0]
        self.n=0

    def graphic(self,nom="KvsP"):
        x=[x for x in range(self._tour-1)]
        y=self.death0[1:]
        z=self.death1[1:]
        fig = plt.figure(figsize=(6,6))
        plt.plot(x,y, label="Armée 0")
        plt.plot(x,z, label="Armée 1")
        plt.title("Population des armées par tour")
        plt.xlabel("Tours")
        plt.ylabel("Population")
        plt.legend()
        plt.savefig(f"Test/{nom}.pdf")
        plt.show()

    def ajouter_unite(self, nom_unite: str, x: int, y: int, equipe: int = 0):
        """
        Crée une unité, l'ajoute à la liste du jeu et la place sur la carte.
        
        Arguments:
            nom_unite: Le type d'unité à créer
            x, y: Position initiale
            equipe: 0 pour équipe bleue, 1 pour équipe rouge
        """
        if self.carte.est_dans_grille(x, y):
            nouvelle_unite = Unit(nomUnite=nom_unite)
            nouvelle_unite.equipe = equipe
            nouvelle_unite.id=self.n
            self.n+=1
            if equipe == 0:
                self.death0[0]+=1
            else:
                self.death1[0]+=1
            nouvelle_unite.coords = (x, y)
            
            self.unites.append(nouvelle_unite)
            self.carte.placer_unite(nouvelle_unite, x, y)
#            print(f"{nom_unite} (équipe {equipe}) ajouté en ({x}, {y}).")
        else:
            print(f"ERREUR : Impossible d'ajouter {nom_unite} en ({x}, {y}), hors de la carte.")

    def est_termine(self) -> bool:
        """
        Vérifie si la partie est terminée (une équipe n'a plus d'unités vivantes).
        """
        # Compter les unités vivantes par équipe
        equipe_0_vivante = any(u.alive and u.equipe == 0 for u in self.unites)
        equipe_1_vivante = any(u.alive and u.equipe == 1 for u in self.unites)
        
        # La partie est terminée si l'une des équipes n'a plus d'unités vivantes
        if not equipe_0_vivante:
            print("\n*** L'EQUIPE ROUGE (1) A GAGNE ! ***")
            return True
        if not equipe_1_vivante:
            print("\n*** L'EQUIPE BLEUE (0) A GAGNE ! ***")
            return True
            
        return False

    def mettre_a_jour(self):
        """
        Méthode principale appelée à chaque tour.
        Gère l'affichage, le déplacement et les combats.
        """
        if self.type=='simple':
            print(f"\n{'='*50}")
            print(f"--- TOUR {self._tour} ---")
            print(f"{'='*50}")

        # 1. AFFICHER L'ÉTAT ACTUEL
            afficher(self)

        # 2. LOGIQUE DU JEU : Chaque unité agit
        for unite in self.unites:
            # Ignorer les unités mortes
            if not unite.alive:
                continue
            
            # Trouver l'ennemi le plus proche
            ennemi, distance = self.find_closest_target(self.unites)
            
            if ennemi is None:
                continue  # Pas d'ennemi trouvé
            
            # Vérifier la portée de l'unité
            portee = unite.Max_Range if unite.Max_Range else 0
            
            # Pour les unités de mêlée (portée 0), elles doivent être sur la même case
            if portee == 0:
                # Vérifier si l'ennemi est sur la même case (distance < 0.1 pour tolérance flottante)
                if distance < 0.1:
                    # ATTAQUE AU CORPS A CORPS !
#                    print(f"[ATTAQUE MELEE] {unite.Unit} (equipe {unite.equipe}) attaque {ennemi.Unit} (equipe {ennemi.equipe}) sur la meme case")
                    
                    unite.target = ennemi
                    unite.inflict_damage()
                    
#                    print(f"   {ennemi.Unit} a maintenant {max(0, ennemi.HP)} HP")
                    
                    if not ennemi.alive:
#                        print(f"[MORT] {ennemi.Unit} est mort !")
                        self.carte.retirer_unite(ennemi)
                else:
                    # SE DÉPLACER vers l'ennemi pour être sur la même case
                    ennemi_x, ennemi_y = ennemi.coords
#                    print(f"[DEPLACEMENT] {unite.Unit} (equipe {unite.equipe}) se deplace vers {ennemi.Unit}")
                    self.deplacer_unite(unite, ennemi_x, ennemi_y)
#                    print(f"   Nouvelle position : {unite.coords}")
            else:
                # Pour les unités à distance
                if distance <= portee:
                    # ATTAQUE A DISTANCE !
#                    print(f"[ATTAQUE DISTANCE] {unite.Unit} (equipe {unite.equipe}) attaque {ennemi.Unit} (equipe {ennemi.equipe}) a distance {distance:.1f}")
                    
                    unite.target = ennemi
                    unite.inflict_damage()
                    
#                    print(f"   {ennemi.Unit} a maintenant {max(0, ennemi.HP)} HP")
                    
                    if not ennemi.alive:
#                        print(f"[MORT] {ennemi.Unit} est mort !")
                        self.carte.retirer_unite(ennemi)
                else:
                    # SE DÉPLACER vers la portée d'attaque
                    ennemi_x, ennemi_y = ennemi.coords
#                    print(f"[DEPLACEMENT] {unite.Unit} (equipe {unite.equipe}) se deplace vers portee d'attaque")
                    self.deplacer_unite(unite, ennemi_x, ennemi_y)
#                    print(f"   Nouvelle position : {unite.coords}")

        # 3. Nettoyer les unités mortes
        self.death0.append(len([u for u in self.unites if u.alive and u.equipe==0]))
        self.death1.append(len([u for u in self.unites if u.alive and u.equipe==1]))
        #print(self.death0,self.death1)
        self.unites = [u for u in self.unites if u.alive]
        self._tour+=1

