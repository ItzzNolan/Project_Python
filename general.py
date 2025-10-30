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
    FORM_UP = auto()

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
    
    def __init__(self, name:str, id_player:int, *, end_assault_after:Optional[int]=60*60):
        #Nom du general et l'ID du joueur
        self.name = name
        self.id_player = id_player

        #Ticks apres lesquels on force un assault final (None=jamais)
        self.end_assault_after = end_assault_after
    
    @abc.abstractmethod
    def decider_actions(self, unit_ally:Iterable[UnitView], game:GameView) -> List[Action]:
        """Doit retourner une liste d'Action pour ce tick
        Le moteur doit appeler cette methode a chaque tick et executer les actions retournes
        """
        raise NotImplementedError
    
    # --- Helpers --- #
    def _should_end_assault(self, game:GameView) -> bool:
        """Determine si on doit declencher l'assault final (empeche fuite infini)"""
        return self.end_assault_after is not None and game.tick >= self.end_assault_after
    
    def _order_attack_focus(self, unit:UnitView, target:UnitView) -> Action:
        """Construit un ordre d'attaque focalisee sur une cible <<target>> pour l'unite <<unit>>"""
        return Action(unit_id=unit.id, type=TypeAction.ATTACK, target_id=target.id)
    
    def _order_move_to(self, unit:UnitView, dest:Cord) -> Action:
        """Construit un ordre de deplacement vers une destination <<dest>> pour l'unite <<unit>>"""
        return Action(unit_id=unit.id, type=TypeAction.MOVE, target_pos=dest)
    
    def _closest_enemies(self, unit:UnitView, game:GameView) -> Optional[UnitView]:
        """Trouver l'ennemi le plus proche"""
        try:
            #Si ca marche, on retourne directement le resultat (l'ennemi le plus proche)
            return game.nearest_enemy(unit)
        except Exception:
            """Si l'appel echoue, on ne bloque pas le reste du tour, on passe dans le fallback manuel
            --> scan local des ennemis visibles
            """
            enemies = game.all_seen_enemies(self.id_player)
            if not enemies:
                return None
            #Selectionne parmi les ennemis celui qui a la plus petite distance à unit
            return min(enemies, key = lambda e:game.distance_tiles(unit.pos, e.pos))

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
    
class MajorDAFT(General):
    """General qui pour chaque unite, si une cible visible alors attaque la plus faible,
    sinon avance vers l'ennemi le plus proche
    """

    def __init__(self, id_player:int):
        super().__init__(name="Major DAFT", id_player=id_player)

    def decider_actions(self, unit_ally:Iterable[UnitView], game:GameView) -> List[Action]:
        #Liste qui contient toutes les actions decidees
        orders:List[Action] = []
        go_all = self.end_assault_after(game) #declencher l'assault final?

        for unit in unit_ally:
            #Ignorer les unites mortes par securite
            if not unit.is_alive():
                continue

            #Regarder les ennemis en LOS
            visibles = game.enemy_in_los(unit)
            target:Optional[UnitView] = None

            if visibles:
                #Choisir l'ennemi avec le plus faible HP
                target = min(visibles, key = lambda e:e.hp)
            else:
                #Pas de visible donc se rapprocher du plus proche connu
                target = self._closest_enemies(unit, game)
            
            #Pas de cible disponible
            if target is None:
                #rien a faire pour cette unite 
                continue

            #On mesure la distance entre l'unite et la cible
            dist = game.distance_tiles(unit.pos, target.pos)

            #Si la cible est dans la portee d'attaque et que l'unite est prete a attaquer alors elle attaque
            if dist <= unit.range and unit.can_attack():
                orders.append(self._order_attack_focus(unit, target))
            else:
                """Se rapprocher de la position cible
                Si go_all = True, on peut choisir une trajectoire plus agressive
                Pour l'instant on se contente d'aller vers la pos de la cible
                """
                orders.append(self._order_move_to(unit, target.pos))
            
        return orders

# ----------------------------
#    Registre + MakeGeneral
# ----------------------------

GENERAL_REGISTRY = {
    "braindead" : CaptainBraindead,
    "daft" : MajorDAFT,
}

"""Cette fonction va creer un general en fonction d'une chaine de caracteres
typ -> type du general ("daft", "braindead"...)
id_player -> l'id du joueur a qui appartient le general 
**kwargs -> parametres suppl "facultatifs" passes au constructeur de la classe choisie
"""
def make_general(typ:str, id_player:int, **kwargs:Any) -> General:
    key = typ.strip().lower() #On nettoie la chaine typ
    if key not in GENERAL_REGISTRY:
        raise KeyError(f"General inconnu '{typ}'. Disponible: {sorted(GENERAL_REGISTRY)}")
    return GENERAL_REGISTRY[typ](id_player=id_player, **kwargs)

"""Exemple concret
general1 = make_general("daft", id_player=1)
general2 = make_general("braindead", id_player=2)

print(general1.name)  #"Major DAFT"
print(general2.name)  #"Captain BRAINDEAD"
"""

