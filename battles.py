import discord
import sqlite3
import random
import bot
import gacha
import math
import copy
from typing import Union
from PIL import Image
from io import BytesIO
from collections import defaultdict
import asyncio
from discord.utils import get
from discord.ui import Select, View
from config import TOKEN, ErrorColour
from config import SERVER
from config import DEBUG

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

class Personality():

    def __init__(self, name, weaknesses):
        ...


class Character():

    def __init__(self, owner: discord.Member, name: str, personality: Personality, moves: list, resolve: int, mental: int, physical: int, social: int, initiative: int, support: tuple, tags: list, ephemeral: bool=False):
        self.owner = owner
        self.battle = None

        self.name = name
        self.personality = personality
        self.moves = [move for move in moves if move['type'] != 'innate']
        self.passives = [move for move in moves if move['type'] == 'innate']


        self.max_resolve = resolve
        self.resolve = resolve
        self.mental = mental
        self.physical = physical
        self.social = social
        self.initiative = initiative

        self.support = support
        self.tags = tags

        self.buffs: list = []
        self.statuses: list = []

        self.ephemeral = ephemeral
        self.secrets_collected = []
        

    def clone(self):

        clone = Character(self.owner, self.name, self.personality, self.moves.copy(), self.max_resolve, self.mental, self.physical, self.social, self.initiative, self.support, self.tags)
        clone.resolve = self.resolve
        clone.buffs = self.buffs.copy()
        clone.statuses = self.statuses.copy()
        return clone

    def set_battle(self, battle):
        self.battle: Battle = battle

    async def inflict_damage(self, amount: int):
        self.resolve -= amount

    async def heal(self, amount: int):
        self.resolve += amount



    def __str__(self) -> str:
        if self.resolve < 1:
            return f'» *{self.name}* :x:'
        
        else:
            battle: Battle = self.battle

            if self.owner == battle.player1:

                if len(battle.player1_active_char) == 1 and battle.player1_active_char[0] == self:
                    return f'**» *__{self.name}__*** - **{self.resolve}**:heart:'
                
            else:
                if len(battle.player2_active_char) == 1 and battle.player2_active_char[0] == self:
                    return f'**» *__{self.name}__*** - **{self.resolve}**:heart:'
                
            return f'» *{self.name}* - **{self.resolve}**:heart:'
        
    
    def get_stat(self, stat_name: str) -> int:

        if stat_name == 'mental':
            base_stat = self.mental
        elif stat_name == 'physical':
            base_stat = self.physical
        elif stat_name == 'social':
            base_stat = self.social
        elif stat_name == 'initiative':
            base_stat = self.initiative

        for buff in self.buffs:

            if stat_name == buff['stat'] or buff['stat'] == 'ability':
                base_stat = base_stat * buff['multiplier']

        stat = round(base_stat)
        if stat < 0:
            stat = 0

        return stat
    

    def has_status(self, status_name: str) -> bool:

        for status in self.statuses:

            if status['name'] == status_name:
                return True
        
        return False

    def has_buff(self, buff_source: str) -> bool:

        for buff in self.buffs:

            if buff['source'] == buff_source:
                return True
        
        return False
        

    async def calculate_damage_taken(self, move: dict, power: int) -> int:

        if self.has_status('invulnerable'):
            return 0

        if move['defense_stat'] == 'mental':
            defense = self.get_stat('mental')

        elif move['defense_stat'] == 'physical':
            defense = self.get_stat('physical')

        elif move['defense_stat'] == 'social':
            defense = self.get_stat('social')
        
        elif move['defense_stat'] == 'resolve':
            defense = self.resolve

        elif move['defense_stat'] == 'initiative':
            defense = self.get_stat('initiative')

        damage = power / ((defense + 10) / 40)

        if move in self.personality.weaknesses:
            damage += damage * 0.5

        # 20% variance in final damage number
        variance = random.randint(80, 120)
        variance = variance / 100
        damage = round(damage * variance)

        if damage < 1:
            damage = 0

        # elif damage < round(power * 0.2):
        #     damage = round(power * 0.2)

        return damage
    

    async def calculate_heal_amount(self, percentage: float) -> int:

        amount = round(self.max_resolve * percentage)
        missing_resolve = self.max_resolve - self.resolve

        if amount > missing_resolve:
            amount = missing_resolve

        return amount
    

    async def check_defeated(self) -> bool:

        if self.resolve < 1:

            self.resolve = 0

            await self.trigger_event('fatal_damage')

            if self.resolve > 0:
                return

            battle: Battle = self.battle

            if self.owner == battle.player1:
                team = battle.player1_team
                active_character = battle.player1_active_char
                alive = battle.player1_alive_characters

            elif self.owner == battle.player2:
                team = battle.player2_team
                active_character = battle.player2_active_char
                alive = battle.player2_alive_characters

            active_character.clear()
            alive.pop(alive.index(self))

            if self.ephemeral:
                team.pop(team.index(self))

            await self.trigger_event('defeated')

            return True
        
        return False
    

    async def trigger_event(self, event: str):

        for passive in self.passives:
            for effect in passive['effects']:
                if effect['trigger'] == event:
                    await effect['effect'](self, self.battle)








class Battle():

    def __init__(self, message: discord.Message, player1: discord.Member, player2: discord.Member, player1_team: list, player2_team: list) -> None:
        
        self.message = message

        self.turn_count =  0
        self.turn_log: list = []

        self.player1 = player1
        self.player2 = player2

        self.player1_team: list = player1_team
        self.player2_team: list = player2_team

        for char in self.player1_team:
            char.set_battle(self)
        for char in self.player2_team:
            char.set_battle(self)

        self.player1_alive_characters: list = player1_team.copy()
        self.player2_alive_characters: list = player2_team.copy()

        self.player1_active_char: list = []
        self.player2_active_char: list = []

        self.player1_action: dict = {}
        self.player2_action: dict = {}

        self.player1_counter_success: list = []
        self.player2_counter_success: list = []

        self.force_end: bool = False


    async def clone(self):

        player1_team = []
        player2_team = []

        for char in self.player1_team:
            new_char = char.clone()
            player1_team.append(new_char)
        for char in self.player2_team:
            new_char = char.clone()
            player2_team.append(new_char)


        clone = Battle(None, self.player1, self.player2, player1_team, player2_team)
    

        for char in clone.player1_team:
            char.set_battle(clone)
        for char in clone.player2_team:
            char.set_battle(clone)

        clone.turn_count = self.turn_count

        clone.player1_alive_characters.clear()
        clone.player2_alive_characters.clear()
        
        # For each alive character, append the corresponding clone to the clone battle
        for char in self.player1_alive_characters:
            for char_2 in player1_team:
                if char.name == char_2.name:
                    clone.player1_alive_characters.append(char_2)

        for char in self.player2_alive_characters:
            for char_2 in player2_team:
                if char.name == char_2.name:
                    clone.player2_alive_characters.append(char_2)

        # Same as above with the active character
        for char in self.player1_active_char:
            for char_2 in player1_team:
                if char.name == char_2.name:
                    clone.player1_active_char.append(char_2)

        for char in self.player2_active_char:
            for char_2 in player2_team:
                if char.name == char_2.name:
                    clone.player2_active_char.append(char_2)

        return clone




    async def display(self, view: Union[View, None], show_turn_events: bool = False) -> None:

        embed = discord.Embed(
        title=f'BATTLE: {self.player1.display_name} vs. {self.player2.display_name}',
        color = 0xf87d72
        )  

        player1_team_display = '\n'.join([str(character) for character in self.player1_team])
        player2_team_display = '\n'.join([str(character) for character in self.player2_team])

        embed.add_field(name=f'{self.player1.display_name}', value=player1_team_display, inline=True)
        embed.add_field(name=f'{self.player2.display_name}', value=player2_team_display, inline=True)

        if show_turn_events == True:
            event_log = ''
            for event in self.turn_log:
                event_log += f'{event}\n'

            embed.add_field(name=f'\n__Turn {self.turn_count}__', value=f'{event_log}', inline=False)

        if view is None:
            await self.message.edit(embed=embed, view=None)
            return
        
        await self.message.edit(embed=embed, view=view)


    async def get_character(self, player: discord.Member, character_name: str) -> Character:

        if player == self.player1:
            team = self.player1_team
        elif player == self.player2:
            team = self.player2_team

        for character in team:
            if character.name == character_name:
                return character

    
    async def switch_character(self, player: discord.Member, character_name: str) -> None:

        if player == self.player1:
            active_char = self.player1_active_char
            team = self.player1_team
        elif player == self.player2:
            active_char = self.player2_active_char
            team = self.player2_team

        target = None
        for character in team:
            if character.name == character_name:
                target: Character = character
                break

        active_char.clear()
        active_char.append(target)
        
        self.turn_log.append(f'**{player.mention}** tagged in **{target.name}**!')

        await target.trigger_event('switch_in')

    
    async def do_attack(self, player: discord.Member, move: dict):

        if player == self.player1:
            opponent_action = self.player2_action
            opponent_counter_success = self.player2_counter_success
            active_character = self.player1_active_char
            defender: Character = self.player2_active_char[0]
        
        elif player == self.player2:
            opponent_action = self.player1_action
            opponent_counter_success = self.player1_counter_success
            active_character = self.player2_active_char
            defender: Character = self.player1_active_char[0]

        if len(active_character) == 0:
            return
        
        attacker: Character = active_character[0]

        # Check if move is countered
        if opponent_action['action'] == 'move' and opponent_action['move']['type'] == 'counter':
            opponent_move = opponent_action['move']

            if opponent_move['counter_damage_type'] == 'any' or opponent_move['counter_damage_type'] == move['damage_type']:
                
                self.turn_log.append(f'**{attacker.name}** used **{move["name"].title()}**!')
                self.turn_log.append(f'**{defender.name}** countered with **{opponent_move["name"].title()}**!')

                await opponent_move['on_success'](self, defender.owner)
                opponent_counter_success.clear()
                opponent_counter_success.append(True)

                return

    
        
        # Calculating move power
        if move['attack_stat'] == 'mental':
            power = attacker.get_stat('mental')

        elif move['attack_stat'] == 'physical':
            power = attacker.get_stat('physical')

        elif move['attack_stat'] == 'social':
            power = attacker.get_stat('social')
        
        elif move['attack_stat'] == 'resolve':
            power = attacker.resolve

        elif move['attack_stat'] == 'missing_resolve':
            power = attacker.max_resolve - attacker.resolve

        elif move['attack_stat'] == 'initiative':
            power = attacker.get_stat('initiative')

        if callable(base_power := move['base_power']):
            base_power = base_power(self, player)
        
        power = power * base_power


        # Deal damage to the defender
        damage = await defender.calculate_damage_taken(move, power)
        await defender.inflict_damage(damage)


        # Logging attack events
        self.turn_log.append(f'**{attacker.name}** used **{move["name"].title()}**!')
        if move['damage_type'] in defender.personality.weaknesses:
            self.turn_log.append(f'**CRITICAL HIT!!**\n**{defender.name}** took **{damage}** damage!')
        else:
            self.turn_log.append(f'**{defender.name}** took **{damage}** damage!')

        # Check if the attack was fatal
        fatal = await defender.check_defeated()

        if fatal:
            self.turn_log.append(f'**{defender.name}** was defeated!')


        # Run any on-hit effects
        if move.get('on_hit', None) is not None:
            await move['on_hit'](self, player, damage)

        


    
    async def do_heal(self, player: discord.Member, move: dict):

        if player == self.player1:
            active_character = self.player1_active_char
            alive_characters = self.player1_alive_characters
        
        elif player == self.player2:
            active_character = self.player2_active_char
            alive_characters = self.player2_alive_characters

        if len(active_character) == 0:
            return
        
        user: Character = active_character[0]

        if move['target'] == 'self':
            targets = [user]

        elif move['target'] == 'allies':
            targets = alive_characters.copy()

        elif move['target'] == 'other_allies':
            targets = alive_characters.copy()
            targets.pop(targets.index(user))

        heal_power = move['heal_power']
    
        self.turn_log.append(f'**{user.name}** used **{move["name"].title()}**!')
        for target in targets:
            heal_amount = await target.calculate_heal_amount(heal_power)
            await target.heal(heal_amount)

            self.turn_log.append(f'**{target.name}** recovered **{heal_amount}** Resolve!')
        


    async def apply_buff(self, player: discord.Member, move: dict):

        if player == self.player1:
            active_character = self.player1_active_char
            alive_characters = self.player1_alive_characters
            opponent_active_character = self.player2_active_char
        
        elif player == self.player2:
            active_character = self.player2_active_char
            alive_characters = self.player2_alive_characters
            opponent_active_character = self.player1_active_char

        if len(active_character) == 0:
            return
        
        user: Character = active_character[0]

        if move['target'] == 'self':
            targets = [user]

        elif move['target'] == 'allies':
            targets = alive_characters.copy()

        elif move['target'] == 'opponent':
            targets = opponent_active_character.copy()

        self.turn_log.append(f'**{user.name}** used **{move["name"].title()}**!')

        if not targets:
            return
        
        for target in targets:
            for buff in move['buffs']:
                if buff.get('can_stack', True) == False and target.has_buff(buff['source']):
                    continue

                target.buffs.append(buff.copy())

                if buff['multiplier'] > 1:
                    self.turn_log.append(f'**{target.name}** had their **{buff["stat"].title()}** boosted!')
                else:
                    self.turn_log.append(f'**{target.name}** had their **{buff["stat"].title()}** weakened!')
        
        # Run any on-hit effects
        if move.get('on_hit', None) is not None:
            await move['on_hit'](self, player)



    async def prepare_counter(self, player: discord.Member, move: dict):

        if player == self.player1:
            counter_success = self.player1_counter_success
            active_character = self.player1_active_char
        
        elif player == self.player2:
            counter_success = self.player2_counter_success
            active_character = self.player2_active_char

        if len(active_character) == 0:
            return
        
        counter_success.append(False)
        
        user: Character = active_character[0]

        self.turn_log.append(f'**{user.name}** is preparing **{move["name"].title()}**...')




    async def new_turn(self) -> None:

        self.turn_count += 1
        self.turn_log.clear()

        self.player1_action.clear()
        self.player2_action.clear()

        self.player1_counter_success.clear()
        self.player2_counter_success.clear()

        for character in self.player1_alive_characters:

            # Buffs
            to_pop = []

            for buff in character.buffs:
                buff['duration'] -= 1

                if buff['duration'] < 1:
                    to_pop.append(buff)
            
            for popped in to_pop:
                character.buffs.pop(character.buffs.index(popped))
            
            # Statuses
            to_pop = []

            for status in character.statuses:
                status['duration'] -= 1

                if status['duration'] < 1:
                    to_pop.append(status)
            
            for popped in to_pop:
                character.statuses.pop(character.statuses.index(popped))

            
                
        for character in self.player2_alive_characters:
            to_pop = []

            for buff in character.buffs:
                buff['duration'] -= 1

                if buff['duration'] < 1:
                    to_pop.append(buff)
            
            for popped in to_pop:
                character.buffs.pop(character.buffs.index(popped))


            # Statuses
            to_pop = []

            for status in character.statuses:
                status['duration'] -= 1

                if status['duration'] < 1:
                    to_pop.append(status)
            
            for popped in to_pop:
                character.statuses.pop(character.statuses.index(popped))







    async def faster_character(self) -> discord.Member:

        # SWITCHING TAKES PRIORITY OVER OTHER MOVES
        if len(self.player1_action) > 0 and self.player1_action['action'] == 'switch':
            return self.player1
        elif len(self.player2_action) > 0 and self.player2_action['action'] == 'switch':
            return self.player2
        
        # STUNNED CHARACTERS GO LAST BY DEFAULT
        if self.player1_action and self.player1_action['action'] in ['stunned', 'pass']:
            return self.player2
        elif self.player2_action and self.player2_action['action'] in ['stunned', 'pass']:
            return self.player1

        
        # CHECK FOR MOVE PRIORITY
        player1_move: dict = self.player1_action['move']
        player2_move: dict = self.player2_action['move']

        player1_priority = player1_move.get('priority', 0)
        player2_priority = player2_move.get('priority', 0)

        if callable(player1_priority):
            player1_priority = await player1_priority(self, self.player1)
        if callable(player2_priority):
            player2_priority = await player2_priority(self, self.player2)

        if player1_priority != player2_priority:

            if player1_priority > player2_priority:
                return self.player1
            else:
                return self.player2


        # IF NO SWITCHES, CHECK CHARACTER INITIATIVES TO DETERMINE MOVE ORDER
        player1_initiative = self.player1_active_char[0].get_stat('initiative')
        player2_initiative = self.player2_active_char[0].get_stat('initiative')

        if player1_initiative == player2_initiative:
            return random.choice([self.player1, self.player2])
        
        elif player1_initiative > player2_initiative:
            return self.player1
        
        else:
            return self.player2
    

    async def get_possible_moves(self, player: discord.Member) -> list:
        
        possible_moves = []

        if player == self.player1:
            alive_characters = self.player1_alive_characters
            active_character = self.player1_active_char

        elif player == self.player2:
            alive_characters = self.player2_alive_characters
            active_character = self.player2_active_char

        if len(active_character) == 1:
            active: Character = active_character[0]

            if active.has_status('stun'):
                possible_moves.append({'action': 'stunned'})
                return possible_moves

            for move in active.moves:
                if move['type'] == 'attack' and active.has_status('pacified'):
                    continue

                if move['type'] != 'attack' and active.has_status('taunted'):
                    continue

                possible_moves.append({'action': 'move', 'move': move})
        
        for character in alive_characters:

            if len(active_character) == 1 and active_character[0] == character:
                continue
            
            if active_character:
                active: Character = active_character[0]
                if active.has_status('trapped') or active.has_status('taunted'):
                    continue
                
            possible_moves.append({'action': 'switch', 'target': character.name})

        return possible_moves
        




    async def choose_move(self, player: discord.Member) -> View:

        if player == self.player1:
            team = self.player1_team
            alive_characters = self.player1_alive_characters
            active_character = self.player1_active_char
            action = self.player1_action
        
        elif player == self.player2:
            team = self.player2_team
            alive_characters = self.player2_alive_characters
            active_character = self.player2_active_char
            action = self.player2_action

        view = View()

        # Checks if there is an active character
        if len(active_character) == 1:
            active: Character = active_character[0]

            if active.has_status('stun'):
                action['action'] = 'stunned'
                return

            ########## MOVE SELECT
            move_select = discord.ui.Select(placeholder=f'{player.display_name}: Select a Move', options=[])

            for move in active.moves:
                
                if move['type'] == 'attack' and active.has_status('pacified'):
                    continue
                if move['type'] != 'attack' and active.has_status('taunted'):
                    continue

                move_select.append_option(discord.SelectOption(
                    label=f'{move["name"].title()}',
                    ))
            
            if move_select.options:    
                view.add_item(move_select)

            async def move_select_callback(interaction: discord.Interaction):
                if interaction.user != player:
                    embed = discord.Embed(title='Turn Error', description=f'It is not your turn to choose!', color=bot.ErrorColour)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
                
                selected_move_name: str = move_select.values[0]
                selected_move = [move for move in active.moves if move['name'] == selected_move_name.lower()]
                selected_move = selected_move[0]

                # Save action chosen
                action['action'] = 'move'
                action['move'] = selected_move

                embed = discord.Embed(title='Selected Move', description=f'You have selected **{move_select.values[0]}**!', color=0x51a95e)
                await interaction.response.send_message(embed=embed, ephemeral=True)

            move_select.callback = move_select_callback


            # If the current active character has a switch-banning status, the player cannot switch
            if active.has_status('trapped') or active.has_status('taunted'):
                if view.children:
                    return view
            
                action['action'] = 'pass'
                return

        
        # If there is only 1 alive character, and it is active, the player cannot switch
        if len(alive_characters) == 1 and len(active_character) == 1:
            if view.children:
                return view
            
            action['action'] = 'pass'
            return


        ########### CHARACTER SWITCH
        switch_select = discord.ui.Select(placeholder=f'{player.display_name}: Switch Characters', options=[])
        for char in alive_characters:
            if char in active_character:
                continue

            switch_select.append_option(discord.SelectOption(
                label=f'{char.name}',
                ))
        
        view.add_item(switch_select)

        async def switch_select_callback(interaction: discord.Interaction):
            if interaction.user != player:
                embed = discord.Embed(title='Turn Error', description=f'It is not your turn to choose!', color=bot.ErrorColour)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            selected_character = await self.get_character(player, switch_select.values[0])

            # Save action chosen
            action['action'] = 'switch'
            action['target'] = selected_character.name

            embed = discord.Embed(title='Switched Character', description=f'You have selected **{switch_select.values[0]}**!', color=0x51a95e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        switch_select.callback = switch_select_callback
        ##################

        return view
    

    async def handle_turn(self) -> None:

        first_mover = await self.faster_character()

        if first_mover == self.player1:
            first_mover_action = self.player1_action

            second_mover = self.player2
            second_mover_action = self.player2_action

        else:
            first_mover_action = self.player2_action

            second_mover = self.player1
            second_mover_action = self.player1_action


        used_moves = []
        if len(first_mover_action) != 0:
            used_moves.append([first_mover, first_mover_action])
        if len(second_mover_action) != 0:
            used_moves.append([second_mover, second_mover_action])


        for used_move in used_moves:
            player = used_move[0]
            action = used_move[1]

            if action['action'] == 'switch':
                await self.switch_character(player, action['target'])

            elif action['action'] == 'move':
                move = action['move']

                if move['type'] == 'attack':
                    await self.do_attack(player, move)

                elif move['type'] == 'heal':
                    await self.do_heal(player, move)
                
                elif move['type'] == 'buff':
                    await self.apply_buff(player, move)

                elif move['type'] == 'counter':
                    await self.prepare_counter(player, move)

                elif move['type'] == 'effect':
                    await move['effect'](self, player)

            
            elif action['action'] == 'stunned':

                if player == self.player1:
                    active_char = self.player1_active_char
                elif player == self.player2:
                    active_char = self.player2_active_char

                if active_char:
                    active_char = active_char[0]
                    self.turn_log.append(f'**{active_char.name}** is **stunned** and unable to move!')

            elif action['action'] == 'pass':

                if player == self.player1:
                    active_char = self.player1_active_char
                elif player == self.player2:
                    active_char = self.player2_active_char

                if active_char:
                    active_char = active_char[0]
                    self.turn_log.append(f'**{active_char.name}** couldn\'t move.')

        
        if self.player1_counter_success:
            if self.player1_counter_success[0] == False and self.player1_active_char:
                active_char: Character = self.player1_active_char[0]
                self.turn_log.append(f'**{active_char.name}\'s** counter failed!')

                await self.player1_action['move']['on_fail'](self, self.player1)

        if self.player2_counter_success:
            if self.player2_counter_success[0] == False and self.player2_active_char:
                active_char: Character = self.player2_active_char[0]
                self.turn_log.append(f'**{active_char.name}\'s** counter failed!')

                await self.player2_action['move']['on_fail'](self, self.player2)




    

##########################################################################################

PERSONALITIES = [Personality('cold', ['scheming', 'empathy']), Personality('bold', ['academic', 'fighting']), Personality('savant', ['athleticism', 'influence']), 
                 Personality('cunning', ['influence', 'empathy']), Personality('benevolent', ['scheming', 'fighting']), Personality('timid', ['athleticism', 'empathy']),
                 Personality('explosive', ['academic', 'scheming']), Personality('reserved', ['athleticism', 'fighting']), Personality('selfish', ['academic', 'influence']),
                 Personality('apathetic', [])]

########################################################################################


async def doBattle(message: discord.Message, player1: discord.Member, player2: discord.Member, difficulty: str=None, gauntlet: bool=False):
    
    forfeit = False
    winner = None

    player1team = await getStats(player1, player2)
    player2team = await getStats(player2, player1)

    battle = Battle(message, player1, player2, player1team, player2team)
    await battle.display(None)

    # GAME LOOP
    while True:

        await asyncio.sleep(1)

        await battle.new_turn()

        # Selecting turn actions
        view = await battle.choose_move(player1)

        if view is not None:
            await battle.display(view)

            timeout_counter = 0
            while len(battle.player1_action) == 0:
                await asyncio.sleep(1)

                timeout_counter += 1
                if timeout_counter > 119:
                    forfeit = True
                    winner = player2
                    loser = player1
                    break

                if battle.force_end:
                    break
            
            if forfeit or battle.force_end:
                break

        # Check if player 2 is the AI (Campaign)
        if player2 != bot.campaigner:
            # If not, repeat selection for p2
            view = await battle.choose_move(player2)

            if view is not None:
                await battle.display(view)

                timeout_counter = 0
                while len(battle.player2_action) == 0:
                    await asyncio.sleep(1)
                    timeout_counter += 1

                    if timeout_counter > 119:
                        forfeit = True
                        winner = player1
                        loser = player2
                        break

                    if battle.force_end:
                        break
                
                if forfeit or battle.force_end:
                    break

        
        else:
            battle.player2_action = await get_battle_decision(battle, difficulty)
            await asyncio.sleep(1)

        await battle.handle_turn()
        await battle.display(None, True)

        await asyncio.sleep(len(battle.turn_log) * 2)


        if len(battle.player1_active_char) == 0 or len(battle.player2_active_char) == 0:

            battle.player1_action.clear()
            battle.player2_action.clear()
            battle.turn_log.clear()

            if len(battle.player1_alive_characters) == 0 or len(battle.player2_alive_characters) == 0:
                break

            if len(battle.player1_active_char) == 0:
                view = await battle.choose_move(player1)
                await battle.display(view)

                timeout_counter = 0
                while len(battle.player1_action) == 0:
                    await asyncio.sleep(1)

                    timeout_counter += 1
                    if timeout_counter > 119:
                        forfeit = True
                        winner = player2
                        loser = player1
                        break

                    if battle.force_end:
                        break
                
                if forfeit or battle.force_end:
                    break

            if len(battle.player2_active_char) == 0:

                if player2 != bot.campaigner:
                    view = await battle.choose_move(player2)
                    await battle.display(view)

                    timeout_counter = 0
                    while len(battle.player2_action) == 0:
                        await asyncio.sleep(1)

                        timeout_counter += 1
                        if timeout_counter > 119:
                            forfeit = True
                            winner = player1
                            loser = player2
                            break

                        if battle.force_end:
                            break
                    
                    if forfeit or battle.force_end:
                        break
                        
                else:
                    battle.player2_action = await get_battle_decision(battle, difficulty)
                    await asyncio.sleep(1)

            await battle.handle_turn()
            await battle.display(None, True)

            await asyncio.sleep(len(battle.turn_log) * 2)


    if battle.force_end:
        return

    if winner is None:
        if len(battle.player1_alive_characters) == 0:
            winner = player2
            loser = player1
        else:
            winner = player1
            loser = player2

    embed = discord.Embed(
    title=f'BATTLE: {battle.player1.display_name} vs. {battle.player2.display_name}',
    color = 0xf87d72
    )
    embed.add_field(name=f'{battle.player1.display_name}', value=f'{str(battle.player1_team[0])}\n{str(battle.player1_team[1])}\n{str(battle.player1_team[2])}', inline=True)
    embed.add_field(name=f'{battle.player2.display_name}', value=f'{str(battle.player2_team[0])}\n{str(battle.player2_team[1])}\n{str(battle.player2_team[2])}', inline=True)

    if forfeit:
        embed.add_field(name=f'WINNER:', value=f'{winner.mention} 🏆\n({loser.mention} forfeit by inactivity.)', inline=False)
    else:
        embed.add_field(name=f'WINNER:', value=f'{winner.mention} 🏆', inline=False)
    
    await message.edit(embed=embed, view=None)

    if player2 == bot.campaigner and player1 == winner:
        await gacha.advanceStage(player1, message)

    if gauntlet:
        await bot.set_br_match_result(winner, loser, embed)


async def getStats(member: discord.Member, opponent: discord.Member=None):

    if member != bot.campaigner:
        party = await gacha.getParty(member)

        char1_level = math.trunc(await gacha.getStars(member, party[0]))
        char2_level = math.trunc(await gacha.getStars(member, party[1]))
        char3_level = math.trunc(await gacha.getStars(member, party[2]))
    
    else:
        campaignParty = await gacha.getCampaignParty(opponent)
        party = campaignParty[0]

        char1_level = campaignParty[1][0]
        char2_level = campaignParty[1][1]
        char3_level = campaignParty[1][2]

    char_list = []

    db = sqlite3.connect('stats.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT * FROM stats WHERE name = "{party[0]}"')
    char1 = cursor.fetchall()
    char1 = char1[0]
    char1 = (char1_level,) + char1
    char_list.append(char1)

    cursor.execute(f'SELECT * FROM stats WHERE name = "{party[1]}"')
    char2 = cursor.fetchall()
    char2 = char2[0]
    char2 = (char2_level,) + char2
    char_list.append(char2)

    cursor.execute(f'SELECT * FROM stats WHERE name = "{party[2]}"')
    char3 = cursor.fetchall()
    char3 = char3[0]
    char3 = (char3_level,) + char3
    char_list.append(char3)

    cursor.close()
    db.close()
    
    # CHARACTER BUFFS
    buffs = []

    if member != bot.campaigner:
        faction = await bot.get_faction(member)
        try:
            strength = await bot.getLevel(faction, 'strength')
        except:
            strength = 0

        if strength >= 3:
            buffs.append([char1[0], 1.1, 1.1, 1.1, 1.1, 1.1])
            buffs.append([char2[0], 1.1, 1.1, 1.1, 1.1, 1.1])
            buffs.append([char3[0], 1.1, 1.1, 1.1, 1.1, 1.1])
        else:
            buffs.append([char1[0], 1.0, 1.0, 1.0, 1.0, 1.0])
            buffs.append([char2[0], 1.0, 1.0, 1.0, 1.0, 1.0])
            buffs.append([char3[0], 1.0, 1.0, 1.0, 1.0, 1.0])
    else:
        buffs.append([char1[0], 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
        buffs.append([char2[0], 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
        buffs.append([char3[0], 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])

    # FOR EACH CHARACTER'S SUPPORT
    for index0, char in enumerate(party):

        if member != bot.campaigner:

            level = await gacha.getStars(member, char)
        else:
            level = campaignParty[1][index0]

        support = await gacha.getSupport(char, level)

        if support is None:
            continue

        # CHECK IF EACH CHARACTER HAS THE SUPPORTED TAG
        for index in range(3):

            target = party[index]
            targetTags = await gacha.getTags(target)
            if targetTags is None:
                continue

            if isinstance(support[2], str) == True:


                if support[2] in targetTags:
                    
                    if support[1] == 'resolve':
                        buffs[index][1] += support[0]
                    if support[1] == 'mental':
                        buffs[index][2] += support[0]
                    if support[1] == 'physical':
                        buffs[index][3] += support[0]
                    if support[1] == 'social':
                        buffs[index][4] += support[0]
                    if support[1] == 'initiative':
                        buffs[index][5] += support[0]
                    if support[1] == 'ability':
                        buffs[index][2] += support[0]
                        buffs[index][3] += support[0]
                        buffs[index][4] += support[0]
                        buffs[index][5] += support[0]
                    
                    #print(f'Applied {char}\'s {support[0]} buff to {buffs[index][0]}')
            
            else:
                if support[2][0] in targetTags or support[2][1] in targetTags:
                    
                    if support[1] == 'resolve':
                        buffs[index][1] += support[0]
                    if support[1] == 'mental':
                        buffs[index][2] += support[0]
                    if support[1] == 'physical':
                        buffs[index][3] += support[0]
                    if support[1] == 'social':
                        buffs[index][4] += support[0]
                    if support[1] == 'initiative':
                        buffs[index][5] += support[0]
                    if support[1] == 'ability':
                        buffs[index][2] += support[0]
                        buffs[index][3] += support[0]
                        buffs[index][4] += support[0]
                        buffs[index][5] += support[0]
                    
                    #print(f'Applied {char}\'s {support[0]} buff to {buffs[index][0]}')


    # CHARACTER STATS
    team = []

    for index, char in enumerate(char_list):
        level = char[0]
        growth = char[9] * (level - 1)

        name = char[1]
        personality = await get_personality_obj(char[2])
        moveset: str = char[3]
        moveset = moveset.split(', ')
        moves = [move.copy() for move in BATTLE_MOVES if move['name'] in moveset]

        resolve = round((char[4] + (growth * 2)) * buffs[index][1])
        mental = round((char[5] + growth) * buffs[index][2])
        physical = round((char[6] + growth) * buffs[index][3])
        social = round((char[7] + growth) * buffs[index][4])
        initiative = round((char[8] + growth) * buffs[index][5])

        support_number = char[10]
        support_stat = char[11]
        support_tags = char[12]
        support_tags = support_tags.split(', ')

        if level >= 4:
            support_number += support_number * 0.5
            if len(support_tags) == 1:
                support_tags = support_tags[0]

        else:
            support_tags = support_tags[0]

        support = (support_number, support_stat, support_tags)

        tags = char[13]

        charObj = Character(member, name, personality, moves, resolve, mental, physical, social, initiative, support, tags)
        team.append(charObj)


    return team

async def get_personality_obj(personality_name: str) -> Personality:

    for personality in PERSONALITIES:

        if personality.name == personality_name:
            return personality
        
async def get_battle_decision(battle: Battle, difficulty: str) -> dict:

    decision = None

    if difficulty == 'easy': #or difficulty == 'medium':
        decision = random.choice(await battle.get_possible_moves(bot.campaigner))

    elif difficulty == 'medium':
        possible_moves = await battle.get_possible_moves(bot.campaigner)
        opponent_possible_moves = await battle.get_possible_moves(battle.player1)
        move_scores = []

        for move in possible_moves:

            if move['action'] == 'switch':
                if battle.player1_active_char and battle.player1_active_char[0].name.lower() == 'horikita manabu' and not battle.player1_active_char[0].has_status('stun'):
                    move_scores.append([move, random.choice([-9000, 9000])])

                continue

            if move['action'] == 'move' and move['move']['name'].lower() == 'kabedon' and battle.player1_active_char and not battle.player1_active_char[0].has_status('stun'):
                move_scores.append([move, random.choice([-9000, 2000])])
                continue

            move_score = 0

            for opp_move in opponent_possible_moves:
                copy_gamestate = await battle.clone()

                copy_gamestate.player2_action = move
                copy_gamestate.player1_action = opp_move

                await copy_gamestate.handle_turn()

                if len(copy_gamestate.player1_active_char) == 0:
                    move_score += 1000
                    continue

                if len(copy_gamestate.player2_active_char) == 0:
                    move_score += -1000
                    continue

                my_char: Character = copy_gamestate.player2_active_char[0]
                opp_char: Character = copy_gamestate.player1_active_char[0]

                move_score += my_char.resolve - opp_char.resolve

            move_scores.append([move, move_score])

        if len(move_scores) == 0:
            decision = random.choice(possible_moves)
            return decision
        
        move_scores = sorted(move_scores, key=lambda x: x[1], reverse=True)
        decision = move_scores[0][0]

        

    return decision




##################### UNIQUE MOVE FUNCTIONS
async def recharge_speed(character: Character, amount: int, **kwargs):
    await character.charge_speed(amount)

async def splash_damage(character: Character, rate: float, **kwargs):
    for opponent in kwargs['targets']:
        damage = round(kwargs['damage_inflicted'] * rate)
        await opponent.inflict_damage(damage)


################### MOVE DEFINITIONS
def attribute_fast(value: int) -> dict:
    return {'name': 'fast', 'on_hit': [{'effect': recharge_speed, 'value': value}]}
def attribute_splash(value: float) -> dict:
    return {'name': 'splash', 'on_hit': [{'effect': 'splash_damage', 'value': value}]}


################### DEFINE MOVES
BATTLE_MOVES = [
    {'name': 'assault', 'type': 'attack', 'damage_type': 'physical', 'base_power': 50, 'attack_stat': 'attack', 'defense_stat': 'defense'},

    {'name': 'whip', 'type': 'attack', 'damage_type': 'physical', 'base_power': 30, 'attack_stat': 'attack', 'defense_stat': 'defense', 'attributes': [attribute_fast(35)]},

    {'name': 'shockwave', 'type': 'attack', 'damage_type': 'energy', 'base_power': 40, 'attack_stat': 'special_attack', 'defense_stat': 'special_defense', 
     'attributes': [attribute_splash(0.1)]},
     
    {'name': 'absolute defense', 'type': 'buff', 'buffs': [{'stat': 'defense', 'multiplier': 3}, {'stat': 'special_defense', 'multiplier': 3}, 
                                                           {'stat': 'attack', 'multiplier': 0}, {'stat': 'special_attack', 'multiplier': 0}]}
]