import battles.battles as battles
import datetime
import discord
import config

class BattleView(discord.ui.View):
    def __init__(self, player: battles.Player, embed: discord.Embed = None):
        super().__init__(timeout=config.DECISION_TIME)
        self.player = player
        self.embed: discord.Embed = embed
        self.selection = None

class CharacterSelect(discord.ui.Select):
    def __init__(self, options, timestamp):
        super().__init__(placeholder="Select a character...", options=options)
        self.timestamp = timestamp

    async def callback(self, interaction):
        if self.view.player.member != interaction.user:
            await interaction.response.send_message(embed=discord.Embed(description='This is not your battle.', color=config.ErrorColour), ephemeral=True)
            return
        
        await self.view.set_selection(self.values[0])
        await interaction.response.edit_message(view=None, embed=discord.Embed(description=f"**You selected {self.values[0]}**.", colour=0xfc0345))


class CharacterSelectView(BattleView):
    def __init__(self, player: battles.Player):
        timestamp = get_timer_timestamp(120)
        super().__init__(player, discord.Embed(description=f"**Select a character to tag in.** (Timeout <t:{timestamp}:R>)", colour=0xfc0345))
        self.add_item(CharacterSelect(options=[discord.SelectOption(label=character.name, value=character.name) for character in player.characters], timestamp=timestamp))
    
    async def set_selection(self, value: str):
        self.selection = value
        self.stop()

def get_timer_timestamp(seconds: int):
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    return int(end_time.timestamp())