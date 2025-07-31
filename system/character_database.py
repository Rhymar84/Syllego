import PIL, io
import PIL.Image
import discord, config
from inspect import cleandoc
from system.emoji import EMOJIS

class BaseChar():

    def __init__(self, id: str, name: str, rarity: str, series: str, short_name: str | None = None, boost_item: str | None = None, alternate_forms: tuple = ()):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.series = series
        self.boost_item = boost_item
        self.alternate_forms = alternate_forms
        
        if short_name:
            self.short_name = short_name
        else:
            self.short_name = self.name


    async def display(self, level: float, colour: int, is_new: bool = False) -> discord.Embed:

        emoji = EMOJIS[self.rarity]

        if is_new:
            info = 'NEW!!'
        else:
            info = ''
        

        if level != 0:
            stars = '<:booststar:1383049826073051253>' * max(int(level - 5), 0) + '⭐' * int(min(level, 10 - level))
        else:
            stars = '🔒'

        series = self.series

        embed = discord.Embed(title=f'{emoji} {self.name} {stars} {info}', color=colour)
        embed.set_footer(text=series)

        return embed
    
class AltForm(BaseChar):
    
    def __init__(self, id: str, name: str, short_name: str | None = None, unlock_item: str | None = None):
        base_character = CHARACTERS[id[:6]]
        super().__init__(id, name, base_character.rarity, base_character.series, short_name=short_name)
        self.unlock_item = unlock_item


class CharInfo(discord.ui.View):

    def __init__(self, original_interaction: discord.Interaction, character: BaseChar, level: int):
        super().__init__()

        self.base_char = character
        self.level = level
        self.original_interaction = original_interaction
        self.timeout = 60

        self.forms = [character] + [ALT_FORMS[x] for x in character.alternate_forms]
        self.current_form = 0

        if len(self.forms) == 1:
            self.add_item(ViewStatsButton())
        else:
            self.add_item(ScrollButton(-1))
            self.add_item(ViewStatsButton())
            self.add_item(ScrollButton(1))

    async def scroll_update(self, interaction: discord.Interaction):

        extension = "gif" if self.base_char.rarity == "mythical" else "jpg"

        embed: discord.Embed = await self.base_char.display(self.level, 0xb71010)
        portrait = discord.File(f'Assets/Portraits/{self.base_char.id}.{extension}', filename=f'portrait.{extension}')
        embed.set_image(url=f'attachment://portrait.{extension}')

        await interaction.response.edit_message(embed=embed, attachments=[portrait], view=self)

class ScrollButton(discord.ui.Button):

    def __init__(self, step: int):
        super().__init__(style=discord.ButtonStyle.grey, emoji='⬅️' if step < 0 else '➡️')
        self.step = step

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.view.original_interaction.user:
            return False
        return True

    async def callback(self, interaction: discord.Interaction):

        view: CharInfo = self.view

        view.current_form = (view.current_form + self.step) % len(view.forms)
        view.base_char = view.forms[view.current_form]

        await view.scroll_update(interaction)


class ViewStatsButton(discord.ui.Button):

    def __init__(self):
        super().__init__(style=discord.ButtonStyle.grey, emoji='📊')

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.view.original_interaction.user:
            return False
        return True

    async def callback(self, interaction):

        view: CharInfo = self.view

        character = FIGHTERS[view.base_char.id]

        attribute = character['attribute']
        growth_style = character['growth_style']
        growth_factor = max(1, view.level) - 1

        stats = {'health': character['health'], 'attack': character['attack'], 'defense': character['defense'], 'magic_attack': character['magic_attack'], 'magic_defense': character['magic_defense'], 'speed': character['speed']}
        stats = apply_growth(stats, growth_style, growth_factor)

        text = f"**HP:** {stats['health']} | **Spe**: {stats['speed']}\n**Atk:** {stats['attack']} | **Def:** {stats['defense']}\n**M.A:** {stats['magic_attack']} | **M.D:** {stats['magic_defense']}"
        text += f"\n\n**(Passive) {character['passive_ability'].name}**\n{character['passive_ability'].display()}" if character['passive_ability'] else ''
        text += f"\n\n**(Active) {character['active_ability'].name}**\n{character['active_ability'].display()}" if character['active_ability'] else ''
        tags = [f"**{x}**🧬" for x in character['chemistry_tags']] + character['tags']
        if tags:
            text +=f"\n\n*Tags: {', '.join(tags)}*"
        if view.base_char.boost_item:
            from system.farming import item_display_string
            newline = '' if tags else '\n'
            text += f"{newline}\n*Boost:* **{item_display_string(view.base_char.boost_item)}**"

        embed = discord.Embed(title=f"{config.COLOUR_EMOJI_KEY[attribute]} {view.base_char.name}", description = text, color=config.CHARACTER_EMBED_COLOUR)
        thumbnail = get_party_image(view.base_char, view.level)
        embed.set_thumbnail(url=f'attachment://{thumbnail.filename}')
        embed.set_footer(text=view.base_char.series)

        await interaction.response.edit_message(embed=embed, view=None, attachments=[thumbnail])
    
CHARACTERS = {

    # DRAGON BALL Z

    "DBZ-01": BaseChar("DBZ-01", "Son Goku", "mythical", "Dragon Ball Z", short_name="Goku", alternate_forms=("DBZ-01-1", "DBZ-01-2")),
    "DBZ-02": BaseChar("DBZ-02", "Vegeta", "mythical", "Dragon Ball Z", alternate_forms=("DBZ-02-1", "DBZ-02-2")),

    "DBZ-03": BaseChar("DBZ-03", "Son Gohan", "shining", "Dragon Ball Z", short_name="Goku", alternate_forms=("DBZ-03-1", "DBZ-03-2")),
    "DBZ-04": BaseChar("DBZ-04", "Frieza", "shining", "Dragon Ball Z", alternate_forms=("DBZ-04-1",)),
    "DBZ-05": BaseChar("DBZ-05", "Cell", "shining", "Dragon Ball Z", alternate_forms=("DBZ-05-1",)),
    "DBZ-06": BaseChar("DBZ-06", "Majin Buu", "shining", "Dragon Ball Z", alternate_forms=("DBZ-06-1", "DBZ-06-2")),
    "DBZ-07": BaseChar("DBZ-07", "Piccolo", "shining", "Dragon Ball Z"),

    "DBZ-08": BaseChar("DBZ-08", "Krillin", "glowing", "Dragon Ball Z"),
    "DBZ-09": BaseChar("DBZ-09", "Tien", "glowing", "Dragon Ball Z"),
    "DBZ-10": BaseChar("DBZ-10", "Trunks", "glowing", "Dragon Ball Z", alternate_forms=("DBZ-10-1",)),
    "DBZ-11": BaseChar("DBZ-11", "Master Roshi", "glowing", "Dragon Ball Z"),
    "DBZ-12": BaseChar("DBZ-12", "Nappa", "glowing", "Dragon Ball Z"),
    "DBZ-13": BaseChar("DBZ-13", "Captain Ginyu", "glowing", "Dragon Ball Z", short_name="Ginyu"),
    "DBZ-14": BaseChar("DBZ-14", "Dabura", "glowing", "Dragon Ball Z"),
    
    "DBZ-15": BaseChar("DBZ-15", "Videl", "common", "Dragon Ball Z", boost_item="senzu_bean"), # These commons were given numbers out of order so that
    "DBZ-16": BaseChar("DBZ-16", "Android 16", "common", "Dragon Ball Z", boost_item="senzu_bean"), # The androids can have their numbers matching :)
    "DBZ-17": BaseChar("DBZ-17", "Android 17", "glowing", "Dragon Ball Z"),
    "DBZ-18": BaseChar("DBZ-18", "Android 18", "glowing", "Dragon Ball Z"),

    "DBZ-19": BaseChar("DBZ-19", "Android 19", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-20": BaseChar("DBZ-20", "Android 20", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-21": BaseChar("DBZ-21", "Yamcha", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-22": BaseChar("DBZ-22", "Chiaotzu", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-23": BaseChar("DBZ-23", "Nail", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-24": BaseChar("DBZ-24", "Son Goten", "common", "Dragon Ball Z", short_name="Goten", boost_item="senzu_bean", alternate_forms=("DBZ-24-1",)),
    "DBZ-25": BaseChar("DBZ-25", "Yajirobe", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-26": BaseChar("DBZ-26", "Zarbon", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-27": BaseChar("DBZ-27", "Jeice", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-28": BaseChar("DBZ-28", "Recoome", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-29": BaseChar("DBZ-29", "Burter", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-30": BaseChar("DBZ-30", "Guldo", "common", "Dragon Ball Z", boost_item="senzu_bean"),
    "DBZ-31": BaseChar("DBZ-31", "Hercule", "common", "Dragon Ball Z", boost_item="senzu_bean"),


    # Jujutsu Kaisen

    "JJK-01": BaseChar("JJK-01", "Satoru Gojo", "mythical", "Jujutsu Kaisen"),
    "JJK-02": BaseChar("JJK-02", "Ryomen Sukuna", "mythical", "Jujutsu Kaisen"),

    "JJK-03": BaseChar("JJK-03", "Yuji Itadori", "shining", "Jujutsu Kaisen"),
    "JJK-04": BaseChar("JJK-04", "Yuta Okkotsu", "shining", "Jujutsu Kaisen"),
    "JJK-05": BaseChar("JJK-05", "Toji Zenin", "shining", "Jujutsu Kaisen"),
    "JJK-06": BaseChar("JJK-06", "Suguru Geto", "shining", "Jujutsu Kaisen"),
    "JJK-07": BaseChar("JJK-07", "Megumi Fushiguro", "shining", "Jujutsu Kaisen"),

    "JJK-08": BaseChar("JJK-08", "Mahito", "glowing", "Jujutsu Kaisen"),
    "JJK-09": BaseChar("JJK-09", "Choso", "glowing", "Jujutsu Kaisen"),
    "JJK-10": BaseChar("JJK-10", "Aoi Todo", "glowing", "Jujutsu Kaisen"),
    "JJK-11": BaseChar("JJK-11", "Jogo", "glowing", "Jujutsu Kaisen"),
    "JJK-12": BaseChar("JJK-12", "Maki Zenin", "glowing", "Jujutsu Kaisen"),
    "JJK-13": BaseChar("JJK-13", "Yuki Tsukumo", "glowing", "Jujutsu Kaisen"),
    "JJK-14": BaseChar("JJK-14", "Hajime Kashimo", "glowing", "Jujutsu Kaisen"),
    "JJK-15": BaseChar("JJK-15", "Kinji Hakari", "glowing", "Jujutsu Kaisen"),
    "JJK-16": BaseChar("JJK-16", "Hiromi Higuruma", "glowing", "Jujutsu Kaisen"),

    "JJK-17": BaseChar("JJK-17", "Nobara Kugisaki", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-18": BaseChar("JJK-18", "Toge Inumaki", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-19": BaseChar("JJK-19", "Panda", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-20": BaseChar("JJK-20", "Kasumi Miwa", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-21": BaseChar("JJK-21", "Kokichi Muta", "common", "Jujutsu Kaisen", short_name="Mechamaru", boost_item="cursed_tool"),
    "JJK-22": BaseChar("JJK-22", "Momo Nishimiya", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-23": BaseChar("JJK-23", "Hanami", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-24": BaseChar("JJK-24", "Dagon", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-25": BaseChar("JJK-25", "Atsuya Kusakabe", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-26": BaseChar("JJK-26", "Uruame", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-27": BaseChar("JJK-27", "Kenjaku", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-28": BaseChar("JJK-28", "Mei Mei", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-29": BaseChar("JJK-29", "Kento Nanami", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-30": BaseChar("JJK-30", "Miguel Oduol", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),
    "JJK-31": BaseChar("JJK-31", "Mai Zenin", "common", "Jujutsu Kaisen", boost_item="cursed_tool"),

    


    # # One Punch Man

    # "OPM-01": BaseChar("OPM-01", "Saitama", 3, "One Punch Man"),
    # "OPM-02": BaseChar("OPM-02", "Garou", 3, "One Punch Man"),
    
    # "OPM-03": BaseChar("OPM-03", "Genos", 2, "One Punch Man"),
    # "OPM-04": BaseChar("OPM-04", "Speed-o'-Sound-Sonic", 2, "One Punch Man", "Sonic"),
    # "OPM-05": BaseChar("OPM-05", "Boros", 2, "One Punch Man"),
    # "OPM-06": BaseChar("OPM-06", "Bang", 2, "One Punch Man"),
    # "OPM-07": BaseChar("OPM-07", "Tatsumaki", 2, "One Punch Man"),

    # "OPM-08": BaseChar("OPM-08", "Fubuki", 1, "One Punch Man"),
    # "OPM-09": BaseChar("OPM-09", "King", 1, "One Punch Man"),
    # "OPM-10": BaseChar("OPM-10", "Metal Bat", 1, "One Punch Man"),
    # "OPM-11": BaseChar("OPM-11", "Zombieman", 1, "One Punch Man"),
    # "OPM-12": BaseChar("OPM-12", "Watchdog Man", 1, "One Punch Man"),
    # "OPM-13": BaseChar("OPM-13", "Metal Knight", 1, "One Punch Man"),
    # "OPM-14": BaseChar("OPM-14", "Atomic Samurai", 1, "One Punch Man"),




    # # My Hero Academia
    # "MHA-01": BaseChar("MHA-01", "Izuku Midoriya", 3, "My Hero Academia", "Deku"),
    # "MHA-02": BaseChar("MHA-02", "Katsuki Bakugo", 3, "My Hero Academia", "Bakugo"),
    # "MHA-03": BaseChar("MHA-03", "Shoto Todoroki", 3, "My Hero Academia", "Todoroki"),

    # "MHA-04": BaseChar("MHA-04", "All Might", 2, "My Hero Academia"),
    # "MHA-05": BaseChar("MHA-05", "Tomura Shigaraki", 2, "My Hero Academia", "Shigaraki"),
    # "MHA-06": BaseChar("MHA-06", "Endeavour", 2, "My Hero Academia"),
    # "MHA-07": BaseChar("MHA-07", "Ochako Uraraka", 2, "My Hero Academia"),
    # "MHA-08": BaseChar("MHA-08", "Himiko Toga", 2, "My Hero Academia"),

    # "MHA-09": BaseChar("MHA-09", "Dabi", 1, "My Hero Academia"),
    # "MHA-10": BaseChar("MHA-10", "Hawks", 1, "My Hero Academia"),
    # "MHA-11": BaseChar("MHA-11", "Eijiro Kirishima", 1, "My Hero Academia"),
    # "MHA-12": BaseChar("MHA-12", "Shota Aizawa", 1, "My Hero Academia"),
    # "MHA-13": BaseChar("MHA-13", "Tenya Ida", 1, "My Hero Academia"),
    # "MHA-14": BaseChar("MHA-14", "Hitoshi Shinso", 1, "My Hero Academia"),
    # "MHA-15": BaseChar("MHA-15", "Neito Monoma", 1, "My Hero Academia"),
    # "MHA-16": BaseChar("MHA-16", "All for One", 1, "My Hero Academia"),
    
    


    # # Demon Slayer
    # "DS-01": BaseChar("DS-01", "Tanjiro Kamado", 3, "Demon Slayer", "Tanjiro"),
    # "DS-02": BaseChar("DS-02", "Nezuko Kamado", 3, "Demon Slayer", "Nezuko"),

    # "DS-03": BaseChar("DS-03", "Zenitsu Agatsuma", 2, "Demon Slayer"),
    # "DS-04": BaseChar("DS-04", "Muzan Kibutsuji", 2, "Demon Slayer"),
    # "DS-05": BaseChar("DS-05", "Giyu Tomioka", 2, "Demon Slayer"),
    # "DS-06": BaseChar("DS-06", "Shinobu Kocho", 2, "Demon Slayer"),
    # "DS-07": BaseChar("DS-07", "Muichiro Tokito", 2, "Demon Slayer"),
    # "DS-08": BaseChar("DS-08", "Inosuke Hashibira", 2, "Demon Slayer"),

    # "DS-09": BaseChar("DS-09", "Kanao Tsuyuri", 1, "Demon Slayer"),
    # "DS-10": BaseChar("DS-10", "Akaza", 1, "Demon Slayer"),
    # "DS-11": BaseChar("DS-11", "Tengen Uzui", 1, "Demon Slayer"),
    # "DS-12": BaseChar("DS-12", "Mitsuri Kanroji", 1, "Demon Slayer"),
    # "DS-13": BaseChar("DS-13", "Obanai Iguro", 1, "Demon Slayer"),
    # "DS-14": BaseChar("DS-14", "Gyomei Himejima", 1, "Demon Slayer"),
    # "DS-15": BaseChar("DS-15", "Sanemi Shinazugawa", 1, "Demon Slayer"),
    # "DS-16": BaseChar("DS-16", "Kyojuro Rengoku", 1, "Demon Slayer"),




    # # Hunter x Hunter
    # "HXH-01": BaseChar("HXH-01", "Gon Freecss", 3, "Hunter x Hunter", "Gon"),
    # "HXH-02": BaseChar("HXH-02", "Killua Zoldyck", 3, "Hunter x Hunter", "Killua"),

    # "HXH-03": BaseChar("HXH-03", "Kurapika", 2, "Hunter x Hunter"),
    # "HXH-04": BaseChar("HXH-04", "Hisoka Morow", 2, "Hunter x Hunter", "Hisoka"),
    # "HXH-05": BaseChar("HXH-05", "Biscuit Krueger", 2, "Hunter x Hunter", "Bisky"),
    # "HXH-06": BaseChar("HXH-06", "Kite", 2, "Hunter x Hunter"),
    # "HXH-07": BaseChar("HXH-07", "Meruem", 2, "Hunter x Hunter"),
    # "HXH-08": BaseChar("HXH-08", "Neferpitou", 2, "Hunter x Hunter", "Pitou"),

    # "HXH-09": BaseChar("HXH-09", "Leorio Paradinight", 1, "Hunter x Hunter", "Leorio"),
    # "HXH-10": BaseChar("HXH-10", "Chrollo Lucilfer", 1, "Hunter x Hunter", "Chrollo"),
    # "HXH-11": BaseChar("HXH-11", "Morel Mackernasey", 1, "Hunter x Hunter", "Morel"),
    # "HXH-12": BaseChar("HXH-12", "Ging Freecss", 1, "Hunter x Hunter", "Ging"),
    # "HXH-13": BaseChar("HXH-13", "Razor", 1, "Hunter x Hunter"),
    # "HXH-14": BaseChar("HXH-14", "Genthru", 1, "Hunter x Hunter"),
    # "HXH-15": BaseChar("HXH-15", "Knuckle Bine", 1, "Hunter x Hunter", "Knuckle"),
    # "HXH-16": BaseChar("HXH-16", "Isaac Netero", 1, "Hunter x Hunter", "Netero")

    }

ALT_FORMS = {
    "DBZ-01-1": AltForm("DBZ-01-1", "Super Saiyan Goku", short_name="Goku"),
    "DBZ-01-2": AltForm("DBZ-01-2", "Super Saiyan 2 Goku", short_name="Goku"),
    "DBZ-02-1": AltForm("DBZ-02-1", "Super Saiyan Vegeta", short_name="Vegeta"),
    "DBZ-02-2": AltForm("DBZ-02-2", "Majin Vegeta", short_name="Vegeta"),
    "DBZ-03-1": AltForm("DBZ-03-1", "Super Saiyan 2 Gohan", short_name="Gohan"),
    "DBZ-03-2": AltForm("DBZ-03-2", "Ultimate Gohan", short_name="Gohan"),
    "DBZ-04-1": AltForm("DBZ-04-1", "Final Form Frieza", short_name="Frieza"),
    "DBZ-05-1": AltForm("DBZ-05-1", "Perfect Cell", short_name="Cell"),
    "DBZ-06-1": AltForm("DBZ-06-1", "Super Buu", short_name="Majin Buu"),
    "DBZ-06-2": AltForm("DBZ-06-2", "Kid Buu", short_name="Majin Buu"),
    "DBZ-10-1": AltForm("DBZ-10-1", "Future Trunks", short_name="Trunks"),
    "DBZ-24-1": AltForm("DBZ-24-1", "Super Saiyan Goten", short_name="Goten"),
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


def get_party_image(character: BaseChar, level: int, save_discord_file: bool = True) -> discord.File | PIL.Image.Image:
    try:
        base: PIL.Image.Image = PIL.Image.open(f'Assets/Party/{character.id}.jpg')
    except FileNotFoundError:
        base = PIL.Image.open(f"Assets/missing_asset.png")
    frame = PIL.Image.open('Assets/{rarity}.png'.format(rarity=character.rarity.title()))
    stars = PIL.Image.open(f'Assets/Level {level if level in [1,2,3,4,5] else 1}.png')

    base.paste(frame, (0, 0), frame)
    base.paste(stars, (0, 0), stars)

    if not save_discord_file:
        return base

    with io.BytesIO() as image_binary:
        base = base.convert('RGB')
        base.save(image_binary, 'JPEG')
        image_binary.seek(0)
        return discord.File(fp=image_binary, filename='party.jpeg')

from battles.characters import FIGHTERS