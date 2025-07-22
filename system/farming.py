import discord
import random
import math
import config
import system.gacha as gacha
import datetime as dt
import aiosqlite
import system.items as items
import system.recipes as recipes
import heapq

FARMING_MODES = {1: 'grow', 2: 'harvest', 3: 'extract'}
FARMING_MODE_MAP = {"grow": "🚜", "harvest": "🐄", "extract": "⛏️"}
REFINING_MODES = {1: "basic", 2: "fire", 3: 'water', 4: "wind", 5: "earth"}
REFINERY_MODE_NAMES = {"basic": "🛠️ Basic Refinement 🛠️", "fire": "🔥 Fire Tempering 🔥", "water": "💧 Water Cleansing 💧", "wind": "💨 Wind Polishing 💨", "earth": "⛰️ Earth Nurturing ⛰️"}
REFINERY_MODE_EMOJIS = {"basic": "🛠️", "fire": "🔥", "water": "💧", "wind": "💨", "earth": "⛰️"}

farming_notifications = []
refinery_notifications = []

async def get_aiofu_progress(member: discord.Member) -> dict:

    async with aiosqlite.connect("databases/farming.sqlite") as db:
        db.row_factory = aiosqlite.Row
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT * FROM farming WHERE user_id = {member.id}')
            row = await cursor.fetchone()

    if not row:
        await gacha.insert_user_record('farming', 'farming', member)
        return {1: {"slot": 1, "item": None, "time_left": -1}, 2: {"slot": 2, "item": None, "time_left": -1}, 3: {"slot": 3, "item": None, "time_left": -1}}
    
    slot1 = {"slot": 1, "item": None, "time_left": -1}
    slot2 = {"slot": 2, "item": None, "time_left": -1}
    slot3 = {"slot": 3, "item": None, "time_left": -1}

    if row["slot1_item"]:
        slot1 = {"slot": 1, "item": row["slot1_item"], "time_left": row["slot1_time_left"], "last_update": row["slot1_last_update"], "processing_type": row["slot1_processing_type"]}
    if row["slot2_item"]:
        slot2 = {"slot": 2, "item": row["slot2_item"], "time_left": row["slot2_time_left"], "last_update": row["slot2_last_update"], "processing_type": row["slot2_processing_type"]}
    if row["slot3_item"]:
        slot3 = {"slot": 3, "item": row["slot3_item"], "time_left": row["slot3_time_left"], "last_update": row["slot3_last_update"], "processing_type": row["slot3_processing_type"]}

    await update_aiofu_slots(member, [x for x in [slot1, slot2, slot3] if x["item"] is not None])

    return {1: slot1, 2: slot2, 3: slot3}


async def update_aiofu_slots(member: discord.Member, slots: list[dict]):

    for slot in slots:

        if slot["time_left"] <= 0:
            continue

        # Get number of seconds since last update
        last_update = dt.datetime.strptime(slot["last_update"], "%d-%m-%Y %H:%M")
        now = dt.datetime.now()
        difference = now - last_update
        seconds = difference.total_seconds()

        if seconds < 60:
            continue

        new_time_left = slot["time_left"] - int(seconds / 60)

        await progress_aiofu_slot(member, slot["slot"], new_time_left)
        slot["time_left"] = max(0, new_time_left)
        slot["last_update"] = dt.datetime.now().strftime("%d-%m-%Y %H:%M")


async def progress_aiofu_slot(member: discord.Member, slot: int, minutes_left: int):

    async with aiosqlite.connect("databases/farming.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE farming SET slot{slot}_time_left = ?, slot{slot}_last_update = ? WHERE user_id = ?')
            val = (max(minutes_left, 0), dt.datetime.now().strftime("%d-%m-%Y %H:%M"), member.id)
            await cursor.execute(sql, val)

        await db.commit()

async def clear_aiofu_slot(member: discord.Member, slot: int):

    async with aiosqlite.connect("databases/farming.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE farming SET slot{slot}_item = null, slot{slot}_time_left = null, slot{slot}_processing_type = null, slot{slot}_last_update = null WHERE user_id = ?')
            val = (member.id,)
            await cursor.execute(sql, val)

        await db.commit()


async def get_aiofu_embed(member: discord.Member) -> tuple[discord.Embed, discord.ui.View]:
    
    progress = await get_aiofu_progress(member)
    content = ""

    for slot in progress.values():
        if slot['item'] is None:
            if await has_unlocked_aiofu_slot(member, slot['slot']):
                content += f"💡 **__SLOT {slot['slot']}__\n** <Available>\n\n"
            else:
                content += f"⛔ **__SLOT {slot['slot']}__\n** <Locked>\n\n"
        else:
            if slot["time_left"] <= 0:
                content += f"✅ **__SLOT {slot['slot']}__\n** {FARMING_MODE_MAP[slot['processing_type']]} *{item_display_string(slot['item'])}* `Done!`\n\n"
            else:
                minutes = slot["time_left"]
                hours = int(minutes / 60)
                days = int(hours / 24)
                minutes = minutes % 60
                hours = hours % 24
                time = f"{('0' + str(days) + ':' if days < 10 else str(days) + ':') if days else ''}{'0' + str(hours) if hours < 10 else str(hours)}:{'0' + str(minutes) if minutes < 10 else str(minutes)}"
                
                content += f"⌛ **__SLOT {slot['slot']}__\n** {FARMING_MODE_MAP[slot['processing_type']]} *{item_display_string(slot['item'])}* `{time}`\n\n"

    embed = discord.Embed(
        title="AIO Farming Unit",
        description=content,
        color=0x32a852
    )
    embed.set_author(name=f"{member.display_name}", icon_url=f'{member.display_avatar}')
    embed.set_footer(text="Use /farming start to begin.")


    harvestables = [x for x in progress.values() if x["time_left"] == 0]
    if harvestables:
        view = discord.ui.View()
        view.add_item(FarmingCollectButton(member))
    else:
        view = None

    return embed, view


async def has_unlocked_aiofu_slot(member: discord.Member, slot: int) -> bool:

    if slot == 1:
        return True
    else:
        return False


class FarmingCollectButton(discord.ui.Button):
    
    def __init__(self, user: discord.Member, *, style = discord.ButtonStyle.gray, label = None, disabled = False, custom_id = None, url = None, emoji = None, row = None, sku_id = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=random.choice(('🍂', '🍃', '🍓', '🍇')), row=row, sku_id=sku_id)
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.user:
            progress = await get_aiofu_progress(self.user)
            slots = [x for x in progress.values() if x["time_left"] == 0]
            if slots:
                return True
            else:
                await interaction.response.send_message(ephemeral=True, embed=discord.Embed(description='These items have already been collected.', color=config.ErrorColour))
                return False
                

        await interaction.response.send_message(ephemeral=True, embed=discord.Embed(description='This is not your button!', color=config.ErrorColour))
        return False
    
    async def callback(self, interaction: discord.Interaction):

        self.view.stop()

        progress = await get_aiofu_progress(self.user)
        slots = [x for x in progress.values() if x["time_left"] == 0]
        
        # Key = item id, Value = count
        harvested = {}

        for slot in slots:
            try:
                # Get loot table for item being processed and make weighted choice from its loot table
                loot_table = items.ITEMS[slot["item"]][f"farming_{slot['processing_type']}"]["loot_table"]
                loot: dict = random.choices([x["loot"] for x in loot_table], [x["chance"] for x in loot_table])[0]

                # For each item id in the loot dict, set item id in harvested count to loot count + any existing ones harvested
                for item in loot.keys():
                    harvested[item] = loot[item] + harvested.get(item, 0)
                
            except IndexError:
                print(f"Error: Item '{slot['item']}' harvesting encountered Index Error. Likely because it has an empty loot table.")
            except KeyError:
                print(f"Error: Item '{slot['item']}' harvesting encountered Key Error. Likely because it has no loot table.")
        
        if harvested:
            harvested_string = '\n'.join([f"- {item_display_string(x[0])} x**{x[1]}**" for x in harvested.items()])
            message = f"✨ **The following items were obtained!** ✨\n{harvested_string}"
        else:
            message = f"Oh no! The processing failed. Nothing was obtained :("

        embed, view = await get_aiofu_embed(self.user)

        for harvested_item in harvested.keys():
            await gacha.gain_item(self.user, harvested_item, harvested[harvested_item])
        for to_clear in [x["slot"] for x in slots]:
            await clear_aiofu_slot(self.user, to_clear)

        embed.description += message
        embed.remove_footer()
        
        await interaction.response.edit_message(embed=embed, view=None)

async def get_available_aiofu_slots(member: discord.Member) -> list[int]:

    progress = await get_aiofu_progress(member)
    available = [x for x in [1,2,3] if progress[x]["item"] is None]
    available = [x for x in available if await has_unlocked_aiofu_slot(member, x)]

    return available


        
async def check_farming_errors(interaction: discord.Interaction, item: str, mode: int) -> bool:

    match mode:
        case 1:
            mode = 'grow'
            error_mode = 'grown'
        case 2:
            mode = 'harvest'
            error_mode = 'harvested'
        case 3:
            mode = 'extract'
            error_mode = 'extracted'

    available_slots = await get_available_aiofu_slots(interaction.user)
    if not available_slots:
        await interaction.response.send_message(embed=discord.Embed(description='Your AIO Farming Unit has no available slots.', color=config.ErrorColour), ephemeral=True)
        return True
    
    if item not in items.ITEMS.keys():
        await interaction.response.send_message(embed=discord.Embed(description=f"Could not find item '{item}'.", color=config.ErrorColour), ephemeral=True)
        return True
    inventory = await gacha.get_inventory(interaction.user)
    if item not in inventory.keys():
        await interaction.response.send_message(embed=discord.Embed(description='You do not own this item.', color=config.ErrorColour), ephemeral=True)
        return True
    if items.ITEMS[item].get(f"farming_{mode}", None) is None:
        await interaction.response.send_message(embed=discord.Embed(description=f"**{items.ITEMS[item]['name']}** cannot be {error_mode}.", color=config.ErrorColour), ephemeral=True)
        return True
    
    
    return False


async def start_farming(member: discord.Member, item: str, mode: int):

    mode = FARMING_MODES[mode]
    available = await get_available_aiofu_slots(member)
    slot = available[0]

    time = items.ITEMS[item][f"farming_{mode}"]["time"]

    async with aiosqlite.connect("databases/farming.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE farming SET slot{slot}_item = ?, slot{slot}_time_left = ?, slot{slot}_processing_type = ?, slot{slot}_last_update = ? WHERE user_id = ?')
            val = (item, time, mode, dt.datetime.now().strftime("%d-%m-%Y %H:%M"), member.id)
            await cursor.execute(sql, val)

        await db.commit()

    await gacha.gain_item(member, item, -1)

    settings = await gacha.get_settings(member)
    if settings["farming_dms"]:
        completion_time = dt.datetime.now() + dt.timedelta(minutes=time)
        heapq.heappush(farming_notifications, (completion_time, member))


async def send_aiofu_notification(member: discord.Member):

    embed = discord.Embed(
        title="✨ Farming Complete! ✨", 
        description=f"Your AIO Farming Unit has finished processing an item! ⏰\nUse /farming view to collect your rewards. 🚜🪓",
        color=0x03fc1c
        )
    embed.set_author(name=f"{member.display_name}", icon_url=f'{member.display_avatar}')

    try:
        await member.send(embed=embed)
    except discord.errors.Forbidden:
        return
    


async def get_item_farming_obtaining(item: str) -> list[dict]:

    if item not in items.ITEMS.keys():
        return []
    
    sources = []

    for id, source in items.ITEMS.items():
        
        for mode in ["grow", "harvest", "extract"]:
            recipe = source.get(f"farming_{mode}", None)
            if not recipe:
                continue

            loot_table = recipe["loot_table"]
            for loot in loot_table:
                if item in loot["loot"].keys() and not any([(x["input_item"] == id and x["mode"] == mode) for x in sources]):
                    sources.append({"input_item": id, "mode": mode, "output_quantity": loot["loot"][item]})

    return sources


################### REFINERY #

async def get_refinery_progress(member: discord.Member) -> dict:

    async with aiosqlite.connect("databases/farming.sqlite") as db:
        db.row_factory = aiosqlite.Row
        async with db.cursor() as cursor:
            await cursor.execute(f'SELECT * FROM refinery WHERE user_id = {member.id}')
            row = await cursor.fetchone()

    if not row:
        await gacha.insert_user_record('farming', 'refinery', member)
        return {1: {"slot": 1, "recipe": None, "time_left": -1}, 2: {"slot": 2, "recipe": None, "time_left": -1}, 3: {"slot": 3, "recipe": None, "time_left": -1}}
    
    slot1 = {"slot": 1, "recipe": None, "time_left": -1}
    slot2 = {"slot": 2, "recipe": None, "time_left": -1}
    slot3 = {"slot": 3, "recipe": None, "time_left": -1}

    if row["slot1_recipe"]:
        slot1 = {"slot": 1, "recipe": row["slot1_recipe"], "time_left": row["slot1_time_left"], "last_update": row["slot1_last_update"], "mode": row["slot1_mode"]}
    if row["slot2_recipe"]:
        slot2 = {"slot": 2, "recipe": row["slot2_recipe"], "time_left": row["slot2_time_left"], "last_update": row["slot2_last_update"], "mode": row["slot2_mode"]}
    if row["slot3_recipe"]:
        slot3 = {"slot": 3, "recipe": row["slot3_recipe"], "time_left": row["slot3_time_left"], "last_update": row["slot3_last_update"], "mode": row["slot3_mode"]}

    await update_refinery_slots(member, [x for x in [slot1, slot2, slot3] if x["recipe"] is not None])

    return {1: slot1, 2: slot2, 3: slot3}


async def update_refinery_slots(member: discord.Member, slots: list[dict]):

    for slot in slots:

        if slot["time_left"] <= 0:
            continue

        # Get number of seconds since last update
        last_update = dt.datetime.strptime(slot["last_update"], "%d-%m-%Y %H:%M")
        now = dt.datetime.now()
        difference = now - last_update
        seconds = difference.total_seconds()

        if seconds < 60:
            continue

        new_time_left = slot["time_left"] - int(seconds / 60)

        await progress_refinery_slot(member, slot["slot"], new_time_left)
        slot["time_left"] = max(0, new_time_left)
        slot["last_update"] = dt.datetime.now().strftime("%d-%m-%Y %H:%M")


async def progress_refinery_slot(member: discord.Member, slot: int, minutes_left: int):

    async with aiosqlite.connect("databases/farming.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE refinery SET slot{slot}_time_left = ?, slot{slot}_last_update = ? WHERE user_id = ?')
            val = (max(minutes_left, 0), dt.datetime.now().strftime("%d-%m-%Y %H:%M"), member.id)
            await cursor.execute(sql, val)

        await db.commit()

async def clear_refinery_slot(member: discord.Member, slot: int):

    async with aiosqlite.connect("databases/farming.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE refinery SET slot{slot}_recipe= null, slot{slot}_time_left = null, slot{slot}_mode = null, slot{slot}_last_update = null WHERE user_id = ?')
            val = (member.id,)
            await cursor.execute(sql, val)

        await db.commit()

async def get_refinery_embed(member: discord.Member) -> tuple[discord.Embed, discord.ui.View]:
    
    progress = await get_refinery_progress(member)
    content = ""

    for slot in progress.values():
        if slot['recipe'] is None:
            if await has_unlocked_refinery_slot(member, slot['slot']):
                content += f"💡 **__SLOT {slot['slot']}__\n** <Available>\n\n"
            else:
                content += f"⛔ **__SLOT {slot['slot']}__\n** <Locked>\n\n"
        else:
            if slot["time_left"] <= 0:
                content += f"✅ **__SLOT {slot['slot']}__\n** {REFINERY_MODE_EMOJIS[slot['mode']]} *[{recipes.RECIPES[slot['recipe']]['name']}]* `Done!`\n\n"
            else:
                minutes = slot["time_left"]
                hours = int(minutes / 60)
                days = int(hours / 24)
                minutes = minutes % 60
                hours = hours % 24
                time = f"{('0' + str(days) + ':' if days < 10 else str(days) + ':') if days else ''}{'0' + str(hours) if hours < 10 else str(hours)}:{'0' + str(minutes) if minutes < 10 else str(minutes)}"
                
                content += f"⌛ **__SLOT {slot['slot']}__\n** {REFINERY_MODE_EMOJIS[slot['mode']]} *[{recipes.RECIPES[slot['recipe']]['name']}]* `{time}`\n\n"

    embed = discord.Embed(
        title="Refinery",
        description=content,
        color=0xbd193f
    )
    embed.set_author(name=f"{member.display_name}", icon_url=f'{member.display_avatar}')
    embed.set_footer(text="Use /refinery start to begin.")


    harvestables = [x for x in progress.values() if x["time_left"] == 0]
    if harvestables:
        view = discord.ui.View()
        view.add_item(RefineryCollectButton(member))
    else:
        view = None

    return embed, view

async def has_unlocked_refinery_slot(member: discord.Member, slot: int) -> bool:

    if slot == 1:
        return True
    else:
        return False

async def send_refinery_notification(member: discord.Member):

    embed = discord.Embed(
        title="✨ Refinement Complete! ✨", 
        description=f"Your Refinery has finished a recipe! ⏰\nUse /refinery view to collect your rewards. 💎🛠️",
        color=0xfc5151
        )
    embed.set_author(name=f"{member.display_name}", icon_url=f'{member.display_avatar}')

    try:
        await member.send(embed=embed)
    except discord.errors.Forbidden:
        return

class RefineryCollectButton(discord.ui.Button):
    
    def __init__(self, user: discord.Member, *, style = discord.ButtonStyle.gray, label = None, disabled = False, custom_id = None, url = None, emoji = None, row = None, sku_id = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji=random.choice(('💎', '❄️', '👑', '📿')), row=row, sku_id=sku_id)
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.user:
            progress = await get_refinery_progress(self.user)
            slots = [x for x in progress.values() if x["time_left"] == 0]
            if slots:
                return True
            else:
                await interaction.response.send_message(ephemeral=True, embed=discord.Embed(description='These items have already been collected.', color=config.ErrorColour))
                return False
                

        await interaction.response.send_message(ephemeral=True, embed=discord.Embed(description='This is not your button!', color=config.ErrorColour))
        return False
    
    async def callback(self, interaction: discord.Interaction):

        self.view.stop()

        progress = await get_refinery_progress(self.user)
        slots = [x for x in progress.values() if x["time_left"] == 0]
        
        # Key = item id, Value = count
        harvested = {}

        for slot in slots:
            try:
                recipe = recipes.RECIPES[slot["recipe"]]
                success_level = "ideal" if slot["mode"] in recipe["ideal_modes"] else "normal" if slot["mode"] in recipe["normal_modes"] else "bad"

                # Get loot table for recipe based on mode used and make weighted choice
                loot_table = recipe["loot_tables"][success_level]
                loot: dict = random.choices([x for x in loot_table], [x["chance"] for x in loot_table])[0]
                failure_text: bool = loot.get("display_failure", False)
                loot = loot["loot"]

                # For each item id in the loot dict, set item id in harvested count to loot count + any existing ones harvested
                for item in loot.keys():
                    harvested[item] = loot[item] + harvested.get(item, 0)
                
            except IndexError:
                print(f"Error: Recipe '{slot['recipe']}' collection encountered Index Error. Likely because it has an empty loot table.")
            except KeyError:
                print(f"Error: Recipe '{slot['recipe']}' collection encountered Key Error. Likely because it has no loot table.")
        
        if harvested:
            harvested_string = '\n'.join([f"- {item_display_string(x[0])} x**{x[1]}**" for x in harvested.items()])
            if not failure_text:
                message = f"✨ **The following items were obtained!** ✨\n{harvested_string}"
            else:
                message = f"😕 **Oh no! The refinement failed. The following items were salvaged: 😕**\n{harvested_string}"
        else:
            message = f"⛈️ Oh no! The refinement failed. Nothing was obtained :( ⛈️"

        embed, view = await get_refinery_embed(self.user)

        for harvested_item in harvested.keys():
            await gacha.gain_item(self.user, harvested_item, harvested[harvested_item])
        for to_clear in [x["slot"] for x in slots]:
            await clear_refinery_slot(self.user, to_clear)

        embed.description += message
        embed.remove_footer()
        
        await interaction.response.edit_message(embed=embed, view=None)

async def get_available_refinery_slots(member: discord.Member) -> list[int]:

    progress = await get_refinery_progress(member)
    available = [x for x in [1,2,3] if progress[x]["recipe"] is None]
    available = [x for x in available if await has_unlocked_refinery_slot(member, x)]

    return available

async def check_refining_errors(interaction: discord.Interaction, recipe: str, mode: int) -> bool:

    mode = REFINING_MODES[mode]

    available_slots = await get_available_refinery_slots(interaction.user)
    if not available_slots:
        await interaction.response.send_message(embed=discord.Embed(description='Your Refinery has no available slots.', color=config.ErrorColour), ephemeral=True)
        return True
    
    if recipe not in recipes.RECIPES.keys():
        await interaction.response.send_message(embed=discord.Embed(description=f"Could not find recipe '{recipe}'.", color=config.ErrorColour), ephemeral=True)
        return True
    inventory = await gacha.get_inventory(interaction.user)
    for item, count in recipes.RECIPES[recipe]["ingredients"].items():
        if item not in inventory.keys() or inventory[item] < count:
            await interaction.response.send_message(embed=discord.Embed(description=f"You do not own enough '{item_display_string(item)}' for this recipe.", color=config.ErrorColour), ephemeral=True)
            return True
    if not await has_unlocked_refinement_mode(interaction.user, mode):
        await interaction.response.send_message(embed=discord.Embed(description=f"You have not unlocked that refinement mode. Use /refinery upgrade to unlock it.", color=config.ErrorColour), ephemeral=True)
        return True
    
    
    return False

async def start_refining(member: discord.Member, recipe_id: str, mode: int):

    mode = REFINING_MODES[mode]
    available = await get_available_refinery_slots(member)
    slot = available[0]

    recipe = recipes.RECIPES[recipe_id]
    time = recipe["time"]
    ingredients = recipe["ingredients"]

    async with aiosqlite.connect("databases/farming.sqlite") as db:
        async with db.cursor() as cursor:
            sql = (f'UPDATE refinery SET slot{slot}_recipe = ?, slot{slot}_time_left = ?, slot{slot}_mode = ?, slot{slot}_last_update = ? WHERE user_id = ?')
            val = (recipe_id, time, mode, dt.datetime.now().strftime("%d-%m-%Y %H:%M"), member.id)
            await cursor.execute(sql, val)

        await db.commit()

    for item, count in ingredients.items():
        await gacha.gain_item(member, item, count * -1)

    settings = await gacha.get_settings(member)
    if settings["refinery_dms"]:
        completion_time = dt.datetime.now() + dt.timedelta(minutes=time)
        heapq.heappush(refinery_notifications, (completion_time, member))

async def has_unlocked_refinement_mode(member: discord.Member, mode: str) -> bool:
    match mode:
        case "basic":
            return True
        case _:
            return False
        
async def get_recipes(item: str) -> list:

    item_recipes = []

    for id, recipe in recipes.RECIPES.items():
        for table in recipe["loot_tables"].values():
            if any([not x.get("display_failure", False) and item in x["loot"].keys() for x in table]):
                item_recipes.append(id)
                break

    return item_recipes

class ViewRecipesButton(discord.ui.Button):
    
    def __init__(self, user: discord.Member, recipes: list[str], *, style = discord.ButtonStyle.gray, label = None, disabled = False, custom_id = None, url = None, emoji = None, row = None, sku_id = None):
        super().__init__(style=style, label=label, disabled=disabled, custom_id=custom_id, url=url, emoji='📝', row=row, sku_id=sku_id)
        self.user = user
        self.recipes = recipes

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.user:
            return True
            
        await interaction.response.send_message(ephemeral=True, embed=discord.Embed(description='This is not your button!', color=config.ErrorColour))
        return False
    
    async def callback(self, interaction: discord.Interaction):

        self.view.stop()

        embeds = []

        for recipe_id in self.recipes:
            recipe = recipes.RECIPES[recipe_id]
            ingredients = recipe["ingredients"]
            loot_table = recipe["loot_tables"]["ideal"][0]["loot"]

            ingredients_strings = "\n".join([f"- {item_display_string(k)} x**{v}**" for k,v in ingredients.items()])
            loot_strings = "\n".join([f"- {item_display_string(k)} x**{v}**" for k,v in loot_table.items()])
            ideal_modes = ", ".join([f"{REFINERY_MODE_NAMES[x][:-2]}" for x in recipe["ideal_modes"]])
            normal_modes = ", ".join([f"{REFINERY_MODE_NAMES[x][:-2]}" for x in recipe["normal_modes"]])

            text = f"**Ingredients**\n{ingredients_strings}\n\n**Output**\n{loot_strings}\n\n**Ideal Refinement Modes:** {ideal_modes}\n**Passable Refinement Modes:** {normal_modes}"
            embeds.append(discord.Embed(description=text, color=0xfcba03))
        
        from bot import Book
        book = Book(interaction, embeds)
        await book.edit_create()

def item_display_string(item_id: str) -> str:
    emoji = items.ITEMS[item_id].get('emoji', '')
    return f"{emoji + ' ' if emoji else ''}{items.ITEMS[item_id]['name']}"