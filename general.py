############################################
############ Made By Nolan Grlt ############
############################################

"""On importe des utilitaires standards : dataclass pour des conteneurs d'Actions, Enum pour les types d'action, 
Protocol pour définir des interfaces minimales que le moteur (IA) devra satisfaire"""
from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Iterable, List, Optional, Tuple, Dict, Any, Protocol

import abc
import math
import random

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
    def distance_tiles(self, x:Cord, y:Cord) -> int:...

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
    FORM_UP = auto() #Pour des ordres de regroupement

@dataclass(frozen=True)
class Action:
    """Objet <<immuable>> representant un ordre pour une unite: quel unit_id, quel type, 
    quel target_id (si attaque) ou target_pos (si déplacement), et un dictionnaire dic pour infos supp"""
    unit_id:int
    type:TypeAction
    target_id:Optional[int] = None
    target_pos:Optional[Cord] = None
    dic:Dict[str, Any] = field(default_factory=dict)

    """Assure qu'on a bien un dict pour dic meme si None est fournie
    def __post_init__(self):
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
    
    def __init__(self, name:str, id_player:int, *, end_assault_after:Optional[int]=60*60, regroup_rad:int = 3):
        #Nom du general et l'ID du joueur
        self.name = name
        self.id_player = id_player

        #Rayon (en tiles) de regroupement
        self.regroup_rad= regroup_rad

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
    
    def _order_hold(self, unit:UnitView) -> Action:
        """Construit un ordre de maintient de l'unite a sa position par defaut"""
        return Action(unit_id=unit.id, type=TypeAction.HOLD)
    
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
    sinon avance vers l'ennemi le plus proches
    --> Evite la surexposition et respecte les cooldowns
    --> Supporte le regroupement des troupes
    """

    def __init__(self, id_player:int, *, regroup_at:Optional[Cord] = None):
        super().__init__(name="Major DAFT", id_player=id_player)
        #Position de regroupement avant d'attaquer
        self.regroup_at = regroup_at

    def _threat_score(self, enemy:UnitView) -> float:
        """Algorithme : Plus la valeur est elevee, plus la cible est prioritaire!
        Ici, on privilegie les unites à distance (plus dangeureuses) et les unites a faible hp (faciles a down)
        On se contente juste des attributs hp/range
        """
        score = 0.0
        
        #Priorite selon la portee de l'unite
        try:
            #Si enemy.range est important, on augmente le score
            score += float(enemy.range) * 0.5
        except Exception:
            pass

        #Priorite selon les HP de l'ennemi
        score += max(0.0, 10.0-float(enemy.hp)) * 0.3
        #Departager des scores identiques pour eviter une eventuelle casse
        score += random.random() * 0.01
        return score
    
    def _avoid_crowd(self, unit:UnitView, allies:List[UnitView], dest:Cord) -> Cord:
        """Si plusieurs allies se dirigent vers la meme case, on decale la destination
        d'une case dans une direction perpendiculaire pour repartir les unites et eviter la congestion
        """

        #Compteur des allies deja proches de la destination dest
        near_sum = sum(1 for a in allies if a.is_alive and (abs(a.pos[0]-dest[0]) + abs(a.pos[1]-dest[1])) <= 1)
        if near_sum <= 1:
            #Pas congestionne
            return dest
        
        """On calcule un decalage (binaire) dependant de l'ID de l'unite, pour que les unites 
        ne choisissent pas toutes la meme direction
        """
        d_x = (unit.id % 2)*1-0 #0 ou 1
        d_y = ((unit.id >> 1)% 2)*1-0
        new_dest = (dest[0]+d_x, dest[1]+d_y)
        return new_dest


    def decider_actions(self, unit_ally:Iterable[UnitView], game:GameView) -> List[Action]:
        #Convertir l'iterable en liste car on veut plusieurs passes
        allies = [unit for unit in unit_ally if unit.is_alive]
        #Liste qui contient toutes les actions decidees
        orders:List[Action] = []
        go_all = self.end_assault_after(game) #declencher l'assault final?

        """Si une position de regroupement est demandee et que les troupes ne se sont pas encore regroupes
        On ordonne un FORM_UP (regroup) qu'on simule par des MOVE(s) vers la position regroup_at
        """
        if self.regroup_at is not None:
            #Il faut determiner si la majorite des unites sont a portee du regroupement
            dist_sum = sum(game.distance_tiles(unit.pos, self.regroup_at) for unit in allies) if allies else 0
            average_dist = dist_sum / len(allies) if allies else 0

            #Si l'unite est "loin" du point de regroupement et pas en assaut final alors on regroupe
            if average_dist > self.regroup_rad and not go_all:
                for unit in allies:
                    #On se deplace vers le point de regroupement
                    orders.append(self._order_move_to(unit, self.regroup_at))
                return orders #Priorite au regroupement
            
        #Rassembler la liste des ennemis visibles globalement
        seen_enemies = game.all_seen_enemies(self.id_player)

        for unit in unit_ally:
            #Ignorer les unites mortes par securite
            if not unit.is_alive():
                continue

            #Regarder les ennemis en LOS
            visibles = game.enemy_in_los(unit)
            target:Optional[UnitView] = None

            if visibles:
                #Choisir la cible la plus prioritaire selon _threat_score
                target = max(visibles, key = lambda e:self._threat_score(e))
            else:
                #Pas de visible donc se rapprocher du plus proche ennemi connu
                target = self._closest_enemies(unit, game)
            
            #Pas de cible disponible
            if target is None:
                #Tenir la position
                orders.append(self._order_hold(unit))
                continue

            #On mesure la distance entre l'unite et la cible
            dist = game.distance_tiles(unit.pos, target.pos)

            #Si la cible est dans la portee d'attaque et que l'unite est prete a attaquer alors elle attaque
            if dist <= unit.range and unit.can_attack():
                orders.append(self._order_attack_focus(unit, target))
                continue

            #Calcul de la destination = pos de la cible
            dest_raw = target.pos
            dest = self._avoid_crowd(unit, allies, dest_raw)

            if go_all:
                """Se rapprocher de la position cible
                Si go_all = True, on peut choisir une trajectoire plus agressive
                On se contente d'aller vers la pos de la cible
                """
                orders.append(self._order_move_to(unit, dest))
            else:
                """Sinon, on teste si se rapprocher est raisonnable 
                (ne pas foncer sur plusieurs ennemis en cas d'inferiorite)
                Si il y a plus d'ennemis visibles que d'allies proches, on garde une distance
                """
                nearby_enemies = sum(1 for e in seen_enemies if game.distance_tiles(unit.pos, e.pos) <= 3)
                nearby_allies = sum(1 for a in allies if game.distance_tiles(unit.pos, a.pos) <= 3)

                if nearby_enemies > nearby_allies and nearby_enemies>=2:
                    #Situation defavorable --> Maintien de l'unite
                    orders.append(self._order_hold(unit))
                else:
                    #On se rapproche normalement
                    orders.append(self._order_move_to(unit, dest))
            
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

# ----------------------------
#  Tests unitaires - FastDev
# ----------------------------

"""Pour simuler rapidement des ticks et observer les Action renvoyes par les generaux"""

@dataclass
class TestUnit:
    """Implementation d'UnitView pour test local
    Champs:
    -id: identifiant unique
    -owner: id du joueur (0 ou 1)
    -pos: position (x,y)
    -hp: points de vie
    -attack_range: portee d'attaque (tiles)
    -attack_damage: dmgs infliges par attaque
    -attack_cd_ticks: ticks entre attaques
    -last_attack_tick: tick du dernier tir (pour cooldown)
    -speed: tiles par tick (ici seulement 0 ou 1)
    """
    id:int
    owner:int
    pos:Cord
    hp:int = 10
    #alive:bool = True
    attack_range:int = 2
    #attack_ready:bool = True
    attack_damage:int = 3
    attack_cd_ticks:int = 3
    last_attack_tick:int = -999
    speed:int = 1  #Tiles par tick (0=imobile, 1=un tile par tick)
    """Utile pour les tests locaux: un nom lisible"""
    unit_class:str = "Soldier"


    @property
    def is_alive(self) -> bool:
        return self.hp > 0 #and self.alive 
    
    @property
    def range(self) -> int:
        return self.attack_range
    
    @property
    def hp_value(self) -> int:
        return self.hp
    
    def can_attack(self) -> bool:
        #Suppose qu'on accede a la variable globale CURRENT_TICK dans le simulateur
        global CURRENT_TICK
        return (CURRENT_TICK - self.last_attack_tick) >= self.attack_cd_ticks and self.is_alive

@dataclass
class TestGameView:
    """Implementation de GameView pour tests: prend des listes d'unites
    Elle garde deux listes: allies et enemies (TestUnit). Elle fournit les helpers
    requis par les Generals: enemy_in_los, nearest_enemy, all_seen_enemies,
    distance_tiles, is_walkable.
    """
    tick:int
    allies: List[TestUnit]
    enemies: List[TestUnit]

    def distance_tiles(self, x:Cord, y:Cord) -> int:
        return abs(x[0]-y[0]) + abs(x[1]-y[1])


    def enemy_in_los(self, unit:UnitView) -> List[UnitView]:
        #LOS = distance <= 5 tiles
        return [e for e in self.enemies if e.is_alive and self.distance_tiles(unit.pos, e.pos) <= 5]
        
    def nearest_enemy(self, unit:UnitView) -> Optional[UnitView]:
        alive = [e for e in self.enemies if e.is_alive]
        if not alive:
            return None
        return min(alive, key = lambda e:self.distance_tiles(unit.pos, e.pos))
        
    def all_seen_enemies(self, id_player:int) -> List[UnitView]:
        #Ici on renvoie juste tous les ennemis vivants
        return [e for e in self.enemies if e.is_alive]
        
    def is_walkable(self, a:Cord) -> bool:
        return True
        
# ----------------------------
#      Simulateur - Tests
# ----------------------------

#Variable globale geree par le simulateur pour le cooldown
CURRENT_TICK = 0

def tick_simulation(gameView:TestGameView, generals:Dict[int, General]) -> None:
    """Execute un tick de simulation qui appele chaque general pour obtenir des ordres,
    qui applique les MOVEs (pas d'1 tile vers la target), qui applique les ATTACKs si la cible
    est a la portee et si le cooldown est ok, met a jour last_attack_tick et hp
    puis affiche un resume du tick
    """
    global CURRENT_TICK
    #Synchronise la var globale typiquement
    CURRENT_TICK = gameView.tick

    """Creation d'un dictionnaire <<id_to_unit>> où chaque cle est l'identifiant (id) 
    d'une unite et la valeur est l'objet TestUnit correspondant
    On accede rapidement a une unite donnee par son identifiant
    """
    id_to_unit:Dict[int, TestUnit] = {unit.id:unit for unit in(gameView.allies + gameView.enemies)}

    """Recuperer les ordres de chaque general pour les unites qu'il controle"""
    all_orders:List[Action] = []
    for id_player, general in generals.items():
        #On selectionne les unites vivantes appartenant a ce joueur pour prepare un interface de jeu adapte au General
        units_for_player = [unit for unit in (gameView.allies + gameView.enemies) if unit.owner == id_player and unit.is_alive]
        orders = general.decider_actions(units_for_player, gameView)
        all_orders.extend(orders)
    
    """On trie les ordres de mouvements (MOVE) et les ordres d'attaques (ATTACK)"""
    move_orders:Dict[int, Action] = {}
    attack_orders:Dict[int, Action] = {}
    for act in all_orders:
        if act.type == TypeAction.MOVE:
            move_orders[act.unit_id] = act
        elif act.type == TypeAction.ATTACK:
            attack_orders[act.unit_id] = act
    #On ignore HOLD (pas de MOVE) et FORM_UP (traite comme un MOVE dans orders)

    """Maintenant, on applique les mouvements (MOVE)"""
    for uid, mov in move_orders.items():
        unit = id_to_unit.get(uid)
        if unit is None or not unit.is_alive:
            continue

        #On cible la position
        dest = mov.target_pos
        #Test pas obligatoire mais conseille :)
        if dest is None:
            continue

        #Coordonnes actuelles de l'unite et de la destination cible
        ux, uy = unit.pos
        tx, ty = dest
        #Calcul des differences de position
        dx = tx - ux
        dy = ty - uy
        #Choix de l'axe pour le deplacement
        if abs(dx) >= abs(dy) and dx!=0:
            move_to = (ux+(1 if dx > 0 else -1), uy)
        elif dy!=0:
            move_to = (ux, uy+(1 if dy > 0 else -1))
        else:
            move_to = (ux, uy) #Toujours la
        
        #Verifier si l'unite peut se deplacer 
        if gameView.is_walkable(move_to):
            unit.pos = move_to #Interchanger les postions
    
    """Desormais, on applique les attaques (ATTACK)"""
    for uid, att in attack_orders.items():
        attacker = id_to_unit.get(uid)
        if attacker is None or not attacker.is_alive:
            continue

        #Trouver la cible par id
        target = id_to_unit.get(att.target_id) if att.target_id is not None else None
        if target is None or not target.is_alive:
            continue
        
        #On verifie la portee
        dist  = gameView.distance_tiles(attacker.pos, target.pos)
        if dist <= attacker.range and attacker.can_attack():
            #On inflige les dmgs
            target.hp -= attacker.attack_damage
            attacker.last_attack_tick = CURRENT_TICK
            #Limite hp à 0
            if target.hp <= 0:
                target.hp = 0
        
    #On incremente le tick global (dans l'objet gameView)
    gameView.tick += 1
