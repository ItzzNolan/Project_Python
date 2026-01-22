import datetime
import matplotlib.pyplot as plt

class Tournament:
    def __init__(self, generals_names, scenarios):
        self.generals = generals_names
        self.scenarios = scenarios
        self.results = {s: {g: 0 for g in generals_names} for s in scenarios}
        
        # Listes pour le graphique (Correction de l'erreur)
        self.history_army0 = []
        self.history_army1 = []

    def enregistrer_evolution(self, pop0, pop1):
        """Cette méthode manquait dans ton code !"""
        self.history_army0.append(pop0)
        self.history_army1.append(pop1)

    def enregistrer_resultat(self, scenario, vainqueur, perdant):
        if scenario in self.results and vainqueur in self.results[scenario]:
            self.results[scenario][vainqueur] += 1

    def generer_graphique(self, nom="Evolution_Population"):
        """Crée le graphique PNG"""
        tours = range(len(self.history_army0))
        plt.figure(figsize=(10, 6))
        plt.plot(tours, self.history_army0, label=f"Equipe 0 ({self.generals[0]})", color='blue')
        plt.plot(tours, self.history_army1, label=f"Equipe 1 ({self.generals[1]})", color='red')
        plt.title("Evolution de la population")
        plt.xlabel("Ticks")
        plt.ylabel("Survivants")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{nom}.png")
        plt.close()
        print(f"Graphique généré : {nom}.png")

    def generer_rapport_html(self, filename="rapport_final.html"):
        """Génère la page HTML"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        html = f"<html><body><h1>Rapport de Tournoi</h1><p>Date : {now}</p><table border='1'><tr><th>Scenario</th><th>IA</th><th>Victoires</th></tr>"
        for s in self.scenarios:
            for g in self.generals:
                html += f"<tr><td>{s}</td><td>{g}</td><td>{self.results[s][g]}</td></tr>"
        html += f"</table><h2>Graphique de la bataille</h2><img src='Evolution_Population.png'></body></html>"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Rapport HTML généré : {filename}")