import discord
import sqlite3
import random
import gacha
import battles
import datetime as dt
import asyncio
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

        embed, file = await gacha.partyDisplay(interaction.user)

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

            portrait = discord.File(f'Portraits/{self.file_names[self.page]}.jpg', filename='portrait.jpg')
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

            portrait = discord.File(f'Portraits/{self.file_names[self.page]}.jpg', filename='portrait.jpg')
            embed.set_image(url=f'attachment://portrait.jpg')

            await interaction.response.edit_message(embed=embed, attachments=[portrait], view=self)
        else:
            await interaction.response.edit_message(embed=self.pages[self.page], view=self)
    

    async def create(self):

        if self.file_names:
            embed = self.pages[0]

            portrait = discord.File(f'Portraits/{self.file_names[self.page]}.jpg', filename='portrait.jpg')
            embed.set_image(url=f'attachment://portrait.jpg')

            await self.original_interaction.response.send_message(embed=embed, file=portrait, view=self)
        else:
            await self.original_interaction.response.send_message(embed=self.pages[0], view=self)


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
    

    ###### GACHA GUIDE
    # @tree.command(
    #         name = 'moveinfo',
    #         description = 'View info about a move.',
    #         guild = discord.Object(id=SERVER)
    # )
    # async def moveinfo(interaction: discord.Interaction, move: str):
        
    #     moves = list(map(lambda x: x['name'], gacha.BATTLE_MOVES))

    #     if move.lower() not in moves:
    #         embed = discord.Embed(title=f'Move Error', description=f'Could not find move "{move}".', color=ErrorColour)
    #         await interaction.response.send_message(embed=embed, ephemeral=True)
    #         return
        
    #     for battle_move in gacha.BATTLE_MOVES:
    #         if move.lower() == battle_move['name']:
    #             move = battle_move
    #             break
        
    #     if move['name'] in ['academic', 'scheming', 'athleticism', 'fighting', 'empathy', 'influence']:
    #         description = f'**Base Power**: 100%\n**Damage Type**: {move["damage_type"].capitalize()}'

    #     elif move['name'] == 'unity':
    #         description = f'Buffs the **Ability** of all allies by 35% for 5 turns. **Doesn\'t stack.**'

    #     elif move['name'] == 'grit':
        #     description = f'**Base Power**: 50% - 250% Scaling with user\'s % Missing Resolve\n**Damage Type**: Fighting'

        # elif move['name'] == 'impulse':
        #     description = f'**Base Power**: 60%\n**Damage Type**: Athleticism\n**Priority**: +3'

        # elif move['name'] == 'kings command':
        #     description = f'''The user summons a **Pawn** to their team, and is debuffed by -25% **Ability** for the rest of the battle. Fails if there is already an allied **Pawn** alive.
        #     \n{gacha.special_emoji} **__Pawn__**\n
        #     Personality: **Timid**\nMoves: **Scheming, Athleticism, Influence**\n
        #     *All stats are inherited from its creator at 75% of their value.*\n\nTags: Persona'''

        # elif move['name'] == 'inspire':
        #     description = f'Heal the user\'s other allies by 33%.'

        # elif move['name'] == 'study':
        #     description = f'Boosts the user\'s **Mental** by 150% and **Initiative** by 100% for 1 turn.'

        # elif move['name'] == 'kabedon':
        #     description = f'Counters any opponent **Attack**.\n\n**Successful Counter**: Opponent is **stunned** for 1 turn.\n**Failed Counter**: User is **stunned** for 1 turn.'

        # elif move['name'] == 'hate':
        #     description = f'Debuffs the opponent\'s **Ability** by 25% for 4 turns.'

        # elif move['name'] == 'dominate':
        #     description = f'**Base Power**: 200%\n**Damage Type**: Influence\n**Priority**: -3\n\nInflicts **Splash Damage** to the opponent\'s other allies. The user\'s **Ability** is debuffed by 75% for 5 turns after use.'
        
        # elif move['name'] == 'charm':
        #     description = f'Debuffs the opponent\'s **Social** by 33% for 4 turns. If it hasn\'t already been, the user collects the opponent\'s **secret** and heals by 25%.'

        # elif move['name'] == 'shatter':
        #     description = f'**Base Power**: 100%\n**Damage Type**: Influence\n\nGains the following bonuses depending on the number of **secrets** the user has collected:\n- **1+**: **Priority**: +3\n- **2+**: Heals the user for 35% of the damage dealt.\n- **3+**: +100% base power.'

        # elif move['name'] == 'unmask':
        #     description = f'The user transforms into their **Unmasked** form, and heals 20%.'

        # elif move['name'] == 'mask':
        #     description = f'The user transforms back into their base form.'

        # elif move['name'] == 'from the shadows':
        #     description = f'**Priority**: -5\n\n**Traps** the opponent for 3 turns. Then, the user tags out to a random ally (if possible), and if they do, the tagged-in ally becomes **pacified** and **invulnerable** for 1 turn.'

        # elif move['name'] == 'arrogance':
        #     description = f'Boosts the user\'s **Ability** by 40% for 2 turns.'

        # elif move['name'] == 'the perfect existence':
        #     description = f'**__Innate Ability__**\n\nCleanses all debuffs when the user tags in.\nWhen the user takes **fatal damage**, they instead apply the following effects:\n- Recover 50% **Resolve**\n- Gain +50% **Ability** for the rest of the battle.\n- Lose this move'
        
        # elif move['name'] == 'boss orders':
        #     description = f'**__Innate Ability__**\n\nApplies the following buff to all allies when this character is defeated:\n- +50% **Mental**'

        # elif move['name'] == 'provoke':
        #     description = f'The user provokes the opponent, causing them to become **taunted** for 3 turns.\n\n(Taunted: Cannot use non-attacking moves or tag out.)'

        # embed = discord.Embed(title=f'{move["name"].title()}', description=description, color=0xffb2ff)
        # await interaction.response.send_message(embed=embed)


    
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

        if await gacha.getGacha(member) is None:
            embed = discord.Embed(title='Collection Error', description=f'{member.mention} does not have a collection!', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
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
            description = 'View your progress for a series!',
            guild = discord.Object(id=SERVER)
    )
    @app_commands.autocomplete(series=autocomplete_series)
    async def series(interaction: discord.Interaction, series: str, member: discord.Member=None):
        
        if member is None:
            member = interaction.user

        if await gacha.getGacha(member) is None:
            embed = discord.Embed(title='Collection Error', description=f'{member.mention} does not have a collection!', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if not await gacha.get_collection(member, 'names'):
            embed = discord.Embed(title=f'{member.display_name}\'s Collection', description=f'This collection is empty :(', color=ErrorColour)
            embed.set_thumbnail(url=member.display_avatar)
            await interaction.response.send_message(embed=embed)
            return
        if series not in SERIES_LIST:
            embed = discord.Embed(title='Series Error', description=f'**{series}** not found.', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        progress = await gacha.get_series_progress(member, series)
        
        total = len(progress)
        owned = len([x for x in progress if x.level > 0])

        progress = list(map(lambda character: f"{gacha.get_rarity_emoji(character.rarity)} {character.name} {f'**{int(character.level)}** ⭐' if character.level != 0 else '🔒'}", progress))


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

        

    


    ###### SPIN
    @tree.command(
            name = 'spin',
            description = 'Obtain a random gacha character!',
            guild = discord.Object(id=SERVER)
    )
    async def spin(interaction: discord.Interaction):

        remaining_spins = await get_remaining_spins(interaction.user)

        if remaining_spins < 1:
            embed = discord.Embed(title='No Spins Left :(', description=f'You do not have any spins left! Spins refresh in {time_to_next_hour()}.', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if await gacha.getGacha(interaction.user) is None:
            embed = discord.Embed(title='Collection Error', description='You do not have a collection!', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

       
        pull: gacha.Character = await gacha.do_spin(interaction.user)
        await set_remaining_spins(interaction.user, remaining_spins - 1)

        spin = gacha.Spin(interaction, pull)
        await spin.create()

        

    ###### PARTY
    @tree.command(
            name = 'party',
            description = 'View/Edit your active party!',
            guild = discord.Object(id=SERVER)
    )
    async def party(interaction: discord.Interaction, member: discord.Member = None):

        if member is None:
            member = interaction.user

        if await gacha.getGacha(member) is None:
            embed = discord.Embed(title='Collection Error', description=f'{member.mention} does not have a collection!', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await interaction.response.defer()

    
        embed, file = await gacha.partyDisplay(member)



        # edit_button = discord.ui.Button(
        #     emoji='✍️',
        #     style=discord.ButtonStyle.red
        # )
        # clear_button = discord.ui.Button(
        #     label='Clear',
        #     style=discord.ButtonStyle.grey
        # )

        # view = View()
        # view.add_item(edit_button)
        # view.add_item(clear_button)


        # slotSelect = SlotSelect(interaction, embed, file, view)
        # view2 = View()
        # view2.add_item(slotSelect)


        # async def edit_callback(binteraction: discord.Interaction):
        #     if binteraction.user != member:
        #         error = discord.Embed(title='User Error', description='This is not your party!', color=ErrorColour)
        #         await binteraction.response.send_message(embed=error, ephemeral=True)
        #         return

        #     await binteraction.response.edit_message(view=view2)


        # async def clear_callback(cinteraction: discord.Interaction):
        #     if cinteraction.user != member:
        #         error = discord.Embed(title='User Error', description='This is not your party!', color=ErrorColour)
        #         await cinteraction.response.send_message(embed=error, ephemeral=True)
        #         return
            
        #     await gacha.clearParty(member)

        #     embed3 = discord.Embed(title='Party Cleared', description=f'All slots in your Party have been reset.', color=0x5fb964)
        #     await cinteraction.response.send_message(embed=embed3, ephemeral=True)




        # edit_button.callback = edit_callback
        # clear_button.callback = clear_callback

        # if interaction.user == member:
        #     await interaction.followup.send(embed=embed, file=file, view=view)
        # else:
        #     await interaction.followup.send(embed=embed, file=file)
        await interaction.followup.send(embed=embed, file=file)
    

    ###### ADD
    @tree.command(
            name = 'add',
            description = 'Add a character to your party.',
            guild = discord.Object(id=SERVER)
    )
    @app_commands.choices(slot=[
        app_commands.Choice(name='1', value=1), app_commands.Choice(name='2', value=2), app_commands.Choice(name='3', value=3),
        app_commands.Choice(name='4', value=4), app_commands.Choice(name='5', value=5), app_commands.Choice(name='6', value=6)
    ])
    @app_commands.autocomplete(character=autocomplete_collection)
    async def add(interaction: discord.Interaction, slot: app_commands.Choice[int], character: str):
        if await gacha.getGacha(interaction.user) is None:
            embed = discord.Embed(title='Collection Error', description=f'{interaction.user.mention} does not have a collection!', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if character not in CHARACTER_LIST:
            embed = discord.Embed(title='Character Error', description=f'No such character "{character}".', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        collection = await gacha.get_collection(interaction.user, 'names')

        if character not in collection:
            embed = discord.Embed(title='Character Unowned', description=f'You do not own **{character}** :(', color=ErrorColour)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await gacha.edit_slot(interaction.user, f'slot{slot.value}', character)

        embed, file = await gacha.partyDisplay(interaction.user)

        embed.description = f'Successfully added **{character}** to Slot **{slot.value}**!'
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

        level = await gacha.getStars(interaction.user, character)
        if level is None:
            level = 0

        embed: discord.Embed = await gacha.get_character(character, level).display()

        portrait = discord.File(f'Portraits/{character}.jpg', filename='portrait.jpg')
        embed.set_image(url=f'attachment://portrait.jpg')

        await interaction.response.send_message(embed=embed, file=portrait)
        


    # ###### BATTLE
    # @tree.command(
    #         name = 'battle',
    #         description = 'Challenge (either open challenge or specific member) to a battle.',
    #         guild = discord.Object(id=SERVER)
    # )
    # async def battle(interaction: discord.Interaction, member: discord.Member = None):
        
        
    #     if await gacha.in_active_battle(interaction.user) == True:
    #         embed = discord.Embed(title='Battle Error', description=f'You are already participating in a battle!', color=ErrorColour)
    #         await interaction.response.send_message(embed=embed, ephemeral=True)
    #         return
        
    #     userParty = await gacha.getParty(interaction.user)
    #     if userParty[0] is None or userParty[1] is None or userParty[2] is None:
    #         embed = discord.Embed(title='Party Error', description=f'You must have 3 Active Party Members to participate in a battle!', color=ErrorColour)
    #         await interaction.response.send_message(embed=embed, ephemeral=True)
    #         return

    #     if member is None:
    #         desc = 'an open challenge'
    #     else:
    #         desc = f'a challenge to {member.mention}'

    #     embed = discord.Embed(
    #         title= 'Battle Challenge',
    #         description= f'{interaction.user.mention} has issued {desc}!',
    #         color = 0xf637e3
    #     )
    #     embed.set_author(name=f'{interaction.user.display_name}', icon_url=f'{interaction.user.display_avatar}')

    #     acceptButton = discord.ui.Button(emoji='⚔️', style=discord.ButtonStyle.red)

    #     view = View()
    #     view.add_item(acceptButton)

    #     async def accept_callback(binteraction: discord.Interaction):

    #         if binteraction.user == interaction.user:
    #             embed2 = discord.Embed(title='Challenge Error', description='You cannot accept your own challenge!', color=ErrorColour)
    #             await binteraction.response.send_message(embed=embed2, ephemeral=True)
    #             return
            
    #         if member is not None:
    #             if binteraction.user != member:
    #                 embed2 = discord.Embed(title='Challenge Error', description='This challenge was not for you!', color=ErrorColour)
    #                 await binteraction.response.send_message(embed=embed2, ephemeral=True)
    #                 return
    #         if await gacha.in_active_battle(binteraction.user) == True:
    #             embed2 = discord.Embed(title='Battle Error', description=f'You are already participating in a battle!', color=ErrorColour)
    #             await binteraction.response.send_message(embed=embed2, ephemeral=True)
    #             return
                
    #         buserParty = await gacha.getParty(binteraction.user)
    #         if buserParty[0] is None or buserParty[1] is None or buserParty[2] is None:
    #             embed2 = discord.Embed(title='Party Error', description=f'You must have 3 Active Party Members to participate in a battle!', color=ErrorColour)
    #             await binteraction.response.send_message(embed=embed2, ephemeral=True)
    #             return
            
    #         emptyView = View()
    #         await binteraction.response.edit_message(embed=embed, view=emptyView)
            
    #         message = await interaction.original_response()

    #         await battles.doBattle(message, interaction.user, binteraction.user)

    #     acceptButton.callback = accept_callback

    #     await interaction.response.send_message(embed=embed, view=view)
        

    #     await battle

    # ##### CAMPAIGN
    # @tree.command(
    #         name = 'campaign',
    #         description = 'Use your party to battle preset stages and earn rewards!.',
    #         guild = discord.Object(id=SERVER)
    # )
    # async def campaign(interaction: discord.Interaction):
        

    #     userParty = await gacha.getParty(interaction.user)
    #     if userParty[0] is None or userParty[1] is None or userParty[2] is None:
    #         embed = discord.Embed(title='Party Error', description=f'You must have 3 Active Party Members to participate in a battle!', color=ErrorColour)
    #         await interaction.response.send_message(embed=embed, ephemeral=True)
    #         return

    #     await interaction.response.defer()

    #     stage = await gacha.getCampaignStage(interaction.user)
    #     maxStage = await gacha.getMaxStage()

    #     if stage > maxStage:
    #         embed = discord.Embed(title='Campaign Complete!', description=f'Congratulations, {interaction.user.mention}! You have completed all of the current campaign stages! Check back in the future when more stages are added.', color=0x7f5fb9)
    #         await interaction.followup.send(embed=embed)
    #         return
        

    #     embed = await gacha.partyDisplay(interaction.user, True)

    #     file = discord.File(f'Campaign/Stage {stage}.png', filename='party.png')
    #     embed.set_image(url=f'attachment://party.png')


    #     acceptButton = discord.ui.Button(emoji='⚔️', style=discord.ButtonStyle.red)

    #     view = View()
    #     view.add_item(acceptButton)

    #     async def accept_callback(binteraction: discord.Interaction):

    #         if binteraction.user != interaction.user:
    #             embed2 = discord.Embed(title='Error', description='This is not your campaign!', color=ErrorColour)
    #             await binteraction.response.send_message(embed=embed2, ephemeral=True)
    #             return
            
            
    #         emptyView = View()
    #         await binteraction.response.edit_message(embed=embed, view=emptyView, attachments=[])
            
    #         message = await interaction.original_response()

    #         difficulty = await gacha.getStageDifficulty(stage)

    #         await battles.doBattle(message, interaction.user, campaigner, difficulty)

    #     acceptButton.callback = accept_callback

    #     await interaction.followup.send(embed=embed, file=file, view=view)


    ##### STATUS
    @tree.command(
            name = 'status',
            description = 'Check your current status.',
            guild = discord.Object(id=SERVER)
    )
    async def status(interaction: discord.Interaction):

        starpower = await get_starpower(interaction.user)
        spins_left = await get_remaining_spins(interaction.user)

        embed = discord.Embed(title=f'{interaction.user.display_name}\'s Status', description=f'Spins Left: **{spins_left}**.\nSpins refresh in {time_to_next_hour()}.\nStarpower: **{starpower}%**.\nRecharge Rate: **20%/h**.\nSummons Cost: **50%** Starpower.', color=0xd2ac41)
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

        db = sqlite3.connect('stats.sqlite')
        cursor = db.cursor()

        cursor.execute('SELECT name FROM stats')
        names = cursor.fetchall()

        cursor.close()
        db.close()

        db = sqlite3.connect('gacha.sqlite')
        cursor = db.cursor()

        names = tuple([name[0] for name in names])

        missing = []

        cursor.execute('PRAGMA table_info(collection)')
        columns = cursor.fetchall()

        cursor.close()
        db.close()

        columns = [x[1] for x in columns]

        for name in names:
            if name not in columns:
                missing.append(name)

        if not missing:
            await interaction.response.send_message('No missing characters :D')
            return
        
        db = sqlite3.connect('gacha.sqlite')
        cursor = db.cursor()

        for character in missing:
            cursor.execute(f'ALTER TABLE collection ADD COLUMN "{character}" INTEGER')

        db.commit()
        cursor.close()
        db.close()

        missing = '\n'.join(missing)
        await interaction.response.send_message(f'# Missing Characters Added:\n{missing}')


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

    
    ##### WISH
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

            display, pull = await gacha.do_spin(interaction.user)
            rarity = await gacha.get_rarity(pull)

            if rarity == 'shining':
                sh += 1
            elif rarity == 'glowing':
                gl += 1
            elif rarity == 'common':
                c += 1
        
        embed = discord.Embed(title='Spins Simulated', description=f'**{sh}** {gacha.shining_emoji}\n**{gl}** {gacha.glowing_emoji}\n**{c}** {gacha.common_emoji}', color=ErrorColour)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)

        await interaction.followup.send(embed=embed)
        

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

        global CHARACTER_LIST, SERIES_LIST
        CHARACTER_LIST = get_characters()
        SERIES_LIST = get_series()
 
        if not daily.is_running():
            daily.start()

        # Sync Commands
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


async def check_freebie(member: discord.Member):

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT freebie FROM misc WHERE user_id = {member.id}')
    freebie = cursor.fetchone()

    cursor.close()
    db.close()

    if freebie == None:
        freebie = 0
    else:
        freebie = freebie[0]
    
    return freebie

async def set_freebie(member: discord.Member, value: int):

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    sql = ('UPDATE misc SET freebie = ? WHERE user_id = ?')
    val = (value, member.id)
    cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()


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

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    sql = (f'UPDATE misc SET starpower = ? WHERE user_id = ?')
    val = (amount, member.id)
    cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()


async def get_starpower(member: discord.Member) -> int:

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT starpower FROM misc WHERE user_id = {member.id}')
    starpower = cursor.fetchone()[0]

    cursor.close()
    db.close()

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

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT spins_left FROM misc WHERE user_id = {member.id}')
    spins_left = cursor.fetchone()[0]

    cursor.close()
    db.close()

    if spins_left is None:
        spins_left = 10

    return spins_left

async def set_remaining_spins(member: discord.Member, amount: int):

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    sql = (f'UPDATE misc SET spins_left = ? WHERE user_id = ?')
    val = (amount, member.id)
    cursor.execute(sql, val)

    db.commit()
    cursor.close()
    db.close()


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

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute('UPDATE misc SET spins_left = 10')

    db.commit()
    cursor.close()
    db.close()

    await log(f'Refreshed spins at **{dt.datetime.now().strftime("%H:%M")}**.', 1)

def get_characters() -> tuple:

    db = sqlite3.connect('stats.sqlite')
    cursor = db.cursor()

    cursor.execute('SELECT name FROM stats')
    characters = cursor.fetchall()

    cursor.close()
    db.close()

    characters = tuple([character[0] for character in characters])

    return characters

def get_series() -> tuple:

    db = sqlite3.connect('stats.sqlite')
    cursor = db.cursor()

    cursor.execute('SELECT series FROM stats')
    fetched = cursor.fetchall()

    cursor.close()
    db.close()

    list = tuple(set([series[0] for series in fetched]))

    return list

async def slot_choices() -> list[app_commands.Choice[str]]:
    return [app_commands.Choice(name=slot) for slot in [1,2,3,4,5,6]]

async def autocomplete_collection(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:

    collection = await gacha.get_collection(interaction.user, 'names')

    return [app_commands.Choice(name=character, value=character) for character in collection if current.lower() in character.lower()]


async def get_wish(member: discord.Member) -> str:

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT wish FROM misc WHERE user_id = {member.id}')
    wish = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return wish

async def set_wish(member: discord.Member, wish: str) -> str:

    db = sqlite3.connect('gacha.sqlite')
    cursor = db.cursor()

    if wish is None:
        sql = f'UPDATE misc SET wish = null WHERE user_id = ?'
        val = (member.id,)
    else:
        sql = f'UPDATE misc SET wish = ? WHERE user_id = ?'
        val = (wish, member.id)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

async def autocomplete_series(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    return [app_commands.Choice(name=series, value=series) for series in SERIES_LIST if current.lower() in series.lower()]

async def autocomplete_character(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    return [app_commands.Choice(name=character, value=character) for character in CHARACTER_LIST if current.lower() in character.lower()]