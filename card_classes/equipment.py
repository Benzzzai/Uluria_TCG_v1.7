from card_classes.card import Card
from config.config_equipment import equipment_set


class Equipment(Card):
    def __init__(self, name):
        config = equipment_set[name]
        super().__init__(name, config.get("classe", ""), config.get("cost", 0), config.get("interrupt", None), config.get("description", ""))
        
        self.atk = config.get("atk", 0)
        self.atk_ori = config.get("atk", 0)
        self.pv = config.get("pv", 0)
        self.pv_max = config.get("pv", 0)
        self.effect = config.get("effect", [])

    def equip(self, unit):
        unit.equipment = self
        unit.buff(self.atk, self.pv)

        if self.name == "Crochet":
            pass

    def desequip(self, unit):
        unit.equipment = None
        unit.buff(-self.atk, -self.pv)