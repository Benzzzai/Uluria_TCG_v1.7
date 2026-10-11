from card_classes.card import Card
from card_classes.unit import Unit
from config.config_structure import structure_set
# from card_classes.fighter import Fighter
import random

class Structure(Unit):
    def __init__(self, name):
        config = structure_set[name]
        super().__init__(name, config.get("classe", ""), config.get("cost", 0), config.get("interrupt", None), config.get("description", ""), config.get("pv", 0), config.get("effect", []), config.get("archetype", ""))
        self.row = config.get("row", "front")
    
    def activate_inv(self, ally_player, ennemy_player, target=None):
        if self.name == "Cité des machines":
            ally_player.discover("Méca")

    def activate_mort(self, ally_player, ennemy_player):
        if self.name == "Cage gobline":
            ally_player.summon_unit("Gobelin bagarreur", "front")

    def activate_start_turn(self, ally_player, ennemy_player):
        if self.name == "Tactirelle":
            if len(ennemy_player.frontrow) > 0:
                target = random.choice(ennemy_player.frontrow)
                ennemy_player.frontrow.remove(target)
                ennemy_player.backrow.append(target)
            self.pv -= 1
        elif self.name == "Chalutier":
            ally_player.draw_card(1)
            self.pv -= 1

    def activate_end_turn(self, ally_player, ennemy_player):
        if self.name == "Harponneuse":
            if len(ennemy_player.frontrow) > 0:
                target = random.choice(ennemy_player.frontrow)
                target.take_damage(3)
            self.pv -= 1
        elif self.name == "Foreuse":
            ennemy_player.take_damage(2)
            self.pv -= 1
        elif self.name == "Gardienne":
            for card in ally_player.frontrow:
                card.heal(1)
            self.pv -= 1
        elif self.name == "Bathyscaphe":
            ally_player.gain_armor(2)
            self.pv -= 1
        elif self.name == "Cage gobline":
            self.pv -= 1

    def take_damage(self, value):
        if self.robuste:
                value -= 1
        if value > 0:
            if self.egide:
                self.egide = False
            else:
                self.pv -= 1
    
    def heal(self, value):
        pass # pas sur encore
        # self.pv = min(self.pv + value, self.pv_max)

    def buff(self, atk, pv):
        self.pv += pv
        self.pv_max += pv
