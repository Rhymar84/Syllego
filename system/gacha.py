import discord
import sqlite3
import random
import math
import datetime as dt
import asyncio
import aiosqlite
import config
from system.character_database import CHARACTERS, BaseChar, get_party_image
from battles.characters import FIGHTERS
from system.emoji import EMOJIS
from time import perf_counter
from PIL import Image
from io import BytesIO
from functools import lru_cache
from discord.utils import get
from discord.ui import Select, View
from dataclasses import dataclass, field

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

shining_colour = 0xf7c01d
glowing_colour = 0xb32bb6
common_colour = 0xc9f2c9

active_wishes = []

########################################################################################




class Wish():

    def __init__(self, interaction: discord.Interaction, character: BaseChar):
        self.interaction = interaction
        self.character = character
        self.is_dupe: bool = False

    async def start(self):
        user = self.interaction.user
        active_wishes.append(user)

        animation = await self.build_animation()
        embed, file = await self.create_embed(animation) 

        await self.interaction.followup.send(embed=embed, file=file)
        await asyncio.sleep(5) # Wait 5 seconds on the wish animation to build suspense
        active_wishes.pop(active_wishes.index(user))
        await self.reveal_character()
        await give_character(user, self.character.id)
        await add_starpower(self.interaction.user, -100)



    async def build_animation(self) -> dict:
        rarity = self.character.rarity

        hint_tables = {
            "common": {
                "sky": {"blue": 0.75, "purple": 0.2, "gold": 0.05, "green": 0},
                "star": {"none": 0.2, "shooting_star": 0.7, "comet": 0.1, "meteors": 0},
                "celestial": {"none": 0.4, "moon": 0.4, "constellation": 0.19, "planet": 0.01}
            },
            "glowing": {
                "sky": {"blue": 0.5, "purple": 0.35, "gold": 0.15, "green": 0 if self.is_dupe else 0.05},
                "star": {"none": 0, "shooting_star": 0.5, "comet": 0.5, "meteors": 0},
                "celestial": {"none": 0.2, "moon": 0.45, "constellation": 0.3, "planet": 0.05}
            },
            "shining": {
                "sky": {"blue": 0.25, "purple": 0.5, "gold": 0.25, "green": 0 if self.is_dupe else 0.2},
                "star": {"none": 0, "shooting_star": 0.3, "comet": 0.45, "meteors": 0.25},
                "celestial": {"none": 0.1, "moon": 0.25, "constellation": 0.45, "planet": 0.3}
            },
            "mythical": {
                "sky": {"blue": 0.1, "purple": 0.3, "gold": 0.6, "green": 0 if self.is_dupe else 0.35},
                "star": {"none": 0, "shooting_star": 0.1, "comet": 0.4, "meteors": 0.5},
                "celestial": {"none": 0, "moon": 0.2, "constellation": 0.3, "planet": 0.5}
            }
        }

        animation = {}
        for hint_type, options in hint_tables[rarity].items():
            animation[hint_type] = random.choices(list(options.keys()), list(options.values()))[0]

        return animation

    async def create_embed(self, animation: dict):

        embed = discord.Embed(title=f"{self.interaction.user.display_name} is making a wish...", color=0xe4ede6)
        embed.set_author(name = self.interaction.user.display_name, icon_url=f'{self.interaction.user.display_avatar}')

        base: Image.Image = Image.open(f"Assets/Wishes/sky_{animation['sky']}.png")

        if animation['star'] != "none":
            star = Image.open(f"Assets/Wishes/{animation['star']}.png")
            base.paste(star, (20, 35), star)

        if animation['celestial'] != "none":
            celestial = Image.open(f"Assets/Wishes/{animation['celestial']}.png")
            base.paste(celestial, (355, 130), celestial)

        with BytesIO() as image_binary:
            party_image = base.convert('RGB')
            party_image.save(image_binary, 'JPEG')
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename='wish.jpeg')
            embed.set_image(url='attachment://wish.jpeg')


        return embed, file
    
    async def reveal_character(self):

        embed = await self.character.display(1, config.RARITY_COLOUR_KEY[self.character.rarity], is_new=not self.is_dupe)
        if self.is_dupe:
            await self.display_dust_conversion(embed)

        extension = "gif" if self.character.rarity == "mythical" else "jpg"

        portrait = discord.File(f'Assets/Portraits/{self.character.id}.{extension}', filename=f'portrait.{extension}')
        embed.set_image(url=f'attachment://portrait.{extension}')
        embed.set_author(name=f'{self.interaction.user.display_name}', icon_url=f'{self.interaction.user.display_avatar}')
    
        await self.interaction.edit_original_response(embed=embed, attachments=[portrait])

    async def display_dust_conversion(self, embed: discord.Embed):
        match self.character.rarity:
            case "common":
                currency = "Green Dust"
            case "glowing": 
                currency = "Purple Dust"
            case "shining":
                currency = "Gold Dust"
            case "mythical":
                currency = "Rainbow Dust"
        
        embed.description = f"{self.character.name} was converted into 10 **{currency}**."



@dataclass
class PartyObject():
    member: discord.Member
    party: list[dict] = field(default_factory=list, init=False)

    def __iter__(self):
        return iter(self.party)

    async def set_party(self):
        party = await get_party(self.member)
        party = [{'character': CHARACTERS[x], 'level': await get_character_level(self.member, x), 'chemistry': 0} if x in CHARACTERS.keys() else {'character': None, 'level': 0} for x in party]

        party[0]['pos'] = (133, 133)
        party[1]['pos'] = (789, 133)
        party[2]['pos'] = (1444, 133)
        party[3]['pos'] = (132, 888)
        party[4]['pos'] = (789, 888)
        party[5]['pos'] = (1444, 888)

        party = [d for d in party if d['character'] is not None]

        self.party = party

    async def calculate_chemistry(self):
        for fighter in self.party:
            character: BaseChar = fighter['character']
            
            series_match = [x for x in self.party if x['character'].series == character.series]
            colour_match = [x for x in self.party if FIGHTERS[x['character'].id]['attribute'] == FIGHTERS[character.id]['attribute']]
            tag_match = [x for x in self.party if set(FIGHTERS[x['character'].id]['chemistry_tags']) & set(FIGHTERS[character.id]['chemistry_tags'])] 

            series_chemistry = min(int(len(series_match) / 3), 2)
            colour_chemistry = int(len(colour_match) / 2)
            tag_chemistry = int(len(tag_match) / 2)

            fighter['chemistry'] = min(sum([series_chemistry, colour_chemistry, tag_chemistry]), 3)

    async def display(self) -> tuple[discord.Embed, discord.File]:

        base: Image.Image = Image.open('Assets/Party Themes/Base.png')

        for character in self.party:
            
            char = get_party_image(character['character'], character['level'], False)
            level = Image.open(f"Assets/Level {character['level']}.png")

            base.paste(char, (character['pos']))
            base.paste(level, (character['pos']), level)


        embed = discord.Embed(
            title=f'Team Chemistry: {sum([x["chemistry"] for x in self.party])}/18',
            color = 0xf69337
        )

        with BytesIO() as image_binary:
            party_image = base.convert('RGB')
            party_image.save(image_binary, 'JPEG')
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename='party.jpeg')
            embed.set_image(url='attachment://party.jpeg')
            embed.set_author(name=f'{self.member.display_name}\'s Party', icon_url=f'{self.member.display_avatar}')
            embed.set_footer(text=f'Use /party add to edit a party slot.')

        return embed, file



########################################################################################

async def seocnds_since_last_spin(member: discord.Member) -> int:

    # Get number of seconds since last spin
    last_spin = await check_last_spin(member)
    now = dt.datetime.now()
    difference = now - last_spin
    seconds = difference.total_seconds()

    return seconds


async def check_last_spin(member: discord.Member) -> dt.datetime:

    async with aiosqlite.connect("databases/gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT last_spin FROM misc WHERE user_id = {member.id}')
            last_update = await cursor.fetchone()

    if not last_update or not last_update[0]:
        if not last_update:
            await insert_user_record("gacha", "misc", member)
        last_update = ('24-09-2003 00:00',)

    return dt.datetime.strptime(last_update[0], "%d-%m-%Y %H:%M")

async def set_last_spin(member: discord.Member, time: dt.datetime):

    async with aiosqlite.connect("databases/gacha.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE misc SET last_spin = ? WHERE user_id = ?')
            val = (time.strftime("%d-%m-%Y %H:%M"), member.id)
            await cursor.execute(sql, val)

        await db.commit()
    


async def set_starpower(member: discord.Member, amount: int):

    async with aiosqlite.connect("databases/gacha.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE misc SET starpower = ? WHERE user_id = ?')
            val = (amount, member.id)
            await cursor.execute(sql, val)

        await db.commit()



async def get_starpower(member: discord.Member) -> int:

    async with aiosqlite.connect("databases/eco.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT starpower FROM currencies WHERE user_id = {member.id}')
            starpower = await cursor.fetchone()
    
    return starpower[0] if starpower is not None and starpower[0] is not None else 0


async def add_starpower(member: discord.Member, amount: int) -> int:

    current_starpower = await get_starpower(member)
    new_starpower = max(current_starpower + amount, 0)

    async with aiosqlite.connect("databases/eco.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE currencies SET starpower = ? WHERE user_id = ?')
            val = (new_starpower, member.id)
            await cursor.execute(sql, val)

        await db.commit()

    return new_starpower


async def get_currency(member: discord.Member, currency: str) -> int:

    async with aiosqlite.connect("databases/eco.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT {currency} FROM currencies WHERE user_id = {member.id}')
            value = await cursor.fetchone()
    
    return value[0] if value is not None and value[0] is not None else 0


async def add_currency(member: discord.Member, currency: str, amount: int) -> int:

    current_value = await get_currency(member, currency)
    new_value = max(current_value + amount, 0)

    async with aiosqlite.connect("databases/eco.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE currencies SET {currency} = ? WHERE user_id = ?')
            val = (new_value, member.id)
            await cursor.execute(sql, val)

        await db.commit()

    return new_value



async def get_collection(member: discord.Member, format: str='images') -> list:

    async with aiosqlite.connect("databases/gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT * FROM collection WHERE user_id = {member.id}')
            levels = await cursor.fetchall()

            await cursor.execute('PRAGMA table_info(collection)')
            ids = await cursor.fetchall()

    if not levels:
        return []
    
    levels = levels[0]
    ids = [x[1] for x in ids]

    collection = list(zip(ids, levels))
    # Removing (user_id and its column)
    collection.pop(0)

    collection = [character for character in collection if character[1] is not None]
    collection = sorted(collection, key=lambda x: get_rarity_sort(x[0]), reverse=True)
    
    if format == 'names':
        return [CHARACTERS[character[0]].name for character in collection]
    
    if format == 'objects':
        return [{'character': CHARACTERS[character[0]], 'level': character[1]} for character in collection]

    if format == 'rarities':
        return [f'{EMOJIS[CHARACTERS[character[0]].rarity]} {CHARACTERS[character[0]].name} **{int(await get_character_level(member, character[0]))}**⭐' for character in collection]
    
    embeds = []
    files = []

    for index, character in enumerate(collection):
        id = character[0]
        rarity = CHARACTERS[id].rarity
        level = character[1]

        embed: discord.Embed = await CHARACTERS[id].display(level, 0xb71010)

        footer = str(embed.footer.text)
        footer += f'\n({index+1}/{len(collection)})'
        embed.set_footer(text=f'{footer}')
        embed.set_author(name=f'{member.display_name}', icon_url=f'{member.display_avatar}')
        
        embeds.append(embed)
        files.append(f"{id}.{'gif' if rarity == 'mythical' else 'jpg'}")

    return embeds, files



async def verify_collection(member: discord.Member, insert_if_missing: bool = True):
    async with aiosqlite.connect("databases/gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT * FROM collection WHERE user_id = {member.id}')
            fetched = await cursor.fetchall()
    
    try:
        fetched = fetched[0]
    except:
        if insert_if_missing:
            async with aiosqlite.connect("databases/gacha.sqlite") as db:
                async with db.cursor() as cursor:
                    await cursor.execute(f'INSERT INTO collection (user_id) VALUES({member.id})')
        else:
            return False
        
    return True


async def do_wish(interaction: discord.Interaction):


    pull = do_pull()

    wish = Wish(interaction, pull)
    if await get_character_level(interaction.user, pull.id) > 0:
        wish.is_dupe = True

    await wish.start()

    

def do_pull() -> BaseChar:

    # Pull odds
    mythical_rate = 0.001
    shining_rate = 0.025
    glowing_rate = 0.33

    roll = random.random()
    if roll <= mythical_rate:
        rarity = "mythical"
    elif roll <= shining_rate:
        rarity = "shining"
    elif roll <= glowing_rate:
        rarity = "glowing"
    else:
        rarity = "common"

    pool = get_pool(rarity)
    return random.choice(pool)



async def do_spin(interaction: discord.Interaction):

    reward = random.choices(list(config.SPIN_OPTIONS.keys()), list(config.SPIN_OPTIONS.values()))[0]
    item_reward = random.choices(list(config.SPIN_ITEM_OPTIONS.keys()), list(config.SPIN_ITEM_OPTIONS.values()))[0]

    embed = discord.Embed(description=f"You have obtained **{reward}** starpower!", color=0x0ffc03)
    embed.set_thumbnail(url="https://media.tenor.com/BBhMdyHEhMMAAAAM/spinning.gif")
    embed.set_author(name = interaction.user.display_name, icon_url=f'{interaction.user.display_avatar}')
    embed.set_footer(text=f"You can spin again in 8 hours.")

    if item_reward:
        from system.items import ITEMS
        embed.description += f"\nYou have obtained a{'n' if ITEMS[item_reward]['name'][0] in ['a','e','i','o','u'] else ''} **{ITEMS[item_reward]['name']}**!"
        await gain_item(interaction.user, item_reward, 1)

    await add_starpower(interaction.user, reward)
    await set_last_spin(interaction.user, dt.datetime.now())
    await interaction.followup.send(embed=embed)



async def get_series_progress(member: discord.Member, series: str) -> dict:

    char_list = [x for x in CHARACTERS.values() if x.series == series]
    char_list = {x: 0 for x in sorted(char_list, key=lambda x: get_rarity_sort(x.id), reverse=True)}

    collected: list[dict] = await get_collection(member, format='objects')
    collected = [x for x in collected if x['character'].series == series]
    
    for character in collected:
        char_list[character['character']] = character['level']
    
    return char_list



def get_rarity(character: str):
    return CHARACTERS[character].rarity

def get_rarity_sort(character: str):
    rarity = get_rarity(character)

    match rarity:
        case "common":
            return 0
        case "glowing":
            return 1
        case "shining":
            return 2
        case "mythical":
            return 3

def get_rarity_emoji(rarity: int):
    return EMOJIS[rarity]
    
def get_rarity_colour(rarity: int):

    if rarity == "shining":
        return shining_colour
    
    if rarity == "glowing":
        return glowing_colour
    
    if rarity == "common":
        return common_colour

async def get_character_level(member: discord.Member, id: str):

    if id is None:
        return 0

    async with aiosqlite.connect("databases/gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT "{id}" FROM collection WHERE user_id = {member.id}')
            level = await cursor.fetchone()


    level = level[0] if level is not None else 0
    
    if level is None:
        level = 0
    
    level = round(level, 1)

    return level


async def give_character(member: discord.Member, character: str) -> float:

    if await get_character_level(member, character) > 0:
        currency = config.RARITY_DUST_CONVERSION[CHARACTERS[character].rarity]
        await add_currency(member, currency, 10)
        return

    async with aiosqlite.connect("databases/gacha.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE collection SET "{character}" = 1 WHERE user_id = ?')
            val = (member.id,)
            await cursor.execute(sql, val)

        await db.commit()


async def get_party(member: discord.Member):

    async with aiosqlite.connect("databases/party.sqlite") as db:
        async with db.cursor() as cursor:

            await cursor.execute(f'SELECT slot1, slot2, slot3, slot4, slot5, slot6 FROM party1 WHERE user_id = {member.id}')
            party = await cursor.fetchall()

    try:
        party = party[0]
    except:
        party = None
    
    return party



async def edit_slot(member: discord.Member, slot: str, character: str):

    slot_index = slot[4::4]

    async with aiosqlite.connect("databases/party.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT slot1, slot2, slot3, slot4, slot5, slot6 FROM party1 WHERE user_id = {member.id}')
            party = await cursor.fetchall()
            party = party[0]

            for index, char in enumerate(party):
                if character == char:
                    sql = (f'UPDATE party1 SET slot{index+1} = null WHERE user_id = ?')
                    val = (member.id,)
                    await cursor.execute(sql, val) 


            sql = (f'UPDATE party1 SET {slot} = ? WHERE user_id = ?')
            val = (character, member.id)
            await cursor.execute(sql, val)
        
        await db.commit()

    # if int(slot_index) in [1, 2, 3]:
    #     moves = await get_moves(character)
    #     moves = moves[:4]
    #     moves = ', '.join(moves)

    #     sql = (f'UPDATE party SET {f"moves{slot_index}"} = ? WHERE user_id = ?')
    #     val = (moves, member.id)
    #     cursor.execute(sql, val)


async def clearParty(member: discord.Member):

    async with aiosqlite.connect("databases/party.sqlite") as db:
        async with db.cursor() as cursor:

            for index in range(6):
                sql = (f'UPDATE party1 SET slot{index+1} = null WHERE user_id = ?')
                val = (member.id,)
                await cursor.execute(sql, val) 

        await db.commit()




def get_pool(rarity: str) -> list[BaseChar]:
    return [character for character in CHARACTERS.values() if character.rarity == rarity]

async def get_jars(member: discord.Member, insert_if_none: bool=False):
    
    async with aiosqlite.connect("databases/eco.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT jars FROM currencies WHERE user_id = {member.id}')
            jars = await cursor.fetchone()

    if not jars:
        if insert_if_none:
            await insert_user_record('eco', 'currencies', member)
        jars = [0]
        
    return 0 if jars[0] is None else jars[0]
            

async def gain_jars(member: discord.Member, amount: int):

    current_jars = await get_jars(member, True)

    async with aiosqlite.connect("databases/eco.sqlite") as db:
        async with db.cursor() as cursor:
            sql = ('UPDATE currencies SET jars = ? WHERE user_id = ?')
            val = (current_jars + amount, member.id)
            await cursor.execute(sql, val)
            await db.commit()

async def get_item_count(member: discord.Member, item_id: str):

    async with aiosqlite.connect("databases/eco.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT {item_id} FROM inventory WHERE user_id = {member.id}')
            count = await cursor.fetchone()

    if not count:
        await insert_user_record('eco', 'inventory', member)
        count = [0]

    return 0 if count[0] is None else count[0]

async def gain_item(member: discord.Member, item_id: str, amount: int):

    current_count = await get_item_count(member, item_id)

    async with aiosqlite.connect("databases/eco.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE inventory SET {item_id} = ? WHERE user_id = ?')
            val = (current_count + amount, member.id)
            await cursor.execute(sql, val)
            await db.commit()

async def redeem_item(member: discord.Member, item_id: str):
    from system.items import ITEMS

    item = ITEMS[item_id]
    func, kwargs = item['redeem'].values()

    response = await func(member, **kwargs)
    await gain_item(member, item_id, -1)
    return response

def get_item_id(item: str) -> str:
    from system.items import ITEMS
    for key, value in ITEMS.items():
        if value['name'] == item:
            return key
        
async def get_inventory(member: discord.Member):
    from system.items import ITEMS
    inventory = {}

    for item_id in ITEMS.keys():
        count = await get_item_count(member, item_id)
        if count > 0:
            inventory[item_id] = count

    return inventory

async def random_card(pack: str = 'base') -> str:
    from battles.cards import Cards

    uncommon_chance = 0.25
    rare_chance = 0.08
    legendary_chance = 0.02

    rarity = random.random()
    if rarity <= legendary_chance:
        rarity = 'legendary'
    elif rarity <= rare_chance + legendary_chance:
        rarity = 'rare'
    elif rarity <= uncommon_chance + rare_chance + legendary_chance:
        rarity = 'uncommon'
    else:
        rarity = 'common'

    pool = [card.name for card in Cards if card.value.rarity == rarity and card.value.card_set == pack]
    return random.choice(pool)


async def open_pack(member: discord.Member, pack: str, count: int):
    from battles.cards import Cards

    pulls = []
    for _ in range(count):
        pulls.append(await random_card(pack))
    
    embed = discord.Embed(title=f'{pack.title()} Pack', color=0xf5ed07, description='\n'.join([f"- {config.CARD_RARITY_KEY[Cards[card].value.rarity]} {Cards[card].value.name}" for card in pulls]))
    embed.set_author(name=f'{member.display_name}', icon_url=f'{member.display_avatar}')

    for pull in pulls:
        await gain_card(member, pull)

    return embed

async def get_card_count(member: discord.Member, card: str):
    
    async with aiosqlite.connect("databases/gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT {card} FROM cards WHERE user_id = {member.id}')
            count = await cursor.fetchone()

    if not count:
        await insert_user_record('gacha', 'cards', member)
        return 0

    return 0 if count[0] is None else count[0]

async def gain_card(member: discord.Member, card: str):

    current_count = await get_card_count(member, card)

    async with aiosqlite.connect("databases/gacha.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE cards SET {card} = ? WHERE user_id = ?')
            val = (current_count + 1, member.id)
            await cursor.execute(sql, val)
            await db.commit()


async def get_binder(member: discord.Member, sort: str = 'rarity') -> dict:

    async with aiosqlite.connect("databases/gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT * FROM cards WHERE user_id = {member.id}')
            copies = await cursor.fetchone()

            await cursor.execute('PRAGMA table_info(cards)')
            card_ids = await cursor.fetchall()

    if not copies:
        return {}
    
    card_ids = [x[1].upper() for x in card_ids]

    binder = list(zip(card_ids, copies))
    # Removing (user_id and its column)
    binder.pop(0)

    binder = [card for card in binder if card[1]]

    match sort:
        case 'rarity':
            binder.sort(key= lambda x: (binder_sort_rarity(x), x[0]))
        case 'alphabetical':
            binder = sorted(binder, key=lambda x: x[0])
        case 'copies':
            binder.sort(key = lambda x: (x[1] * -1, binder_sort_rarity(x), x[0]))
        case _:
            binder.sort(key= lambda x: (binder_sort_rarity(x), x[0]))
    
    return {x[0]: x[1] for x in binder}





def binder_sort_rarity(card: tuple) -> int:
    from battles.cards import Cards
    card: str = card[0]

    rarity = Cards[card].value.rarity

    match rarity:
        case 'basic':
            return 4
        case 'common':
            return 3
        case 'uncommon':
            return 2
        case 'rare':
            return 1
        case 'legendary':
            return 0
        case _:
            return 4


async def get_daily_missions(member: discord.Member) -> dict:

    async with aiosqlite.connect("databases/missions.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT * FROM daily WHERE user_id = {member.id}')
            missions = await cursor.fetchone()

            await cursor.execute('PRAGMA table_info(daily)')
            mission_ids = await cursor.fetchall()

    ids = [x[1] for x in mission_ids][1:]

    if not missions:
        await insert_user_record('missions', 'daily', member)
        return {id: False for id in ids}

    missions = missions[1:]

    return {id: bool(mission) for id, mission in zip(ids, missions)}


async def get_item_obtaining_string(item: str) -> str:
    import system.farming as farming
    from system.items import ITEMS

    farming_sources = await farming.get_item_farming_obtaining(item)

    if not farming_sources:
        return ''
    
    text = f"\n\n**Obtaining**\n"
    farming_sources_strings = [f"- **{config.blue(ITEMS[x['input_item']]['name'])}** {farming.FARMING_MODE_MAP[x['mode']]}➡️ **{config.blue(ITEMS[item]['name'])}** x**{x['output_quantity']}**" for x in farming_sources]

    text += "\n".join(farming_sources_strings)

    return text
    
async def get_settings(member: discord.Member) -> dict:
    return {"farming_dms": True, "refinery_dms": True}

async def insert_user_record(database: str, table: str, member: discord.Member):
    async with aiosqlite.connect(f"databases/{database}.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'INSERT INTO {table}(user_id) VALUES ({member.id})')
        await db.commit()