from player import Player
from card_classes.fighter import Fighter
from card_classes.structure import Structure
from card_classes.spell import Spell

class Game:
    def __init__(self, deck_name_1, deck_name_2):
        self.player_1 = Player(deck_name_1)
        self.player_2 = Player(deck_name_2)
        self.turn = 1
        self.active_player = self.player_1
        self.ennemy_player = self.player_2
        self.active_player.draw_card()

    def change_turn(self):
        self.active_player.end_turn(self.ennemy_player)

        if self.active_player == self.player_1:
            self.active_player = self.player_2
            self.ennemy_player = self.player_1
        else:
            self.active_player = self.player_1
            self.ennemy_player = self.player_2
        self.turn += 1

        self.active_player.start_turn(self.ennemy_player)

    def encre_card(self, card):
        self.active_player.encre_card(card)

    def play_unit(self, unit_card, target_place=None, target_effect=None):
        self.active_player.play_unit(unit_card, self.ennemy_player, target_place=target_place, target_effect=target_effect)

    def play_spell(self, spell_card, target_card=None):
        self.active_player.play_spell(spell_card, self.ennemy_player, target=target_card)

    def play_equipment(self, equipment_card, target_card):
        self.active_player.play_equipment(equipment_card, self.ennemy_player, target=target_card)

    def move_fighter_front(self, fighter_card, target_place=None, target_effect=None):
        self.active_player.move_fighter_front(fighter_card, self.ennemy_player, target_place=target_place, target_effect=target_effect)

    def move_fighter_back(self, fighter_card, target_place=None):
        self.active_player.move_fighter_back(fighter_card, target_place=target_place)

    def fight(self, off_card, def_card, interrupt_card=None):
        boost = 0
        block = 0
        if interrupt_card:
            if interrupt_card.interrupt == "cancel":
                self.ennemy_player.discard_card(interrupt_card)
                off_card.actionable = False
                return
            elif interrupt_card.interrupt == "boost_2":
                self.ennemy_player.discard_card(interrupt_card)
                boost = 2
            elif interrupt_card.interrupt == "boost_3":
                self.ennemy_player.discard_card(interrupt_card)
                boost = 3
            elif interrupt_card.interrupt == "block_2":
                self.ennemy_player.discard_card(interrupt_card)
                block = 2
            elif interrupt_card.interrupt == "block_3":
                self.ennemy_player.discard_card(interrupt_card)
                block = 3
        if off_card.actionable and not off_card.frozen and not off_card.stunned:
            if off_card.on_atk:
                off_card.activate_attaque(self.active_player, self.ennemy_player)
            def_card.take_damage(off_card.atk - block)
            if off_card.vol_vie:
                self.active_player.heal(off_card.atk - block)
            if off_card.percee and (def_card.pv < 0):
                self.ennemy_player.take_damage(-def_card.pv)
            if (off_card.rapide and def_card.pv <= 0) or isinstance(def_card, Structure) or def_card.stunned:
                pass
            else:
                off_card.take_damage(def_card.atk + boost)
            off_card.actionable = False

    def fight_face(self, off_card, interrupt_card=None):
        block = 0
        if interrupt_card:
            if interrupt_card.interrupt == "cancel":
                self.ennemy_player.discard_card(interrupt_card)
                off_card.actionable = False
                return
            elif interrupt_card.interrupt == "block_2":
                self.ennemy_player.discard_card(interrupt_card)
                block = 2
            elif interrupt_card.interrupt == "block_3":
                self.ennemy_player.discard_card(interrupt_card)
                block = 3
        if off_card.actionable and not off_card.frozen and not off_card.stunned:
            if off_card.on_atk:
                off_card.activate_attaque(self.active_player, self.ennemy_player)
            self.ennemy_player.take_damage(off_card.atk - block)
            if off_card.vol_vie:
                self.active_player.heal(off_card.atk - block)
            off_card.actionable = False

    def activate_champion_action(self, selected_champion):
        self.active_player.activate_champion_action(selected_champion, self.ennemy_player)

    def summon_champion_incarnation(self, selected_champion):
        self.active_player.summon_champion_incarnation(selected_champion)

    def champion_leveling(self, selected_champion):
        self.active_player.champion_leveling(selected_champion)

    def activate_champion_trigger(self, selected_champion):
        self.active_player.activate_champion_trigger(selected_champion, self.ennemy_player)

    def check_death(self):
        self.active_player.check_death(self.ennemy_player)
        self.ennemy_player.check_death(self.active_player)

    def check_end(self):
        return (self.player_1.health == 0 or self.player_2.health == 0)
                