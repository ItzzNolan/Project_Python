#importe la classe Unit du fichier Classe.py -> les fichiers doivent être dans le même dossier pour que cette ligne fonctionne
from Classes import Unit 

#Crée un dictionnaire des unités pour faciliter la fonction crea_units
DictUnits={'Knight':0,'Pikeman':1,'Crossbowman':2,'Long_Swordman':3,'Elite_Skirmisher':4,'Cavalery_Archer':5,'Onager':6,'Light_Cavalry':7,'Scorpion':8,'Capped_Ram':9,'Castle':10,'Trebuchet':11,'Elite_War_Elephant':12,'Monk':13,'Wonder':14}

#Tableau stockant l'intégralité des unités d'une armée
Armee1=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
Armee2=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

def crea_units(n,nomUnite, armee):
    """
    Crée n fois l'unité en entrée nomUnite et les ajoute dans armee
    """
    for i in range(n):
        armee[DictUnits[nomUnite]].append(Unit(nomUnite))


crea_units(20,'Pikeman',Armee1) #Crée 20 Pikemen et les ajoute dans Armee1
crea_units(10,'Knight',Armee1) #Crée 10 Knights et les ajoute dans Armee1
crea_units(5,'Crossbowman',Armee2) #Crée 5 Crossbowmen et les ajoute dans Armee2

    

Unitee=Unit('Knight') #Crée un Knight
Unitee.target=Armee1[1][1] #Affecte à target un Pikeman de Armee1 
print(Unitee.Min_Range,Unitee.Accuracy,Unitee.Blast_Radius, Unitee.target.HP)
Unitee.target.HP -= 4 #Modifie la vie du Pikeman ciblé par Unitee
print(Unitee.Min_Range,Unitee.Accuracy,Unitee.Blast_Radius, Unitee.target.HP)







"""
with open('Stats_Units.csv', 'r') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter='\t')
    for row in spamreader:
        if row['Unit']=='Pikeman':
            print(f"Unité: {row['Unit']}, HP: {row['HP']}, Attack: {row['Attack']}")

class Unit():
    def __init__(self,nomUnite):
            pass                 

    def deplacement():
        pass

    def degats_infliges():
        pass

    def degats_pris():
        pass
"""
