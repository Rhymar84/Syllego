# Bot IDs
TOKEN = "MTE0ODgzODQ3MjAyMzU1NjE0OA.GR1s4Z.eoYwM7QBVna1gfNKBkhuB9BiSOHEyWSJGsugog"
SERVER = 944337125149663282
BOT_ID = 1148838472023556148

# Channel IDs
DEBUG = 1148842953733853184


# Colours
ErrorColour = 0xe73232
StarShopColour = 0xfacf42
CHARACTER_EMBED_COLOUR = 0xb71010
INVENTORY_COLOUR = 0x03d3fc


# Keys
FRAME_KEY = {
    1: 'Common',
    2: 'Glowing',
    3: 'Shining'
}
RARITY_EMOJI_KEY = {
    3: '<:shining:1105901981299638343>',
    2: '<:glowing:1105937849976631417>',
    1: '<:common:1105901985024192642>'
}
CARD_RARITY_KEY = {
    'basic': '◽',
    'common': '⬜',
    'uncommon': '🔷',
    'rare': '🔶',
    'legendary': '💠',
    'imaginary': '🔳'
}
BUFF_STAT_KEY = {
    'dmg_inflicted': 'Damage Inflicted',
    'dmg_received': 'Damage Received',
    'spd': 'Speed'
}
COLOUR_EMOJI_KEY = {
    'red': '<:red:1340777064214822954>',
    'blue': '<:blue:1340777059743567992>',
    'green': '<:green:1340777061232545864>',
    'yellow': '<:yellow:1340777065590292530>',
    'orange': '<:orange:1340777062553747456>',
    'black': ''
}
SWITCH_CD_KEY = {
    10: '🕑',
    9: '🕒',
    8: '🕓',
    7: '🕔',
    6: '🕕',
    5: '🕖',
    4: '🕗',
    3: '🕘',
    2: '🕙',
    1: '🕚',
}
COLOUR_MATCHUPS = {
    'red': {'red': 1, 'blue': 0.5, 'green': 1.5, 'yellow': 1, 'orange': 1},
    'blue': {'red': 1.5, 'blue': 1, 'green': 1, 'yellow': 0.5, 'orange': 1},
    'green': {'red': 0.5, 'blue': 1, 'green': 1, 'yellow': 1, 'orange': 1.5},
    'yellow': {'red': 1, 'blue': 1.5, 'green': 1, 'yellow': 1, 'orange': 0.5},
    'orange': {'red': 1, 'blue': 1, 'green': 0.5, 'yellow': 1.5, 'orange': 1}
}

# Battle Parameters
MAX_HAND_SIZE = 5
DECISION_TIME = 120
SWITCH_COOLDOWN = 8
def round_energy(round:int) -> int:
    return 3 if round < 5 else 4 if round < 10 else 5