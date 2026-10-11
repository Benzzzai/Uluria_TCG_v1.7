from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from card_classes.fighter import Fighter
    from card_classes.structure import Structure

from card_classes.card import Card
from config.config_spell import spell_set
import random

class Spell(Card):
    def __init__(self, name):
        config = spell_set[name]
        super().__init__(name, config.get("classe", ""), config.get("cost", 0), config.get("interrupt", None), config.get("description", ""))

    def dmg(self, ally_player, base):
        return base + ally_player.get_puissance()

    def units(self, *players):
        return [unit for player in players for unit in player.frontrow + player.backrow]

    def remove_from_board(self, unit, *players):
        for player in players:
            if unit in player.frontrow:
                player.frontrow.remove(unit)
                return player
            if unit in player.backrow:
                player.backrow.remove(unit)
                return player
        return None

    def activate_spell(self, ally_player, ennemy_player, target=None):
        from card_classes.fighter import Fighter
        from card_classes.structure import Structure

        # Azur
        if self.name == "Pluie de balles":
            for unit in self.units(ally_player, ennemy_player):
                if unit in ally_player.frontrow or unit in ennemy_player.frontrow:
                    unit.take_damage(self.dmg(ally_player, 1))
            ally_player.draw_card(1)
        elif self.name == "Harponnage":
            if target in ennemy_player.backrow and len(ennemy_player.frontrow) < ennemy_player.max_row_size:
                ennemy_player.backrow.remove(target)
                ennemy_player.frontrow.append(target)
            target.frozen = True
        elif self.name == "Élan des flots":
            target.boost(3)
        elif self.name == "Sur la planche":
            fighters = [unit for unit in ennemy_player.frontrow if isinstance(unit, Fighter)]
            if len(fighters) > 0:
                random.choice(fighters).kill()
        elif self.name == "Prière des profondeurs":
            ally_player.summon_unit("Tentacule", "front")
            ally_player.summon_unit("Tentacule", "front")
        elif self.name == "Corrosion":
            ennemy_player.reduce_armor(3)
            ennemy_player.take_damage(self.dmg(ally_player, 3))
        elif self.name == "Marée écrasante":
            for unit in ally_player.frontrow + ennemy_player.frontrow:
                unit.take_damage(self.dmg(ally_player, 3))
        elif self.name == "Faveur de l'océan":
            ally_player.draw_card(2) # the cost reduction is not handled here
        elif self.name == "Orage":
            for unit in self.units(ennemy_player):
                unit.take_damage(self.dmg(ally_player, 2))
                unit.frozen = True
        elif self.name == "Tsunami":
            for player in (ally_player, ennemy_player):
                for unit in player.frontrow + player.backrow:
                    player.deck.append(player.create_card(unit.name))
                player.frontrow.clear()
                player.backrow.clear()
        elif self.name == "Descente dans les abysses":
            pass # needs a persistent cost modifier for the rest of the game

        # Nébuleux
        elif self.name == "Rune contrefaite":
            ally_player.gain_mana(1)
        elif self.name == "Coup bas":
            target.take_damage(self.dmg(ally_player, 1))
            if target.pv <= 0:
                ennemy_player.take_damage(self.dmg(ally_player, 1))
        elif self.name == "Plumeau":
            if target in ennemy_player.frontrow and len(ennemy_player.backrow) < ennemy_player.max_row_size:
                ennemy_player.frontrow.remove(target)
                ennemy_player.backrow.append(target)
        elif self.name == "Chapardage":
            if len(ennemy_player.deck) > 0:
                ally_player.hand.append(ennemy_player.deck.pop(0))
        elif self.name == "Sabotage":
            target.frozen = True
            target.equipment = None
        elif self.name == "Tir reflexe":
            target.take_damage(self.dmg(ally_player, 3))
            if target.pv <= 0:
                ally_player.draw_card(1)
        elif self.name == "Tir meurtrier":
            if ally_player.controls_archetype("Elf"):
                target.kill()
            else:
                pass # needs the player to choose a card to discard
        elif self.name == "Rugissement sauvage":
            for unit in self.units(ally_player):
                if isinstance(unit, Fighter) and unit.has_archetype("Bête"):
                    unit.boost(2)
        elif self.name == "Tir de barrage":
            row = ennemy_player.frontrow if target in ennemy_player.frontrow else ennemy_player.backrow
            for unit in list(row):
                unit.take_damage(self.dmg(ally_player, 5 if unit is target else 2))
        elif self.name == "Aspiration d'ame":
            if self.remove_from_board(target, ennemy_player) is not None:
                ally_player.heal(2)
        elif self.name == "Controle mental":
            was_front = target in ennemy_player.frontrow
            row = ally_player.frontrow if was_front else ally_player.backrow
            if len(row) < ally_player.max_row_size:
                self.remove_from_board(target, ennemy_player)
                row.append(target)
                target.actionable = False
        elif self.name == "Avarice":
            for _ in range(3):
                ally_player.hand.append(ally_player.create_card("Trésort"))

        # Obsidienne
        elif self.name == "Poussière temporelle":
            target.take_damage(self.dmg(ally_player, 2))
            if target.pv <= 0:
                ally_player.mana = min(ally_player.mana + 2, ally_player.mana_max)
        elif self.name == "Piège à ressort":
            owner = self.remove_from_board(target, ennemy_player)
            if owner is not None:
                owner.hand.append(owner.create_card(target.name))
        elif self.name == "Pétrification":
            pass # needs the mana pile
        elif self.name == "Drain de vie":
            target.take_damage(self.dmg(ally_player, 3))
            ally_player.heal(3)
        elif self.name == "Trait de la mort":
            for player in (ally_player, ennemy_player):
                for row in (player.frontrow, player.backrow):
                    if target in row:
                        for unit in list(row):
                            unit.take_damage(self.dmg(ally_player, 3))
        elif self.name == "Frénésie mortelle":
            for unit in self.units(ally_player):
                if isinstance(unit, Fighter):
                    unit.boost(3)
            # needs a "destroy at end of turn" mechanism
        elif self.name == "Néant":
            for unit in self.units(ally_player, ennemy_player):
                unit.kill()
        elif self.name == "Vision de l'au-delà":
            target.kill()
            ally_player.draw_card(2)
        elif self.name == "Rembobinage":
            for player in (ally_player, ennemy_player):
                for unit in list(player.frontrow):
                    if len(player.backrow) < player.max_row_size:
                        player.frontrow.remove(unit)
                        player.backrow.append(unit)
                        unit.actionable = False
        elif self.name == "Tablette de la destinée":
            ally_player.heal(8) # the cost reduction is not handled here
        elif self.name == "Cadran temporel":
            pass # needs the player to choose a card to discard

        # Ocre
        elif self.name == "Fissure":
            fighters = [unit for unit in self.units(ennemy_player) if isinstance(unit, Fighter)]
            if len(fighters) > 0:
                lowest = min(unit.atk for unit in fighters)
                random.choice([unit for unit in fighters if unit.atk == lowest]).kill()
        elif self.name == "Humilité":
            for unit in self.units(ennemy_player):
                if isinstance(unit, Fighter) and unit.atk > 1:
                    unit.boost(1 - unit.atk)
        elif self.name == "En garde":
            target.boost(2)
            ally_player.draw_card(1)
        elif self.name == "Éclat sysmique":
            if isinstance(target, Structure):
                target.kill()
        elif self.name == "Marteau divin":
            owner = self.remove_from_board(target, ennemy_player)
            if owner is not None:
                owner.deck.append(owner.create_card(target.name))
        elif self.name == "Tempete du désert":
            for unit in self.units(ally_player, ennemy_player):
                if isinstance(unit, Fighter) and unit.atk >= 4:
                    unit.kill()
        elif self.name == "Nova sacrée":
            for unit in self.units(ennemy_player):
                unit.take_damage(self.dmg(ally_player, 2))
            for unit in self.units(ally_player):
                unit.heal(2)
        elif self.name == "Garnison du désert":
            for _ in range(3):
                ally_player.summon_unit("Garde des sables", "back")

        # Pourpre
        elif self.name == "Détonation":
            if target:
                target.take_damage(self.dmg(ally_player, 1))
            else:
                ennemy_player.take_damage(self.dmg(ally_player, 1))
        elif self.name == "Uppercut":
            target.frozen = True
        elif self.name == "Execution":
            if target.pv < target.pv_max:
                target.kill()
        elif self.name == "Sang brulant":
            for unit in self.units(ally_player, ennemy_player):
                unit.take_damage(self.dmg(ally_player, 3 if unit.pv < unit.pv_max else 1))
        elif self.name == "Cri de guerre":
            for unit in self.units(ally_player):
                if isinstance(unit, Fighter):
                    unit.boost(1)
        elif self.name == "Boule de feu":
            if target:
                target.take_damage(self.dmg(ally_player, 4))
            else:
                ennemy_player.take_damage(self.dmg(ally_player, 2))
        elif self.name == "Déflagration":
            target.take_damage(self.dmg(ally_player, 7))
        elif self.name == "Flammes des enfers":
            for unit in self.units(ally_player, ennemy_player):
                if not unit.has_archetype("Démon"):
                    unit.take_damage(self.dmg(ally_player, 4))
        elif self.name == "Coup victoire":
            ennemy_player.take_damage(self.dmg(ally_player, 8))

        # Turquoise
        elif self.name == "Coup de bouclier":
            target.take_damage(self.dmg(ally_player, ally_player.armor))
        elif self.name == "Sortilège de mort":
            if target.atk <= 3:
                target.kill()
        elif self.name == "Engelure":
            target.silence()
            target.frozen = True
        elif self.name == "Salve de flèches":
            for _ in range(2):
                for unit in self.units(ennemy_player):
                    unit.take_damage(self.dmg(ally_player, 1))
        elif self.name == "Intelligence":
            ally_player.draw_card(2)
        elif self.name == "Nova de givre":
            for unit in self.units(ennemy_player):
                if isinstance(unit, Fighter):
                    unit.frozen = True
        elif self.name == "Potion de lave":
            for unit in self.units(ally_player, ennemy_player):
                if isinstance(unit, Fighter):
                    unit.take_damage(self.dmg(ally_player, 3))
            if ally_player.reveal_elementaire():
                ally_player.summon_unit("Flammèche", "back")
        elif self.name == "Fracture tellurique":
            for unit in self.units(ennemy_player):
                unit.take_damage(self.dmg(ally_player, 5))
            ally_player.mana_max -= 1
        elif self.name == "Wyrm de givre":
            for unit in self.units(ennemy_player):
                if isinstance(unit, Fighter):
                    unit.frozen = True
            if len(ally_player.frontrow) == 0:
                ally_player.summon_unit("Drake primitif", "front")
        elif self.name == "Avalanche":
            pass # needs 2 targets
        elif self.name == "Heurtoir":
            target.take_damage(self.dmg(ally_player, 4))
            ally_player.gain_armor(4)

        # Verdant
        elif self.name == "Concentration":
            ally_player.mana = min(ally_player.mana + 2, ally_player.mana_max)
        elif self.name == "Serre de vautour":
            target.take_damage(self.dmg(ally_player, 2))
        elif self.name == "Fouet de liane":
            for unit in self.units(ennemy_player):
                unit.take_damage(self.dmg(ally_player, 1))
        elif self.name == "Écorce":
            if len(ally_player.deck) > 0:
                ally_player.draw_card(1)
                if isinstance(ally_player.hand[-1], Spell):
                    ally_player.gain_armor(2)
        elif self.name == "Tir de recule":
            target.take_damage(self.dmg(ally_player, 3))
            if target in ennemy_player.frontrow and len(ennemy_player.backrow) < ennemy_player.max_row_size:
                ennemy_player.frontrow.remove(target)
                ennemy_player.backrow.append(target)
        elif self.name == "Tir explosif":
            target.take_damage(self.dmg(ally_player, 5))
        elif self.name == "Floraison":
            ally_player.mana_max += 1
            # retire carte deck
        elif self.name == "Purification":
            for unit in self.units(ally_player, ennemy_player):
                if isinstance(unit, Fighter):
                    unit.equipment = None
        elif self.name == "Régénération":
            ally_player.heal(8)
        elif self.name == "Ronce aggressive":
            for unit in self.units(ennemy_player):
                unit.take_damage(self.dmg(ally_player, 2))
                if isinstance(unit, Fighter):
                    unit.boost(-2)
        elif self.name == "Surcroissance":
            ally_player.mana_max += 2
            # retire carte deck
        elif self.name == "Puissance sylvestre":
            for unit in self.units(ally_player):
                if isinstance(unit, Fighter):
                    unit.boost(2)
                unit.heal(2)
        elif self.name == "Force de la nature":
            ally_player.draw_card(3)
            ally_player.gain_armor(4)
