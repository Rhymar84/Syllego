import discord
import sqlite3
import random
import config
import system.gacha as gacha
import battles.battles as battles
import datetime as dt
import aiosqlite
import math
from time import perf_counter
from discord.ext import tasks
from discord import app_commands
from discord.utils import get
from discord.ui import Select, View
from difflib import get_close_matches
from config import TOKEN, BOT_ID, ErrorColour
from config import SERVER
from config import DEBUG
from system.character_database import CHARACTERS, BaseChar, CharInfo
from battles.cards import Cards, BaseCard, create_card
from battles.characters import FIGHTERS


CHARACTER_LIST = sorted(tuple([character.name for character in CHARACTERS.values()]))
SERIES_LIST = sorted(tuple(dict.fromkeys([character.series for character in CHARACTERS.values()])))
CARD_LIST = tuple([card.value.name for card in Cards])


class SlotSelect(Select):
    def __init__(self, original_interaction: discord.Interaction, embed: discord.Embed, file: discord.File, view: discord.ui.View):
        super().__init__()

        self.placeholder = 'Select a Slot'

        self.original_interaction = original_interaction
        self.embed = embed
        self.file = file
        self.original_view = view
        self.options = [
                    discord.SelectOption(label='slot1'), discord.SelectOption(label='slot2'), discord.SelectOption(label='slot3'), 
                    discord.SelectOption(label='slot4'), discord.SelectOption(label='slot5'), discord.SelectOption(label='slot6'),
                ]

    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.original_interaction.user:
            error = discord.Embed(title='User Error', description='This is not your party!', color=ErrorColour)
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        chosen_slot = self.values[0]
            
        slot_edit = EditSlot(interaction, chosen_slot, self.original_view)
        await interaction.response.send_modal(slot_edit)

class EditSlot(discord.ui.Modal, title = 'Edit Slot'):
    input = discord.ui.TextInput(
        label='Enter a character name',
        max_length=50,
        style=discord.TextStyle.short,
        required=True,
        placeholder='Syllego'
    )

    def __init__(self, original_interaction: discord.Interaction, slot: str, original_view: discord.ui.View):
        super().__init__()
        self.original_interaction = original_interaction
        self.slot = slot
        self.original_view = original_view

    async def on_submit(self, interaction: discord.Interaction):
        
        character = str(self.input)

        if character not in CHARACTER_LIST:
            if get_close_matches(character, CHARACTER_LIST):
                matches = get_close_matches(character, CHARACTER_LIST, 1)[0]
                character = matches

            else:
                embed = discord.Embed(title='Character Error', description=f'No such character "{character}".', color=ErrorColour)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        
        if character not in await gacha.get_collection(interaction.user, 'names'):
            embed = discord.Embed(title='Character Unowned', description=f'You do not own **{character}** :(', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await gacha.edit_slot(interaction.user, self.slot, character)
        await interaction.response.defer()

        embed, file = await gacha.party_display(interaction.user)

        await self.original_interaction.edit_original_response(embed=embed, attachments=[file], view=self.original_view)


class Book(discord.ui.View):
    def __init__(self, original_interaction: discord.Interaction, pages: list[discord.Embed], file_names: list=[]):
        super().__init__()
        self.original_interaction = original_interaction
        self.page = 0
        self.pages = pages
        self.file_names = file_names



    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.grey)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.original_interaction.user:
            error = discord.Embed(title='User Error', description='This is not your command!', color=ErrorColour)
            await interaction.response.send_message(embed=error, ephemeral=True)
            return

        self.page -= 1
        if self.page < 0:
            self.page = len(self.pages) - 1
        
        if self.file_names:
            embed = self.pages[self.page]

            portrait = discord.File(f'Assets/Portraits/{self.file_names[self.page]}.jpg', filename='portrait.jpg')
            embed.set_image(url=f'attachment://portrait.jpg')

            await interaction.response.edit_message(embed=embed, attachments=[portrait], view=self)
        else:
            await interaction.response.edit_message(embed=self.pages[self.page], view=self)



    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.grey)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button): 
        if interaction.user != self.original_interaction.user:
            error = discord.Embed(title='User Error', description='This is not your command!', color=ErrorColour)
            await interaction.response.send_message(embed=error, ephemeral=True)
            return  

        self.page += 1
        if self.page > len(self.pages) - 1:
            self.page = 0

        if self.file_names:
            embed = self.pages[self.page]

            portrait = discord.File(f'Assets/Portraits/{self.file_names[self.page]}.jpg', filename='portrait.jpg')
            embed.set_image(url=f'attachment://portrait.jpg')

            await interaction.response.edit_message(embed=embed, attachments=[portrait], view=self)
        else:
            await interaction.response.edit_message(embed=self.pages[self.page], view=self)
    

    async def create(self):

        if self.file_names:
            embed = self.pages[0]

            portrait = discord.File(f'Assets/Portraits/{self.file_names[self.page]}.jpg', filename='portrait.jpg')
            embed.set_image(url=f'attachment://portrait.jpg')

            if len(self.pages) == 1:
                await self.original_interaction.response.send_message(embed=embed, file=portrait)
            else:
                await self.original_interaction.response.send_message(embed=embed, file=portrait, view=self)
                
        else:
            if len(self.pages) == 1:
                await self.original_interaction.response.send_message(embed=self.pages[0])
            else:
                await self.original_interaction.response.send_message(embed=self.pages[0], view=self)


info_group = app_commands.Group(name="info", description="Check information on various battle mechanics.")
party_group = app_commands.Group(name="party", description="Commands relating to your battle party.")


def run_discord_bot():
    intents = discord.Intents.all()
    intents.message_content = True
    global client
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)


    ############################################### COMMANDS ######################################################################

    
     ###### HELP
    @tree.command(
            name = 'help',
            description= 'Get a list of all commands.',
            guild = discord.Object(id=SERVER)
    )
    async def help(interaction: discord.Interaction):
        
        commands = tree._get_all_commands(guild=discord.Object(id=SERVER))

        embed = discord.Embed(title='FOTE Commands', color=0x2363ac)
        
        for command in commands:
            if 'ADMIN ONLY' in command.description or 'OWNER ONLY' in command.description:
                continue

            embed.add_field(name=f'/{command.name}', value=f'{command.description}', inline=False)

        await interaction.response.send_message(embed=embed)
    


    
    ###### COLLECTION
    @tree.command(
            name = 'collection',
            description = 'View your character collection!',
            guild = discord.Object(id=SERVER)
    )
    @app_commands.choices(mode=[
        app_commands.Choice(name='images', value=1), app_commands.Choice(name='list', value=2)
    ])
    async def collection(interaction: discord.Interaction, member: discord.Member=None, mode: app_commands.Choice[int]=None):
        
        if member is None:
            member = interaction.user

        if mode is None:
            mode = app_commands.Choice(name='images', value=1)

        if not await gacha.get_collection(member, 'names'):
            embed = discord.Embed(title=f'{member.display_name}\'s Collection', description=f'This collection is empty :(', color=ErrorColour)
            embed.set_thumbnail(url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
            return
        

        if mode.value == 1:
            embeds, file_names = await gacha.get_collection(member)

        elif mode.value == 2:
            names = await gacha.get_collection(member, 'rarities')

            file_names = []
            embeds: list[discord.Embed] = []
            while names:
                page_names = names[:20]
                
                embed = discord.Embed(title='', description='\n'.join(page_names), color=0xb71010)
                embed.set_author(name=member.display_name, icon_url=member.display_avatar)
                embeds.append(embed)

                names = names[21:]
            
            for index, embed in enumerate(embeds):
                embed.set_footer(text=f'\n({index+1}/{len(embeds)})')
            
        collection = Book(interaction, embeds, file_names)
        await collection.create()


            
    

    ###### SERIES
    @tree.command(
            name = 'series',
            description = 'View your progress towards collecting a series!',
            guild = discord.Object(id=SERVER)
    )
    @app_commands.autocomplete(series=autocomplete_series)
    async def series(interaction: discord.Interaction, series: str, member: discord.Member=None):
        
        if member is None:
            member = interaction.user

        if series not in SERIES_LIST:
            embed = discord.Embed(title='Series Error', description=f'**{series}** not found.', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        progress = await gacha.get_series_progress(member, series)
        
        total = len(progress)
        owned = len([x for x in progress.values() if x > 0])

        progress = [to_progress_string(x) for x in progress.items()]

        embeds: list[discord.Embed] = []
        while progress:
            page_names = progress[:20]
            
            embed = discord.Embed(title=f"{series}: {owned}/{total}", description='\n'.join(page_names), color=0xb71010)
            embed.set_author(name=member.display_name, icon_url=member.display_avatar)
            embeds.append(embed)

            progress = progress[21:]
        
        for index, embed in enumerate(embeds):
            embed.set_footer(text=f'\n({index+1}/{len(embeds)})')
            
        collection = Book(interaction, embeds)
        await collection.create()

    
    @tree.command(
            name = 'badges',
            description = 'View your progress towards collecting series badges.',
            guild = discord.Object(id=SERVER)
    )
    async def badges(interaction: discord.Interaction, member: discord.Member=None):
        if member is None:
            member = interaction.user
        
        if member == interaction.user:
            await gacha.verify_collection(member)
        else:
            if await gacha.verify_collection(member, False):
                await interaction.response.send_message(embed=discord.Embed(description='This user is not registered.', color=ErrorColour))
                return
        
        badges = []
        for series in SERIES_LIST:
            progress = await gacha.get_series_progress(member, series)
            
            total = len(progress)
            owned = len([x for x in progress.values() if x > 0])

            badges.append({'series': series, 'string': f"{'✅' if total == owned else '🔒'} {series}: **{owned}/{total}**"})
        
        embeds: list[discord.Embed] = []
        while badges:
            page_names = [x['string'] for x in badges[:20]]
            
            embed = discord.Embed(title=f"Badges", description='\n'.join(page_names), color=0xb71010)
            embed.set_author(name=member.display_name, icon_url=member.display_avatar)
            embeds.append(embed)

            badges = badges[21:]

        for index, embed in enumerate(embeds):
            embed.set_footer(text=f'\n({index+1}/{len(embeds)})')
            
        collection = Book(interaction, embeds)
        await collection.create()




    


    ###### SPIN
    @tree.command(
            name = 'spin',
            description = 'Roll a random character that can be claimed using starpower!',
            guild = discord.Object(id=SERVER)
    )
    async def spin(interaction: discord.Interaction):

        remaining_spins = await get_remaining_spins(interaction.user)

        if remaining_spins < 1:
            embed = discord.Embed(title='No Spins Left :(', description=f'You do not have any spins left! Spins refresh in {time_to_next_hour()}.', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await gacha.verify_collection(interaction.user)

        pull: BaseChar = await gacha.do_spin(interaction.user)

        spin = gacha.Spin(interaction, pull)
        await spin.create()
        

        

    ###### PARTY
    @party_group.command(description = 'View/Edit your active party!')
    async def view(interaction: discord.Interaction, member: discord.Member = None):

        if member is None:
            member = interaction.user

        if member == interaction.user:
            registered = await gacha.verify_collection(member)
        else:
            registered = await gacha.verify_collection(member, False)
        if not registered:
            await interaction.response.send_message(embed=discord.Embed(description=f'This user is not registered.', color=ErrorColour))
            return

        await interaction.response.defer()

        party = gacha.PartyObject(member)
        await party.set_party()
        await party.calculate_chemistry()

        embed, file = await party.display()
        await interaction.followup.send(embed=embed, file=file)
    

    ###### ADD
    @party_group.command(description = 'Add a character to your party.')
    @app_commands.choices(slot=[
        app_commands.Choice(name='1', value=1), app_commands.Choice(name='2', value=2), app_commands.Choice(name='3', value=3),
        app_commands.Choice(name='4', value=4), app_commands.Choice(name='5', value=5), app_commands.Choice(name='6', value=6)
    ])
    @app_commands.autocomplete(character=autocomplete_collection)
    async def add(interaction: discord.Interaction, slot: app_commands.Choice[int], character: str):
        await gacha.verify_collection(interaction.user)
        
        if character not in CHARACTER_LIST:
            embed = discord.Embed(title='Character Error', description=f'No such character "{character}".', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        collection = await gacha.get_collection(interaction.user, 'names')

        if character not in collection:
            embed = discord.Embed(title='Character Unowned', description=f'You do not own **{character}** :(', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        character: BaseChar = [char for char in CHARACTERS.values() if char.name == character][0]
        
        await gacha.edit_slot(interaction.user, f'slot{slot.value}', character.id)

        party = gacha.PartyObject(interaction.user)
        await party.set_party()
        await party.calculate_chemistry()
        embed, file = await party.display()

        embed.description = f'Successfully added **{character.name}** to Slot **{slot.value}**!'
        embed.color = 0x36ec42

        await interaction.response.send_message(embed=embed, file=file, ephemeral=True)
        



        


    ###### CHARACTER
    @tree.command(
            name = 'character',
            description = 'View a character\'s information. (Entered name does not need to be exact)',
            guild = discord.Object(id=SERVER)
    )
    @app_commands.autocomplete(character=autocomplete_character)
    async def character(interaction: discord.Interaction, character: str):
        

        if character not in CHARACTER_LIST:
            
            if get_close_matches(character, CHARACTER_LIST):
                matches = get_close_matches(character, CHARACTER_LIST, 1)[0]
                character = matches

            else:
                embed = discord.Embed(title='Character Error', description=f'No such character "{character}".', color=ErrorColour)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
        character: BaseChar = [char for char in CHARACTERS.values() if char.name == character][0]

        level = await gacha.get_character_level(interaction.user, character.id)
        if level is None:
            level = 0

        embed: discord.Embed = await character.display(level, 0xb71010)

        portrait = discord.File(f'Assets/Portraits/{character.id}.jpg', filename='portrait.jpg')
        embed.set_image(url=f'attachment://portrait.jpg')

        await interaction.response.send_message(embed=embed, file=portrait, view=CharInfo(interaction, character, level))
        


    @info_group.command(description='Display a card\'s information.')
    @app_commands.autocomplete(card=autocomplete_card)
    async def card(interaction: discord.Interaction, card: str):
        if card not in CARD_LIST:
            await interaction.response.send_message(embed=discord.Embed(description=f'No such card "{card}".', color=ErrorColour), ephemeral=True)
            return
        
        await interaction.response.defer()
        card_id = card.upper().replace(' ', '_').translate({ord(i): None for i in ':;.,!@#$%^&*()[]{}<>?/\\'})
        card: BaseCard = Cards[card_id].value

        card_description = await card.info_text()
        embed = discord.Embed(
            title = f"{config.CARD_RARITY_KEY[card.rarity]} {card.name.title()} ({card.cost})",
            description = card_description,
            color = 0xfcba03
        )
        if card.tags:
            embed.set_footer(text=', '.join(card.tags).title())

        thumbnail = None
        if card.filename:
            try:
                thumbnail = discord.File(fp=f"Assets/Cards/{card.filename}", filename=f'card.{card.filename.split(".")[-1]}')
            except FileNotFoundError:
                pass
            embed.set_thumbnail(url=f"attachment://{thumbnail.filename}")

        await interaction.followup.send(embed=embed, file=thumbnail)

    ##### STATUS
    @tree.command(
            name = 'status',
            description = 'Check your current status.',
            guild = discord.Object(id=SERVER)
    )
    async def status(interaction: discord.Interaction):

        starpower = await get_starpower(interaction.user)
        spins_left = await get_remaining_spins(interaction.user)

        embed = discord.Embed(title=f'{interaction.user.display_name}\'s Status', description=f'Spins Left: **{spins_left}**.\nSpins refresh in {time_to_next_hour()}.\nStarpower: **{starpower}%**.\nRecharge Rate: **20%/h**.\nClaim Cost: **50%**.', color=0xd2ac41)
        embed.set_thumbnail(url=interaction.user.display_avatar)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)

        await interaction.response.send_message(embed=embed)


    ##### STATUS
    @tree.command(
            name = 'tableupdate',
            description = 'RHYMAR ONLY COMMAND.',
            guild = discord.Object(id=SERVER)
    )
    async def tableupdate(interaction: discord.Interaction):

        if interaction.user.id != 209985174081896450:
            embed2 = discord.Embed(title='Error', description='You do not have permission!', color=ErrorColour)
            await interaction.response.send_message(embed=embed2, ephemeral=True)
            return
        
        await interaction.response.defer()

        ids = tuple(CHARACTERS.keys())
        missing = []

        db = sqlite3.connect('gacha.sqlite')
        cursor = db.cursor()

        cursor.execute('PRAGMA table_info(collection)')
        columns = cursor.fetchall()

        cursor.close()
        db.close()

        columns = [x[1] for x in columns]

        for id in ids:
            if id not in columns:
                missing.append(id)

        if not missing:
            await interaction.followup.send('No missing characters :D')
            return
        
        db = sqlite3.connect('gacha.sqlite')
        cursor = db.cursor()

        for character in missing:
            cursor.execute(f'ALTER TABLE collection ADD COLUMN "{character}" INTEGER')

        db.commit()
        cursor.close()
        db.close()

        added = "\n".join([CHARACTERS[char].name for char in missing])
        await interaction.followup.send(f'# Missing Characters Added:\n{added}')


    ##### WISHINFO
    @tree.command(
            name = 'wishinfo',
            description = 'View info about your wished series.',
            guild = discord.Object(id=SERVER)
    )
    async def wishinfo(interaction: discord.Interaction):

        wish = await get_wish(interaction.user)

        if wish is None:
            info_text = 'You are not currently wishing for a series.'
        else:
            info_text = f'You have a +10% chance to pull characters from **{wish}**.'
        
        embed = discord.Embed(description=f'{info_text}', color=0x144066)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
        embed.set_footer(text='Use /wish to wish for a series. Use "/wish None" to remove your wish.')

        await interaction.response.send_message(embed=embed)

    ##### WISH
    @tree.command(
            name = 'wish',
            description = 'Wish for a series.',
            guild = discord.Object(id=SERVER)
    )
    @app_commands.autocomplete(series=autocomplete_series)
    async def wish(interaction: discord.Interaction, series: str):

        if series not in SERIES_LIST and series.lower() != 'none':
            error = discord.Embed(title='Series Not Found :(', description=f'Could not find series called **{series}**!', color=ErrorColour)
            await interaction.response.send_message(embed=error, ephemeral=True)
            return
        
        if series.lower() == 'none':
            series = None

        await set_wish(interaction.user, series)

        if series is None:
            description = 'Successfully cleared your wished series.'
        else:
            description = f'Successfully set your wished series to **{series}**!'

        embed = discord.Embed(title='Wish Set', description=description, color=0x29d16c)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)

        await interaction.response.send_message(embed=embed)

    
    ##### SIM
    @tree.command(
            name = 'simulate',
            description = 'Simulate X spins, default 1000. (ADMIN ONLY)',
            guild = discord.Object(id=SERVER)
    )
    async def simulate(interaction: discord.Interaction, number: int=None):

        if interaction.user.id not in [209985174081896450, 649239777257979925]:
            await interaction.response.send_message('No permission.')
            return
        
        if number is None:
            number = 1000

        await interaction.response.defer()

        sh = 0
        gl = 0
        c = 0
        for _ in range(number):

            pull = await gacha.do_spin(interaction.user)
            rarity = pull.rarity

            if rarity == 3:
                sh += 1
            elif rarity == 2:
                gl += 1
            elif rarity == 1:
                c += 1
        
        embed = discord.Embed(title='Spins Simulated', description=f'**{sh}** {gacha.shining_emoji}\n**{gl}** {gacha.glowing_emoji}\n**{c}** {gacha.common_emoji}', color=ErrorColour)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)

        await interaction.followup.send(embed=embed)
    

    @tree.command(
            name = 'test',
            description = 'Test command',
            guild = discord.Object(id=SERVER)
    )
    async def test(interaction: discord.Interaction):
        for thread in interaction.channel.threads:
            await thread.delete(reason='Clearing test threads.')

        test_party1 = [
            battles.Character(CHARACTERS['AOT-10'], **FIGHTERS['AOT-10']), 
            battles.Character(CHARACTERS['AOT-11'], **FIGHTERS['AOT-11']), 
            battles.Character(CHARACTERS['HXH-08'], **FIGHTERS['HXH-08'])
        ]
        test_party2 = [
            battles.Character(CHARACTERS['JJK-08'], **FIGHTERS['JJK-08']), 
            battles.Character(CHARACTERS['JJK-12'], **FIGHTERS['JJK-12']), 
            battles.Character(CHARACTERS['JJK-13'], **FIGHTERS['JJK-13'])
        ]

        
        player1 = battles.Player(interaction.user, interaction.channel)
        player1.set_party(test_party1)
        player2 = battles.Player(interaction.user, interaction.channel)
        player2.set_party(test_party2)

        battle = battles.Battle(player1, player2)
        
        deck = [Cards.STRIKE] * 5 + [Cards.BLAST] * 5 + [Cards.BLOCK] * 5 + [Cards.SCRYING_TOME] * 3 + [Cards.SLAM] * 3 + [Cards.PIERCE] * 3 + [Cards.FOCUS] * 3 + [Cards.EXPLOSION] * 3
        await player1.zones.initialise_deck(deck)
        await player2.zones.initialise_deck(deck)

        await interaction.response.send_message("Created test battle")
        await battle.start()
        


    ########################################### LOOP ##########################################################

    @tasks.loop(seconds=1)
    async def daily():
        now = dt.datetime.now()

        with open ("last_refresh.txt", "r") as file:
            line = file.readline()


        if now.hour != int(line):
            await refresh_spins()



    ########################################### ON READY ##########################################################
    @client.event
    async def on_ready():
        
        guild0 = client.get_guild(SERVER)
        rhymar = guild0.get_member(209985174081896450)

        global campaigner
        campaigner = guild0.get_member(BOT_ID)

        if not daily.is_running():
            daily.start()

        # Sync Commands
        try:
            tree.add_command(info_group, guild=discord.Object(id=SERVER))
            tree.add_command(party_group, guild=discord.Object(id=SERVER))
        except discord.app_commands.errors.CommandAlreadyRegistered:
            pass
        await tree.sync(guild=discord.Object(id=SERVER))

        print(f"{client.user} is now running!")

    client.run(TOKEN)














 ####################################### FUNCTIONS ###########################################



async def log(log: str, admin: int):
    channel = client.get_channel(DEBUG)
    
    if admin == 1:
        colour = 0xfc864a
    else:
        colour = 0x3b56ed
    
    ###---EMBED GENERATION---###
    embed = discord.Embed(
        title = 'Syllego Log',
        description= f'{log}',
        color = colour
    )
    await channel.send(embed=embed)



async def check_last_starpower_update(member: discord.Member) -> dt.datetime:

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT last_starpower_update FROM misc WHERE user_id = {member.id}')
    last_update = cursor.fetchone()[0]

    cursor.close()
    db.close()

    if not last_update:
        last_update = '24-09-2003 00:00'

    return dt.datetime.strptime(last_update, "%d-%m-%Y %H:%M")

async def set_last_starpower_update(member: discord.Member, time: dt.datetime):

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    sql = (f'UPDATE misc SET last_starpower_update = ? WHERE user_id = ?')
    val = (time.strftime("%d-%m-%Y %H:%M"), member.id)
    cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()


async def set_starpower(member: discord.Member, amount: int):

    async with aiosqlite.connect("gacha.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE misc SET starpower = ? WHERE user_id = ?')
            val = (amount, member.id)
            await cursor.execute(sql, val)

        await db.commit()



async def get_starpower(member: discord.Member) -> int:

    async with aiosqlite.connect("gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT starpower FROM misc WHERE user_id = {member.id}')
            starpower = await cursor.fetchone()

    starpower = starpower[0]

    if not starpower:
        starpower = 0


    last_update = await check_last_starpower_update(member)
    now = dt.datetime.now()
    difference = now - last_update
    seconds = difference.total_seconds()

    if starpower >= 100 or starpower is None:
        return 100
    
    if seconds < 180:
        return starpower

    
    missing_starpower = 100 - starpower
    recharged_starpower = int(seconds / 180)

    leftover = seconds - (180 * recharged_starpower)
    leftover = dt.timedelta(seconds=leftover)


    await set_last_starpower_update(member, now-leftover)

    if recharged_starpower > missing_starpower:
        recharged_starpower = missing_starpower

    await set_starpower(member, starpower + recharged_starpower)
    
    return starpower + recharged_starpower


async def get_remaining_spins(member: discord.Member) -> int:

    async with aiosqlite.connect("gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT spins_left FROM misc WHERE user_id = {member.id}')
            spins_left = await cursor.fetchone()
    
    spins_left = spins_left[0]

    if spins_left is None:
        spins_left = 10

    return spins_left

async def set_remaining_spins(member: discord.Member, amount: int):

    async with aiosqlite.connect("gacha.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE misc SET spins_left = ? WHERE user_id = ?')
            val = (amount, member.id)
            await cursor.execute(sql, val)

        await db.commit()


def time_to_next_hour() -> int:

    delta = dt.timedelta(hours=1)
    now = dt.datetime.now()
    next_hour = (now + delta).replace(microsecond=0, second=0, minute=0)

    minutes_left = math.ceil((next_hour - now).seconds / 60)

    if minutes_left == 1:
        return '**1** minute'

    return f'**{minutes_left}** minutes'

async def refresh_spins():
    
    with open ("last_refresh.txt", "w") as file:
        file.write(f'{dt.datetime.now().hour}')

    async with aiosqlite.connect("gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute('UPDATE misc SET spins_left = 10')

        await db.commit()

    await log(f'Refreshed spins at **{dt.datetime.now().strftime("%H:%M")}**.', 1)


async def slot_choices() -> list[app_commands.Choice[str]]:
    return [app_commands.Choice(name=slot) for slot in [1,2,3,4,5,6]]



async def get_wish(member: discord.Member) -> str:

    async with aiosqlite.connect("gacha.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT wish FROM misc WHERE user_id = {member.id}')
            wish = await cursor.fetchone()

    return wish[0]


async def set_wish(member: discord.Member, wish: str) -> str:

    async with aiosqlite.connect("gacha.sqlite") as db:
        async with db.cursor() as cursor:

            if wish is None:
                sql = f'UPDATE misc SET wish = null WHERE user_id = ?'
                val = (member.id,)
            else:
                sql = f'UPDATE misc SET wish = ? WHERE user_id = ?'
                val = (wish, member.id)

            await cursor.execute(sql, val)
        await db.commit()

async def insert_user_record(database: str, table: str, member: discord.Member):
    async with aiosqlite.connect(f"{database}.sqlite") as db:
        async with db.cursor() as cursor:
            await cursor.execute(f'INSERT INTO {table}(user_id) VALUES ({member.id})')
        await db.commit()

def to_progress_string(character: tuple) -> str:
    char: BaseChar = character[0]
    level = character[1]

    return f"{gacha.get_rarity_emoji(char.rarity)} {char.name} {f'**{int(level)}** ⭐' if level != 0 else '🔒'}"


async def autocomplete_series(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    series = [app_commands.Choice(name=series, value=series) for series in SERIES_LIST if current.lower() in series.lower()]
    if len(series) > 25:
        series = series[:25]
    return series

async def autocomplete_character(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    chars = [app_commands.Choice(name=character, value=character) for character in CHARACTER_LIST if current.lower() in character.lower()]
    if len(chars) > 25:
        chars = chars[:25]
    return chars

async def autocomplete_collection(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    collection = await gacha.get_collection(interaction.user, 'names')
    chars = [app_commands.Choice(name=character, value=character) for character in collection if current.lower() in character.lower()]
    if len(chars) > 25:
        chars = chars[:25]
    return chars

async def autocomplete_card(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    cards = [app_commands.Choice(name=card, value=card) for card in CARD_LIST if current.lower() in card.lower()]
    if len(cards) > 25:
        cards = cards[:25]
    return cards
    