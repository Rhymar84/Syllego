import discord
import sqlite3
import random
import bot
import math
import datetime as dt
import asyncio
import aiosqlite
from character_database import CHARACTERS, BaseChar
from battles.characters import FIGHTERS
from time import perf_counter
from PIL import Image
from io import BytesIO
from functools import lru_cache
from discord.utils import get
from discord.ui import Select, View
from config import TOKEN, ErrorColour
from config import SERVER
from config import DEBUG
from dataclasses import dataclass, field

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

shining_colour = 0xf7c01d
glowing_colour = 0xb32bb6
common_colour = 0xc9f2c9

shining_emoji = '<:shining:1105901981299638343>'
glowing_emoji = '<:glowing:1105937849976631417>'
common_emoji = '<:common:1105901985024192642>'
special_emoji = '<:special:1107411921201799238>'


#######################################################################################

common_characters = ['Asahina Nazuna', 'Sakura Airi', 'Ibuki Mio', 'Ike Kanji', 'Hasebe Haruka', 'Miyake Akito', 'Yukimura Keisei', 'Satō Maya', 'Shinohara Satsuki', 'Sotomura Hideo', 'Amikura Mako', 'Shiranami Chihiro', 'Himeno Yuki', 'Sakagami Kazuma', 'Mashima Tomonari', 'Totsuka Yahiko', 'Kamuro Masumi', 'Hashimoto Masayoshi', 'Kitō Hayato', 'Yamamura Miki', 'Tachibana Akane', 'Shibata Sō', 'Ishizaki Daichi', 'Tsubaki Sakurako', 'Yamauchi Haruki']
glowing_characters = ['Karuizawa Kei', 'Hirata Yōsuke', 'Sudō Ken', 'Chabashira Sae', 'Kanzaki Ryuji', 'Hoshinomiya Chie', 'Yamada Albert', 'Shiina Hiyori', 'Hōsen Kazuomi', 'Nanase Tsubasa', 'Matsushita Chiaki', 'Kaneda Satoru', 'Wang Meiyu', 'Utomiya Riku', 'Ishigami Kyō', 'Katsuragi Kōhei', 'Ayanokōji Atsuomi', 'Sakayanagi Narumori', 'Tsukishiro Tokinari', 'False Ayanokōji Kiyotaka', 'Shizuku']
shining_characters = ['Ayanokōji Kiyotaka', 'Horikita Suzune', 'Ichinose Honami', 'Sakayanagi Arisu', 'Kushida Kikyō', 'Ryūen Kakeru', 'Horikita Manabu', 'Kōenji Rokusuke', 'Yagami Takuya', 'Nagumo Miyabi', 'Amasawa Ichika', 'Kiryūin Fūka', 'True Kushida Kikyō', 'Delinquent Ishizaki Daichi']
special_characters = ['Shiba Katsunori', 'Shiro', 'Perfect Kōenji Rokusuke']

POOL_BASE_COMMON = ['Asahina Nazuna', 'Sakura Airi', 'Ibuki Mio', 'Ike Kanji', 'Hasebe Haruka', 'Miyake Akito', 'Yukimura Keisei', 'Satō Maya', 'Shinohara Satsuki', 'Sotomura Hideo', 'Amikura Mako', 'Shiranami Chihiro', 'Himeno Yuki', 'Sakagami Kazuma', 'Mashima Tomonari', 'Totsuka Yahiko', 'Kamuro Masumi', 'Hashimoto Masayoshi', 'Kitō Hayato', 'Yamamura Miki', 'Tachibana Akane', 'Shibata Sō', 'Ishizaki Daichi', 'Tsubaki Sakurako', 'Yamauchi Haruki']
POOL_BASE_GLOWING = ['Karuizawa Kei', 'Hirata Yōsuke', 'Sudō Ken', 'Chabashira Sae', 'Kanzaki Ryuji', 'Hoshinomiya Chie', 'Yamada Albert', 'Shiina Hiyori', 'Hōsen Kazuomi', 'Nanase Tsubasa', 'Matsushita Chiaki', 'Kaneda Satoru', 'Wang Meiyu', 'Utomiya Riku', 'Ishigami Kyō', 'Katsuragi Kōhei', 'Ayanokōji Atsuomi', 'Sakayanagi Narumori', 'Tsukishiro Tokinari']
POOL_BASE_SHINING = ['Ayanokōji Kiyotaka', 'Horikita Suzune', 'Ichinose Honami', 'Sakayanagi Arisu', 'Kushida Kikyō', 'Ryūen Kakeru', 'Horikita Manabu', 'Kōenji Rokusuke', 'Yagami Takuya', 'Nagumo Miyabi', 'Amasawa Ichika', 'Kiryūin Fūka']


########################################################################################



class Spin(discord.ui.View):
    def __init__(self, original_interaction: discord.Interaction, character: BaseChar):
        super().__init__()
        self.original_interaction = original_interaction
        self.character = character
        self.character_level = 0
        self.is_new = False
        self.timeout = 180

    @discord.ui.button(emoji='<:claim:1149647515063439380>', style=discord.ButtonStyle.grey)
    async def summon_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        if interaction.user != self.original_interaction.user:
            embed = discord.Embed(title='Error', description='This is not your spin!', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        starpower = await bot.get_starpower(interaction.user)
        
        if starpower < 50:
            embed = discord.Embed(title='Not Enough Starpower :(', description=f'Your summons cost 50% Starpower, but you only have **{starpower}%**. Starpower recharges at a rate of 20%/h.', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        

        char_level = await give_character(interaction.user, self.character.id)
        await bot.set_starpower(interaction.user, starpower - 50)
        await bot.set_last_starpower_update(interaction.user, dt.datetime.now())

        self.character_level = char_level
        if char_level == 1:
            self.is_new = True

        await self.claim(interaction)

    

    async def create(self):

        self.character_level = await get_character_level(self.original_interaction.user, self.character.id)
        if self.character_level >= 5:
            self.remove_item(self.summon_button)
            self.add_item(TakeJarButton(self.original_interaction, self.character, self.character_level))

        embed = await self.character.display(self.character_level, get_rarity_colour(self.character.rarity))

        portrait = discord.File(f'Assets/Portraits/{self.character.id}.jpg', filename='portrait.jpg')
        embed.set_image(url=f'attachment://portrait.jpg')
        embed.set_author(name=f'{self.original_interaction.user.display_name}', icon_url=f'{self.original_interaction.user.display_avatar}')
        
        remaining_spins = await bot.get_remaining_spins(self.original_interaction.user)
        await bot.set_remaining_spins(self.original_interaction.user, remaining_spins - 1)
        await self.original_interaction.response.send_message(embed=embed, file=portrait, view=self)



    async def claim(self, interaction: discord.Interaction):

        embed = await self.character.display(self.character_level, 0xb71010, self.is_new)

        portrait = discord.File(f'Assets/Portraits/{self.character.id}.jpg', filename='portrait.jpg')
        embed.set_image(url=f'attachment://portrait.jpg')
        embed.set_author(name=f'{interaction.user.display_name}', icon_url=f'{interaction.user.display_avatar}')

        await interaction.response.edit_message(embed=embed, attachments=[portrait], view=None)

        channel = interaction.channel
        await channel.send(f'**{interaction.user.display_name}** made an offering to the stars, and was gifted **{self.character.name}**.')



class TakeJarButton(discord.ui.Button):
    
    def __init__(self, original_interaction: discord.Interaction, character: BaseChar, level: int, *, style = discord.ButtonStyle.grey, label = None, disabled = False, custom_id = None, url = None, emoji = None, row = None, sku_id = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji='✨', row=row, sku_id=sku_id)
        self.original_interaction = original_interaction
        self.character = character
        self.character_level = level

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.original_interaction.user:
            return True
        await interaction.response.send_message(ephemeral=True, embed=discord.Embed(description='This is not your spin!', color=ErrorColour))
        return False
    
    async def callback(self, interaction: discord.Interaction):

        starpower = await bot.get_starpower(interaction.user)
        
        if starpower < 50:
            embed = discord.Embed(title='Not Enough Starpower :(', description=f'Your summons cost 50% Starpower, but you only have **{starpower}%**. Starpower recharges at a rate of 20%/h.', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await bot.set_starpower(interaction.user, starpower - 50)
        await bot.set_last_starpower_update(interaction.user, dt.datetime.now())

        jars_gained = 1 if self.character.rarity == 1 else 3 if self.character.rarity == 2 else 10
        await gain_jars(interaction.user, jars_gained)

        embed = await self.character.display(self.character_level, 0x710ddb)

        portrait = discord.File(f'Assets/Portraits/{self.character.id}.jpg', filename='portrait.jpg')
        embed.set_image(url=f'attachment://portrait.jpg')
        embed.set_author(name=f'{interaction.user.display_name}', icon_url=f'{interaction.user.display_avatar}')

        await interaction.response.edit_message(embed=embed, attachments=[portrait], view=None)

        channel = interaction.channel
        await channel.send(f'**{interaction.user.display_name}** made an offering to the stars, and captured **{jars_gained}** Star in a Jar{"s"[:(jars_gained)^1]}.')



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
            
            try:
                char = Image.open(f"Assets/Party/{character['character'].id}.png")
            except FileNotFoundError:
                char = Image.open(f"Assets/missing_asset.png")

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
            embed.set_footer(text=f'Use /add to edit a party slot.')

        return embed, file



########################################################################################

    


async def get_collection(member: discord.Member, format: str='images') -> list:

    async with aiosqlite.connect("gacha.sqlite") as db:
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
    collection = sorted(collection, key=lambda x: get_rarity(x[0]), reverse=True)
    
    if format == 'names':
        return [CHARACTERS[character[0]].name for character in collection]
    
    if format == 'objects':
        return [{'character': CHARACTERS[character[0]], 'level': character[1]} for character in collection]

    if format == 'rarities':
        return [f'{globals()[f"{get_rarity(character[0])}_emoji"]} {CHARACTERS[character[0]].name} **{int(await get_character_level(member, character[0]))}**⭐' for character in collection]
    
    embeds = []
    files = []

    for index, character in enumerate(collection):
        id = character[0]
        level = character[1]

        embed: discord.Embed = await CHARACTERS[id].display(level, 0xb71010)

        footer = str(embed.footer.text)
        footer += f'\n({index+1}/{len(collection)})'
        embed.set_footer(text=f'{footer}')
        embed.set_author(name=f'{member.display_name}', icon_url=f'{member.display_avatar}')
        
        embeds.append(embed)
        files.append(id)

    return embeds, files



async def verify_collection(member: discord.Member, insert_if_missing: bool = True):
    async with aiosqlite.connect("gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT * FROM collection WHERE user_id = {member.id}')
            fetched = await cursor.fetchall()
    
    try:
        fetched = fetched[0]
    except:
        if insert_if_missing:
            async with aiosqlite.connect("gacha.sqlite") as db:
                async with db.cursor() as cursor:
                    await cursor.execute(f'INSERT INTO collection (user_id) VALUES({member.id})')
        else:
            return False
        
    return True




async def do_spin(member: discord.Member):
    

    shining_chance = 2
    glowing_chance = 10
    
    # 10% chance to guarantee a character from wished series 
    wish = await bot.get_wish(member)
    if wish is not None:
        wish_chance = 10
        wish_roll = random.randint(1, 100)
        if wish_roll > wish_chance:
            wish = None

    roll = random.randint(1, 100)

    if roll <= shining_chance:
        rarity = 3
    elif roll <= shining_chance + glowing_chance:
        rarity = 2
    else:
        rarity = 1

    pool = get_pool(rarity, wish)
    pull = random.choice(pool)

    return pull






async def get_series_progress(member: discord.Member, series: str) -> dict:

    char_list = [x for x in CHARACTERS.values() if x.series == series]
    char_list = {x: 0 for x in sorted(char_list, key=lambda x: get_rarity(x.id), reverse=True)}

    collected: list[dict] = await get_collection(member, format='objects')
    collected = [x for x in collected if x['character'].series == series]
    
    for character in collected:
        char_list[character['character']] = character['level']
    
    return char_list



def get_rarity(character: str):
    rarity = CHARACTERS[character].rarity
    return 'shining' if rarity == 3 else 'glowing' if rarity == 2 else 'common'

def get_rarity_emoji(rarity: int):

    if rarity == 3:
        return shining_emoji
    
    if rarity == 2:
        return glowing_emoji
    
    if rarity == 1:
        return common_emoji
    
def get_rarity_colour(rarity: int):

    if rarity == 3:
        return shining_colour
    
    if rarity == 2:
        return glowing_colour
    
    if rarity == 1:
        return common_colour

async def get_character_level(member: discord.Member, id: str):

    if id is None:
        return 0

    async with aiosqlite.connect("gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT "{id}" FROM collection WHERE user_id = {member.id}')
            level = await cursor.fetchone()


    level = level[0]
    
    if level is None:
        level = 0
    
    level = round(level, 1)

    return level


async def give_character(member: discord.Member, character: str) -> float:

    level = await get_character_level(member, character)
    
    if level == 0:
        newLevel = 1
    elif level >= 5:
        newLevel = 5
    else:
        newLevel = level + 1

    async with aiosqlite.connect("gacha.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE collection SET "{character}" = ? WHERE user_id = ?')
            val = (newLevel, member.id)
            await cursor.execute(sql, val)

        await db.commit()

    return newLevel


async def get_party(member: discord.Member):

    async with aiosqlite.connect("party.sqlite") as db:
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

    async with aiosqlite.connect("party.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT slot1, slot2, slot3, slot4, slot5, slot6 FROM party1 WHERE user_id = {member.id}')
            party = await cursor.fetchall()
            party = party[0]

            for index, char in enumerate(party):
                if character == char:
                    sql = (f'UPDATE party1 SET slot{index+1} = null WHERE user_id = ?')
                    val = (member.id,)
                    await cursor.execute(sql, val) 


            sql = (f'UPDATE party SET {slot} = ? WHERE user_id = ?')
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

    async with aiosqlite.connect("party.sqlite") as db:
        async with db.cursor() as cursor:

            for index in range(6):
                sql = (f'UPDATE party1 SET slot{index+1} = null WHERE user_id = ?')
                val = (member.id,)
                await cursor.execute(sql, val) 

        await db.commit()




def get_pool(rarity: int, series: str):
    pool = [character for character in CHARACTERS.values() if character.rarity == rarity]
    return pool

async def get_jars(member: discord.Member, insert_if_none: bool=False):
    
    async with aiosqlite.connect("eco.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT jars FROM currencies WHERE user_id = {member.id}')
            jars = await cursor.fetchone()

    if not jars:
        if insert_if_none:
            await bot.insert_user_record('eco', 'currencies', member)
        jars = [0]
        
    return jars[0]
            

async def gain_jars(member: discord.Member, amount: int):

    current_jars = await get_jars(member, True)

    async with aiosqlite.connect("eco.sqlite") as db:
        async with db.cursor() as cursor:
            sql = ('UPDATE currencies SET jars = ? WHERE user_id = ?')
            val = (current_jars + amount, member.id)
            await cursor.execute(sql, val)
            await db.commit()