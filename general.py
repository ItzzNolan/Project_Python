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

# ----------------------------
#         Protocoles
# ----------------------------

"""Interface que le moteur doit implementer ou adapter lorsqu'il appelle l'<<IA>>"""
class UnitView(Protocol):
    id:int

    #Identifiant du joueur -->
    owner:int

    #Coordonnees de l'unit -->
    @property
    def pos(self) -> Cord:...

    #Unit toujours vivante -->
    @property
    def is_alive(self) -> bool:...

    #HP de l'unit -->
    @property
    def hp(self) -> int:...

    #Attaque dans la portee (tiles) -->
    @property
    def range(self) -> int:...

    def can_attack(self) -> bool:... #cooldown ready




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

    #Renvoie la liste des ennemis dans la ligne de vue d'une unite
    def enemy_in_los(self, unit:UnitView) -> List[UnitView]:...

    #Renvoie l'ennemi le plus proche d’une unite, ou None s'il n'y en a pas
    def nearest_enemy(self, unit:UnitView) -> Optional[UnitView]:...

    #Renvoie toutes les unites ennemies visibles par un joueur donne
    def all_seen_enemies(self, id_player:int) -> List[UnitView]:...

    #Calcule la distance (en nombre de cases) entre deux coord
    def distance_tiles(self, x:Cord, b:Cord) -> int:...

    #Indique si une case donnee peut etre traversee ou non
    def is_walkable(self, a:Cord) -> bool:...


# ----------------------------
#           Actions
# ----------------------------

class TypeAction(Enum):
    """Type d'actions que le general peut retourner"""
    HOLD = auto()
    MOVE = auto()
    ATTACK = auto()

@dataclass(frozen=True)
class Action:
    """Objet <<immuable>> representant un ordre pour une unite: quel unit_id, quel type, 
    quel target_id (si attaque) ou target_pos (si déplacement), et un dictionnaire dic pour infos supp"""
    unit_id:int
    type:TypeAction
    target_id:Optional[int] = None
    target_pos:Optional[Cord] = None
    dic:Dict[str, Any] = None

    #Assure qu'on a bien un dict pour dic meme si None est fournie
    """def __post_init__(self):
        if self.dic is None:
            object.__setattr__(self,"dic",{})
    """

# ----------------------------
#    Classe de base General
# ----------------------------

class General(abc.ABC):
    """Classe de base pour les généraux tactiques.
    Le moteur doit appeler decider_actions a chaque tick en passant
    un itérable d'unités alliés et une GameView"""
    
    def __init__(self, name:str, id_player:int):
        #Nom du general et l'ID du joueur
        self.name = name
        self.id_player = id_player
    
    @abc.abstractmethod
    def decider_actions(self, unit_ally:Iterable[UnitView], game:GameView) -> List[Action]:
        """Doit retourner une liste d'Action pour ce tick
        Le moteur doit appeler cette methode a chaque tick et executer les actions retournes
        """
        raise NotImplementedError
    

# ----------------------------
#       Generaux du jeu
# ----------------------------

class CaptainBraindead(General):
    """General qui ne donne aucun ordre et qui sert de baseline"""

    def __init__(self, id_player:int):
        super().__init__(name="Captain BRAINDEAD", id_player=id_player)

    def decider_actions(self, unit_ally:Iterable[UnitView], game:GameView) -> List[Action]:
        """On choisit volontairement de ne rien ordonner []
        Le moteur doit interpreter ça comme << laisser les unites suivre leur comportement par defaut >>
        """
        return []
    
