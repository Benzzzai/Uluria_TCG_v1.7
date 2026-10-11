from card_classes.structure import Structure
from card_classes.unit import Unit
from card_classes.spell import Spell
from config.config_fighter import fighter_set
import random




class Fighter(Unit):
    def __init__(self, name):
        config = fighter_set[name]
        super().__init__(name, config.get("classe", ""), config.get("cost", 0), config.get("interrupt", None), config.get("description", ""), config.get("pv", 0), config.get("effect", []), config.get("archetype", []))

        self.atk = config.get("atk", 0)
        self.atk_ori = config.get("atk", 0)
        self.atk_temp = 0

        self.equipment = None

    def activate_inv_target(self, ally_player, ennemy_player, target):
        if self.name == "Robot barbier":
            if target.has_archetype("Méca") or target.has_archetype("Pirate"):
                target.boost(1)
        elif self.name == "Face de poulpe":
            target.equipment = None
        elif self.name == "Esprit déchainé":
            target.kill()
        elif self.name == "Robot de soin":
            target.heal(3)
        elif self.name == "Sergent cruel":
            target.take_damage(1)
            target.boost(2)
        elif self.name == "Manieur de sabre":
            if ally_player.controls_archetype("Pirate", exclude=self):
                target.take_damage(2)
        elif self.name == "Éclat glaciaire":
            target.frozen = True
        elif self.name == "Troll des neiges":
            target.frozen = True
        elif self.name == "Friselame":
            if target.frozen:
                target.kill()
            else:
                target.frozen = True
        elif self.name == "Bouftou de guerre":
            if target in ally_player.backrow and len(ally_player.frontrow) < ally_player.max_row_size:
                ally_player.backrow.remove(target)
                ally_player.frontrow.append(target)
        elif self.name == "Bouftou primitif":
            target.take_damage(3)
        elif self.name == "Royalmouth":
            target.heal(2)
            target.boost(2)
        elif self.name == "Archère elf":
            target.take_damage(1)
        elif self.name == "Papillon enchanté":
            target.silence()
        elif self.name == "Druidesse du sabre":
            if ally_player.mana_max >= 5:
                target.take_damage(3)
        elif self.name == "Gardien des bois":
            if target.has_archetype("Elf"):
                target.heal(2)
                target.boost(2)
        elif self.name == "Diablotin de service":
            if target.has_archetype("Démon"):
                target.boost(1)
        elif self.name == "Mordekaiser":
            pass # sacrifice an ally then summon a same-cost fighter from the discard (player choice)

    def activate_inv(self, ally_player, ennemy_player):
        if self.name == "Roi de fondor":
            ally_player.take_damage(5)
            ally_player.gain_armor(10)
        elif self.name == "Vigie pirate":
            ally_player.hand.append(ally_player.create_card("Crochet du pirate"))
        elif self.name == "Barboteur des flots":
            ally_player.summon_unit("Tentacule", "back")
        elif self.name == "Bébé phorreur":
            pass # needs the player to choose a card in hand
        elif self.name == "Gnome Maléfique":
            if len(ennemy_player.deck) > 0:
                ennemy_player.discard.append(ennemy_player.deck.pop(0))
        elif self.name == "Albatros puant":
            ally_player.draw_card(1)
            ennemy_player.draw_card(1)
        elif self.name == "Diablotin sournois":
            pass # needs the player to choose a card to discard
        elif self.name == "Saccagueur démoniaque":
            ally_player.mana_max -= 1
        elif self.name == "Chef de gang des diablotins":
            ally_player.discover("Démon")
            # check to play it
        elif self.name == "Seigneur déchainé des enfers":
            ally_player.mana_max -= 1
        elif self.name == "Archer squelette":
            ennemy_player.take_damage(1)
        elif self.name == "Sombre cultiste":
            ally_player.heal(3)
        elif self.name == "Collecteur d'ames":
            ally_player.mana_max += 1
        elif self.name == "Disciple de Thot":
            self.egide = True
        elif self.name == "Homoncule nonchalent":
            self.frozen = True
        elif self.name == "Matelot sanglant":
            if ally_player.controls_archetype("Pirate", exclude=self):
                self.charge = True
        elif self.name == "Diablotin des abimes":
            ally_player.take_damage(2)
        elif self.name == "Berger porcass":
            pass # needs the player to choose a 1 mana fighter in hand
        elif self.name == "Conservateur du musée":
            pass # needs the player to choose an equipment in the discard
        elif self.name == "Serviteur de Caor":
            ally_player.discover("spell")
        elif self.name == "Maitre blessé":
            self.take_damage(4)
        elif self.name == "Corsaire furtif":
            ennemy_player.reduce_armor(3)
        elif self.name == "Guerrier d'élite Cognefer":
            if len(ennemy_player.frontrow) > 0 and len(ally_player.frontrow) == 0:
                self.charge = True
        elif self.name == "Garde infernal":
            ally_player.take_damage(2)
            ennemy_player.take_damage(2)
        elif self.name == "Garde tortue":
            ally_player.discover("protecteur")
        elif self.name == "Silencieux":
            for unit in ennemy_player.frontrow + ennemy_player.backrow:
                unit.silence()
        elif self.name == "Dragarde":
            ally_player.draw_card(1)
        elif self.name == "Lutin des bois":
            ally_player.discover("spell")
        elif self.name == "Sylvenier du bosquet":
            ally_player.encre = False
        elif self.name == "Protecteur Runique":
            ally_player.gain_armor(5)

    def activate_front(self, ally_player, ennemy_player, target=None):
        if self.name == "Capitaine pirate":
            if target and target.has_archetype("Pirate"):
                target.boost(2)
        elif self.name == "Capitaine double crochet":
            if target in ennemy_player.backrow and len(ennemy_player.frontrow) < ennemy_player.max_row_size:
                ennemy_player.backrow.remove(target)
                ennemy_player.frontrow.append(target)
        elif self.name == "Tofu ventripotent":
            if target in ennemy_player.frontrow and len(ennemy_player.backrow) < ennemy_player.max_row_size:
                ennemy_player.frontrow.remove(target)
                ennemy_player.backrow.append(target)
        elif self.name == "Phorreur cuirassé":
            ally_player.gain_armor(2)
        elif self.name == "Pacificateur":
            if target and target.atk > 1:
                target.boost(1 - target.atk)
        elif self.name == "Garde lumière":
            for unit in ally_player.frontrow:
                unit.heal(2)
        elif self.name == "Pillard gobelin":
            ally_player.hand.append(ally_player.create_card("Trésort"))
        elif self.name == "Samurai porcass":
            pass # needs 2 targets to swap on the enemy frontline
        elif self.name == "Archidruide":
            ally_player.summon_unit("Tréant", "front")
            ally_player.summon_unit("Tréant", "front")
        elif self.name == "Ancien de la forêt":
            ally_player.draw_card(1)

    def activate_trigger(self, ally_player, ennemy_player):
        if self.name == "Caor":
            ennemy_player.take_damage(1)
        elif self.name == "Diablotin des bois":
            ally_player.draw_card()
        elif self.name == "Acolyte de la souffrance":
            ally_player.draw_card()
        elif self.name == "Frondeur Nimbos":
            ally_player.gain_armor(1)

    def activate_attaque(self, ally_player, ennemy_player):
        if self.name == "Tofu royal":
            if self in ally_player.frontrow and len(ally_player.backrow) < ally_player.max_row_size:
                ally_player.frontrow.remove(self)
                ally_player.backrow.append(self)
        elif self.name == "Jeteur d'encre":
            pass # needs to know the attacked fighter died, then summon a Pirate (<= 2 mana) from the discard (player choice)

    def activate_soin(self, ally_player, ennemy_player):
        if self.name == "Clerc du royaume":
            self.boost(2)
        elif self.name == "Prêtresse corrompue":
            for unit in ennemy_player.frontrow + ennemy_player.backrow:
                unit.take_damage(1)

    def activate_mort(self, ally_player, ennemy_player):
        if self.name == "Flibustière fantome":
            ally_player.discover("Pirate")
        elif self.name == "Corbeau pourpre":
            ally_player.discover("interrupt")
        elif self.name == "Berserkoffre":
            ally_player.hand.append(ally_player.create_card("Trésort"))
        elif self.name == "Spectre":
            ally_player.draw_card(1)
        elif self.name == "Mimigoule":
            ally_player.gain_mana(1)
        elif self.name == "Ombre cosmique":
            ally_player.mana_max += 1
        elif self.name == "Mage de sang":
            pass # needs the player to choose a spell in the discard
        elif self.name == "Invocateur du vide":
            pass # needs the player to choose a Démon (<= 2 mana) in the discard
        elif self.name == "Abomination":
            for unit in ally_player.frontrow + ennemy_player.frontrow:
                if unit is not self:
                    unit.take_damage(2)
        elif self.name == "Rejeton de lumière":
            ennemy_player.heal(3)
        elif self.name == "Gobelin malade":
            ennemy_player.take_damage(2)
        elif self.name == "Destrier funeste":
            for unit in ally_player.frontrow + ally_player.backrow:
                if unit is not self:
                    unit.boost(1)
        elif self.name == "Hacheur Nimbos":
            ally_player.gain_armor(2)

    def activate_start_turn(self, ally_player, ennemy_player):
        if self.name == "Gardien de la porte":
            self.pv = self.pv_max
        elif self.name == "Mortamor":
            if self in ally_player.frontrow:
                pass # needs the opponent to choose a card in hand to discard

    def activate_end_turn(self, ally_player, ennemy_player):
        if self.name == "Boufmouth":
            row = ally_player.frontrow if self in ally_player.frontrow else ally_player.backrow
            idx = row.index(self)
            if idx > 0:
                row[idx - 1].heal(1)
            if idx < len(row) - 1:
                row[idx + 1].heal(1)
        elif self.name == "Dragon ancestral":
            ally_player.summon_unit("Drake primitif", "back")
        elif self.name == "Ancien de la forêt":
            if self in ally_player.backrow:
                ally_player.heal(3)

    def take_damage(self, value):
        if self.robuste:
                value -= 1
        if value > 0:
            if self.egide:
                self.egide = False
            else:
                self.pv -= value

    def heal(self, value):
        self.pv = min(self.pv + value, self.pv_max)

    def buff(self, atk, pv):
        self.atk += atk
        self.pv += pv
        self.pv_max += pv

    def boost(self, atk):
        self.atk += atk
        self.atk_temp += atk

    def clear_boost(self):
        self.atk -= self.atk_temp
        self.atk_temp = 0

    def silence(self):
        self.clear_boost()

        self.frozen = False
        self.stunned = False

        self.on_inv = False
        self.on_inv_target = False
        self.front = False
        self.front_target = False
        self.on_atk = False
        self.on_soin = False
        self.on_mort = False
        self.start_turn = False
        self.end_turn = False
        self.avant_garde = False
        self.charge = False
        self.egide = False
        self.insaisissable = False
        self.magnetisme = False
        self.percee = False
        self.protecteur = False
        self.puissance = False
        self.rapide = False
        self.reincarnation = False
        self.robuste = False
        self.vol_vie = False
