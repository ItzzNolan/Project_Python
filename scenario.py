from carte import Carte
from jeu import Jeu
from generals import * 
from tournament import Tournament

def scenario_piquiers_vs_chevaliers(tournoi=None):
    jeu = Jeu()
    carte = Carte(200, 200)
    jeu.carte = carte

    # Correction de l'erreur MajorDAFT (image_d69935.png)
    # On retire "side" car ton code MajorDAFT ne l'accepte pas
    g1 = MajorDAFT(id_player=0, regroup_at=(4,4))
    g2 = CaptainBraindead(id_player=1)
    generals = {0: g1, 1: g2}

    # Placement des unités
    for x in range(3):
        for y in range(5):
            jeu.ajouter_unite("Crossbowman", x, y, 0)
    for x in range(5, 8):
        for y in range(5):
            jeu.ajouter_unite("Crossbowman", x, y, 1)

    gv = TestGameView(tick=0, units=jeu.unites)
    winner_team = None

    # Simulation
    for tick in range(2000):
        tick_simulation(gv, generals)
        
        # Enregistrement de la population pour le graphique
        pop0 = len([u for u in gv.units if u.alive and u.equipe == 0])
        pop1 = len([u for u in gv.units if u.alive and u.equipe == 1])
        
        if tournoi:
            tournoi.enregistrer_evolution(pop0, pop1)

        winner_team = check_victory(gv)
        if winner_team is not None:
            break

    # Enregistrement du score final
    if tournoi and winner_team:
        vainqueur = g1.name if winner_team == 1 else g2.name
        tournoi.enregistrer_resultat("Piquiers vs Chevaliers", vainqueur, "Autre")

    return jeu

if __name__ == "__main__":
    mon_tournoi = Tournament(["Major DAFT", "Captain BRAINDEAD"], ["Piquiers vs Chevaliers"])
    scenario_piquiers_vs_chevaliers(mon_tournoi)
    
    # Génération des fichiers finaux
    mon_tournoi.generer_graphique("Evolution_Population")
    mon_tournoi.generer_rapport_html("rapport_scenario.html")