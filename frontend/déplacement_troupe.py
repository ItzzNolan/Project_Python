import os
import time

# --- Création du terrain ---
def creer_terrain():
    return  [[" " for _ in range(30)] for _ in range(30)]  # matrice 30x15

# --- Affichage du terrain ---
def afficher_terrain(tab):
    os.system('cls' if os.name == 'nt' else 'clear')  # efface la console
    for ligne in tab:
        print("\033[32m=\033[0m".join(ligne))
    print()

# --- Placement initial des troupes bleu/rouge ---
def installer_troupe(tab, type_troupe, nb_troupe, start_index=0):
    # Symboles colorés ANSI
    if type_troupe == "knight":
        symbole_bleu = "\033[34mK\033[0m"  # K bleu
        symbole_rouge = "\033[31mK\033[0m"  # K rouge
    elif type_troupe == "pickman":
        symbole_bleu = "\033[34mP\033[0m"
        symbole_rouge = "\033[31mP\033[0m"
    elif type_troupe == "crossbow":
        symbole_bleu = "\033[34mC\033[0m"
        symbole_rouge = "\033[31mC\033[0m"
    else:
        print("Type de troupe inconnu !")
        return start_index

    total_cases = 30 * 30

    for n in range(nb_troupe):
        pos = start_index + n
        if pos >= total_cases:
            break  # éviter de dépasser le terrain
        i = pos // 30   # ligne
        j = pos % 30    # colonne
        # Effet miroir
        tab[25+i][j] = symbole_bleu 
        tab[5-i][j] = symbole_rouge

    return start_index + nb_troupe

# --- Trouver toutes les positions des troupes d'une couleur ---
def positions_troupes(tab, symbole):
    pos = []
    for i in range(30):
        for j in range(30):
            if symbole in tab[i][j]:
                pos.append([i, j])
    return pos

# --- Déplacer les troupes vers la droite (bleus) ou vers la gauche (rouges) ---
def deplacer_troupes(tab, symbole, direction):
    nouvelles_pos = []
    for i in range(30):
        for j in range(30):
            if symbole in tab[i][j]:
                ni, nj = i+ direction, j 
                # Vérifie que la case suivante est libre
                if 0 <= nj < 30 and tab[ni][nj] == " ":
                    nouvelles_pos.append((ni, nj, tab[i][j]))  # nouvelle position
                    tab[i][j] = " "  # libère l’ancienne
                else:
                    nouvelles_pos.append((i, j, tab[i][j]))  # reste sur place
    # Met à jour le terrain
    for (i, j, val) in nouvelles_pos:
        tab[i][j] = val

# --- Programme principal ---
terrain = creer_terrain()
installer_troupe(terrain, "knight", 20)  # 10 chevaliers bleus et rouges

# Boucle d’animation
for frame in range(30):
    afficher_terrain(terrain)
    deplacer_troupes(terrain, "\033[34m", -1)  # bleus → droite
    deplacer_troupes(terrain, "\033[31m", +1)  # rouges → gauche
    time.sleep(0.3)
