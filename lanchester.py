from carte import Carte
from Units import Unit  
from jeu import Jeu
from general import *
from vue_terminal import afficher
from math import ceil, sqrt

def lanchester(unite:Unit,n:int):
    
    jeu =Jeu("lanchester",n,n)
    x=ceil(sqrt(3*n))
    carte=Carte(x,x)
    jeu.carte=carte
    k=0
    stat=[ceil(sqrt((2*n)**2-n**2))]

    general_joueur1 = MajorDAFT(0)
    general_joueur2 = MajorDAFT(1)


    for i in range(x):
        for j in range(x):
            jeu.ajouter_unite(unite,i,j,0)
            k+=1
            if k>=2*n:
                break
        if k>=2*n:
            k=0
            break

    for i in range(x-1,0,-1):
        for j in range(x-1,0,-1):
            jeu.ajouter_unite(unite,i,j,1)
            k+=1
            if k>=n:
                break
        if k>=n:
            break

    
    gv = TestGameView(tick=0, units=jeu.unites)
    jeu.death0[0]=len([u for u in gv.units if u.alive and u.equipe==0])
    jeu.death1[0]=len([u for u in gv.units if u.alive and u.equipe==1])
    #MajorDAFT pour l'equipe 1 avec un point de regroupement proche
    g1 = MajorDAFT(id_player=0, regroup_at=(2,2))

    #CaptainBraindead pour l'equipe 2 pour voir la difference
    g2 = MajorDAFT(id_player=1,regroup_at=(x-2, x-2))

    generals = {0:g1, 1:g2}

    TICKS = 20000000

    for _ in range(TICKS):
        print_state(gv)
        tick_simulation(gv, generals)
        jeu.death0.append(len([u for u in gv.units if u.alive and u.equipe==0]))
        jeu.death1.append(len([u for u in gv.units if u.alive and u.equipe==1]))
        if check_victory(gv)!=None:
            break

    print(len(gv.units), [i.equipe for i in gv.units])
    jeu.graphic(_,unite)
    return jeu

"""
    afficher(jeu)

    while jeu.est_termine()!=True:
        jeu.mettre_a_jour()
    stat.append(jeu.death1[-1])
    print(stat)
    jeu.graphic(unite)
    return jeu
"""


# A mettre dans jeu.py
def graphic(self,tick:int, nom="KvsP"):
        # PARAMETRES : tick -> nombre final de tour; nom -> nom du fichier 
        x=[x for x in range(tick+1)]
        y=self.death0[1:] #tableau contenant le nombre d'unités vivantes de l'equipe 1
        z=self.death1[1:] #tableau contenant le nombre d'unités vivantes de l'equipe 1
        fig = plt.figure(figsize=(6,6))
        plt.plot(x,y, label="Armée 0")
        plt.plot(x,z, label="Armée 1")
        plt.title("Population des armées par tour")
        plt.xlabel("Tours")
        plt.ylabel("Population")
        plt.legend()
        plt.savefig(f"Test/{nom}.pdf")
        plt.show()