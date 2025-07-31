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

HYPERLINK_URL = "https://i.pinimg.com/474x/49/c0/f0/49c0f0470a24e4562faf23210277a23a.jpg"

SPIN_OPTIONS = {
    50: 0.25,
    100: 0.35,
    200: 0.25,
    350: 0.1,
    500: 0.05
}
SPIN_ITEM_OPTIONS = {
    None: 0.7,
    "basic_pack": 0.3
}
SPIN_COOLDOWN = 25200

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
RARITY_COLOUR_KEY = {
    "common": 0xc9f2c9,
    "glowing": 0xb32bb6,
    "shining": 0xf7c01d,
    "mythical": 0xf54290
}
RARITY_DUST_CONVERSION = {
    "common": "green_dust",
    "glowing": "purple_dust",
    "shining": "shining_dust",
    "mythical": "mythical_dust"
}
CURRENCY_KEY = {
    "starpower": "Starpower",
    "green_dust": "Green Dust",
    "purple_dust": "Purple Dust",
    "gold_dust": "Gold Dust",
    "rainbow_dust": "Rainbow Dust"
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


# Functions
def blue(text: str) -> str:
    return f"[{text}]({HYPERLINK_URL})"