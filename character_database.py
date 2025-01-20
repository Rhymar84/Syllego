import PIL, io
import PIL.Image
import discord, gacha, config
from enum import Enum

class BaseChar():

    def __init__(self, id: str, name: str, rarity: int, series: str, short_name: str | None = None):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.series = series
        
        if short_name:
            self.short_name = short_name
        else:
            self.short_name = self.name


    async def display(self, level: float, colour: int, is_new: bool = False) -> discord.Embed:

        emoji = gacha.shining_emoji if self.rarity == 3 else gacha.glowing_emoji if self.rarity == 2 else gacha.common_emoji

        if level >= 5:
            info = '(Max Level)'
        elif is_new:
            info = 'NEW!!'
        else:
            info = ''
        

        if level != 0:
            stars = '⭐' * int(level)
        else:
            stars = '🔒'

        series = self.series

        embed = discord.Embed(title=f'{emoji} {self.name} {stars} {info}', color=colour)
        embed.set_footer(text=series)

        return embed


class CharInfo(discord.ui.View):

    def __init__(self, original_interaction: discord.Interaction, character: BaseChar, level: int):
        super().__init__()

        self.base_char = character
        self.level = level
        self.original_interaction = original_interaction
        self.timeout = 60

    @discord.ui.button(emoji='📊', style=discord.ButtonStyle.grey)
    async def stats(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.original_interaction.user:
            await interaction.response.send_message(embed=discord.Embed(title='User Error', description='This is not your command!', color=config.ErrorColour), ephemeral=True)
            return
        
        character = FIGHTERS[self.base_char.id]

        attribute = character['attribute']
        growth_style = character['growth_style']
        growth_factor = max(1, self.level) - 1

        stats = {'health': character['health'], 'attack': character['attack'], 'defense': character['defense'], 'magic_attack': character['magic_attack'], 'magic_defense': character['magic_defense'], 'speed': character['speed']}
        stats = apply_growth(stats, growth_style, growth_factor)

        text = f"**HP:** {stats['health']} | **Spe**: {stats['speed']}\n**Atk:** {stats['attack']} | **Def:** {stats['defense']}\n**M.A:** {stats['magic_attack']} | **M.D:** {stats['magic_defense']}"
        text += f"\n\n**(Passive) {character['passive_ability'].name}**\n>>> {character['passive_ability'].__doc__}"

        embed = discord.Embed(title=f"{COLOUR_EMOJI_KEY[attribute]} {self.base_char.name}", description = text, color=config.CHARACTER_EMBED_COLOUR)
        thumbnail = get_party_image(self.base_char.id, self.level)
        embed.set_thumbnail(url=f'attachment://{thumbnail.filename}')

        await interaction.response.edit_message(embed=embed, view=self, attachments=[thumbnail])
    
CHARACTERS = {

    # DRAGON BALL Z

    "DBZ-01": BaseChar("DBZ-01", "Son Goku", 3, "Dragon Ball Z", "Goku"),
    "DBZ-02": BaseChar("DBZ-02", "Vegeta", 3, "Dragon Ball Z"),

    "DBZ-03": BaseChar("DBZ-03", "Son Gohan", 2, "Dragon Ball Z", "Gohan"),
    "DBZ-04": BaseChar("DBZ-04", "Frieza", 2, "Dragon Ball Z"),
    "DBZ-05": BaseChar("DBZ-05", "Cell", 2, "Dragon Ball Z"),
    "DBZ-06": BaseChar("DBZ-06", "Majin Buu", 2, "Dragon Ball Z"),
    "DBZ-07": BaseChar("DBZ-07", "Piccolo", 2, "Dragon Ball Z"),

    "DBZ-08": BaseChar("DBZ-08", "Krillin", 1, "Dragon Ball Z"),
    "DBZ-09": BaseChar("DBZ-09", "Tien", 1, "Dragon Ball Z"),
    "DBZ-10": BaseChar("DBZ-10", "Future Trunks", 1, "Dragon Ball Z", "Trunks"),
    "DBZ-11": BaseChar("DBZ-11", "Android 17", 1, "Dragon Ball Z"),
    "DBZ-12": BaseChar("DBZ-12", "Android 18", 1, "Dragon Ball Z"),
    "DBZ-13": BaseChar("DBZ-13", "Master Roshi", 1, "Dragon Ball Z"),
    "DBZ-14": BaseChar("DBZ-14", "Yamcha", 1, "Dragon Ball Z"),
    "DBZ-15": BaseChar("DBZ-15", "Trunks", 1, "Dragon Ball Z"),
    "DBZ-16": BaseChar("DBZ-16", "Son Goten", 1, "Dragon Ball Z"),



    # Re:Zero

    "RZ-01": BaseChar("RZ-01", "Subaru Natsuki", 3, "Re:Zero - Starting Life in Another World"),
    "RZ-02": BaseChar("RZ-02", "Emilia", 3, "Re:Zero - Starting Life in Another World"),

    "RZ-03": BaseChar("RZ-03", "Rem", 2, "Re:Zero - Starting Life in Another World"),
    "RZ-04": BaseChar("RZ-04", "Ram", 2, "Re:Zero - Starting Life in Another World"),
    "RZ-05": BaseChar("RZ-05", "Roswaal L Mathers", 2, "Re:Zero - Starting Life in Another World", "Roswaal"),
    "RZ-06": BaseChar("RZ-06", "Reinhard Van Astrea", 2, "Re:Zero - Starting Life in Another World", "Reinhard"),
    "RZ-07": BaseChar("RZ-07", "Puck", 2, "Re:Zero - Starting Life in Another World"),
    "RZ-08": BaseChar("RZ-08", "Satella", 2, "Re:Zero - Starting Life in Another World"),

    "RZ-09": BaseChar("RZ-09", "Beatrice", 1, "Re:Zero - Starting Life in Another World"),
    "RZ-10": BaseChar("RZ-10", "Wilhelm Van Astrea", 1, "Re:Zero - Starting Life in Another World", "Wilhelm"),
    "RZ-11": BaseChar("RZ-11", "Crusch", 1, "Re:Zero - Starting Life in Another World"),
    "RZ-12": BaseChar("RZ-12", "Felis", 1, "Re:Zero - Starting Life in Another World"),
    "RZ-13": BaseChar("RZ-13", "Petelgeuse Romanée-Conti", 1, "Re:Zero - Starting Life in Another World", "Petelgeuse"),
    "RZ-14": BaseChar("RZ-14", "Julius Juuklius", 1, "Re:Zero - Starting Life in Another World"),
    "RZ-15": BaseChar("RZ-15", "Elsa Granhiert", 1, "Re:Zero - Starting Life in Another World"),
    "RZ-16": BaseChar("RZ-16", "Garfiel Tinzel", 1, "Re:Zero - Starting Life in Another World"),




    # Attack on Titan

    "AOT-01": BaseChar("AOT-01", "Eren Jaeger", 3, "Attack on Titan"),
    "AOT-02": BaseChar("AOT-02", "Levi Ackerman", 3, "Attack on Titan"),

    "AOT-03": BaseChar("AOT-03", "Mikasa Ackerman", 2, "Attack on Titan"),
    "AOT-04": BaseChar("AOT-04", "Armin Arlert", 2, "Attack on Titan"),
    "AOT-05": BaseChar("AOT-05", "Reiner Braun", 2, "Attack on Titan"),
    "AOT-06": BaseChar("AOT-06", "Zeke Jaeger", 2, "Attack on Titan"),
    "AOT-07": BaseChar("AOT-07", "Erwin Smith", 2, "Attack on Titan"),
    "AOT-08": BaseChar("AOT-08", "Hange Zoe", 2, "Attack on Titan"),

    "AOT-09": BaseChar("AOT-09", "Annie Leonhart", 1, "Attack on Titan"),
    "AOT-10": BaseChar("AOT-10", "Jean Kirstein", 1, "Attack on Titan"),
    "AOT-11": BaseChar("AOT-11", "Sasha Braus", 1, "Attack on Titan"),
    "AOT-12": BaseChar("AOT-12", "Gabi Braun", 1, "Attack on Titan"),
    "AOT-13": BaseChar("AOT-13", "Kenny Ackerman", 1, "Attack on Titan"),
    "AOT-14": BaseChar("AOT-14", "Connie Springer", 1, "Attack on Titan"),
    "AOT-15": BaseChar("AOT-15", "Ymir", 1, "Attack on Titan"),
    "AOT-16": BaseChar("AOT-16", "Bertolt Hoover", 1, "Attack on Titan"),




    # Jujutsu Kaisen

    "JJK-01": BaseChar("JJK-01", "Satoru Gojo", 3, "Jujutsu Kaisen"),
    "JJK-02": BaseChar("JJK-02", "Ryomen Sukuna", 3, "Jujutsu Kaisen"),

    "JJK-03": BaseChar("JJK-03", "Yuji Itadori", 2, "Jujutsu Kaisen"),
    "JJK-04": BaseChar("JJK-04", "Yuta Okkotsu", 2, "Jujutsu Kaisen"),
    "JJK-05": BaseChar("JJK-05", "Megumi Fushiguro", 2, "Jujutsu Kaisen"),
    "JJK-06": BaseChar("JJK-06", "Toji Fushiguro", 2, "Jujutsu Kaisen"),
    "JJK-07": BaseChar("JJK-07", "Mahito", 2, "Jujutsu Kaisen"),

    "JJK-08": BaseChar("JJK-08", "Nobara Kugisaki", 1, "Jujutsu Kaisen"),
    "JJK-09": BaseChar("JJK-09", "Suguru Geto", 1, "Jujutsu Kaisen"),
    "JJK-10": BaseChar("JJK-10", "Choso", 1, "Jujutsu Kaisen"),
    "JJK-11": BaseChar("JJK-11", "Kento Nanami", 1, "Jujutsu Kaisen"),
    "JJK-12": BaseChar("JJK-12", "Toge Inumaki", 1, "Jujutsu Kaisen"),
    "JJK-13": BaseChar("JJK-13", "Maki Zenin", 1, "Jujutsu Kaisen"),
    "JJK-14": BaseChar("JJK-14", "Jogo", 1, "Jujutsu Kaisen"),
    "JJK-15": BaseChar("JJK-15", "Aoi Todo", 1, "Jujutsu Kaisen"),

    


    # One Punch Man

    "OPM-01": BaseChar("OPM-01", "Saitama", 3, "One Punch Man"),
    "OPM-02": BaseChar("OPM-02", "Garou", 3, "One Punch Man"),
    
    "OPM-03": BaseChar("OPM-03", "Genos", 2, "One Punch Man"),
    "OPM-04": BaseChar("OPM-04", "Speed-o'-Sound-Sonic", 2, "One Punch Man", "Sonic"),
    "OPM-05": BaseChar("OPM-05", "Boros", 2, "One Punch Man"),
    "OPM-06": BaseChar("OPM-06", "Bang", 2, "One Punch Man"),
    "OPM-07": BaseChar("OPM-07", "Tatsumaki", 2, "One Punch Man"),

    "OPM-08": BaseChar("OPM-08", "Fubuki", 1, "One Punch Man"),
    "OPM-09": BaseChar("OPM-09", "King", 1, "One Punch Man"),
    "OPM-10": BaseChar("OPM-10", "Metal Bat", 1, "One Punch Man"),
    "OPM-11": BaseChar("OPM-11", "Zombieman", 1, "One Punch Man"),
    "OPM-12": BaseChar("OPM-12", "Watchdog Man", 1, "One Punch Man"),
    "OPM-13": BaseChar("OPM-13", "Metal Knight", 1, "One Punch Man"),
    "OPM-14": BaseChar("OPM-14", "Atomic Samurai", 1, "One Punch Man"),




    # My Hero Academia
    "MHA-01": BaseChar("MHA-01", "Izuki Midoriya", 3, "My Hero Academia"),
    "MHA-02": BaseChar("MHA-02", "Katsuki Bakugo", 3, "My Hero Academia"),
    "MHA-03": BaseChar("MHA-03", "Shoto Todoroki", 3, "My Hero Academia"),

    "MHA-04": BaseChar("MHA-04", "All Might", 2, "My Hero Academia"),
    "MHA-05": BaseChar("MHA-05", "Tomura Shigaraki", 2, "My Hero Academia"),
    "MHA-06": BaseChar("MHA-06", "Endeavour", 2, "My Hero Academia"),
    "MHA-07": BaseChar("MHA-07", "Ochako Uraraka", 2, "My Hero Academia"),
    "MHA-08": BaseChar("MHA-08", "Himiko Toga", 2, "My Hero Academia"),

    "MHA-09": BaseChar("MHA-09", "Dabi", 1, "My Hero Academia"),
    "MHA-10": BaseChar("MHA-10", "Hawks", 1, "My Hero Academia"),
    "MHA-11": BaseChar("MHA-11", "Eijiro Kirishima", 1, "My Hero Academia"),
    "MHA-12": BaseChar("MHA-12", "Shota Aizawa", 1, "My Hero Academia"),
    "MHA-13": BaseChar("MHA-13", "Tenya Ida", 1, "My Hero Academia"),
    "MHA-14": BaseChar("MHA-14", "Hitoshi Shinso", 1, "My Hero Academia"),
    "MHA-15": BaseChar("MHA-15", "Neito Monoma", 1, "My Hero Academia"),
    "MHA-16": BaseChar("MHA-16", "All for One", 1, "My Hero Academia"),
    
    


    # Demon Slayer
    "DS-01": BaseChar("DS-01", "Tanjiro Kamado", 3, "Demon Slayer"),
    "DS-02": BaseChar("DS-02", "Nezuko Kamado", 3, "Demon Slayer"),

    "DS-03": BaseChar("DS-03", "Zenitsu Agatsuma", 2, "Demon Slayer"),
    "DS-04": BaseChar("DS-04", "Muzan Kibutsuji", 2, "Demon Slayer"),
    "DS-05": BaseChar("DS-05", "Giyu Tomioka", 2, "Demon Slayer"),
    "DS-06": BaseChar("DS-06", "Shinobu Kocho", 2, "Demon Slayer"),
    "DS-07": BaseChar("DS-07", "Muichiro Tokito", 2, "Demon Slayer"),
    "DS-08": BaseChar("DS-08", "Inosuke Hashibira", 2, "Demon Slayer"),

    "DS-09": BaseChar("DS-09", "Kanao Tsuyuri", 1, "Demon Slayer"),
    "DS-10": BaseChar("DS-10", "Akaza", 1, "Demon Slayer"),
    "DS-11": BaseChar("DS-11", "Tengen Uzui", 1, "Demon Slayer"),
    "DS-12": BaseChar("DS-12", "Mitsuri Kanroji", 1, "Demon Slayer"),
    "DS-13": BaseChar("DS-13", "Obanai Iguro", 1, "Demon Slayer"),
    "DS-14": BaseChar("DS-14", "Gyomei Himejima", 1, "Demon Slayer"),
    "DS-15": BaseChar("DS-15", "Sanemi Shinazugawa", 1, "Demon Slayer"),
    "DS-16": BaseChar("DS-16", "Kyojuro Rengoku", 1, "Demon Slayer"),




    

    }


def apply_growth(stats: dict, growth_style: str, growth_factor: int) -> dict:

    if growth_factor:
        match growth_style:
            case 'balanced':
                stats['health'] += growth_factor * 5
                stats['attack'] += growth_factor * 5
                stats['defense'] += growth_factor * 5
                stats['magic_attack'] += growth_factor * 5
                stats['magic_defense'] += growth_factor * 5
                stats['speed'] += growth_factor * 3
            case 'offensive':
                stats['health'] += growth_factor * 3
                stats['attack'] += growth_factor * 8
                stats['defense'] += growth_factor * 3
                stats['magic_attack'] += growth_factor * 8
                stats['magic_defense'] += growth_factor * 3
                stats['speed'] += growth_factor * 3
            case 'defensive':
                stats['health'] += growth_factor * 7
                stats['attack'] += growth_factor * 3
                stats['defense'] += growth_factor * 8
                stats['magic_attack'] += growth_factor * 3
                stats['magic_defense'] += growth_factor * 8
                stats['speed'] += growth_factor * 2
            case 'technical':
                stats['health'] += growth_factor * 6
                stats['attack'] += growth_factor * 4
                stats['defense'] += growth_factor * 3
                stats['magic_attack'] += growth_factor * 4
                stats['magic_defense'] += growth_factor * 3
                stats['speed'] += growth_factor * 6

    return stats


def get_party_image(character_id: str, level: int) -> discord.File:
    base: PIL.Image.Image = PIL.Image.open(f'Party/{character_id}.png')
    stars = PIL.Image.open(f'Assets/Level {level if level in [1,2,3,4,5] else 1}.png')

    base.paste(stars, (0, 0), stars)

    with io.BytesIO() as image_binary:
        base = base.convert('RGB')
        base.save(image_binary, 'JPEG')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename='party.jpeg')

from battles.characters import FIGHTERS
from battles.battles import COLOUR_EMOJI_KEY