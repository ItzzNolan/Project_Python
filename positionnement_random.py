 import random


#placer les unité de façon random
#taille map / 2 (longueur)

#dimension map
H = 50
L= 50

L1= L/2 - 3
L2 = L/2 + 3

#definir les unités de façon random
N = H * L1
a1 = random.randint(0, N)
b1 = random.randint(0, N)

c1 = N - a - b

a2 =a1
b2 =b1
c2 = c1

# 3. Ajouter les unités sur la carte
    #  (joueur 1)

    for x in range(L1):
        for y in range(H):  
           if c2 > 0:
              jeu.ajouter_unite("Crossbowman",x,y,0)
              c2 _= 1

            if b2 > 0:
              jeu.ajouter_unite("Knight",x,y,0)
              b2 -= 1

            if a2 > 0:
              jeu.ajouter_unite("Pikeman",x,y,0)
              a2 -= 1
              

    # (joueur 2)
    for x in range(L2, L):
        for y in range(H):
           if a2 > 0:
              jeu.ajouter_unite("Pikeman",x,y,1)
              a2 -= 1

            if b2 > 0:
              jeu.ajouter_unite("Knight",x,y,1)
              b2 -= 1

            if c2 > 0:
              jeu.ajouter_unite("Crossbowman",x,y,1)
              c2 -= 1
