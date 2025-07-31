from battles.battles import Character
import battles.passives as passives
import battles.actives as actives

FIGHTERS = {

    # Dragon Ball Z

    "DBZ-01": { # Goku
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Son Family"], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-01-1": { # SSJ Goku
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Son Family"], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-01-2": { # SSJ2 Goku
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Son Family"], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-02": { # Vegeta
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Vegeta Family"], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-02-1": { # SSJ Vegeta
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Vegeta Family"], "tags": [""], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-02-2": { # Majin Vegeta
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Vegeta Family"], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-03": { # Gohan
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Son Family"], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-03-1": { # SSJ2 Gohan
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Son Family"], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-03-2": { # Ultimate Gohan
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Son Family"], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-04": { # Frieza
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-04-1": { # Final Form Frieza
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-05": { # Cell
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Android"], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-05-1": { # Perfect Cell
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Android"], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-06": { # Majin Buu
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-06-1": { # Super Buu
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-06-2": { # Kid Buu
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-07": { # Piccolo
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-08": { # Krillin
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-09": { # Tien
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Tien-Shin Dojo"], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-10": { # Trunks
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Vegeta Family"], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-10-1": { # Future Trunks
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Vegeta Family"], "tags": ["Hero", "Swordsman"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-11": { # Roshi
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": ["Hero"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-12": { # Nappa
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": ["Villain"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-13": { # Ginyu
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": ["Villain"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-14": { # Dabura
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": ["Villain"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-15": { # Videl
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-16": { # 16
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Android"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-17": { # 17
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Android"], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-18": { # 18
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Android"], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-19": { # 19
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Android"], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-20": { # 20
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Android"], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-21": { # Yamcha
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": ["Hero"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-22": { # Chaiotzu
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Tien-Shin Dojo"], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-23": { # Nail
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": ["Hero"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-24": { # Goten
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Son Family"], "tags": ["Hero"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-24-1": { # SSJ Goten
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Son Family"], "tags": ["Hero"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-25": { # Yajirobe
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": ["Hero", "Swordsman"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-26": { # Zarbon
        "passive_ability": None, "active_ability": None, "attribute": "", "chemistry_tags": [], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-27": { # Jeice
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-28": { # Recoome
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-29": { # Burter
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-30": { # Guldo
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": ["Villain"], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "DBZ-31": { # Hercule
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [], 
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },

    # Jujutsu Kaisen
    "JJK-01": { # Gojo
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Team Gojo"], "tags": ["Domain User", "Hero"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-02": { # Sukuna
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Team Sukuna"], "tags": ["Vilain", "Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-03": { # Yuji
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Team Gojo"], "tags": ["Hero"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-04": { # Yuta
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Team Gojo"], "tags": ["Domain User", "Hero", "Swordsman"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-05": { # Toji
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-06": { # Geto
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-07": { # Megumi
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Team Gojo"], "tags": ["Domain User", "Hero"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-08": { # Mahito
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Disaster Curse"], "tags": ["Vilain", "Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-09": { # Choso
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-10": { # Todo
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Jujutsu Kyoto"], "tags": ["Hero"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-11": { # Jogo
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Disaster Curse"], "tags": ["Vilain", "Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-12": { # Maki
        "passive_ability": passives.HeavenlyRestriction, "active_ability": actives.MakiActive, "attribute": "green", "chemistry_tags": ["Jujutsu Tokyo", "Zenin Sisters"], "tags": ["Swordsman"],
        "health": 485, "attack": 100, "defense": 70, "magic_attack": 0, "magic_defense": 70, "speed": 132, "growth_style": "offensive"
    },
    "JJK-13": { # Yuki
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "offensive"
    },
    "JJK-14": { # Kashimo
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "offensive"
    },
    "JJK-5": { # Hakari
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": ["Hero", "Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "offensive"
    },
    "JJK-16": { # Higuruma
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": ["Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "offensive"
    },
    "JJK-17": { # Nobara
        "passive_ability": passives.NobaraPassive, "active_ability": actives.NobaraActive, "attribute": "orange", "chemistry_tags": ["Jujutsu Tokyo"], "tags": ["Hero"],
        "health": 460, "attack": 40, "defense": 110, "magic_attack": 70, "magic_defense": 120, "speed": 109, "growth_style": "balanced"
    },
    "JJK-18": { # Inumaki
        "passive_ability": passives.MusterEnergy, "active_ability": actives.InumakiActive, "attribute": "yellow", "chemistry_tags": ["Jujutsu Tokyo"], "tags": ["Hero"],
        "health": 470, "attack": 35, "defense": 90, "magic_attack": 105, "magic_defense": 90, "speed": 114, "growth_style": "balanced"
    },
    "JJK-19": { # Panda
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Jujutsu Tokyo"], "tags": ["Hero"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-20": { # Miwa
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Jujutsu Kyoto"], "tags": ["Hero", "Swordsman"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-21": { # Mechamaru
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Jujutsu Kyoto"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-22": { # Momo
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Jujutsu Kyoto"], "tags": ["Hero"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-23": { # Hanami
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Disaster Curse"], "tags": ["Vilain", "Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-24": { # Dagon
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Disaster Curse"], "tags": ["Vilain", "Domain User"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-25": { # Kusakabe
        "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": ["Swordsman"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-26": { # Uruame
        "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Team Sukuna"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-27": { # Kenjaku
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": ["Vilain"],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-28": { # Mei Mei
        "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-29": { # Nanami
        "passive_ability": passives.NanamiPassive, "active_ability": actives.NanamiActive, "attribute": "red", "chemistry_tags": [], "tags": [],
        "health": 440, "attack": 100, "defense": 100, "magic_attack": 50, "magic_defense": 80, "speed": 97, "growth_style": "balanced"
    },
    "JJK-30": { # Miguel
        "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },
    "JJK-31": { # Mai
        "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Jujutsu Kyoto", "Zenin Sisters"], "tags": [],
        "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    },

    # # Re:Zero
    # "RZ-01": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-02": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-03": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Mathers Estate"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-04": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Mathers Estate"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-05": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Mathers Estate"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-06": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Royal Knight"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-07": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-08": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-09": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Mathers Estate"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-10": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Royal Knight"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-11": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-12": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": ["Royal Knight"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-13": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-14": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Royal Knight"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-15": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": ["Assassin"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "RZ-16": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },


    # # Attack on Titan
    # "AOT-01": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": ["Titan Shifter", "Scout"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-02": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Survey Corps", "Ackerman"], "tags": ["Scout"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-03": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Ackerman"], "tags": ["Scout"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-04": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": ["Scout"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-05": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Marleyan Warrior"], "tags": ["Titan Shifter", "Scout"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-06": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": ["Marleyan Warrior"], "tags": ["Titan Shifter"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-07": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Survey Corps"], "tags": ["Scout"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-08": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Survey Corps"], "tags": ["Scout"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-09": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Marleyan Warrior"], "tags": ["Titan Shifter", "Scout"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-10": {
    #     "passive_ability": passives.Safeguard, "active_ability": actives.JeanActive, "attribute": "blue", "chemistry_tags": [], "tags": ["Scout"],
    #     "health": 500, "attack": 80, "defense": 130, "magic_attack": 25, "magic_defense": 130, "speed": 86, "growth_style": "defensive"
    # },
    # "AOT-11": {
    #     "passive_ability": passives.SashaPassive, "active_ability": actives.SashaActive, "attribute": "green", "chemistry_tags": [], "tags": ["Scout"],
    #     "health": 420, "attack": 80, "defense": 100, "magic_attack": 50, "magic_defense": 90, "speed": 105, "growth_style": "technical"
    # },
    # "AOT-12": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-13": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-14": {
    #     "passive_ability": passives.ConniePassive, "active_ability": actives.LethalBlow, "attribute": "orange", "chemistry_tags": [], "tags": ["Scout"],
    #     "health": 435, "attack": 110, "defense": 80, "magic_attack": 10, "magic_defense": 70, "speed": 124, "growth_style": "balanced"
    # },
    # "AOT-15": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": ["Titan Shifter", "Scout"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "AOT-16": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": ["Marleyan Warrior"], "tags": ["Titan Shifter", "Scout"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },




    # # One Punch Man
    # "OPM-01": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-02": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-03": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-04": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-05": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-06": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-07": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-08": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-09": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-10": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-11": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-12": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-13": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "OPM-14": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },


    # # My Hero Academia
    # "MHA-01": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-02": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-03": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-04": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-05": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-06": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-07": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-08": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-09": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-10": {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-11": {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-12": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-13": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-14": {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-15": {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "MHA-16": {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },

    # # Demon Slayer
    # "DS-01": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-02": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-03": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-04": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-05": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-06": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-07": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-08": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-09": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-10": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-11": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-12": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-13": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-14": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-15": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "DS-16": {
    #     "passive_ability": None, "active_ability": None, "attribute": "black", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },

    # # Hunter x Hunter
    # "HXH-01": {
    #     "passive_ability": passives.GonPassive, "active_ability": actives.GonActive, "attribute": "green", "chemistry_tags": [], "tags": [],
    #     "health": 470, "attack": 115, "defense": 100, "magic_attack": 60, "magic_defense": 95, "speed": 98, "growth_style": "balanced"
    # },
    # "HXH-02" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": ["Assassin"],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-03" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-04" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-05" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-06" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-07" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Chimera Ant"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-08" : {
    #     "passive_ability": passives.PitouPassive, "active_ability": actives.DoctorBlythe, "attribute": "yellow", "chemistry_tags": ["Chimera Ant"], "tags": [],
    #     "health": 465, "attack": 100, "defense": 90, "magic_attack": 50, "magic_defense": 90, "speed": 87, "growth_style": "balanced"
    # },
    # "HXH-09" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-10" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-11" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "yellow", "chemistry_tags": ["Morel School"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-12" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "blue", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-13" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "orange", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-14" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-15" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "green", "chemistry_tags": ["Morel School"], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    # "HXH-16" : {
    #     "passive_ability": None, "active_ability": None, "attribute": "red", "chemistry_tags": [], "tags": [],
    #     "health": 0, "attack": 0, "defense": 0, "magic_attack": 0, "magic_defense": 0, "speed": 0, "growth_style": "balanced"
    # },
    

}