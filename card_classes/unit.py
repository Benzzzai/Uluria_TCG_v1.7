from card_classes.card import Card


class Unit(Card):
    def __init__(self, name, classe, cost, interrupt, description, pv, effect, archetype):
        super().__init__(name, classe, cost, interrupt, description)
        self.pv = pv
        self.pv_max = pv
        self.pv_ori = pv
        self.pv_temp = 0
        self.archetype = archetype

        self.actionable = False
        self.frozen = False
        self.stunned = False

        self.on_inv = ("on_inv" in effect)
        self.on_inv_target = ("on_inv_target" in effect)
        self.front = ("front" in effect)
        self.front_target = ("front_target" in effect)
        self.on_atk = ("on_atk" in effect)
        self.on_soin = ("on_soin" in effect)
        self.on_mort = ("on_mort" in effect)
        self.start_turn = ("start_turn" in effect)
        self.end_turn = ("end_turn" in effect)

        self.avant_garde = ("avant_garde" in effect)
        self.charge = ("charge" in effect)
        self.egide = ("egide" in effect)
        self.insaisissable = ("insaisissable" in effect)
        self.magnetisme = ("magnetisme" in effect)
        self.percee = ("percee" in effect)
        self.protecteur = ("protecteur" in effect)
        self.puissance = ("puissance" in effect)
        self.rapide = ("rapide" in effect)
        self.reincarnation = ("reincarnation" in effect)
        self.robuste = ("robuste" in effect)
        self.vol_vie = ("vol_vie" in effect)

    def has_archetype(self, archetype):
        return archetype in self.archetype

    def activate_inv(self, ally_player, ennemy_player, target=None):
        pass # in subclasses

    def activate_mort(self, ally_player, ennemy_player):
        pass # in subclasses

    def activate_start_turn(self, ally_player, ennemy_player):
        pass # in subclasses

    def activate_end_turn(self, ally_player, ennemy_player):
        pass # in subclasses

    def take_damage(self, value):
        pass # in subclasses

    def heal(self, value):
        pass # in subclasses

    def buff(self, atk, pv):
        pass # in subclasses

    def boost(self, atk):
        pass # in subclasses

    def clear_boost(self):
        pass # in subclasses

    def kill(self):
        self.pv = 0