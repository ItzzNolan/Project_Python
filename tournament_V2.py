import datetime

class Tournament:
    def __init__(self, generals_names, scenarios):
        self.generals = generals_names
        self.scenarios = scenarios
        # Matrice : {Scénario: {IA_A: {IA_B: [victoires, total]}}}
        self.matrix = {s: {g1: {g2: [0, 0] for g2 in generals_names} 
                       for g1 in generals_names} for s in scenarios}

    def enregistrer_resultat(self, scenario, ia_a, ia_b, vainqueur):
        """Enregistre le résultat d'un match précis."""
        if scenario in self.matrix:
            # On incrémente le nombre de matchs joués pour ce duel
            self.matrix[scenario][ia_a][ia_b][1] += 1
            self.matrix[scenario][ia_b][ia_a][1] += 1
            
            # On incrémente la victoire si elle existe
            if vainqueur == ia_a:
                self.matrix[scenario][ia_a][ia_b][0] += 1
            elif vainqueur == ia_b:
                self.matrix[scenario][ia_b][ia_a][0] += 1

    def generer_rapport_html(self, filename="rapport_final.html"):
        """Génère le rapport complet avec toutes les matrices demandées."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # --- CALCULS PRÉALABLES ---
        global_scores = {g: [0, 0] for g in self.generals}
        for s in self.scenarios:
            for g1 in self.generals:
                for g2 in self.generals:
                    # Pour le score global (a), on cumule tout
                    global_scores[g1][0] += self.matrix[s][g1][g2][0]
                    global_scores[g1][1] += self.matrix[s][g1][g2][1]

        # --- DÉBUT DU HTML ---
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial; margin: 30px; line-height: 1.6; color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 40px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }}
                th {{ background-color: #6cbb6c; color: white; padding: 12px; border: 1px solid #ddd; }}
                td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                h1 {{ color: #2c3e50; text-align: center; }}
                h2 {{ color: #27ae60; border-bottom: 2px solid #27ae60; padding-bottom: 5px; }}
                .highlight {{ font-weight: bold; color: #2e7d32; }}
                .reflexive {{ background-color: #edf2f7; font-style: italic; }}
            </style>
        </head>
        <body>
            <h1>Rapport de Tournoi Automatisé</h1>
            <p style="text-align:center;">Généré le : {now}</p>

            <h2>5.a Score Général (Global)</h2>
            <p>Pourcentage de victoires cumulées sur tous les adversaires et tous les scénarios.</p>
            <table>
                <tr><th>Général</th><th>Taux de Victoire Global</th></tr>
        """
        for g in self.generals:
            stats = global_scores[g]
            rate = (stats[0] / stats[1] * 100) if stats[1] > 0 else 0.0
            html += f"<tr><td><strong>{g}</strong></td><td class='highlight'>{rate:.1f}%</td></tr>"

        html += """
            </table>
            <h2>5.b Matrice Général vs Général (Global)</h2>
            <p>Performances cumulées sur l'ensemble des scénarios.</p>
            <table>
                <tr><th>vs</th>
        """
        for g in self.generals: html += f"<th>{g}</th>"
        html += "</tr>"
        for g1 in self.generals:
            html += f"<tr><td><strong>{g1}</strong></td>"
            for g2 in self.generals:
                wins = sum(self.matrix[s][g1][g2][0] for s in self.scenarios)
                total = sum(self.matrix[s][g1][g2][1] for s in self.scenarios)
                rate = (wins / total * 100) if total > 0 else 0.0
                css_class = "reflexive" if g1 == g2 else ""
                html += f"<td class='{css_class}'>{rate:.1f}%</td>"
            html += "</tr>"

        # --- 5.c MATRICE PAR SCÉNARIO ---
        html += "<h2>5.c Détails par Scénario</h2>"
        for s in self.scenarios:
            html += f"<h3>Scénario : {s}</h3><table><tr><th>vs</th>"
            for g in self.generals: html += f"<th>{g}</th>"
            html += "</tr>"
            for g1 in self.generals:
                html += f"<tr><td><strong>{g1}</strong></td>"
                for g2 in self.generals:
                    wins = self.matrix[s][g1][g2][0]
                    total = self.matrix[s][g1][g2][1]
                    rate = (wins / total * 100) if total > 0 else 0.0
                    css_class = "reflexive" if g1 == g2 else ""
                    html += f"<td class='{css_class}'>{rate:.1f}%</td>"
                html += "</tr>"
            html += "</table>"

        # --- 5.d GÉNÉRAL VS SCÉNARIO ---
        html += """
            <h2>5.d Général vs Scénario</h2>
            <p>Analyse de la performance de chaque IA selon le terrain (moyenne face à tous les opposants).</p>
            <table>
                <tr><th>Général \ Scénario</th>
        """
        for s in self.scenarios: html += f"<th>{s}</th>"
        html += "</tr>"
        for g1 in self.generals:
            html += f"<tr><td><strong>{g1}</strong></td>"
            for s in self.scenarios:
                wins = sum(self.matrix[s][g1][g2][0] for g2 in self.generals)
                total = sum(self.matrix[s][g1][g2][1] for g2 in self.generals)
                rate = (wins / total * 100) if total > 0 else 0.0
                html += f"<td>{rate:.1f}%</td>"
            html += "</tr>"

        html += """
            </table>
            <div style="background: #fff3cd; padding: 15px; border-left: 5px solid #ffc107;">
                <strong>Note sur les biais (X vs X) :</strong> Les cases en gris représentent les matchs miroirs. 
                Si ces valeurs s'éloignent significativement de 50%, cela indique un avantage structurel pour l'un des joueurs 
                (ex: camp de départ, ordre de tick) dans votre moteur de jeu.
            </div>
        </body></html>
        """

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Rapport HTML complet généré : {filename}")
