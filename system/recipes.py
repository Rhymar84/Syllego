import system.gacha as gacha

RECIPES = {

    "myriad_flames": {
        "name": "Myriad Flames",
        "ingredients": {
            "emberblossom": 1,
            "burning_egg": 1,
            "persistent_lava": 1
        },
        "time": 120,
        "ideal_modes": ("fire",),
        "normal_modes": ("basic", "earth", "wind"),
        "loot_tables": {
            "ideal": (
                {
                    "chance": 1,
                    "loot": {"myriad_flames": 1}
                },
            ),
            "normal": (
                {
                    "chance": 0.8,
                    "loot": {"myriad_flames": 1}
                },
                {
                    "chance": 0.2,
                    "loot": {}
                }
            ),
            "bad": (    
                {
                    "chance": 0.33,
                    "loot": {"myriad_flames": 1}
                },
                {
                    "chance": 0.67,
                    "loot": {}
                }
            )
        }
    },

    "myriad_waves": {
        "name": "Myriad Waves",
        "ingredients": {
            "riverleaf": 1,
            "aquatic_tail": 1,
            "aquamarine_ingot": 1
        },
        "time": 120,
        "ideal_modes": ("water",),
        "normal_modes": ("basic", "earth", "wind"),
        "loot_tables": {
            "ideal": (
                {
                    "chance": 1,
                    "loot": {"myriad_waves": 1}
                },
            ),
            "normal": (
                {
                    "chance": 0.8,
                    "loot": {"myriad_waves": 1}
                },
                {
                    "chance": 0.2,
                    "loot": {}
                }
            ),
            "bad": (    
                {
                    "chance": 0.33,
                    "loot": {"myriad_waves": 1}
                },
                {
                    "chance": 0.67,
                    "loot": {}
                }
            )
        }
    },

    "myriad_winds": {
        "name": "Myriad Winds",
        "ingredients": {
            "gustbloom": 1,
            "circular_winds": 1,
            "super_steel_ingot": 1
        },
        "time": 120,
        "ideal_modes": ("wind",),
        "normal_modes": ("basic", "fire", "water"),
        "loot_tables": {
            "ideal": (
                {
                    "chance": 1,
                    "loot": {"myriad_winds": 1}
                },
            ),
            "normal": (
                {
                    "chance": 0.8,
                    "loot": {"myriad_winds": 1}
                },
                {
                    "chance": 0.2,
                    "loot": {}
                }
            ),
            "bad": (    
                {
                    "chance": 0.33,
                    "loot": {"myriad_winds": 1}
                },
                {
                    "chance": 0.67,
                    "loot": {}
                }
            )
        }
    },

    "myriad_mineral": {
        "name": "Myriad Mineral",
        "ingredients": {
            "rockroot": 1,
            "earth_core": 1,
            "lead_ingot": 1
        },
        "time": 120,
        "ideal_modes": ("earth",),
        "normal_modes": ("basic", "fire", "water"),
        "loot_tables": {
            "ideal": (
                {
                    "chance": 1,
                    "loot": {"myriad_mineral": 1}
                },
            ),
            "normal": (
                {
                    "chance": 0.8,
                    "loot": {"myriad_mineral": 1}
                },
                {
                    "chance": 0.2,
                    "loot": {}
                }
            ),
            "bad": (    
                {
                    "chance": 0.33,
                    "loot": {"myriad_mineral": 1}
                },
                {
                    "chance": 0.67,
                    "loot": {}
                }
            )
        }
    },

    "elemental_nucleus": {
        "name": "Elemental Nucleus",
        "ingredients": {
            "myriad_flames": 1,
            "myriad_waves": 1,
            "myriad_winds": 1,
            "myriad_mineral": 1,
        },
        "time": 180,
        "ideal_modes": ("earth", "fire", "water", "wind"),
        "normal_modes": ("basic",),
        "loot_tables": {
            "ideal": (
                {
                    "chance": 0.75,
                    "loot": {"elemental_nucleus": 1}
                },
                {
                    "chance": 0.25,
                    "display_failure": True,
                    "loot": {"myriad_flames": 1, "myriad_waves": 1, "myriad_winds": 1, "myriad_mineral": 1}
                },
            ),
            "normal": (
                {
                    "chance": 0.66,
                    "loot": {"myriad_mineral": 1}
                },
                {
                    "chance": 0.08,
                    "display_failure": True,
                    "loot": {"myriad_flames": 1, "myriad_waves": 1, "myriad_winds": 1}
                },
                {
                    "chance": 0.08,
                    "display_failure": True,
                    "loot": {"myriad_mineral": 1, "myriad_waves": 1, "myriad_winds": 1}
                },
                {
                    "chance": 0.08,
                    "display_failure": True,
                    "loot": {"myriad_flames": 1, "myriad_mineral": 1, "myriad_winds": 1}
                },
                {
                    "chance": 0.08,
                    "display_failure": True,
                    "loot": {"myriad_flames": 1, "myriad_waves": 1, "myriad_mineral": 1}
                },
            ),
            "bad": (    
                {
                    "chance": 0.25,
                    "loot": {"elemental_nucleus": 1}
                },
                {
                    "chance": 0.19,
                    "display_failure": True,
                    "loot": {"myriad_waves": 1}
                },
                {
                    "chance": 0.19,
                    "display_failure": True,
                    "loot": {"myriad_flames": 1}
                },
                {
                    "chance": 0.19,
                    "display_failure": True,
                    "loot": {"myriad_winds": 1}
                },
                {
                    "chance": 0.19,
                    "display_failure": True,
                    "loot": {"myriad_mineral": 1}
                },
            )
        }
    },
}