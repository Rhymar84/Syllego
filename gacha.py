import discord
import sqlite3
import random
import bot
import math
import datetime as dt
import asyncio
from time import perf_counter
from PIL import Image
from io import BytesIO
from functools import lru_cache
from discord.utils import get
from discord.ui import Select, View
from config import TOKEN, ErrorColour
from config import SERVER
from config import DEBUG

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


class Character():

    def __init__(self, name: str, rarity: str, series: str, health: int, attack: int, magic_power: int, armor: int, magic_defense: int, speed: int, 
                 level: float=0, xp: str='', colour=0xb71010):
        self.name = name
        self.rarity = rarity
        self.series = series

        self.health = health
        self.attack = attack
        self.magic_power = magic_power
        self.armor = armor
        self.magic_defense = magic_defense
        self.speed = speed

        self.level = level
        self.xp = xp
        self.colour = colour

    def __str__(self) -> str:
        return self.name
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Character):
            return False
        
        return self.name == __value.name
    

    async def display(self) -> discord.Embed:

        emoji = globals()[f'{self.rarity}_emoji']

        truncLevel = math.trunc(self.level)

        xp = self.xp
        if not xp:
            if self.level >= 5:
                xp = '(Max Level)'
            else:
                xp = ''
        

        if self.level != 0:
            stars = '⭐' * truncLevel
        else:
            stars = '🔒'

        series = self.series

        embed = discord.Embed(title=f'{emoji} {self.name} {stars} {xp}', color=self.colour)
        embed.set_footer(text=series)

        return embed




class Spin(discord.ui.View):
    def __init__(self, original_interaction: discord.Interaction, character: Character):
        super().__init__()
        self.original_interaction = original_interaction
        self.character = character

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
        

        char_level = await give_character(interaction.user, self.character.name)
        await bot.set_starpower(interaction.user, starpower - 50)
        await bot.set_last_starpower_update(interaction.user, dt.datetime.now())

        if char_level == 1.0:
            self.character = get_character(self.character.name, char_level, 'NEW!!')
        else:
            self.character = get_character(self.character.name, char_level)

        await self.claim(interaction)

        


    async def create(self):

        embed = await self.character.display()

        portrait = discord.File(f'Portraits/{self.character.name}.jpg', filename='portrait.jpg')
        embed.set_image(url=f'attachment://portrait.jpg')
        embed.set_author(name=f'{self.original_interaction.user.display_name}', icon_url=f'{self.original_interaction.user.display_avatar}')

        await self.original_interaction.response.send_message(embed=embed, file=portrait, view=self)

        await asyncio.sleep(180)
        self.stop()

    async def claim(self, interaction: discord.Interaction):

        embed = await self.character.display()

        portrait = discord.File(f'Portraits/{self.character.name}.jpg', filename='portrait.jpg')
        embed.set_image(url=f'attachment://portrait.jpg')
        embed.set_author(name=f'{interaction.user.display_name}', icon_url=f'{interaction.user.display_avatar}')

        await interaction.response.edit_message(embed=embed, attachments=[portrait], view=None)

        channel = interaction.channel
        await channel.send(f'**{interaction.user.display_name}** made an offering to the stars, and was gifted **{self.character.name}**.')








########################################################################################

    


async def get_collection(member: discord.Member, format: str='images') -> list[str]:

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT * FROM collection WHERE user_id = {member.id}')
    characters = cursor.fetchall()[0]

    cursor.execute('PRAGMA table_info(collection)')
    columns = cursor.fetchall()

    cursor.close()
    db.close()

    columns = [x[1] for x in columns]

    collection = list(zip(columns, characters))
    collection.pop(0)

    collection = [character for character in collection if character[1] is not None]
    collection = sorted(collection, key=lambda x: get_rarity(x[0]), reverse=True)
    
    if format == 'names':
        return [character[0] for character in collection]
    
    if format == 'objects':
        return [get_character(character[0], character[1]) for character in collection]

    if format == 'rarities':
        return [f'{globals()[f"{get_rarity(character[0])}_emoji"]} {character[0]} **{int(await getStars(member, character[0]))}**⭐' for character in collection]
    
    embeds = []
    files = []

    for index, character in enumerate(collection):
        name = character[0]

        level = await getStars(member, name)

        embed = await character_display(name, level, False)
        footer = str(embed.footer.text)

        footer += f'\n({index+1}/{len(collection)})'
        embed.set_footer(text=f'{footer}')
        embed.set_author(name=f'{member.display_name}', icon_url=f'{member.display_avatar}')
        
        embeds.append(embed)
        files.append(name)

    return embeds, files



async def getGacha(member: discord.Member):
    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT * FROM collection WHERE user_id = {member.id}')
    fetched = cursor.fetchall()
    
    try:
        fetched = fetched[0]
    except:
        return None

    cursor.close()
    db.close()

    return fetched


def get_character(character: str, level: float=0, xp: str='', colour=0xb71010) -> Character:

    db = sqlite3.connect('stats.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT * FROM stats WHERE name = "{character}"')
    char = cursor.fetchone()

    cursor.close()
    db.close()

    try:
        name, rarity, series, hp, atk, mp, pdef, mdef, speed, growth = char
    except IndexError:
        return None
    
    if level > 1:
        gain = (int(level) - 1) * growth
        hp += 2 * gain
        atk += gain
        mp += gain
        pdef += gain
        mdef += gain
        speed += int(gain / 2)

    
    return Character(character, rarity, series, hp, atk, mp, pdef, mdef, speed, level, xp, colour)





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
        rarity = 'shining'
    elif roll <= shining_chance + glowing_chance:
        rarity = 'glowing'
    else:
        rarity = 'common'

    pool = get_pool(rarity, wish)
    pull = random.choice(pool)
    level = await getStars(member, pull)

    pull = get_character(pull, level, colour=globals()[f'{rarity}_colour'])

    return pull




async def multi_spin(member: discord.Member, wheel: str):

    embeds = []
    pulls = []
    recap = ''


    for i in range(10):
        pull = await do_spin(member, wheel)
        rarity = get_rarity(pull)
        level = await getStars(member, pull)

        emojiName = f'{rarity}_emoji'
        emoji = globals()[f'{emojiName}']

        embed = await character_display(pull, level, True)
        footer = str(embed.footer.text)

        footer += f'\n({i+1}/10)'
        embed.set_footer(text=f'{footer}')

        embed.set_author(name=f'{member.display_name}', icon_url=f'{member.display_avatar}')
        
        embeds.append(embed)
        pulls.append(pull)
        recap += f'{i+1}. {emoji} **{pull}**\n'


    # RECAP EMBED
    embed = discord.Embed(title='Spin Recap', description=f'{recap}', color=0x1053b7)
    embeds.append(embed)

    # PAGE COUNTER
    return embeds, pulls



async def get_series_progress(member: discord.Member, series: str):

    char_list = [get_character(x) for x in bot.CHARACTER_LIST]
    char_list = [x for x in char_list if x.series == series]

    collected = await get_collection(member, format='objects')
    collected = [x for x in collected if x.series == series]
    char_list = sorted(char_list, key=lambda x: get_rarity(x.name), reverse=True)

    for character in char_list:
        if character in collected:
            character.level = [x for x in collected if x == character][0].level
    
    return char_list





async def character_display(name: str, level: float, spin: bool=False, xp: str=''):

    db = sqlite3.connect('stats.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT * FROM stats WHERE name = "{name}"')
    info = cursor.fetchall()
    try:
        info = info[0]
    except IndexError:
        print(f'Error: {name} not found in Stats')
        return


    cursor.close()
    db.close()

    rarity = get_rarity(name)
    emoji = globals()[f'{rarity}_emoji']

    truncLevel = math.trunc(level)

    if not xp:
        if level >= 5:
            xp = '(Max Level)'
        else :
            xp = ''
    

    if level != 0:
        stars = await getStarsString(truncLevel)
    else:
        stars = '🔒'
        level = 1
        truncLevel = 1

    if spin == True:
        colour = globals()[f'{rarity}_colour']
    else:
        colour = 0xb71010

    series = info[2]

    growth = info[11]
    growth = growth * (truncLevel - 1)

    emotion: str = info[3]

    health = info[5] + (growth * 2)
    attack = info[6] + growth
    special_attack = info[7] + growth
    defense = info[8] + growth
    special_defense = info[9] + growth
    speed = info[10] + (2 * (int(level) - 1))
    
    description = f'Base State: **{emotion.title()}**\n\nHP: **{health}**\nAtk: **{attack}** | Def: **{defense}**\nSp.A: **{special_attack}** | Sp.D: **{special_defense}**\nSpeed: **{speed}**'

    embed = discord.Embed(title=f'{emoji} {name} {stars} {xp}', description = f'{description}', color=colour)
    embed.set_footer(text=series)

    return embed


async def getStarsString(level):

    stars = ''
    for star in range(math.trunc(level)):
        stars += '⭐'
    
    return stars


def get_rarity(character: str):

    db = sqlite3.connect('stats.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT rarity FROM stats WHERE name = "{character}"')
    rarity = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return rarity

def get_rarity_emoji(rarity: str):

    if rarity == 'shining':
        return shining_emoji
    
    if rarity == 'glowing':
        return glowing_emoji
    
    if rarity == 'common':
        return common_emoji

async def getStars(member: discord.Member, character: str):

    if character is None:
        return 0

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT "{character}" FROM collection WHERE user_id = {member.id}')
    level = cursor.fetchone()

    cursor.close()
    db.close()

    level = level[0]
    
    if level is None:
        level = 0
    
    level = round(level, 1)

    return level

async def give_character(member: discord.Member, character: str) -> float:

    level = await getStars(member, character)

    rarity = get_rarity(character)
    
    if level == 0:
        newLevel = 1
    elif level >= 5:
        newLevel = 5
    else:
        newLevel = level + 1

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    sql = (f'UPDATE collection SET "{character}" = ? WHERE user_id = ?')
    val = (newLevel, member.id)
    cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()

    return newLevel


async def getParty(member: discord.Member):

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT slot1, slot2, slot3, slot4, slot5, slot6 FROM party WHERE user_id = {member.id}')
    party = cursor.fetchall()

    cursor.close()
    db.close()

    try:
        party = party[0]
    except:
        party = None
    
    return party


async def partyDisplay(member: discord.Member, campaign: bool=False):

    if campaign == False:
        party = await getParty(member)

        slot1 = [party[0], await getStars(member, party[0])]
        slot2 = [party[1], await getStars(member, party[1])]
        slot3 = [party[2], await getStars(member, party[2])]
        slot4 = [party[3], await getStars(member, party[3])]
        slot5 = [party[4], await getStars(member, party[4])]
        slot6 = [party[5], await getStars(member, party[5])]

    else:
        campaignParty = await getCampaignParty(member)

        party = campaignParty[0]
        levels = campaignParty[1]

        slot1 = [party[0], levels[0]]
        slot2 = [party[1], levels[1]]
        slot3 = [party[2], levels[2]]
        slot4 = [party[3], levels[3]]
        slot5 = [party[4], levels[4]]
        slot6 = [party[5], levels[5]]


    pos1 = (133, 133)
    pos2 = (789, 133)
    pos3 = (1444, 133)
    pos4 = (132, 888)
    pos5 = (789, 888)
    pos6 = (1444, 888)

    base = Image.open('Assets/Party Themes/Base.png')


    for index, character in enumerate(party):

        slot = locals()[f'slot{index + 1}']

        if slot[0] is None:
            continue
        
        stars = math.trunc(slot[1])

        pos = locals()[f'pos{index + 1}']

        char = Image.open(f'Party/{character}.png')

        level = Image.open(f'Assets/Level {stars}.png')

        base.paste(char, (pos))
        base.paste(level, (pos), level)


    embed = discord.Embed(
        title=f'',
        color = 0xf69337
    )


    with BytesIO() as image_binary:
        party_image = base.convert('RGB')
        party_image.save(image_binary, 'JPEG')
        image_binary.seek(0)
        file = discord.File(fp=image_binary, filename='party.jpeg')
        embed.set_image(url='attachment://party.jpeg')
        embed.set_author(name=f'{member.display_name}\'s Party', icon_url=f'{member.display_avatar}')
        embed.set_footer(text=f'Use /add to edit a party slot.')

    return embed, file



async def edit_slot(member: discord.Member, slot: str, character: str):

    slot_index = slot[4::4]

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT slot1, slot2, slot3, slot4, slot5, slot6 FROM party WHERE user_id = {member.id}')
    party = cursor.fetchall()
    party = party[0]

    for index, char in enumerate(party):
        if character == char:
            sql = (f'UPDATE party SET slot{index+1} = null WHERE user_id = ?')
            val = (member.id,)
            cursor.execute(sql, val) 


    sql = (f'UPDATE party SET {slot} = ? WHERE user_id = ?')
    val = (character, member.id)
    cursor.execute(sql, val)

    # if int(slot_index) in [1, 2, 3]:
    #     moves = await get_moves(character)
    #     moves = moves[:4]
    #     moves = ', '.join(moves)

    #     sql = (f'UPDATE party SET {f"moves{slot_index}"} = ? WHERE user_id = ?')
    #     val = (moves, member.id)
    #     cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()


async def clearParty(member: discord.Member):

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    for index in range(6):
        sql = (f'UPDATE party SET slot{index+1} = null WHERE user_id = ?')
        val = (member.id,)
        cursor.execute(sql, val) 

    db.commit()
    cursor.close()
    db.close()


async def characterInfo(member: discord.Member, character: str):
    
    level = await getStars(member, character)
    if level is None:
        level = 0

    embed = await character_display(character, level, False)

    return embed










######################################################## BATTLE




        



        
    
    

    

    




    
    


async def getCampaignParty(member: discord.Member):

    stage = await getCampaignStage(member)

    db = sqlite3.connect('campaign.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT * FROM campaign WHERE stage = {stage}')
    stageStats = cursor.fetchall()

    cursor.close()
    db.close()

    stageStats = stageStats[0]

    stage, char1, char2, char3, char4, char5, char6, char1lv, char2lv, char3lv, char4lv, char5lv, char6lv, rewards, difficulty = stageStats

    return [[char1, char2, char3, char4, char5, char6], [char1lv, char2lv, char3lv, char4lv, char5lv, char6lv]]



async def getCampaignStage(member: discord.Member):

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT campaign FROM misc WHERE user_id = {member.id}')
    stage = cursor.fetchone()

    cursor.close()
    db.close()

    stage = stage[0]
   
    if stage is None:
        stage = 1
    else:
        pass

    return stage
    

async def getStageRewards(stage: int):
    
    db = sqlite3.connect('campaign.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT rewards FROM campaign WHERE stage = {stage}')
    rewards = cursor.fetchone()

    cursor.close()
    db.close()

    rewards = rewards[0]

    return rewards


async def getStageDifficulty(stage: int):
    
    db = sqlite3.connect('campaign.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT difficulty FROM campaign WHERE stage = {stage}')
    difficulty = cursor.fetchone()

    cursor.close()
    db.close()

    difficulty = difficulty[0]

    return difficulty


async def advanceStage(member: discord.Member, message: discord.Message):

    stage = await getCampaignStage(member)

    # REWARDS
    if stage == 1 or stage == 2 or stage == 4 or stage == 5 or stage == 12 or stage == 16:
        balance = await bot.get_balance(member)
        await bot.updateBalance(member, balance + 10000)

    elif stage == 7:
        balance = await bot.get_balance(member)
        await bot.updateBalance(member, balance + 5000)

    elif stage == 3 or stage == 6 or stage == 11:
        balance = await bot.getTokens(member)
        await bot.updateTokens(member, balance + 10)

    elif stage == 13 or stage == 17:
        await bot.set_freebie(member, 0)
    
    elif stage == 8 or stage == 14:
        faction = await bot.get_faction(member)
        
        db = sqlite3.connect('faction.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT str_xp FROM faction WHERE role_id = {faction.id}')
        xp = cursor.fetchone()
        try:
            xp = xp[0]
        except:
            xp = 0

        sql = ('UPDATE faction SET str_xp = ? WHERE role_id = ?')
        if stage == 8:
            val = (xp + 15000, faction.id)
        elif stage == 14:
            val = (xp + 10000, faction.id)

        cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()

        await bot.check_level_up(faction, 'strength')
    
    elif stage == 9 or stage == 20:
        faction = await bot.get_faction(member)
        
        await bot.giveFPts(faction, 2)

    elif stage == 10 or stage == 15 or stage == 19:
        await give_character(member, 'Shiba Katsunori')
    
    elif stage == 18:
        await bot.add_stardust(member, 18000)



    embed = discord.Embed(title='Stage Completed!', description=f'Congratulations {member.mention}, you completed Stage **{stage}** of the campaign and were awarded {await getStageRewards(stage)}!', color=0x44d5c8)
    await message.reply(embed=embed)
    
    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    sql = ('UPDATE misc SET campaign = ? WHERE user_id = ?')
    val = (stage + 1, member.id)
    cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()

    


async def getMaxStage():
    
    db = sqlite3.connect('campaign.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT stage FROM campaign ORDER BY stage DESC')
    maxStage = cursor.fetchone()

    cursor.close()
    db.close()

    maxStage = maxStage[0]

    return maxStage


def get_pool(rarity: str, series: str):

    db = sqlite3.connect('stats.sqlite')
    cursor = db.cursor()

    if series is None:
        sql = (f'SELECT name FROM stats WHERE rarity = ?')
        val = (rarity,)
    else:
        sql = (f'SELECT name FROM stats WHERE rarity = ? AND series = ?')
        val = (rarity, series)


    cursor.execute(sql, val)
    pool = cursor.fetchall()

    cursor.close()
    db.close()

    pool = [character[0] for character in pool]

    return pool


######### MONTE CARLO ALGORITHM


async def get_moves(character: str) -> list:

    db = sqlite3.connect('stats.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT strategies FROM stats WHERE name = "{character.title()}"')
    moves = cursor.fetchall()

    cursor.close()
    db.close()

    moves: str = moves[0][0]

    moves = moves.split(', ')

    return moves

