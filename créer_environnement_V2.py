def creer_terrain():
    return [[" " for _ in range(60)] for _ in range(60)] # dimension du terrain (modifier à 120*120)

def afficher_terrain(tab):
    for ligne in tab:
        print("\033[32m=\033[0m".join(ligne))   # crée le sol vert "=" 
        # je ne sais pas vraiment comment fonctionne .join(ligne) et pourquoi ça crée un espace entre chaque "="

def installer_troupe(tab, type_troupe, nb_troupe, start_index=0): 
    # Choisir le symbole selon le type d'unité
    if type_troupe == "knight":
        symbole_bleu = "\033[34mK\033[0m" # écrit "K" en bleu
        symbole_rouge = "\033[31mK\033[0m" # écrit "K" en rouge
    elif type_troupe == "pickman":
        symbole_bleu = "\033[34mP\033[0m" # écrit "P" en bleu
        symbole_rouge = "\033[31mP\033[0m"  # écrit "P" en rouge
    elif type_troupe == "crossbow":
        symbole_bleu = "\033[34mC\033[0m"  # écrit "C" en bleu
        symbole_rouge = "\033[31mC\033[0m" # écrit "C" en rouge
        # pour les couleur il doit surment y avoir une autre façon de faire
    else:
        print("Type de troupe inconnu !") # en cas d'erreur
        return start_index

    total_cases = 60 * 60 # j'ai choisi 60*60 pour voir tout le terrain sans saut à la ligne

    for n in range(nb_troupe):
        pos = start_index + n # la position des troupe dépend du placement de la première unité (pos) et fait un boucle de nb_troupe
        if pos >= total_cases:
            break  # éviter de dépasser le terrain
        i = pos // 60   # ligne
        j = pos % 60    # colonne
        tab[34+i][j] = symbole_bleu # effet miroir entre rouge et bleu
        tab[24-i][59-j] = symbole_rouge

    return start_index + nb_troupe   # renvoie la nouvelle position libre


terrain = creer_terrain()
# pos permet de définir de définir la position initial de pose des unités
pos = 0
pos = installer_troupe(terrain, "knight", 250, pos) #250 chevaliers
pos = installer_troupe(terrain, "pickman", 100, pos) #100 hommes à lances
pos = installer_troupe(terrain, "crossbow", 500, pos) #500 archers

afficher_terrain(terrain) # affiche tout