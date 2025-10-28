############################################
############ Made By Nolan Grlt ############
############################################

"""On importe des utilitaires standards : dataclass pour des conteneurs d'Actions, Enum pour les types d'action, 
Protocol pour définir des interfaces minimales que le moteur (IA) devra satisfaire"""
from dataclasses import dataclass
from enum import auto, Enum
from typing import Iterable, List, Optional, Tuple, Dict, Any, Protocol

import abc

#Alias Tuple pour représenter une position sur la grille (x,y)
Cord = Tuple[int,int]

"""Interface que le moteur doit implementer ou adapter lorsqu'il appelle l'<<IA>>"""
class UnitView(Protocol):
    id:int
    #Identifiant du joueur -->
    owner:int
    #Coordonnees de l’unit -->
    @property
    def pos(self) -> Cord:...
    #Unit toujours vivante -->
    @property
    def is_alive(self) -> bool:...

"""Tests UnitView -->

class Cord:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

class Soldier:
    def __init__(self, id:int, owner:int, pos:Cord):
        self.id = id
        self.owner = owner
        self._pos = pos
        self._hp = 100

    @property
    def pos(self) -> Cord:
        return self._pos

    @property
    def is_alive(self) -> bool:
        return self._hp > 0
"""
"""Interface de la vue du jeu"""
class GameView(Protocol):
    #Compteur de ticks (ou de tours) dans le jeu
    @property
    def tick(self) -> int:...

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
