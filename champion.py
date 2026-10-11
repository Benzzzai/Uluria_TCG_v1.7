import pygame
from config.parameters import CHAMPION_SIZE
from config.config_champion import champion_set


class Champion():
    def __init__(self, name):
        self.name = name
        config = champion_set[name]

        self.classe = config.get("classe", "")
        self.action_cost = config.get("action_cost", None)
        self.evo_target = config.get("evo_target", None)
        self.evo_count = 0
        self.evolved = False
        self.incarnation_cost = config.get("incarnation_cost", None)
        self.effect = config.get("effect", [])

        self.rectangle = pygame.Rect(0, 0, CHAMPION_SIZE, CHAMPION_SIZE + 20)

        self.action = ("action" in self.effect)
        self.evolution = ("evolution" in self.effect)
        self.incarnation = ("incarnation" in self.effect)
        self.trigger = ("trigger" in self.effect)
        self.start_turn = ("start_turn" in self.effect)
        self.end_turn = ("end_turn" in self.effect)

    def leveling(self):
        if not self.evolved and self.evo_target:
            if self.evo_count < self.evo_target:
                self.evo_count += 1
            else:
                self.evolved = True

    def activate_champion_action(self, ally_player, ennemy_player, target=None):
        if self.name == "Seigneur de feu":
            target.take_damage(1)
        elif self.name == "Azir":
            ally_player.summon_unit("Garde de sable", "back")
        elif self.name == "Barbe Bronze":
            ally_player.gain_armor(2 if self.evolved else 1)
        elif self.name == "Najarin":
            ally_player.draw_card()
        elif self.name == "Illaoi":
            ally_player.summon_unit("Tentacule", "front")
        elif self.name == "Manari":
            pass
        elif self.name == "Moria":
            ally_player.heal(2)
        elif self.name == "Thot":
            ally_player.summon_unit("Squelette", "front")

    def activate_champion_trigger(self, ally_player, ennemy_player):
        if self.name == "Caor":
            ally_player.gain_mana(1)
        elif self.name == "Ashe":
            pass
        elif self.name == "Chasseur":
            ally_player.gain_mana(1)
        elif self.name == "Ishtar":
            pass

    def activate_champion_start_turn(self, ally_player, ennemy_player):
        if self.name == "Chargeur orc":
            if len(ally_player.hand) < 3:
                ally_player.draw_card()

    def activate_champion_end_turn(self, ally_player, ennemy_player):
        if self.name == "Garen":
            if len(ally_player.frontrow) > 3:
                ally_player.draw_card()
