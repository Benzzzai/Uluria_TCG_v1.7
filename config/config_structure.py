structure_set = {
    "Harponneuse": {
        "classe": "Azur",
        "archetype": ["Tourelle"],
        "cost": 3,
        "pv": 3,
        "row": "front",
        "interrupt": None,
        "effect": ["end_turn"],
        "description": "A la fin de votre tour, infligez 3 dégats à une unité adverse aléatoire en frontline"
    },
    "Foreuse": {
        "classe": "Azur",
        "archetype": ["Tourelle"],
        "cost": 3,
        "pv": 2,
        "row": "back",
        "interrupt": None,
        "effect": ["end_turn"],
        "description": "A la fin de votre tour, infligez 2 dégats à l'adversaire"
    },
    "Gardienne": {
        "classe": "Azur",
        "archetype": ["Tourelle"],
        "cost": 2,
        "pv": 3,
        "row": "front",
        "interrupt": None,
        "effect": ["end_turn"],
        "description": "A la fin de votre tour, soignez de 1 vos combattants en frontline"
    },
    "Bathyscaphe": {
        "classe": "Azur",
        "archetype": ["Tourelle"],
        "cost": 3,
        "pv": 2,
        "row": "back",
        "interrupt": None,
        "effect": ["end_turn"],
        "description": "A la fin de votre tour, gagnez 2 d'armure"
    },
    "Tactirelle": {
        "classe": "Azur",
        "archetype": ["Tourelle"],
        "cost": 2,
        "pv": 3,
        "row": "front",
        "interrupt": None,
        "effect": ["start_turn"],
        "description": "Au début de votre tour, repoussez un combattant adverse aléatoire en back line"
    },
    "Chalutier": {
        "classe": "Azur",
        "archetype": ["Tourelle"],
        "cost": 2,
        "pv": 2,
        "row": "back",
        "interrupt": None,
        "effect": ["start_turn"],
        "description": "Au début de votre tour, piochez 1 carte"
    },
    "Tour de guet": {
        "classe": "Turquoise",
        "archetype": [],
        "cost": 2,
        "pv": 3,
        "row": "front",
        "interrupt": None,
        "effect": ["protecteur"],
        "description": "Protecteur"
    },
    "Cage gobeline": {
        "classe": "Pourpre",
        "archetype": [],
        "cost": 2,
        "pv": 2,
        "row": "front",
        "interrupt": "boost_2",
        "effect": ["end_turn", "on_mort"],
        "description": "Dernier souffle : invoquez un Gobelin bagarreur"
    },
    "Canon du navire": {
        "classe": "Pourpre",
        "archetype": [],
        "cost": 2,
        "pv": 2,
        "row": "front",
        "interrupt": None,
        "effect": ["trigger"],
        "description": "Lorsque vous déplacer un Pirate sur votre frontline, infligez 1 dégat à l'adversaire"
    },
    "Cité des machines": {
        "classe": "Ocre",
        "archetype": [],
        "cost": 3,
        "pv": 2,
        "row": "front",
        "interrupt": None,
        "effect": ["on_inv"],
        "description": "Apparition : découvrez un Méca. Vos Mécas sur cette ligne ont +1 Atk"
    },


}