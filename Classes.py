from csv import *


class Unit():
    """
    Crée une classe générale Unit avec l'ensemble des statistiques me semblant interressantes (n'hesitez pas à me dire si quelque chose
    ne convient pas parmi les stats indiquées), les coordonnées ainsi que la cible des attaques. Les 2 dernières étant simplement en 
    figuration pour l'instant
    """
    def __init__(self,nomUnite):
        self.Unit = self.def_stat('Unit',nomUnite)
        self.HP = self.def_stat('HP',nomUnite)
        #self.Type_Attack = self.def_stat('Type_Attack',nomUnite)
        #self.Attack = self.def_stat('Attack',nomUnite)
        #self.Armor = self.def_stat('Armor',nomUnite)
        #self.Pierce_Armor = self.def_stat('Pierce_Armor',nomUnite)
        self.Min_Range = self.def_stat('Min_Range',nomUnite)
        self.Max_Range = self.def_stat('Max_Range',nomUnite)
        self.Line_of_Sight = self.def_stat('Line_of_Sight',nomUnite)
        self.Speed = self.def_stat('Speed',nomUnite)
        self.Attack_Delay = self.def_stat('Attack_Delay',nomUnite)
        self.Reload_Time = self.def_stat('Reload_Time',nomUnite)
        self.Accuracy = self.def_stat('Accuracy',nomUnite)
        self.Blast_Radius = self.def_stat('Blast_Radius',nomUnite)
        self.Garrison = self.def_stat('Garrison',nomUnite)
        
        
        self.Attack = self.def_stat('Attack',nomUnite)
        self.Armor = self.def_stat('Armor',nomUnite)


        self.coords = None 
        self.target = None
        self.alive = False

    def def_stat(self, stat, nomUnite):
        """
        Methode definissant la statistique en entrée en prenant en compte le nom de l'unité 
        """
        if stat=='Attack' or stat=='Armor':
            liste=[]
            with open(f'{stat}.csv', 'r') as csvfile:
                file = list(DictReader(csvfile, delimiter='\t'))
                for row in file:
                    if row['Unit']==nomUnite:
                        statistique = row
            del statistique['Unit']
            for k in statistique:
                if statistique[k]=='None' or statistique[k]==nomUnite:
                    liste.append(k)
                else:
                    statistique[k]=float(statistique[k])
            for i in range(len(liste)):
                del statistique[liste[i]]
            # return row
            return statistique

        else:
            with open('Stats_Units.csv', 'r') as csvfile:
                file = DictReader(csvfile, delimiter='\t')
                for row in file:
                    if row['Unit']==nomUnite:
                        if (stat=='Unit' or stat=='Type_Attack') or row[stat]=='None':
                            return row[stat]
                        return float(row[stat]) #retourne un flottant pour pouvoir réaliser des opérations (ex: HP)
                
    def inflict_damage(self):
        assert type(self.target)!= "<class 'Classes.Unit'>"
        degat=0
        for k in self.Attack:
            for l in self.target.Armor:
                if k == l:
                    degat += max(0,self.Attack[k]-self.target.Armor[l])

        degat=max(1,degat)
        self.target.HP-=degat

    