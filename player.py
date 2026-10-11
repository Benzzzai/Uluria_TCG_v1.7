from card_classes.unit import Unit
from card_classes.fighter import Fighter
from card_classes.structure import Structure
from card_classes.spell import Spell
from card_classes.equipment import Equipment
from champion import Champion
from config.config_deck import deck_set
from config.config_card import card_set
import random

class Player:
    def __init__(self, deck_name):
        self.name = deck_name
        self.champions = [Champion(champion_name) for champion_name in deck_set[self.name]["champions"]]

        self.deck = []
        self.hand = []
        self.frontrow = []
        self.backrow = []
        self.discard = []
        self.build_deck_and_hand(deck_name)

        self.health = 25 if "Tréant protecteur" in deck_set[self.name]["champions"] else 20
        self.armor = 0
        self.mana = 0
        self.mana_max = 0
        self.encre = False

        self.puissance = 0

        self.max_row_size = 5
    
    def create_card(self, name):
        card_type = card_set[name]
        if card_type == "fighter":
            return Fighter(name)
        elif card_type == "structure":
            return Structure(name)
        elif card_type == "spell":
            return Spell(name)
        elif card_type == "equipment":
            return Equipment(name)

    def build_deck_and_hand(self, deck_name):
        for card_name, n_copy in deck_set[deck_name]["main_deck"].items():
            for _ in range(n_copy):
                self.deck.append(self.create_card(card_name))
        random.shuffle(self.deck)
        self.draw_card(3)

    def start_turn(self, ennemy):
        for champion in self.champions:
            champion.activate_champion_start_turn(self, ennemy)
        if len(self.hand) < 5:
            self.draw_card(2)
        else:
            self.draw_card(1)
        self.refresh_actionable()
        self.mana = self.mana_max
        self.encre = False
        
        for card in self.backrow:
            if card.start_turn:
                card.activate_start_turn(self, ennemy)
        for card in self.frontrow:
            if card.start_turn:
                card.activate_start_turn(self, ennemy)

    def end_turn(self, ennemy):
        for card in self.backrow:
            card.frozen = False
            card.stunned = False
            card.clear_boost()
            if card.end_turn:
                card.activate_end_turn(self, ennemy)
        for card in self.frontrow:
            card.frozen = False
            card.stunned = False
            card.clear_boost()
            if card.end_turn:
                card.activate_end_turn(self, ennemy)
        for champion in self.champions:
            champion.activate_champion_end_turn(self, ennemy)
                    
    def refresh_actionable(self):
        for card in self.backrow:
            card.actionable = True
        for card in self.frontrow:
            card.actionable = True

    def gain_mana(self, value):
        self.mana += value      

    def use_mana(self, cost):
        if cost > self.mana:
            return False
        else:
            self.mana -= cost
            return True

    def draw_card(self, n=1):
        for _ in range(n):
            if len(self.deck) > 0:
                card = self.deck.pop(0)
                self.hand.append(card)
            else:
                self.take_damage(1)

    def discover(self, type):
        self.draw_card()
       
    def encre_card(self, card):
        if not self.encre:
            self.hand.remove(card)
            self.mana += 1
            self.mana_max += 1
            self.encre = True

    def play_unit(self, card, ennemy_player, target_place=None, target_effect=None):
        if target_place:
            if target_place in self.frontrow:
                if card.avant_garde:
                    row = self.frontrow
                    pos = self.frontrow.index(target_place) + 1
                else:
                    return
            elif target_place in self.backrow:
                if card.avant_garde:
                    return
                else:   
                    row = self.backrow
                    pos = self.backrow.index(target_place) + 1
        else:
            row = self.frontrow if card.avant_garde else self.backrow
            pos = 0

        if len(row) < self.max_row_size:
            if self.use_mana(card.cost):
                self.hand.remove(card)
                row.insert(pos, card)
                if card.on_inv_target and target_effect:
                    card.activate_inv_target(self, ennemy_player, target_effect)
                if card.on_inv:
                    card.activate_inv(self, ennemy_player)
                if card.charge:
                    card.actionable = True

    def move_fighter_front(self, card, ennemy_player, target_place=None, target_effect=None):
        if target_place:
            pos = self.frontrow.index(target_place) + 1
        else:
            pos = 0
        if card.actionable and not card.frozen and not card.stunned and len(self.frontrow) < self.max_row_size:
            self.backrow.remove(card)
            self.frontrow.insert(pos, card)
            if card.front_target and target_effect:
                card.activate_front(self, ennemy_player, target_effect)
            if card.front:
                card.activate_front(self, ennemy_player)

    def move_fighter_back(self, card, target_place=None):
        if target_place:
            pos = self.backrow.index(target_place) + 1
        else:
            pos = 0
        if card.actionable and not card.frozen and not card.stunned and len(self.backrow) < self.max_row_size:
            self.frontrow.remove(card)
            self.backrow.insert(pos, card)
            card.actionable = False

    def summon_unit(self, unit_name, row, buff_atk=0, buff_pv=0):
        if row == "front" and len(self.frontrow) < self.max_row_size:
            unit = self.create_card(unit_name)
            self.frontrow.append(unit)
            unit.buff(buff_atk, buff_pv)
        elif row == "back" and len(self.backrow) < self.max_row_size:
            unit = self.create_card(unit_name)
            self.backrow.append(unit)
            unit.buff(buff_atk, buff_pv)
            
    def play_spell(self, card, ennemy_player, target=None):
        if self.use_mana(card.cost):
            self.hand.remove(card)
            self.discard.append(card)
            card.activate_spell(self, ennemy_player, target)

    def play_equipment(self, card, ennemy_player, target):
        if self.use_mana(card.cost):
            self.hand.remove(card)
            card.equip(target)

    def discard_card(self, card):
        self.hand.remove(card)
        self.discard.append(card)

    def activate_champion_action(self, champion, ennemy_player):
        if champion.action:
            if self.use_mana(champion.action_cost):
                champion.activate_champion_action(self, ennemy_player)

    def summon_champion_incarnation(self, champion):
        if champion.incarnation:
            if self.use_mana(champion.incarnation_cost):
                self.summon_unit(champion.name, "back")

    def champion_leveling(self, champion):
        champion.leveling()

    def activate_champion_trigger(self, champion, ennemy_player):
        if champion.trigger:
            champion.activate_champion_trigger(self, ennemy_player)
        
    def check_death(self, ennemy_player):
        for card in self.frontrow:
            if card.pv <= 0:
                if card.on_mort:
                    card.activate_mort(self, ennemy_player)
                if card.reincarnation:
                    card.pv = 1
                    card.reincarnation = False
                else:
                    self.frontrow.remove(card)
                    self.discard.append(card)
        for card in self.backrow:
            if card.pv <= 0:
                if card.on_mort:
                    card.activate_mort(self, ennemy_player)
                if card.reincarnation:
                    card.pv = 1
                    card.reincarnation = False
                else:
                    self.backrow.remove(card)
                    self.discard.append(card)

    def get_puissance(self):
        puissance = 0
        for card in self.backrow + self.frontrow:
            if card.puissance:
                puissance += 1
        puissance += self.puissance
        return puissance
    
    def heal(self, value):
        self.health = min(self.health + value, 20)

    def gain_armor(self, value):
        self.armor += value

    def reduce_armor(self, value):
        self.armor = max(0, self.armor - value)

    def take_damage(self, value):
        if value <= self.armor:
            self.armor -= value
        else:
            value -= self.armor
            self.armor = 0
            self.health = max(0, self.health - value)

    def controls_archetype(self, archetype, exclude=None):
        for card in self.backrow + self.frontrow:
            if card is not exclude and card.has_archetype(archetype):
                return True
        return False
    
    def reveal_elementaire(self):
        for card in self.hand:
            if isinstance(card, Unit):
                if card.has_archetype("Élémentaire"):
                    return True
        return False