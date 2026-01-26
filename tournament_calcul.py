import datetime

class Tournament:
    def __init__(self, generals_names, scenarios):
        self.generals = generals_names
        self.scenarios = scenarios
        # On stocke les résultats sous forme de matrice
        self.matrix = {s: {g1: {g2: [0, 0] for g2 in generals_names} 
                       for g1 in generals_names} for s in scenarios}

    def enregistrer_resultat(self, scenario, ia_a, ia_b, vainqueur):
        """
        Enregistre le résultat d'un match précis.
        vainqueur: nom de l'IA gagnante ou None pour un nul.
        """
        if scenario in self.matrix:
            # On incrémente le nombre de matchs joués pour ce duel
            self.matrix[scenario][ia_a][ia_b][1] += 1
            self.matrix[scenario][ia_b][ia_a][1] += 1
            
            # On incrémente la victoire si elle existe
            if vainqueur == ia_a:
                self.matrix[scenario][ia_a][ia_b][0] += 1
            elif vainqueur == ia_b:
                self.matrix[scenario][ia_b][ia_a][0] += 1
            else pass

    def generer_rapport_html(self, filename="rapport_final.html"):
        """Génère le rapport avec Score Global et Matrice"""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # --- CALCULS DES SCORES GLOBAUX ---
        global_scores = {g: [0, 0] for g in self.generals}
        for s in self.scenarios:
            for g1 in self.generals:
                for g2 in self.generals:
                        global_scores[g1][0] += self.matrix[s][g1][g2][0]
                        global_scores[g1][1] += self.matrix[s][g1][g2][1]

        # --- DÉBUT DU HTML ---
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial; margin: 30px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 30px; }}
                th {{ background-color: #6cbb6c; color: white; padding: 10px; border: 1px solid #ddd; }}
                td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                h2 {{ color: #333; }}
            </style>
        </head>
        <body>
            <h1>Rapport de Tournoi Automatisé</h1>
            <p>Date : {now}</p>

            <h2>5.a Score Général (Toutes catégories)</h2>
            <table>
                <tr><th>Général</th><th>Taux de Victoire Global</th></tr>
        """
        for g, stats in global_scores.items():
            rate = (stats[0] / stats[1] * 100) if stats[1] > 0 else 0.0
            html += f"<tr><td>{g}</td><td style='color: green; font-weight: bold;'>{rate:.1f}%</td></tr>"

        html += """
            </table>
            <h2>5.b Matrice Général vs Général (Global)</h2>
            <table>
                <tr><th>vs</th>
        """
        # En-têtes de colonnes pour la matrice
        for g in self.generals:
            html += f"<th>{g}</th>"
        html += "</tr>"

        # Corps de la matrice
        for g1 in self.generals:
            html += f"<tr><td><strong>{g1}</strong></td>"
            for g2 in self.generals:
                if g1 == g2:
                    html += "<td>-</td>"
                else:
                    wins = 0
                    total = 0
                    for s in self.scenarios:
                        wins += self.matrix[s][g1][g2][0]
                        total += self.matrix[s][g1][g2][1]
                    rate = (wins / total * 100) if total > 0 else 0.0
                    html += f"<td>{rate:.1f}%</td>"
            html += "</tr>"

        html += "</table></body></html>"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Rapport HTML généré : {filename}")






