import discord
import random
import config
import asyncio

class CardZones():

    def __init__(self, player: "Player"):
        self.player = player
        self.deck: list[BaseCard] = []
        self.hand: list[BaseCard] = []
        self.discard_pile: list[BaseCard] = []
        self.selection: list[BaseCard] = []

        self.locations: dict[str, list[BaseCard]] = {
            'deck': self.deck,
            'hand': self.hand,
            'discard_pile': self.discard_pile,
            'selection': self.selection
        }

    async def initialise_deck(self, deck: list["BaseCard"]):
        for card in deck:
            await self.create_card(card, 'deck')
        await self.shuffle_deck()

    def card_select_options(self) -> list[discord.SelectOption]:
        return [discord.SelectOption(label=f"{index+1}: {card.name} ({card.cost})", value=f"{index+1}: {card.name} ({card.cost})") for index, card in enumerate(self.hand)]

    def display_hand(self, is_opponent: bool = False):
        if is_opponent: # Opponent hand display
            return '\n'.join([f"- {card.display()}" if card.revealed else f"- **[?]**" for card in self.hand]) if self.hand else "<Empty>"
        # Own hand display
        return '\n'.join([f"- {card.display()}" for card in self.hand]) if self.hand else "<Empty>"
    
    def mobile_display_hand(self, is_opponent: bool = False):
        if is_opponent: # Opponent hand display
            return ', '.join([card.display() if card.revealed else f"**[?]**" for card in self.hand]) if self.hand else "<Empty>"
        # Own hand display
        return ', '.join([card.display() for card in self.hand]) if self.hand else "<Empty>"

    async def shuffle_deck(self):
        random.shuffle(self.deck)

    async def move(self, card: "BaseCard", destination: str):
        """
        Moves a card to the specified destination.
        Destination can be 'deck', 'hand', or 'discard_pile'.
        """

        if destination not in ['deck', 'hand', 'discard_pile'] or destination == card.location:
            return False
        
        current_location = self.locations[card.location]
        destination_location = self.locations[destination]

        current_location.remove(card)
        destination_location.append(card)
        card.set_location(destination)
        return True

    async def discard(self, card: "BaseCard", run_on_discard: bool = True):
        await card.move_to('discard_pile')
        if run_on_discard:
            await card.on_discard()

    async def random_discard(self):
        if self.hand:
            card = random.choice(self.hand)
            await card.discard()
            if card.location != 'erased':
                return card

    async def erase(self, card: "BaseCard"):
        if card.location not in ['deck', 'hand', 'discard_pile', 'selection']:
            return
        
        location = self.locations[card.location]
        location.remove(card)
        card.set_location('erased')

    async def replenish_deck(self):
        for card in self.discard_pile:
            self.deck.append(card)
            card.set_location('deck')

        self.discard_pile.clear()
        await self.shuffle_deck()

    async def new_hand(self):
        for card in [x for x in self.hand if 'sticky' not in x.keywords] + self.selection:
            await card.discard(False)

        await self.player.draw(5, False)

    async def remove_selection(self):
        """Moves the selected card to the discard pile, if there is one.
        This function doesn't trigger the card's on_discard function.
        """
        for card in self.selection:
            await card.discard(False)

    def select_card(self, card: "BaseCard"):
        """Moves a card to the selection zone. Does nothing if selection already contains a card."""
        if self.selection:
            return

        current_location = self.locations[card.location]  
        current_location.remove(card)
        self.selection.append(card)
        card.set_location('selection')


    async def draw(self) -> "BaseCard":
        """
        Moves the first card in the deck to the hand. Does nothing if the hand is full (5 cards).
        If the deck is empty, call replenish_deck(). If it is still empty, a card cannot be drawn.
        """
        if len(self.hand) >= config.MAX_HAND_SIZE:
            return
        if not self.deck:
            await self.replenish_deck()
            if not self.deck:
                return
            
        card = self.deck[0]
        await self.move(card, 'hand')
        await card.on_draw()
        return card


    async def create_card(self, card: "BaseCard", location: str):
        if (location == 'selection' and self.selection) or (location == 'hand' and len(self.hand) >= config.MAX_HAND_SIZE):
            return
        if not isinstance(card, BaseCard):
            try:
                card = card.value
            except AttributeError:
                return

        match location:
            case 'deck':
                destination = self.deck
            case 'hand':
                destination = self.hand
            case 'discard_pile':
                destination = self.discard_pile
            case 'selection':
                destination = self.selection
        
        clone = card.copy()
        destination.append(clone)
        clone.set_location(location)
        clone.set_owner(self.player)

        return clone
        
        
        
        

        

class Character():

    def __init__(self, base: "BaseChar", attribute: str, health: int, attack: int, defense: int, magic_attack: int, magic_defense: int, speed: int, 
                 passive_ability: "passives.BasePassive", active_ability: "actives.BaseActive", growth_style: str, 
                 chemistry_tags: list[str] = [], tags: list[str] = []):
        
        self.name = base.short_name
        self.tags = tuple([base.series] + chemistry_tags + tags)
        self.attribute = attribute
        self.growth_style = growth_style

        self.owner: Player | None = None

        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
        self.magic_attack = magic_attack
        self.magic_defense = magic_defense
        self.speed = speed
        
        self.passive_ability: passives.BasePassive = passive_ability()
        self.passive_ability.set_user(self)
        self.active_ability: actives.BaseActive = active_ability()
        self.active_ability.set_user(self)

        self.shield = 0
        self.statuses: list[statuses.BaseStatus] = []
        self.switch_cooldown = 0

    def __repr__(self):
        return f"{config.COLOUR_EMOJI_KEY[self.attribute]} {self.name} - {self.health}❤️{f' {self.shield}🛡️' if self.shield else ''}"
    
    def display(self, is_opponent: bool = False):
        opponent = self.owner.opponent.active_character
        multiplier_emoji = ''
        if opponent:
            multiplier_emoji = '⬆️' if self.get_attribute_multiplier(opponent) > 1 else '⬇️' if self.get_attribute_multiplier(opponent) < 1 else ''

        if self.owner.active_character is not self:
            return f"{(config.COLOUR_EMOJI_KEY[self.attribute] + multiplier_emoji) if self.switch_cooldown == 0 else config.SWITCH_CD_KEY[self.switch_cooldown]} {self.name} - {self.health}❤️{f' {self.shield}🛡️' if self.shield else ''}"
        
        name_row = f"{config.COLOUR_EMOJI_KEY[self.attribute]}{multiplier_emoji} **__{self.name}__** - {self.health}❤️{f' {self.shield}🛡️' if self.shield else ''}"
        status_row = ' '.join([status.display_emoji for status in self.get_statuses() if status.display_emoji is not None])
        if not is_opponent:
            status_row = (f"❕" if self.active_ability.has_been_used else "❗✅" if self.active_ability.can_be_used() else "❗⌛") + ' ' + status_row

        return '\n'.join([name_row, status_row])

    def set_owner(self, player: "Player"):
        self.owner = player

    def get_stat(self, stat: str):
        KEY = {
            'atk': self.attack,
            'def': self.defense,
            'm.a': self.magic_attack,
            'm.d': self.magic_defense,
            'spe': self.speed
        }
        return KEY[stat]

    def get_speed(self):
        speed = self.get_stat('spe')

        speed_buffs: list[statuses.SpeedBuff] = self.get_statuses(statuses.SpeedBuff)
        for buff in speed_buffs:
            speed = buff.add_multiplier(speed)

        return speed
    
    def get_attribute_multiplier(self, opponent: "Character"):
        multiplier = config.COLOUR_MATCHUPS[self.attribute][opponent.attribute]
        multiplier = min(multiplier, 1 if opponent.has_status(statuses.NegateAttributeDisadvantage) else 99) # Cap multiplier to 1 if opponent is type neutral.
        multiplier = max(multiplier, 1 if self.has_status(statuses.NegateAttributeDisadvantage) else -99) # Multiplier minimum is 1 if user is type neutral
        return multiplier
    
    def requirements_met(self, requirements: dict):
        met = True
        for key, value in requirements.items():
            match key:
                case 'round_min':
                    if self.owner.battle.round < value:
                        met = False
                case 'user_tag':
                    if value not in self.tags:
                        met = False
                case 'user_name':
                    if value.lower() not in self.name.lower():
                        met = False
                case 'active_cooldown':
                    if self.active_ability.cooldown > value:
                        met = False
                case _:
                    continue

        return met
    
    def is_active(self) -> bool:
        return self.owner.active_character is self
    def is_defeated(self) -> bool:
        return not self in self.owner.characters
    
    def can_use_card(self, card: "BaseCard") -> bool:
        return self.owner.energy >= card.cost and self.requirements_met(card.requirements) and self.passive_ability.can_use_card(card)
    def can_switch_in(self, bypass_cooldown: bool = False) -> bool:
        return self.owner.can_switch() and (self.switch_cooldown == 0 or bypass_cooldown) and self.owner.active_character is not self
    
    def reduce_switch_cooldown(self, turns: int):
        self.switch_cooldown = max(self.switch_cooldown - turns, 0)

    def has_permission(self, permission: str) -> bool:
        statuses = [status for status in self.get_statuses() if permission in status.permissions.keys()]
        permissions = [status.permissions[permission] for status in statuses] + [self.passive_ability.permissions.get(permission, True)] + [self.active_ability.permissions.get(permission, True)]
        return all(permissions)

    async def inflict_damage(self, damage: int, type_text: str = ''):
        amount = int(damage)
        
        self.shield -= amount
        if self.shield < 0:
            self.health += self.shield # Shield will now be a negative value equal to excess damage, so add that amount to health to subtract the excess from HP.
            self.shield = 0

        self.owner.battle.log(f"> *{self.name}* took **{amount}** {type_text}damage.")

        if self.health <= 0:
            self.health = 0
            await self.fatal_damage()

    async def fatal_damage(self):
        if self.health > 0:
            return

        self.owner.battle.log(f"> *{self.name}* was defeated!")
        self.owner.characters.remove(self)

        if self.owner.active_character is self:
            self.owner.active_character = None
            await self.on_defeat()

    async def inflict_attack_damage(self, damage: int, attacker: "Character") -> int | None:

        card = attacker.owner.selected_card()
        
        attribute_multiplier = attacker.get_attribute_multiplier(self)
        damage = int(damage * attribute_multiplier)

        await self.inflict_damage(damage)
        await attacker.on_hit_attack(damage)
        await self.hit_by_attack(damage)

        if attribute_multiplier > 1:
            self.owner.battle.log(f"> It was super effective!")
        if attribute_multiplier < 1:
            self.owner.battle.log(f"> It was not very effective...")

        return damage
        
    
    async def add_shield(self, amount: int):
        self.shield += amount
        self.owner.battle.log(f"> *{self.name}* gained **{amount}** shield.")
    
    async def heal(self, amount: int):
        amount = int(min(amount, self.max_health - self.health))
        self.health = self.health + amount
        if amount:
            self.owner.battle.log(f"> *{self.name}* recovered **{(amount)}** health.")
        return amount
        
    async def apply_status(self, status: "statuses.BaseStatus"):
        if isinstance(status, statuses.BaseStatus):

            if await self.can_apply_status(status):
                # Add stacks for stacking statuses
                if isinstance(status, statuses.StackingStatus) and self.has_status(type(status)):
                    existing_status: statuses.StackingStatus = next((x for x in self.get_statuses() if x.name == status.name), None)
                    existing_status.duration = max(existing_status.duration, status.duration)
                    existing_status.stacks += status.stacks
                    await existing_status.on_apply(stacks_added=status.stacks)

                # Else append status normally
                else:
                    self.statuses.append(status)
                    status.set_user(self)
                    await status.on_apply()
            else:
                # If the status is negated, trigger the negation function.
                await status.on_negation()

    async def remove_status(self, status: "statuses.BaseStatus"):
        self.statuses = [x for x in self.statuses if x is not status]
        await status.on_remove()

    async def can_apply_status(self, status: "statuses.BaseStatus"):
        if any(isinstance(status, immunity) for immunity in [x.immune_to for x in self.get_statuses() if isinstance(x, statuses.StatusImmunity)]):
            return False

        return True
    
    async def tick_statuses(self, duration_type: str = 'rounds', card: "BaseCard" = None):
        statuses = [x for x in self.get_statuses() if x.duration_type == duration_type]
        if card:
            statuses = [x for x in statuses if await x.applicable_to_card(card)]

        for status in statuses:
            await status.tick()
    
    def has_status(self, status_type: "statuses.BaseStatus") -> bool:
        return any(isinstance(status, status_type) for status in self.statuses)
    
    def get_statuses(self, status_type: "statuses.BaseStatus" = None) -> list["statuses.BaseStatus"]:
        if not status_type:
            status_type = statuses.BaseStatus
        return [status for status in self.statuses if isinstance(status, status_type)] + [status for status in self.passive_ability.passive_statuses if isinstance(status, status_type)]

    async def gain_energy(self, amount: int):
        if self.has_permission('gain_energy'):
            self.owner.gain_energy(amount)
            return True
        return False
    
    async def reduce_energy_delta(self, amount: int):
        if self.has_permission('reduce_energy_delta'):
            self.owner.next_round_energy_delta -= amount
            self.owner.log(f"> Your energy next turn will be reduced by **{amount}**.")
            self.owner.opponent.log(f"> Opponent's energy next turn will be reduced by **{amount}**.")
            return True
        return False
    
    async def modify_switch_cooldown(self, turns: int):
        self.switch_cooldown = max(0, self.switch_cooldown + turns)
        self.owner.battle.log(f"> *{self.name}*'s switch cooldown was {'increased' if turns > 0 else 'reduced'} by **{turns}**.")


    ## Event trigger functions: simply calls the associated function in the ability object(s).
    async def targeted_by_attack(self):
        await self.passive_ability.targeted_by_attack()
    async def on_hit_attack(self, damage: int):
        await self.passive_ability.on_hit_attack(damage)
    async def hit_by_attack(self, damage: int):
        await self.passive_ability.hit_by_attack(damage)
    async def on_switch_in(self, ally: "Character" = None):
        await self.passive_ability.switch_in(ally)
    async def on_switch_out(self, ally: "Character"):
        await self.passive_ability.switch_out(ally)
    async def on_round_start(self):
        await self.passive_ability.round_start_global()
        await self.active_ability.round_start_global()
        if self.is_active():
            await self.passive_ability.round_start()
    async def on_round_end(self):
        await self.passive_ability.round_end_global()
        if self.is_active():
            await self.passive_ability.round_end()
    async def on_turn_start(self):
        await self.passive_ability.turn_start_global()
        await self.active_ability.turn_start_global()
        if self.is_active():
            await self.passive_ability.turn_start()
    async def on_turn_end(self):
        await self.passive_ability.turn_end_global()
        if self.is_active():
            await self.passive_ability.turn_end()
    async def on_defeat(self):
        await self.passive_ability.on_death()
    async def on_card_activation(self, card: "BaseCard"):
        await self.passive_ability.activate_card(card)


class Player():
    def __init__(self, member: discord.Member, channel: discord.TextChannel):
        self.member = member
        self.channel = channel

        self.battle: Battle | None = None
        self.opponent: Player | None = None

        self.active_character: Character | None = None
        self.zones = CardZones(self)
        self.energy: int = 0
        self.next_round_energy_delta: int = 0

        self.party: tuple[Character] = ()
        self.characters: list[Character] = []

        self.turn_log = []
        self.has_ended = False


    def log(self, message: str):
        self.turn_log.append(message)

    def set_party(self, party: list[Character]):
        self.party = tuple(party)
        self.characters = party.copy()
        for char in self.party:
            char.set_owner(self)

    def set_battle(self, battle: "Battle"):
        self.battle = battle

    def set_opponent(self, opponent: "Player"):
        self.opponent = opponent
    
    def selected_card(self):
        if self.zones.selection:
            return self.zones.selection[0]
        
    def can_switch(self):
        can_switch_out = True
        if self.active_character:
            can_switch_out = self.active_character.has_permission('switch_out')
        else:
            return True
        return len([x for x in self.characters if x is not self.active_character]) > 0 and can_switch_out
    
    def get_round_energy(self):
        return config.round_energy(self.battle.round)
        
    async def send_display(self):
        await self.channel.send(embed=self.display_embed())

    def display_embed(self) -> discord.Embed:
        if self.channel.guild.get_member(self.member.id)._client_status.desktop is not None:
            return self._desktop_display()
        else:
            return self._mobile_display()
    
    def _desktop_display(self) -> discord.Embed:
        embed = discord.Embed(color=0x4287f5)
        embed.add_field(name=f'You - ({self.energy})', value='\n'.join([f'{char.display()}\n' for char in self.characters if char is self.active_character] + [character.display() for character in self.characters if character is not self.active_character]))
        embed.add_field(name=f'Opponent - ({self.opponent.energy})', value='\n'.join([f'{char.display(True)}\n' for char in self.opponent.characters if char is self.opponent.active_character] + [character.display(True) for character in self.opponent.characters if character is not self.opponent.active_character]), inline=True)
        embed.add_field(name='\t', value='\t', inline=False)
        embed.add_field(name="__Your Hand__", value=self.zones.display_hand())
        embed.add_field(name="__Opponent Hand__", value=self.opponent.zones.display_hand(True))
        embed.set_author(name=f"Round {self.battle.round} - Turn {self.battle.turn}", icon_url="https://cdn-icons-png.flaticon.com/512/3104/3104645.png")

        return embed
    
    def _mobile_display(self) -> discord.Embed:
        text = f"**You - ({self.energy})**\n" + '\n'.join([f'{char.display()}\n' for char in self.characters if char is self.active_character] + [character.display() for character in self.characters if character is not self.active_character])
        text += f"\n\n**__Your Hand__**\n{self.zones.mobile_display_hand()}"
        text += f"\n\n**Opponent - ({self.opponent.energy})**\n" + '\n'.join([f'{char.display(True)}\n' for char in self.opponent.characters if char is self.opponent.active_character] + [character.display(True) for character in self.opponent.characters if character is not self.opponent.active_character])
        text += f"\n\n**__Opponent Hand__**\n{self.opponent.zones.mobile_display_hand(True)}"

        embed = discord.Embed(description=text, color=0x4287f5)
        embed.set_author(name=f"Round {self.battle.round} - Turn {self.battle.turn}", icon_url="https://cdn-icons-png.flaticon.com/512/3104/3104645.png")

        return embed
    
    def get_characters(self) -> list[Character]:
        return [char for char in self.characters]
    
    async def push_log(self):
        if self.turn_log:
            embed=discord.Embed(color=0x0a7a22, description='\n'.join(self.turn_log))
            embed.set_author(name=f"Round {self.battle.round} - Turn {self.battle.turn}", icon_url="https://cdn-icons-png.flaticon.com/512/3104/3104645.png")
            await self.channel.send(embed=embed)
            self.turn_log.clear()
    
    async def draw(self, amount: int, log: bool = True):
        amount = min(amount, config.MAX_HAND_SIZE - len(self.zones.hand))
        for _ in range(amount):
            await self.zones.draw()
        if log:
            self.battle.log(f"> *{self.member.display_name}* drew **{amount}** card{'s' if amount > 1 else ''}.")
    
    async def gain_energy(self, amount: int, log: bool = True):
        energy_cap = config.round_energy(self.battle.round) + 2
        energy_gain = min(amount, energy_cap - self.energy)
        self.energy += energy_gain

        if log:
            self.log(f"> You replenished **{energy_gain}** energy.")
            self.opponent.log(f"> Opponent replenished **{energy_gain}** energy.")

    async def reduce_energy(self, amount: int, log: bool = True):
        energy_loss = min(amount, self.energy)
        if not energy_loss:
            return 

        self.energy -= energy_loss
        if log:
            self.log(f"> You lost **{energy_loss}** energy.")
            self.opponent.log(f"> Opponent lost **{energy_loss}** energy.")

    async def spend_energy(self, amount: int):
        self.energy = max(self.energy - amount, 0)

    async def switch_character(self, target: Character, log: bool = True, bypass_cooldown: bool = False):
        active = self.active_character

        # Fail switch if current active is trapped
        if not target.can_switch_in(bypass_cooldown):
            return False
        
        self.active_character = target
        if log:
            self.log(f"- **You tagged in *{target.name}***.")
            self.opponent.log(f"- **Opponent tagged in *{target.name}***.")

        if active:
            active.switch_cooldown = min(active.switch_cooldown, 0) + config.SWITCH_COOLDOWN
            await active.on_switch_out(target)
        await target.on_switch_in(active)
        target.switch_cooldown = 0 # In case a character is forced in despite being on cooldown

        return True
    
    async def discard_random(self, count: int, log: bool = True):

        discarded: list[BaseCard] = []
        for _ in range(count):
            if self.zones.hand:
                card = await self.zones.random_discard()
                discarded.append(card)

        if discarded and log:
            self.log(f"> You discarded {', '.join([f'**[{card.name}]**' for card in discarded])}.")
            cards = ', '.join([f'**[{card.name if card.revealed else "?"}]**' for card in discarded])
            self.opponent.log(f"> Opponent discarded {cards}.")

    async def create_card(self, card: "BaseCard", location: str, log: bool = True):
        card = await self.zones.create_card(card, location)
        if card and log:
            self.log(f"> A **[{card.name}]** was created in your {location.replace('_', ' ')}.")
            self.log(f"> A {f'**[{card.name}]**' if card.revealed else 'card'} was created in your opponent's {location.replace('_', ' ')}.")



class Battle():
    def __init__(self, player1: Player, player2: Player):
        self.players: list[Player] = [player1, player2]
        self.round = 0
        self.turn = 0
        self.since_last_card = 0

        for player in self.players:
            player.set_opponent(player2 if player is player1 else player1)
            player.set_battle(self)

    def log(self, message: str):
        for player in self.players:
            player.log(message)

    def sort_action_order(self, actions: list["buttons.BaseAction"]):
        actions.sort(key=lambda x: (x.priority, x.player.active_character.get_speed()), reverse=True)

    async def push_logs(self, wait: bool = False):
        if not [player.turn_log for player in self.players if player.turn_log]:
            return
        wait_duration = len([player.turn_log for player in self.players if player.turn_log][0])

        for player in self.players:
            await player.push_log()
        if wait:
            await asyncio.sleep(wait_duration)
        return True

    async def send_displays(self):
        for player in self.players:
            await player.send_display()

    async def switch_missing_actives(self):
        views = [buttons.CharacterSelectView(player, 'Select a character to switch in') for player in self.players if not player.active_character]
        for view in views:
            await view.player.send_display()

        await self.wait_for_input(views)

        for view in views:
            await view.player.switch_character(view.selection)
    

    async def start(self):
        # Create battle threads
        for player in self.players:
            thread = await player.channel.create_thread(name=f"{player.member.display_name}'s Battle", auto_archive_duration=60)
            await thread.add_user(player.member)
            player.channel = thread


        # Choose a starting character
        await self.switch_missing_actives()

        await self.next_round()

    async def next_round(self):
        self.round += 1
        self.turn = 0

        # Step 1: Draw cards, gain energy, clear logs
        for player in self.players:
            player.has_ended = False
            await player.zones.new_hand()
            player.energy = player.get_round_energy() + min(player.next_round_energy_delta, 2)
            player.next_round_energy_delta = 0
            await player.channel.send(f"## Round {self.round}{' - Base Energy Raised To {energy}'.format(energy = 4 if self.round == 5 else 5) if self.round in [5,10] else ''}")
        
        # Step 2: Round Start Event + tick statuses
        for player in self.players:
            # Tick statuses
            for character in player.characters:
                await character.tick_statuses()
                character.shield = 0
                await character.on_round_start()

        await self.next_turn()

    
    async def next_turn(self):

        # Step 1: Increment turn counter and character counters, and tick turn duration statuses
        self.turn += 1
        self.since_last_card += 1

        for player in self.players:
            await player.zones.remove_selection()

            for character in player.characters:
                character.reduce_switch_cooldown(1)

        # Step 2: Turn Start Event
        for player in self.players:
            for character in player.characters:
                await character.on_turn_start()

        # Step 3: Send display and log
        await self.switch_missing_actives()
        await self.push_logs(True)
        await self.send_displays()

        # Step 4: Wait for players to input actions
        views = [buttons.ActionSelectBuilder(player) for player in self.players if not player.has_ended]
        await self.wait_for_input(views)

        actions = []
        for view in views:
            if view.selection:
                actions.append(view.selection)
            else:
                actions.append(buttons.EndAction(view.player))

        # Step 5: Resolve actions
        await self.resolve_actions(actions)

        # Step 6: Turn End Event + tick statuses
        for player in self.players:
            for character in player.characters:
                await character.on_turn_end()
                await character.tick_statuses('turns')

        # Step 7: Send display and log
        await self.push_logs(True)

        # Step 8: End the battle if all a player's characters are defeated.
        # Move to the next round if both players ended, or 3 turns have passed without a card being used.
        # Else move to the next turn
        if any(not player.characters for player in self.players):
            await self.end()
        elif all(player.has_ended for player in self.players) or self.since_last_card >= 3:
            await self.next_round()
        else:
            await self.next_turn()
        

    async def resolve_actions(self, actions: list["buttons.BaseAction"]):
        self.sort_action_order(actions)

        # First run each action's activation
        for action in actions:
                await action.activate()

        self.sort_action_order(actions)

        # Then run each action's resolution
        for action in actions:
                await action.resolve()

        

    async def wait_for_input(self, views: list["buttons.BattleView"]):
        views = [view for view in views if not view.selection] # If a view already selected, don't include them
        if not views:
            return

        for view in views:
            await view.player.channel.send(view=view, embed=view.embed)
        for player in [x for x in self.players if x not in [view.player for view in views]]:
            await player.channel.send(embed=discord.Embed(description=f"Opponent is making a selection... (Timeout <t:{views[0].timestamp if views[0].timestamp is not None else buttons.get_timer_timestamp(config.DECISION_TIME)}:R>)", color=0xfc0345))

        await asyncio.gather(*[x.wait() for x in views])


    async def end(self):
        raise NotImplementedError("Battle end function not implemented.")



from battles.cards import BaseCard
from system.character_database import BaseChar
import battles.statuses as statuses
import battles.passives as passives
import battles.actives as actives
import battles.buttons as buttons