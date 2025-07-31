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
        "description": "A sturdy plant able to thrive in almost any conditions."
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

    "prismatic_seed": {
        "name": "Prismatic Seed",
        "description": "A multi-coloured seed.",
        "farming_grow": {
            "time": 120,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"prismatic_plant": 1}
                },
            )
        }
    },

    "prismatic_plant": {
        "name": "Prismatic Plant",
        "description": "The petals of this flower each glow with a different colour."
    },

    "dragon": {
        "name": "Dragon",
        "description": "A young adult dragon! It won't eat you. Probably.",
        "farming_harvest": {
            "time": 120,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"dragon_wings": 1}
                },
            )
        },
        "farming_extract": {
            "time": 120,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"dragon_breath": 1}
                },
            )
        }
    },

    "dragon_breath": {
        "name": "Dragon's Breath",
        "description": "The fiery breath of a dragon."
    },

    "dragon_wings": {
        "name": "Dragon's Wings",
        "description": "The wings of a dragon."
    },

    "mythril_chunk": {
        "name": "Mythril Chunk",
        "description": "A fused chunk of various metals. It seems greater than the sum of its parts.",
        "farming_extract": {
            "time": 120,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"mythril_ingot": 1}
                },
            )
        }
    },

    "mythril_ingot": {
        "name": "Mythril Ingot",
        "description": "This material is unlike any found naturally underground..."
    },

    "spirit_fountain": {
        "name": "Spirit Fountain",
        "description": "An elegant fountain. Apparently, submerging one's body in it soothes the soul.",
        "farming_extract": {
            "time": 120,
            "loot_table": (
                {
                    "chance": 0.3,
                    "loot": {"holy_water": 2}
                },
                {
                    "chance": 0.7,
                    "loot": {"holy_water": 1}
                },
            )
        }
    },

    "holy_water": {
        "name": "Holy Water",
        "description": "This water is blessed by divine spirits. It seems to shine when you look into it."
    },

    "senzu_bean": {
        "name": "Senzu Bean",
        "description": "A divine bean grown on Korin's tower. It possesses increadible regenerative and boosting properties."
    },

    "ghostly_knight": {
        "name": "Ghostly Knight",
        "description": "This hollow set of armor is possessed by a ghost. Spooky.",
        "farming_harvest": {
            "time": 150,
            "loot_table": (
                {
                    "chance": 1,
                    "loot": {"broken_sword": 1}
                },
            )
        }
    },

    "broken_sword": {
        "name": "Broken Sword",
        "description": "This once-pristine blade is now shattered at the hilt."
    },

    "cursed_tool": {
        "name": "Cursed Tool",
        "description": "A sharp knife with black fur around its guard. Ideal for exorcising curses!"
    },

}