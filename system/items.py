import system.gacha as gacha

ITEMS = {

    # Cards

    "basic_pack": {
        "name": "Basic Pack",
        "description": "Contains 5 cards from the base set.",
        "redeem": {
            "function": gacha.open_pack,
            "kwargs": {
                "pack": "base",
                "count": 5
            }
        }
    },


    # Farming

    "emberblossom_seed": {
        "name": "Emberblossom Seed",
        "description": "Can be grown in the AIO Farming Unit.",
        "farming_grow": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"emberblossom": 1}
                },
            )
        }
    },

    "emberblossom": {
        "name": "Emberblossom",
        "description": "A small flower that emits hot motes."
    },


    "riverleaf_seed": {
        "name": "Riverleaf Seed",
        "description": "Can be grown in the AIO Farming Unit.",
        "farming_grow": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"riverleaf": 1}
                },
            )
        }
    },

    "riverleaf": {
        "name": "Riverleaf",
        "description": "A small, aquatic plant that grows in riverbeds."
    },

    "gustbloom_seed": {
        "name": "Gustbloom Seed",
        "description": "Can be grown in the AIO Farming Unit.",
        "farming_grow": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"gustbloom": 1}
                },
            )
        }
    },

    "gustbloom": {
        "name": "Gustbloom",
        "description": "A tall flower common in high altitude regions."
    },

    "rockroot_seed": {
        "name": "Rockroot Seed",
        "description": "Can be grown in the AIO Farming Unit.",
        "farming_grow": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"rockroot": 1}
                },
            )
        }
    },

    "rockroot": {
        "name": "Rockroot",
        "description": "A sturdy flower made entirely of minerals."
    },

    "minature_phoenix": {
        "name": "Minature Phoenix",
        "description": "A phoenix the size of a regular bird. Aww...",
        "farming_harvest": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"burning_egg": 1}
                },
            )
        }
    },

    "burning_egg": {
        "name": "Burning Egg",
        "description": "A small egg radiating heat."
    },

    "water_snake": {
        "name": "Water Snake",
        "description": "A snake equipped with gills that lives in deep ocean.",
        "farming_harvest": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"aquatic_tail": 1}
                },
            )
        }
    },

    "aquatic_tail": {
        "name": "Aquatic Tail",
        "description": "A long, serpentine tail with a slippery texture."
    },

    "flying_dolphin": {
        "name": "Flying Dolphin",
        "description": "These special dolphins can fly in the air! Not for long, though, since they don't have lungs...",
        "farming_harvest": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"circular_winds": 1}
                },
            )
        }
    },

    "circular_winds": {
        "name": "Circular Winds",
        "description": "A basketball-sized lump of wind currents orbiting each other."
    },

    "little_titan": {
        "name": "Little Titan",
        "description": "They're so strong and powerful! For their size.",
        "farming_harvest": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"earth_core": 1}
                },
            )
        }
    },

    "earth_core": {
        "name": "Earth Core",
        "description": "Formed deep underground, these mystical stones can give life to the inanimate."
    },

    "molten_chunk": {
        "name": "Molten Chunk",
        "description": "An impossibly hot chunk of rock. The source can be extracted by an AIO Farming Unit.",
        "farming_extract": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"persistent_lava": 1}
                },
            )
        }
    },

    "persistent_lava": {
        "name": "Persistent Lava",
        "description": "It looks like ordinary lava, but for some reason, it never cools down."
    },

    "aquamarine_ore": {
        "name": "Aquamarine Ore",
        "description": "Found exclusively in deep seabeds, this ore can be extracted to acquire one of the world's most beautiful metals.",
        "farming_extract": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"aquamarine_ingot": 1}
                },
            )
        }
    },

    "aquamarine_ingot": {
        "name": "Aquamarine Ingot",
        "description": "A blue-green metal that shines with a brilliant luster. It is extraordinary flexible and almost impossible to snap."
    },

    "super_steel_ore": {
        "name": "Super Steel Ore",
        "description": "A mysterious ore which forms naturally inside of floating islands.",
        "farming_extract": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"super_steel_ingot": 1}
                },
            )
        }
    },

    "super_steel_ingot": {
        "name": "Super Steel Ingot",
        "description": "A metal originating the sky. It is extremely strong whilst also being impossibly light."
    },

    "lead_ore": {
        "name": "Lead Ore",
        "description": "An ore abundant underground. Extract it to obtain one of the pillars of modern society!",
        "farming_extract": {
            "time": 60,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"lead_ingot": 1}
                },
            )
        }
    },

    "lead_ingot": {
        "name": "Lead Ingot",
        "description": "Good old-fashioned lead. Sometimes, simpler is better."
    },

    "myriad_flames": {
        "name": "Myriad Flames",
        "description": "A bunch of flames. Despite burning together, each one seems to be slightly different."
    },

    "myriad_waves": {
        "name": "Myriad Waves",
        "description": "A pool of turbulent waves. The waves continuously crash and intersect, but never merge."
    },

    "myriad_winds": {
        "name": "Myriad Winds",
        "description": "A sphere of various wind currents. The winds all blow in different directions and at different speeds."
    },

    "myriad_mineral": {
        "name": "Myriad Mineral",
        "description": "A lump composed of several underground resources. The material takes on properties of all its comprising elements."
    },

    "elemental_nucleus": {
        "name": "Elemental Nucleus",
        "description": "This mysterious object shines with four distinct lights. It seems to have a deep connection with the world..."
    },

    







}