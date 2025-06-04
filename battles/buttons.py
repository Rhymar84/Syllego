import battles.battles as battles
import datetime
import discord
import config

# Views

class BattleView(discord.ui.View):
    def __init__(self, player: battles.Player, embed: discord.Embed = None, timeout: int = config.DECISION_TIME):
        super().__init__(timeout=timeout)
        self.player = player
        self.embed: discord.Embed = embed
        self.selection = None
        self.timestamp = get_timer_timestamp(timeout)

    def set_selection(self, value):
        self.selection = value
        self.stop()


class CharacterSelect(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder="Select a character...", options=options)

    async def callback(self, interaction):
        if await check_is_player(interaction, self.view.player.member) is False:
            return
        
        self.view.set_selection([char for char in self.view.player.characters if char.name == self.values[0]][0])
        await interaction.response.edit_message(view=None, embed=discord.Embed(description=f"You selected **{self.values[0]}**.", colour=0xfc0345))

class CharacterSelectView(BattleView):
    def __init__(self, player: battles.Player, prompt: str):
        timestamp = get_timer_timestamp(config.DECISION_TIME / 2)
        super().__init__(player, discord.Embed(description=f"**{prompt}.** (Timeout <t:{timestamp}:R>)", colour=0xfc0345), timeout=config.DECISION_TIME / 2)
        self.add_item(CharacterSelect(options=[discord.SelectOption(label=character.name, value=character.name) for character in player.characters]))


class CardSelect(discord.ui.Select):
    def __init__(self, cards: list["BaseCard"]):
        self.cards = cards
        super().__init__(placeholder="Select a card.", 
                         options=[discord.SelectOption(label=f"{index+1}: {card.name} ({card.cost})", value=f"{index+1}: {card.name} ({card.cost})") for index, card in enumerate(self.cards)])

    async def callback(self, interaction):
        if await check_is_player(interaction, self.view.player.member) is False:
            return

        card = self.cards[int(self.values[0][0])-1]
        self.view.set_selection(card)
        await interaction.response.edit_message(view=None, embed=discord.Embed(description=f"You selected **{self.values[0][3:]}**.", colour=0xfc0345))

class CardSelectView(BattleView):
    def __init__(self, player: battles.Player, options: list["BaseCard"], prompt: str = "Select a card"):
        timestamp = get_timer_timestamp(config.DECISION_TIME / 2)
        super().__init__(player, discord.Embed(description=f"**{prompt}** (Timeout <t:{timestamp}:R>)", colour=0xfc0345), timeout=config.DECISION_TIME / 2)
        self.add_item(CardSelect(options))







class EndButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="End", style=discord.ButtonStyle.danger)

    async def callback(self, interaction):
        if await check_is_player(interaction, self.view.player.member) is False:
            return
        
        self.view.set_selection(EndAction(self.view.player))
        await interaction.response.edit_message(view=None, embed=discord.Embed(description=f"**You passed**.", colour=0xfc0345))

class ActiveButton(discord.ui.Button):
    def __init__(self):
        super().__init__(emoji="❗", style=discord.ButtonStyle.green)

    async def callback(self, interaction):
        if await check_is_player(interaction, self.view.player.member) is False:
            return
        
        self.view.set_selection(UseActiveAbility(self.view.player))
        await interaction.response.edit_message(view=None, embed=discord.Embed(description=f"**You activated ❗{self.view.player.active_character.active_ability.name}❗**", colour=0xfc0345))

class UseCardSelect(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder="Select a card.", options=options)

    async def callback(self, interaction):
        if await check_is_player(interaction, self.view.player.member) is False:
            return
        player: battles.Player = self.view.player
        card = player.zones.hand[int(self.values[0][0])-1]

        if not player.active_character.can_use_card(card):
            await interaction.response.send_message(embed=discord.Embed(description='You cannot use this card.', color=config.ErrorColour), ephemeral=True)
            return

        self.view.set_selection(UseCard(self.view.player, card))
        await interaction.response.edit_message(view=None, embed=discord.Embed(description=f"You selected **Card: {self.values[0][3:]}**.", colour=0xfc0345))

class SwitchSelect(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder="Switch characters.", options=options)

    async def callback(self, interaction):
        if await check_is_player(interaction, self.view.player.member) is False:
            return
        
        character: battles.Character = [char for char in self.view.player.characters if char.name == self.values[0]][0]
        if not character.can_switch_in():
            await interaction.response.send_message(embed=discord.Embed(description='You cannot switch to this character.', color=config.ErrorColour), ephemeral=True)
            return
        
        self.view.set_selection(SwitchCharacters(self.view.player, character))
        await interaction.response.edit_message(view=None, embed=discord.Embed(description=f"You selected **Switch: {self.values[0]}**.", colour=0xfc0345))


class ActionSelectBuilder(BattleView):
    def __init__(self, player: battles.Player):
        self.timestamp = get_timer_timestamp(config.DECISION_TIME)
        super().__init__(player, discord.Embed(description=f"**Select an action.** (Timeout <t:{self.timestamp}:R>)", colour=0xfc0345))

        # If the player has cards in hand, add card select menu
        card_options = player.zones.card_select_options()
        if card_options:
            self.add_item(UseCardSelect(options=card_options))

        # If the player can switch, add switch select menu
        switch_options = [discord.SelectOption(label=character.name, value=character.name) for character in player.characters if character.can_switch_in()]
        if switch_options:
            self.add_item(SwitchSelect(options=switch_options))

        # If the player can use their active, add active button
        if player.active_character.active_ability.can_be_used():
            self.add_item(ActiveButton())

        # If none of the above, automatically select pass. Else, add end button
        if not self.children:
            if player.opponent.has_ended:
                self.set_selection(EndAction(player))
            else:
                self.set_selection(PassAction(player))
            return
        self.add_item(EndButton())






# Actions
class BaseAction():
    """Base class for all actions. Provides interface for actions to be executed."""
    def __init__(self, player: battles.Player):
        self.player = player
        self.priority = 0

    async def activate(self):
        """Processes the action's activation."""
        pass

    async def resolve(self):
        """Processes the action's resolution."""
        pass

class PassAction(BaseAction):
    """Action for passing the rest of your round.
    Does nothing."""


class EndAction(BaseAction):
    """Action for ending your round."""
    async def resolve(self):
        self.player.log(f"- **You have finished acting this round.**")
        self.player.opponent.log(f"- **Opponent has finished acting this round.**")
        self.player.has_ended = True

class UseActiveAbility(BaseAction):
    """Action for using an active ability."""
    async def activate(self):
        user: battles.Character = self.player.active_character
        if user:
            await user.active_ability.on_activation()
            user.active_ability.has_been_used = True

    async def resolve(self):
        user: battles.Character = self.player.active_character
        if user:
            self.player.battle.log(f"- **{user.name} used ❗{user.active_ability.name}❗**")
            await user.active_ability.resolve()

class UseCard(BaseAction):
    """Action for using a card."""
    def __init__(self, player: battles.Player, card: "BaseCard"):
        super().__init__(player)
        player.zones.select_card(card)
        self.priority = card.priority

    async def activate(self):
        card: "BaseCard" = self.player.selected_card()
        user: battles.Character = self.player.active_character
        cost = user.owner.energy if card.cost == 'X' else card.cost
        if not card or not user or cost > user.owner.energy or user.is_defeated():
            return

        await self.player.spend_energy(cost)
        card.energy_spent = cost
        await card.on_activation()
        await user.on_card_activation(card)

    async def resolve(self):
        card: "BaseCard" = self.player.selected_card()
        user: battles.Character = self.player.active_character
        if not card or not user or user.is_defeated():
            return
        
        self.player.battle.log(f"- **{user.name} used [{card.name}]**")
        self.player.battle.since_last_card = 0

        if card.negated:
            self.player.battle.log(f"> It was negated...")
            await card.discard()
            return

        await card.resolve()
        await card.discard()

        # Increment the duration of 'card' duration type statuses if they were applicable to this card
        await user.tick_statuses('cards', card)


class SwitchCharacters(BaseAction):
    """Action for switching characters."""
    def __init__(self, player: battles.Player, character: battles.Character):
        super().__init__(player)
        self.character = character
        self.priority = 6

    async def activate(self):
        await self.player.switch_character(self.character)

def get_timer_timestamp(seconds: int):
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    return int(end_time.timestamp())

async def check_is_player(interaction: discord.Interaction, player: discord.Member):
    if player != interaction.user:
        await interaction.response.send_message(embed=discord.Embed(description='This is not your battle.', color=config.ErrorColour), ephemeral=True)
        return False
    return True

from battles.cards import BaseCard