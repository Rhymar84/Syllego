from battles.battles import Character
import battles.passives as passives
import battles.actives as actives

FIGHTERS = {

    # Dragon Ball Z
    "DBZ-01": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Son Family"], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-02": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Vegeta Family"], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-03": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Son Family"], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-04": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-05": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Android"], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-06": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-07": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-08": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-09": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-10": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Vegeta Family"], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-11": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Android"], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-12": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Android"], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-13": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-14": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-15": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Vegeta Family"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-16": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Son Family"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },

    # Re:Zero
    "RZ-01": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-02": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-03": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Mathers Estate"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-04": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Mathers Estate"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-05": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Mathers Estate"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-06": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Royal Knight"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-07": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-08": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-09": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Mathers Estate"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-10": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Royal Knight"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-11": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-12": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Royal Knight"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-13": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-14": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Royal Knight"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-15": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": ["Assassin"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "RZ-16": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },


    # Attack on Titan
    "AOT-01": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": ["Titan Shifter", "Scout"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-02": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Survey Corps", "Ackerman"], "tags": ["Scout"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-03": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Ackerman"], "tags": ["Scout"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-04": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": ["Scout"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-05": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Marleyan Warrior"], "tags": ["Titan Shifter", "Scout"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-06": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Marleyan Warrior"], "tags": ["Titan Shifter"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-07": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Survey Corps"], "tags": ["Scout"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-08": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Survey Corps"], "tags": ["Scout"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-09": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Marleyan Warrior"], "tags": ["Titan Shifter", "Scout"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-10": {
        "passive_ability": passives.Safeguard, "active_ability": actives.JeanActive, "attribute": "blue", "chemistry_tags": [], "tags": ["Scout"],
        "health": 500, "attack": 80, "defense": 130, "magic_attack": 25, "magic_defense": 130, "speed": 86, "growth_style": "defensive"
    },
    "AOT-11": {
        "passive_ability": passives.SashaPassive, "active_ability": actives.SashaActive, "attribute": "green", "chemistry_tags": [], "tags": ["Scout"],
        "health": 420, "attack": 80, "defense": 100, "magic_attack": 50, "magic_defense": 90, "speed": 105, "growth_style": "technical"
    },
    "AOT-12": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-13": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-14": {
        "passive_ability": passives.ConniePassive, "active_ability": actives.LethalBlow, "attribute": "orange", "chemistry_tags": [], "tags": ["Scout"],
        "health": 435, "attack": 110, "defense": 80, "magic_attack": 10, "magic_defense": 70, "speed": 124, "growth_style": "balanced"
    },
    "AOT-15": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": ["Titan Shifter", "Scout"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "AOT-16": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Marleyan Warrior"], "tags": ["Titan Shifter", "Scout"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },


    # Jujutsu Kaisen
    "JJK-01": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Team Gojo"], "tags": ["Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-02": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": ["Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-03": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Team Gojo"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-04": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Team Gojo"], "tags": ["Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-05": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Team Gojo"], "tags": ["Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-06": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-07": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Disaster Curse"], "tags": ["Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-08": {
        "passive_ability": passives.NobaraPassive, "active_ability": actives.NobaraActive, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 460, "attack": 40, "defense": 110, "magic_attack": 70, "magic_defense": 120, "speed": 109, "growth_style": "balanced"
    },
    "JJK-09": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-10": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-11": {
        "passive_ability": passives.NanamiPassive, "active_ability": actives.NanamiActive, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 440, "attack": 100, "defense": 100, "magic_attack": 50, "magic_defense": 80, "speed": 97, "growth_style": "balanced"
    },
    "JJK-12": {
        "passive_ability": passives.MusterEnergy, "active_ability": actives.InumakiActive, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 470, "attack": 35, "defense": 90, "magic_attack": 105, "magic_defense": 90, "speed": 114, "growth_style": "balanced"
    },
    "JJK-13": {
        "passive_ability": passives.HeavenlyRestriction, "active_ability": actives.MakiActive, "attribute": "green", "chemistry_tags": [], "tags": [],
        "health": 485, "attack": 100, "defense": 70, "magic_attack": 0, "magic_defense": 70, "speed": 132, "growth_style": "offensive"
    },
    "JJK-14": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Disaster Curse"], "tags": ["Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-15": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },


    # One Punch Man
    "OPM-01": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-02": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-03": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-04": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-05": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-06": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-07": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-08": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-09": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-10": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-11": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-12": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-13": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "OPM-14": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },


    # My Hero Academia
    "MHA-01": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-02": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-03": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-04": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-05": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-06": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-07": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-08": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-09": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-10": {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-11": {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-12": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-13": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-14": {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-15": {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "MHA-16": {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },

    # Demon Slayer
    "DS-01": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-02": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-03": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-04": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-05": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-06": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-07": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-08": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-09": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-10": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-11": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-12": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-13": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-14": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-15": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DS-16": {
        "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },

    # Hunter x Hunter
    "HXH-01": {
        "passive_ability": passives.GonPassive, "active_ability": actives.GonActive, "attribute": "green", "chemistry_tags": [], "tags": [],
        "health": 470, "attack": 115, "defense": 100, "magic_attack": 60, "magic_defense": 95, "speed": 98, "growth_style": "balanced"
    },
    "HXH-02" : {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": ["Assassin"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-03" : {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-04" : {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-05" : {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-06" : {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-07" : {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Chimera Ant"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-08" : {
        "passive_ability": passives.PitouPassive, "active_ability": actives.DoctorBlythe, "attribute": "yellow", "chemistry_tags": ["Chimera Ant"], "tags": [],
        "health": 465, "attack": 100, "defense": 90, "magic_attack": 50, "magic_defense": 90, "speed": 87, "growth_style": "balanced"
    },
    "HXH-09" : {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-10" : {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-11" : {
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Morel School"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-12" : {
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-13" : {
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-14" : {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-15" : {
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Morel School"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "HXH-16" : {
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    

}