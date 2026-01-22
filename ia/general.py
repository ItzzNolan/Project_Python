############################################
############ Made By Nolan Grlt ############
############################################
import time
import os
import sys
parent_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(parent_dir)
from frontend.manager_vue import ManagerVue
"""On importe des utilitaires standards : dataclass pour des conteneurs d'Actions, Enum pour les types d'action, 
Protocol pour définir des interfaces minimales que le moteur (IA) devra satisfaire"""
from dataclasses import dataclass, field
from enum import auto, Enum
from typing import Iterable, List, Optional, Tuple, Dict, Any, Protocol
import os
import abc
import random
from time import sleep
#Alias Tuple pour représenter une position sur la grille (x,y)
Cord = Tuple[int,int]

# ----------------------------
#         Protocoles
# ----------------------------

"""Interface que le moteur doit implementer ou adapter lorsqu'il appelle l'<<IA>>"""
class UnitView(Protocol):
    id:int

    #Identifiant du joueur -->
    equipe:int

    #Coordonnees de l'unit -->
    @property
    def pos(self) -> Cord:...

    #Unit toujours vivante -->
    @property
    def alive(self) -> bool:...

    #HP de l'unit -->
    @property
    def HP(self) -> int:...

    #Attaque dans la portee (tiles) -->
    @property
    def range(self) -> int:...

    @property
    def unit_class(self) -> str:...

    def can_attack(self) -> bool:... #cooldown ready




"""Tests UnitView -->

class Cord:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y

class Soldier:
    def __init__(self, id:int, equipe:int, pos:Cord):
        self.id = id
        self.equipe = equipe
        self._pos = pos
        self._HP = 100

    @property
    def pos(self) -> Cord:
        return self._pos

    @property
    def alive(self) -> bool:
        return self._HP > 0
"""


"""Interface de la vue du jeu"""
class GameView(Protocol):
    #Compteur de ticks (ou de tours) dans le jeu
    @property
    def tick(self) -> int:...

    #LOS
    def raycast(self, x:Cord, y:Cord) -> bool:...

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

    #On cree une carte visible des joueurs sur le plateau
    def map_ascii(self) -> List[str]:...


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
        """Trouver l'ennemi le plus proche --> scan local des ennemis visibles"""
        enemies = game.all_seen_enemies(self.id_player)
        enemies = [e for e in enemies if e.equipe!=self.id_player]
        if not enemies:
            return None
        #Selectionne parmi les ennemis celui qui a la plus petite distance à unit
        return min(enemies, key = lambda e:game.distance_tiles(unit.coords, e.coords))

# ----------------------------
#       Generaux du jeu
# ----------------------------

class CaptainBraindead(General):
    """General qui ne donne aucun ordre et qui sert de baseline
    Maintenant : baseline simple de poursuite et d'attaque. 
    Se deplace vers l'ennemi le plus proche s'il n'y en a aucun a portee
    """

    def __init__(self, id_player:int, chase_range:int = 999):
        super().__init__("Captain BRAINDEAD", id_player)
        self.chase_range = chase_range #Si on veut limite la distance de chasse

    def decider_actions(self, unit_ally:Iterable[UnitView], game:GameView) -> List[Action]:
        """Captain BrainDead Upgraded"""
        orders:List[Action] = []
        for unit in unit_ally:
            if not unit.alive:
                continue
            #Enemies actuellement visibles : preference (raycast + LOS distance)
            visibles = game.enemy_in_los(unit)
            if visibles:
                #Trouver un ennemi dans la range a attaquer
                in_range = [e for e in visibles if game.distance_tiles(unit.coords, e.coords) <= unit.Max_Range+unit.hitbox]
                if in_range and unit.can_attack():
                    target = min(in_range, key = lambda e:e.HP)
                    orders.append(self._order_attack_focus(unit, target))
                    continue
                #Sinon on bouge vers l'ennemi le plus proche
                target = min(visibles, key = lambda e:game.distance_tiles(unit.coords, e.coords))
                orders.append(self._order_move_to(unit, target.coords))
            else:
                #Sinon on bouge vers l'ennemi le plus proche connu s'il y en a un
                nearest = game.nearest_enemy(unit)
                if nearest is None:
                    orders.append(self._order_hold(unit))
                else:
                    #Limite optimale: Ne pas chasser un ennemi toujours trop loin
                    if game.distance_tiles(unit.coords, nearest.coords) <= self.chase_range:
                        orders.append(self._order_move_to(unit, nearest.coords))
                    else:
                        orders.append(self._order_hold(unit))
        return orders
    
class MajorDAFT(General):
    """General qui pour chaque unite, si une cible visible alors attaque la plus faible,
    sinon avance vers l'ennemi le plus proches
    --> Evite la surexposition et respecte les cooldowns
    --> Supporte le regroupement des troupes
    """

    def __init__(self, id_player:int, regroup_at:Optional[Cord] = None, los_range:int=12):
        super().__init__("Major DAFT", id_player)
        #Position de regroupement avant d'attaquer
        self.regroup_at = regroup_at

    def _threat_score(self, enemy:UnitView) -> float:
        """Algorithme : Plus la valeur est elevee, plus la cible est prioritaire!
        Ici, on privilegie les unites à distance (plus dangeureuses) et les unites a faible HP (faciles a down)
        On se contente juste des attributs HP/range
        """
        #Priorite selon les HP de l'ennemi et la portee de l'unite
        score = (enemy.Max_Range*0.5) + ((10-enemy.HP)*0.3)
        #Departager des scores identiques pour eviter une eventuelle casse
        score += random.random() * 0.01
        return score
    
    def _neighbour_step_towards(self, from_pos:Cord, to_pos:Cord, occupied:set, game:GameView) -> Cord:
        """Renvoie un voisin à un seul pas (4 directions) à partir de from_pos qui reduit la distance vers to_pos.
        Essaie d'abord l'axe prefere, sinon essaie les alternatives. Evite si possible de marcher sur des cases occupees.
        Cette fonction empeche l'oscillation car elle selectionne un voisin deterministe qui reduit la distance.
        """

        fx,fy = from_pos
        tx,ty = to_pos
        dx = tx-fx
        dy = ty-fy
        candidats:List[Cord] = []

        #On choisit par preference l'axe avec le plus large delta
        if abs(dx)>=abs(dy):
            if dx>0:
                candidats.append((fx+1, fy))
            elif dx<0:
                candidats.append((fx-1, fy))
            #A la verticale
            if dy>0:
                candidats.append((fx, fy+1))
            elif dy<0:
                candidats.append((fx, fy-1))
        else:
            if dy>0:
                candidats.append((fx, fy+1))
            elif dy<0:
                candidats.append((fx, fy-1))
            if dx>0:
                candidats.append((fx+1, fy))
            elif dx<0:
                candidats.append((fx-1, fy))
        
        #On rentre dans le fallback : on reste en position
        candidats.append((fx, fy))

        #On choisit par preference un candidat inoccupe et accessible à pied qui reduit la distance
        best_dest = from_pos
        best_dist = game.distance_tiles(from_pos, to_pos)
        for c in candidats:
            if not game.is_walkable(c):
                continue
            dest = game.distance_tiles(c, to_pos)
            #Necessite dest < best_dist pour progresser, sauf si seul le maintien en position est possible
            if dest<best_dist and c not in occupied:
                return c
            #Fallback
            if dest<best_dist:
                best_dest = c
                best_dist = dest
        
        #Si rien ne reduit la distance ou si tous sont occupes, le candidat inoccupe
        for c in candidats:
            if game.is_walkable(c) and c not in occupied:
                return c
            
        #Derniere chance : on retourne la meilleure destination
        return best_dest


    def decider_actions(self, unit_ally, game):
        #Convertir l'iterable en liste car on veut plusieurs passes
        allies = [unit for unit in unit_ally if unit.alive]
        #Liste qui contient toutes les actions decidees
        orders = []
        go_all = self._should_end_assault(game) #declencher l'assault final?

        """Si une position de regroupement est demandee et que les troupes ne se sont pas encore regroupes
        On ordonne un FORM_UP (regroup) qu'on simule par des MOVE(s) vers la position regroup_at
        """
        if self.regroup_at is not None and allies:
            #Il faut determiner si la majorite des unites sont a portee du regroupement
            dist_sum = sum(game.distance_tiles(unit.coords, self.regroup_at) for unit in allies)
            average_dist = (dist_sum / len(allies) if allies else 0)

            #Si l'unite est "loin" du point de regroupement et pas en assaut final alors on regroupe
            if average_dist > self.regroup_rad and not go_all:
                for unit in allies:
                    #On se deplace vers le point de regroupement
                    orders.append(self._order_move_to(unit, self.regroup_at))
                return orders #Priorite au regroupement
            
        #Rassembler la liste des ennemis visibles globalement
        seen_enemies = [e for e in game.all_seen_enemies(self.id_player) if e.equipe!=self.id_player]

        #Creer un ensemble de positions actuellement occupees (par des unites vivantes)
        occupied = {unit.coords for unit in (getattr(game, "unit_ally", []) or []) if getattr(unit, "is_alive", False)}

        for unit in allies:
            """ #Ignorer les unites mortes par securite
            if not unit.alive():
                continue """

            #Regarder les ennemis en LOS
            visibles = [e for e in game.enemy_in_los(unit) if e.equipe!=self.id_player]
            target = None

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
            dist = game.distance_tiles(unit.coords, target.coords)

            #Si la cible est dans la portee d'attaque et que l'unite est prete a attaquer alors elle attaque
            if dist <= unit.Max_Range and unit.can_attack():
                orders.append(self._order_attack_focus(unit, target))
                continue

            #Calculer un seul pas vers la cible qui reduit la distance et evite les cases occupees
            step = self._neighbour_step_towards(unit.coords, target.coords, occupied-{unit.coords}, game)

            #Marquer le pas dans le jeu d'occupation pour eviter que deux units choisissent la meme case au meme tick
            occupied.discard(unit.coords)
            occupied.add(step)

            orders.append(self._order_move_to(unit, step))

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
def make_general(typ:str, id_player:int, **kwargs) -> General:
    key = typ.strip().lower() #On nettoie la chaine typ
    if key not in GENERAL_REGISTRY:
        raise KeyError(f"General inconnu '{typ}'. Disponible: {sorted(GENERAL_REGISTRY)}")
    return GENERAL_REGISTRY[key](id_player=id_player, **kwargs)

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

#Cooldown global
CURRENT_TICK = 0

@dataclass
class TestUnit:
    """Implementation d'UnitView pour test local
    Champs:
    -id: identifiant unique
    -equipe: id du joueur (0 ou 1)
    -pos: position (x,y)
    -HP: points de vie
    -attack_range: portee d'attaque (tiles)
    -attack_damage: dmgs infliges par attaque
    -attack_cd_ticks: ticks entre attaques
    -last_attack_tick: tick du dernier tir (pour cooldown)
    -speed: tiles par tick (ici seulement 0 ou 1)
    """
    id:int
    equipe:int
    pos:Cord
    HP:int = 10
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
    def alive(self):
        return self.HP > 0 #and self.alive 
    
    @property
    def range(self):
        return self.attack_range
    
    """@property
    def HP_value(self) -> int:
        return self.HP
    """
    
    def can_attack(self):
        #Suppose qu'on accede a la variable globale CURRENT_TICK dans le simulateur
        global CURRENT_TICK
        #return (self.alive and ((CURRENT_TICK - self.last_attack_tick) >= self.attack_cd_ticks))
        return (CURRENT_TICK - self.last_attack_tick) >= self.attack_cd_ticks

@dataclass
class TestGameView:
    """Implementation de GameView pour tests: prend des listes d'unites
    Elle garde deux listes: allies et enemies (TestUnit). Elle fournit les helpers
    requis par les Generals: enemy_in_los, nearest_enemy, all_seen_enemies,
    distance_tiles, is_walkable.
    """
    tick:int
    """allies: List[TestUnit]
    enemies: List[TestUnit]"""
    units:List[TestUnit] #Toutes les units (equipe 0 et equipe 1)
    width:int = 12
    height:int = 12

    def distance_tiles(self, x, y):
        return abs(x[0]-y[0]) + abs(x[1]-y[1])
    
    #---RAYCAST LOS---#
    def raycast(self, x:Cord, y:Cord) -> bool:
        """Rayon LOS simple (pas d'obstacles pour l'instant)"""
        return True

    def enemy_in_los(self, unit):
        #LOS = distance <= 5 tiles
        return [e for e in self.units if e.alive and e.equipe!=unit.equipe and self.distance_tiles(unit.coords, e.coords) <= 200 and self.raycast(unit.coords, e.coords)]
        
    def nearest_enemy(self, unit):
        alive = [e for e in self.units if e.alive and e.equipe!=unit.equipe]
        if not alive:
            return None
        return min(alive, key = lambda e:self.distance_tiles(unit.coords, e.coords))
        
    def all_seen_enemies(self, id_player):
        #Ici on renvoie juste tous les ennemis vivants
        return [e for e in self.units if e.alive and e.equipe!=id_player]
        
    def is_walkable(self, a):
        return True
    
    #---MAP ASCII---#
    def map_ascii(self) -> List[str]:
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]

        for unit in self.units:
            if not unit.alive:
                continue
            x, y = unit.coords
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[x][y] = str(unit.equipe)

        return ["".join(row) for row in grid]
        

# ----------------------------
#      Simulateur - Tests
# ----------------------------

#Variable globale geree par le simulateur pour le cooldown
CURRENT_TICK = 0


def check_victory(gameView:TestGameView) -> Optional[int]:
    #Verifier les equipes
    alive_player_0 = [unit for unit in gameView.units if unit.equipe==0 and unit.alive]
    alive_player_1 = [unit for unit in gameView.units if unit.equipe==1 and unit.alive]
    
    if not alive_player_0:
        print("\nVICTOIRE DE L'EQUIPE 1")
        return 1
    if not alive_player_1:
        print("\nVICTOIRE DE L'EQUIPE 2")
        return 2
    return None

# def show_map(game:TestGameView):
#     if os.name=='posix':
#         os.system('clear')
#     else:
#         os.system('cls')
    
    print("\n---MAP---")
    for row in game.map_ascii():
        print(row)
    print("")
    sleep(0.1)

def tick_simulation(gameView:TestGameView, generals):
    """Execute un tick de simulation qui appele chaque general pour obtenir des ordres,
    qui applique les MOVEs (pas d'1 tile vers la target), qui applique les ATTACKs si la cible
    est a la portee et si le cooldown est ok, met a jour last_attack_tick et HP
    puis affiche un resume du tick avec des logs complets :
    -actions donnees par chaque general
    -mouvements effectues
    -attaques + degats infliges
    -etat final des units
    """
    global CURRENT_TICK
    #Synchronise la var globale typiquement
    CURRENT_TICK = gameView.tick


    #show_map(gameView)

    """Creation d'un dictionnaire <<id_to_unit>> où chaque cle est l'identifiant (id) 
    d'une unite et la valeur est l'objet TestUnit correspondant
    On accede rapidement a une unite donnee par son identifiant
    """
    id_to_unit = {unit.id:unit for unit in gameView.units}

    """Recuperer les ordres de chaque general pour les unites qu'il controle"""
    all_orders:Dict[int, Action] = {}
    for id_player, general in generals.items():
        #On selectionne les unites vivantes appartenant a ce joueur pour prepare un interface de jeu adapte au General
        units_for_player = [unit for unit in gameView.units if unit.equipe == id_player and unit.alive]
        orders = general.decider_actions(units_for_player, gameView)

        print(f"\n---Ordres donnes par {general.name} (Player {id_player})---")
        if not orders:
            print("Aucuns ordres donnes")
            pass
        for act in orders:
            all_orders[act.unit_id] = act
            print(f"\n---Unit{act.unit_id} -> {act.type.name}" + (f" vers {act.target_pos}" if act.target_pos else "") + (f" cible Unit{act.target_id}" if act.target_id else ""))
    
    """On trie les ordres de mouvements (MOVE) et les ordres d'attaques (ATTACK)"""
    move_orders = {uid: act for uid, act in all_orders.items() if act.type == TypeAction.MOVE}
    attack_orders = {uid: act for uid, act in all_orders.items() if act.type == TypeAction.ATTACK}

#    print("\n---MOUVEMENTS---")

    """Maintenant, on applique les mouvements (MOVE)"""
    for uid, mov in move_orders.items():
        unit = id_to_unit.get(uid)
        if not unit or not unit.alive:
            continue

        before = unit.coords #pos avant deplacement

        #On cible la position
        dest = mov.target_pos
        #Test pas obligatoire mais conseille :)
        if dest is None:
            continue

        #Coordonnes actuelles de l'unite et de la destination cible
        ux, uy = unit.coords
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
            move_to = unit.coords #Toujours la
        
        """#Verifier si l'unite peut se deplacer 
        if gameView.is_walkable(move_to):
            unit.coords = move_to #Interchanger les postions
        """

        unit.coords = move_to
        after = unit.coords #pos apres deplacement
#        print(f"\n-> Unit{uid} se déplace de {before} à {after}")
    
    
#    print("\n---ATTAQUES---")
    """Desormais, on applique les ordres d'attaques (ATTACK)"""
    for uid, att in attack_orders.items():
        attacker = id_to_unit.get(uid)
        #Trouver la cible par id
        attacker.target = id_to_unit.get(att.target_id) #if att.target_id is not None else None

        if not attacker or not attacker.target:
            continue

        if not attacker.alive or not attacker.target.alive:
            continue

        if attacker.equipe == attacker.target.equipe:
            """Ordre d'attaquer un allie - Ignore"""
            continue
        
        #On verifie la portee
        dist  = gameView.distance_tiles(attacker.coords, attacker.target.coords)
        if dist <= attacker.Max_Range and attacker.can_attack():
            before_HP = attacker.target.HP
            #On inflige les dmgs
            damage=attacker.inflict_damage()
            #Limite HP à 0
            if attacker.target.HP <= 0:
                attacker.target.HP = 0
            
#            print(f"\n-> Unit{uid} attaque Unit{attacker.target.id} ")
#            print(f"pour {damage} dégats ")
#            print(f"(HP {before_HP} -> {attacker.target.HP})")
        else:
#            print(f"\n-> Unit{uid} voulait attaquer Unit{att.target_id} mais n'est pas en portee")
            pass
        
    """Auto attaque (si aucuns ordres est donne)"""
    for unit in gameView.units:
        if not unit.alive:
            continue
        if unit.id in attack_orders:
            continue

        enemies = [e for e in gameView.units if (e.alive and e.equipe!=unit.equipe) and gameView.distance_tiles(unit.coords, e.coords) <= unit.Max_Range]

        if enemies and unit.can_attack():
            unit.target = min(enemies, key = lambda e:e.HP)
            before = unit.target.HP
            unit.inflict_damage()
            if unit.target.HP <= 0:
                unit.target.HP = 0
#            print(f"-> (AUTO) Unit{unit.id} attaque Unit{unit.target.id} ")
#            print(f"(HP {before} -> {unit.target.HP})")
    
    #On incremente le tick global (dans l'objet gameView)
    winner = check_victory(gameView)
    if winner:
        print(f"\nL'equipe {winner} a gagne")
        return
    gameView.tick += 1



#    print("\n---ETAT APRES TICK---")
    for unit in sorted(id_to_unit.values(), key=lambda x:(x.equipe, x.id)):
#        print(f"Unit{unit.id:02d} (Player{unit.equipe}) pos={unit.coords} HP={unit.HP}")
        unit.timer+=1
    # time.sleep(0.1)

def print_state(gameView:TestGameView) -> None:
    """Affiche l'etat des unites pour le debugging et les tests"""
    def unit_line(unit:TestUnit) -> str:
        return f"U{unit.id:02d} (P{unit.equipe}) {unit.Unit:8} pos={unit.coords} HP={unit.HP:2f}"
    
#    print(f"---- Tick {gameView.tick} ----")

    for unit in sorted(gameView.units, key = lambda x:(x.equipe, x.id)):
#        print(unit_line(unit))
        pass
#    print("")


if __name__ == "__main__":
    #On installe une seed pour notre GameTesting
    random.seed(1)

    """On cree mtn deux equipes toutes simples pour notre GameTesting 
    (-- Attention ! --) Implementer les classes Unit prochainement !!
    """

    #Equipe 1 - 3 soldats && Equipe 2 - 3 soldats ennemis
    units = [
        TestUnit(1, 0, (0,0), HP=10, attack_range=1, attack_damage=3, attack_cd_ticks=2, unit_class="Melee"),
        TestUnit(2, 0, (0,1), HP=10, attack_range=1, attack_damage=3, attack_cd_ticks=2, unit_class="Melee"),
        TestUnit(3, 0, (1,0), HP=8, attack_range=2, attack_damage=2, attack_cd_ticks=3, unit_class="Archer"),
    
        TestUnit(11, 1, (8,8), HP=10, attack_range=1, attack_damage=3, attack_cd_ticks=2, unit_class="Melee"),
        TestUnit(12, 1, (8,7), HP=8, attack_range=2, attack_damage=2, attack_cd_ticks=3, unit_class="Archer"),
        TestUnit(13, 1, (7,8), HP=6, attack_range=1, attack_damage=4, attack_cd_ticks=3, unit_class="Pikeman"),
    ]

    #On initialise le gameView
    gv = TestGameView(tick=0, units=units)

    """On cree les generaux"""
    #MajorDAFT pour l'equipe 1 avec un point de regroupement proche
    g1 = MajorDAFT(id_player=0, regroup_at=(2,2))

    #CaptainBraindead pour l'equipe 2 pour voir la difference
    g2 = CaptainBraindead(id_player=1)

    generals = {0:g1, 1:g2}

    """Maintenant on simule N ticks et on affiche l'etat des unites"""
    TICKS = 20

    for _ in range(TICKS):
        print_state(gv)
        tick_simulation(gv, generals)
        if check_victory(gv)!=None:
            break
