import discord
from collections import defaultdict

EMOJIS = defaultdict(str)

def load_emojis(emojis: list[discord.Emoji]):
    for e in emojis:
        EMOJIS[e.name] = str(e)