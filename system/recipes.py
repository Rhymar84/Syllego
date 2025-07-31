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

    "prismatic_seed": {
        "name": "Prismatic Seed",
        "ingredients": {
            "emberblossom": 1,
            "riverleaf": 1,
            "gustbloom": 1,
            "rockroot": 1
        },
        "time": 150,
        "ideal_modes": ("water", "earth"),
        "normal_modes": ("basic", "wind", "fire"),
        "loot_tables": {
            "ideal": (
                {
                    "chance": 1,
                    "loot": {"prismatic_seed": 1}
                },
            ),
            "normal": (
                {
                    "chance": 0.8,
                    "loot": {"prismatic_seed": 1}
                },
                {
                    "chance": 0.2,
                    "loot": {}
                }
            ),
            "bad": (    
                {
                    "chance": 0.33,
                    "loot": {"prismatic_seed": 1}
                },
                {
                    "chance": 0.67,
                    "loot": {}
                }
            )
        }
    },

    "dragon": {
        "name": "Dragon",
        "ingredients": {
            "burning_egg": 1,
            "aquatic_tail": 1,
            "circular_winds": 1,
            "earth_core": 1
        },
        "time": 150,
        "ideal_modes": ("fire", "wind"),
        "normal_modes": ("basic", "water", "earth"),
        "loot_tables": {
            "ideal": (
                {
                    "chance": 1,
                    "loot": {"dragon": 1}
                },
            ),
            "normal": (
                {
                    "chance": 0.8,
                    "loot": {"dragon": 1}
                },
                {
                    "chance": 0.2,
                    "loot": {}
                }
            ),
            "bad": (    
                {
                    "chance": 0.33,
                    "loot": {"dragon": 1}
                },
                {
                    "chance": 0.67,
                    "loot": {}
                }
            )
        }
    },

    "mythril_chunk": {
        "name": "Mythril Chunk",
        "ingredients": {
            "persistent_lava": 1,
            "aquamarine_ore": 1,
            "super_steel_ore": 1,
            "lead_ore": 1
        },
        "time": 150,
        "ideal_modes": ("earth", "fire"),
        "normal_modes": ("basic", "water", "wind"),
        "loot_tables": {
            "ideal": (
                {
                    "chance": 1,
                    "loot": {"mythril_chunk": 1}
                },
            ),
            "normal": (
                {
                    "chance": 0.8,
                    "loot": {"mythril_chunk": 1}
                },
                {
                    "chance": 0.2,
                    "loot": {}
                }
            ),
            "bad": (    
                {
                    "chance": 0.33,
                    "loot": {"mythril_chunk": 1}
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
                    "loot": {"elemental_nucleus": 1}
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

    "senzu_bean": {
        "name": "Senzu Bean",
        "ingredients": {
            "prismatic_plant": 1,
            "holy_water": 2,
            "myriad_mineral": 1
        },
        "time": 180,
        "ideal_modes": ("water",),
        "normal_modes": ("basic", "earth", "wind"),
        "loot_tables": {
            "ideal": (
                {
                    "chance": 1,
                    "loot": {"senzu_bean": 1}
                },
            ),
            "normal": (
                {
                    "chance": 0.7,
                    "loot": {"senzu_bean": 1}
                },
                {
                    "chance": 0.3,
                    "display_failure": True,
                    "loot": {"myriad_mineral": 1, "prismatic_plant": 1}
                }
            ),
            "bad": (    
                {
                    "chance": 0.3,
                    "loot": {"senzu_bean": 1}
                },
                {
                    "chance": 0.7,
                    "display_failure": True,
                    "loot": {"myriad_mineral": 1}
                }
            )
        }
    },

    "cursed_tool": {
        "name": "Cursed Tool",
        "ingredients": {
            "mythril_ingot": 1,
            "broken_sword": 1,
            "myriad_flames": 1
        },
        "time": 180,
        "ideal_modes": ("fire",),
        "normal_modes": ("basic", "wind", "water"),
        "loot_tables": {
            "ideal": (
                {
                    "chance": 1,
                    "loot": {"cursed_tool": 1}
                },
            ),
            "normal": (
                {
                    "chance": 0.7,
                    "loot": {"cursed_tool": 1}
                },
                {
                    "chance": 0.3,
                    "display_failure": True,
                    "loot": {"myriad_flames": 1, "mythril_ingot": 1}
                }
            ),
            "bad": (    
                {
                    "chance": 0.3,
                    "loot": {"cursed_tool": 1}
                },
                {
                    "chance": 0.7,
                    "display_failure": True,
                    "loot": {"mythril_ingot": 1}
                }
            )
        }
    },
}