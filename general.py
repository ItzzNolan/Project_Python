############################################
############ Made By Nolan Grlt ############
############################################

"""On importe des utilitaires standards : dataclass pour des conteneurs d'Actions, Enum pour les types d'action, 
Protocol pour définir des interfaces minimales que le moteur (IA) devra satisfaire"""
from dataclasses import dataclass
from enum import auto, Enum
from typing import Iterable, List, Optional, Tuple, Dict, Any, Protocol

import abc

#Alias simple pour représenter une position sur la grille (x,y)
Cord = Tuple[int, int]

class General(abc.ABC):
    """Classe de base pour les généraux tactiques.
    Le moteur doit appeler decider_actions a chaque tick en passant
    un itérable d'unités alliés et une GameView"""
    
    def __init__(self, name:str, id_player:int):
        #Nom du general et l'ID du joueur
        self.name = name
        self.id_player = id_player
    
    @abc.abstractmethod
    def decider_actions(self):
        pass
