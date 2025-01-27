import discord
import random
import config
import asyncio

class CardZones():

    def __init__(self):
        self.deck: list[BaseCard] = []
        self.hand: list[BaseCard] = []
        self.discard_pile: list[BaseCard] = []
        self.selection: list[BaseCard] = []

    async def initialise_deck(self, deck: list["BaseCard"]):
        for card in deck:
            await self.create_card(card, 'deck')
        await self.shuffle_deck()

    def display_hand(self, is_opponent: bool = False):
        if is_opponent: # Opponent hand display
            return '\n'.join([f"- **[{card.name}]** ({card.cost})" if card.revealed else f"- **[?]**" for card in self.hand]) if self.hand else "<Empty>"
        # Own hand display
        return '\n'.join([f"- **[{card.name}]** ({card.cost})" for card in self.hand]) if self.hand else "<Empty>"
    
    def mobile_display_hand(self, is_opponent: bool = False):
        if is_opponent: # Opponent hand display
            return ', '.join([f"**[{card.name}]** ({card.cost})" if card.revealed else f"**[?]**" for card in self.hand]) if self.hand else "<Empty>"
        # Own hand display
        return ', '.join([f"**[{card.name}]** ({card.cost})" for card in self.hand]) if self.hand else "<Empty>"

    async def shuffle_deck(self):
        random.shuffle(self.deck)

    async def move(self, card: "BaseCard", destination: str):
        """
        Moves a card to the specified destination.
        Destination can be 'deck', 'hand', or 'discard_pile'.
        """

        if destination not in ['deck', 'hand', 'discard_pile'] or destination == card.location:
            return
        
        match card.location:
            case 'deck':
                current_location = self.deck
            case 'hand':
                current_location = self.hand
            case 'discard_pile':
                current_location = self.discard_pile
            case 'selection':
                current_location = self.selection
        match destination:
            case 'deck':
                destination_location = self.deck
            case 'hand':
                destination_location = self.hand
            case 'discard_pile':
                destination_location = self.discard_pile

        current_location.remove(card)
        destination_location.append(card)
        card.set_location(destination)

    async def discard(self, card: "BaseCard"):
        await self.move(card, 'discard_pile')
        await card.on_discard()

    async def erase(self, card: "BaseCard"):
        if card.location not in ['deck', 'hand', 'discard_pile', 'selection']:
            return

        match card.location:
            case 'deck':
                self.deck.remove(card)
            case 'hand':
                self.hand.remove(card)
            case 'discard_pile':
                self.discard_pile.remove(card)
            case 'selection':
                self.selection.remove(card)

        card.set_location('erased')

    async def replenish_deck(self):
        for card in self.discard_pile:
            self.deck.append(card)
            card.set_location('deck')

        self.discard_pile.clear()
        await self.shuffle_deck()

    async def discard_hand(self):
        for card in self.hand:
            await card.discard()

    async def choose_card(self, card: "BaseCard"):
        """Moves a card to the selection zone. Does nothing if selection already contains a card."""
        if self.selection:
            return

        match card.location:
            case 'deck':
                current_location = self.deck
            case 'hand':
                current_location = self.hand
            case 'discard_pile':
                current_location = self.discard_pile
            case 'selection':
                return
            
        current_location.remove(card)
        self.selection.append(card)
        card.set_location('selection')


    async def draw(self):
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

    def __repr__(self):
        return f"{config.COLOUR_EMOJI_KEY[self.attribute]} {self.name} - {self.health}❤️{f' {self.shield}🛡️' if self.shield else ''}"
    
    def display(self, is_opponent: bool = False):
        opponent = self.owner.opponent.active_character
        multiplier_emoji = ''
        if opponent:
            multiplier_emoji = '⬆️' if self.get_attribute_multiplier(opponent) > 1 else '⬇️' if self.get_attribute_multiplier(opponent) < 1 else ''

        if self.owner.active_character is not self:
            return f"{config.COLOUR_EMOJI_KEY[self.attribute]}{multiplier_emoji} {self.name} - {self.health}❤️{f' {self.shield}🛡️' if self.shield else ''}"
        
        name_row = f"{config.COLOUR_EMOJI_KEY[self.attribute]}{multiplier_emoji} **__{self.name}__** - {self.health}❤️{f' {self.shield}🛡️' if self.shield else ''}"
        status_row = ' '.join([status.display_emoji for status in self.statuses if status.display_emoji is not None])
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
            'spd': self.speed
        }
        return KEY[stat]
    
    def get_statuses(self) -> list["statuses.BaseStatus"]:
        return self.statuses + self.passive_ability.passive_statuses
    
    def get_attribute_multiplier(self, opponent: "Character"):
        return config.COLOUR_MATCHUPS[self.attribute][opponent.attribute]
    
    def requirements_met(self, requirements: dict):
        met = True
        for key, value in requirements.items():
            match key:
                case 'round_min':
                    if self.owner.battle.round < value:
                        met = False

        return met

    async def inflict_damage(self, amount: int):
        
        self.shield -= amount
        if self.shield < 0:
            self.health += self.shield # Shield will now be a negative value equal to excess damage, so add that amount to health to subtract the excess from HP.
            self.shield = 0

    async def calculate_damage(self, damage_value: int):
        return int(damage_value)
    
    async def add_shield(self, amount: int):
        self.shield += amount
    
    async def heal(self, amount: int):
        self.health = min(self.health + amount, self.max_health)

    async def apply_status(self, status: "statuses.BaseStatus"):
        if isinstance(status, statuses.BaseStatus):

            if await self.can_apply_status(status):
                # Apply the status effect.
                self.statuses.append(status)
                await status.on_apply()
            else:
                # If the status is negated, trigger the negation function.
                await status.on_negation()

    async def remove_status(self, status_name: str):
        to_remove = [status for status in self.statuses if status.name == status_name]

        if to_remove:
            self.statuses = [status for status in self.statuses if status not in to_remove]

    async def can_apply_status(self, status: "statuses.BaseStatus"):
        if any(isinstance(status, immunity) for immunity in [x.immune_to for x in self.get_statuses() if isinstance(x, statuses.StatusImmunity)]):
            return False

        return True
    
    def has_status(self, status_type: "statuses.BaseStatus"):
        return any(isinstance(status, status_type) for status in self.statuses)

    ## Event trigger functions: simply calls the associated function in the ability object.
    async def targeted_by_attack(self):
        await self.passive_ability.targeted_by_attack()
    async def on_hit_attack(self, damage: int):
        await self.passive_ability.on_hit_attack(damage)
    async def hit_by_attack(self):
        await self.passive_ability.hit_by_attack()
    async def on_switch_in(self):
        await self.passive_ability.switch_in()
    async def on_switch_out(self, ally: "Character"):
        await self.passive_ability.switch_out(ally)
    async def on_round_start(self):
        await self.passive_ability.round_start()
    async def on_round_end(self):
        await self.passive_ability.round_end()
    async def on_turn_start(self):
        await self.passive_ability.turn_start()
    async def on_turn_end(self):
        await self.passive_ability.turn_end()


class Player():
    def __init__(self, member: discord.Member, channel: discord.TextChannel):
        self.member = member
        self.channel = channel

        self.battle: Battle | None = None
        self.opponent: Player | None = None

        self.active_character: Character | None = None
        self.zones = CardZones()
        self.energy: int = 0

        self.party: tuple[Character] = ()
        self.characters: list[Character] = []

        self.turn_log = []

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
    
    async def draw(self, amount: int):
        for _ in range(amount):
            await self.zones.draw()
    
    async def gain_energy(self, amount: int):
        self.energy = min(self.energy + amount, 3)

    async def switch_character(self, target: Character):
        active = self.active_character

        # Fail switch if current active is trapped
        if active and active.has_status(statuses.Trapped):
            return False
        
        self.active_character = target
        self.battle.log(f"- {self.member.display_name} tagged in **{target.name}**.")

        if active:
            await active.on_switch_out(target)
        await target.on_switch_in()

        return True



class Battle():
    def __init__(self, player1: Player, player2: Player):
        self.players: list[Player] = [player1, player2]
        self.round = 0
        self.turn = 0

        for player in self.players:
            player.set_opponent(player2 if player is player1 else player1)
            player.set_battle(self)

    def log(self, message: str):
        for player in self.players:
            player.log(message)

    async def start(self):
        # Create battle threads
        for player in self.players:
            thread = await player.channel.create_thread(name=f"{player.member.display_name}'s Battle", auto_archive_duration=60)
            await thread.add_user(player.member)
            player.channel = thread

            await player.send_display()

        
        
        # Choose a starting character
        views = [buttons.CharacterSelectView(player) for player in self.players]
        await self.wait_for_input(views)

        for view in views:
            target = [char for char in view.player.characters if char.name == view.selection][0]
            await view.player.switch_character(target)

        await self.next_round()

    async def next_round(self):
        self.round += 1
        self.turn = 1

        # Step 1: Draw cards, gain energy, clear logs
        for player in self.players:
            await player.draw(5)
            await player.gain_energy(3)
            player.turn_log.clear()
        
        # Step 2: Activate round start abilities
        for player in self.players:
            if player.active_character:
                await player.active_character.on_round_start()
        
        # Step 3: Send display embeds
        for player in self.players:
            await player.send_display()
        

        
        

    async def wait_for_input(self, views: list["buttons.BattleView"]):

        for view in views:
            await view.player.channel.send(view=view, embed=view.embed)

        await asyncio.gather(*[x.wait() for x in views])



from battles.cards import BaseCard, create_card
from character_database import BaseChar
import battles.statuses as statuses
import battles.passives as passives
import battles.actives as actives
import battles.buttons as buttons