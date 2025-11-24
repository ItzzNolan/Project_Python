#Ci-dessous se trouve la classe Major DAFT.
#Nolan a créé une version de ce commandant plus intelligente, donc j’ai modifié un peu le code.
#Vous pouvez proposer un nouveau nom pour le commandant de Nolan.
class MajorDAFT(General):
    """
    Major DAFT: Dumb-As-Fuck-Tactician
    Chaque unité attaque l'ennemi le plus proche ou se déplace vers lui sans aucune autre considération.
    """

    def __init__(self, id_player: int):
        super().__init__(name="Major DAFT", id_player=id_player)

    def decider_actions(self, unit_ally: Iterable[UnitView], game: GameView) -> List[Action]:
        actions: List[Action] = []

        for unit in unit_ally:
            if not unit.is_alive:
                continue

            # Trouver l'ennemi le plus proche
            target = self._closest_enemies(unit, game)

            if target is None:
                # Aucun ennemi visible → unit reste sur place
                actions.append(self._order_hold(unit))
                continue

            # Calcul distance
            dist = game.distance_tiles(unit.pos, target.pos)

            if dist <= unit.range:
                # Si l'ennemi est à portée → attaque
                actions.append(self._order_attack_focus(unit, target))
            else:
                # Sinon → se déplacer vers l'ennemi
                actions.append(self._order_move_to(unit, target.pos))

        return actions
