import discord
import config
from system.emoji import EMOJIS


SHOPS = {

    "green_dust_shop": {
        "name": "Green Dust Exchange",
        "stock": {
            "emberblossom_seed": {"currency": "green_dust", "price": 4},
            "riverleaf_seed": {"currency": "green_dust", "price": 4},
            "gustbloom_seed": {"currency": "green_dust", "price": 4},
            "rockroot_seed": {"currency": "green_dust", "price": 4},
            "minature_phoenix": {"currency": "green_dust", "price": 4},
            "water_snake": {"currency": "green_dust", "price": 4},
            "flying_dolphin": {"currency": "green_dust", "price": 4},
            "little_titan": {"currency": "green_dust", "price": 4},
            "molten_chunk": {"currency": "green_dust", "price": 4},
            "aquamarine_ore": {"currency": "green_dust", "price": 4},
            "super_steel_ore": {"currency": "green_dust", "price": 4},
            "lead_ore": {"currency": "green_dust", "price": 4},
            "spirit_fountain": {"currency": "green_dust", "price": 10},
            "ghostly_knight": {"currency": "green_dust", "price": 10},
        }
    }
}           


class ShopSelect(discord.ui.Select):
    def __init__(self, user: discord.Member):
        options = [discord.SelectOption(label=v["name"], value=k) for k, v in SHOPS.items()]
        super().__init__(placeholder="Select a shop.", options=options)
        
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == self.user

    async def callback(self, interaction: discord.Interaction):
        self.view.stop()
        await interaction.response.defer()
        
        selected_shop = self.values[0]
        embed = await generate_shop_embed(self.user, selected_shop)
        await interaction.edit_original_response(embed=embed, view=ShopView(self.user, selected_shop, await interaction.original_response()))

async def generate_shop_embed(user: discord.Member, selected_shop: str) -> discord.Embed:
    import system.farming as farming
    import system.gacha as gacha

    shop = SHOPS[selected_shop]

    currencies = list(set([x["currency"] for x in shop["stock"].values()]))
    currencies = {x: await gacha.get_currency(user, x) for x in currencies}
    description = "\n".join([f"You have **{config.blue(v)} {config.CURRENCY_KEY[k]}**." for k, v in currencies.items()])

    embed = discord.Embed(title=shop["name"], url=config.HYPERLINK_URL, description=description, color=0xbd4e04)
    embed.set_author(name=f'{user.display_name}', icon_url=f'{user.display_avatar}')

    return embed
    

class ShopView(discord.ui.View):

    def __init__(self, user: discord.Member, shop_id: str, message: discord.InteractionMessage):
        super().__init__(timeout=180)
        self.user = user
        self.shop_id = shop_id
        self.message = message

        self.selected_item = None

        self.add_item(ItemSelect(user, shop_id))
        self.add_item(BuyButton(self))

    async def interaction_check(self, interaction: discord.Interaction):
        return self.user == interaction.user
    
    async def update_selection(self, item: str | None):
        self.selected_item = item

    async def confirm_purchase(self, button_interaction: discord.Interaction, item: str, quantity: int, confirmation_embed: discord.Embed):
        import system.gacha as gacha

        shop_item = SHOPS[self.shop_id]["stock"][item]
        currency = shop_item["currency"]
        unit_price = shop_item["price"]
        
        total_price = unit_price * quantity
        user_balance = await gacha.get_currency(self.user, currency)

        if user_balance < total_price:
            confirmation_embed.description += f"\n⛔ You have insufficient funds. ❌"
            confirmation_embed.color = config.ErrorColour
            await button_interaction.response.edit_message(view=None, embed=confirmation_embed)
            return
        
        await gacha.add_currency(self.user, currency, -1 * total_price)
        await gacha.gain_item(self.user, item, quantity)
        
        confirmation_embed.description += f"\n💲 Purchase complete! 💸"
        await button_interaction.response.edit_message(view=None, embed=confirmation_embed)

        await self.message.edit(embed=await generate_shop_embed(self.user, self.shop_id))
        

    

class ItemSelect(discord.ui.Select):

    def __init__(self, user: discord.Member, shop_id: str):
        options = self.generate_options(shop_id)
        super().__init__(placeholder="Select an item.", options=options)
        
        self.user = user

    def generate_options(self, shop_id: str) -> list[discord.SelectOption]:
        import system.items as items
        shop = SHOPS[shop_id]
        
        return [discord.SelectOption(label=items.ITEMS[k]['name'], value=k, description=f"{v['price']:n} {config.CURRENCY_KEY[v['currency']]}", emoji=EMOJIS.get(k)) for k, v in shop["stock"].items()]

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == self.user

    async def callback(self, interaction: discord.Interaction):
        view: ShopView = self.view
        await view.update_selection(self.values[0])
        await interaction.response.defer()


class BuyButton(discord.ui.Button):

    def __init__(self, shop_view: ShopView):
        super().__init__(style=discord.ButtonStyle.green, label="Purchase", row=2)
        self.shop_view = shop_view

    async def interaction_check(self, interaction: discord.Interaction):
        return self.shop_view.user == interaction.user

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BuyModal(self.shop_view, self.shop_view.selected_item))


class BuyModal(discord.ui.Modal, title = "Shop Purchase"):
    input = discord.ui.TextInput(
        label="Purchase Quantity",
        max_length=2,
        style=discord.TextStyle.short,
        required=True,
        placeholder='1',
    )

    def __init__(self, shop_view: ShopView, selected_item: str):
        super().__init__()
        self.shop_view = shop_view
        self.selected_item = selected_item

    async def on_submit(self, interaction: discord.Interaction):
        try:
            quantity = int(str(self.input))
        except ValueError:
            await interaction.response.send_message(ephemeral=True, embed=discord.Embed(description=f"You must submit a whole number.", color=config.ErrorColour))
            return
        
        import system.farming as farming
        item = self.selected_item
        shop = SHOPS[self.shop_view.shop_id]
        item_name = farming.item_display_string(item)
        item_price = shop["stock"][item]["price"]
        currency = shop["stock"][item]["currency"]

        embed = discord.Embed(
            title="Confirm Purchase", 
            url=config.HYPERLINK_URL, 
            description=f"You are about to exchange:\n- **{config.blue(f'{item_price * quantity:n}')} {config.CURRENCY_KEY[currency]}**\nFor:\n- **{config.blue(str(quantity))} {item_name}**", 
            color=0x32a852
            )

        view = discord.ui.View()
        view.add_item(ConfirmBuyButton(self.shop_view, self.selected_item, quantity, embed))
        
        await interaction.response.send_message(ephemeral=True, embed=embed, view=view)
        self.stop()


class ConfirmBuyButton(discord.ui.Button):

    def __init__(self, shop_view: ShopView, selected_item: str, quantity: int, confirmation_embed: discord.Embed):
        super().__init__(style=discord.ButtonStyle.green, label="Confirm")
        self.shop_view = shop_view
        self.selected_item = selected_item
        self.quantity = quantity
        self.confirmation_embed = confirmation_embed

    async def interaction_check(self, interaction: discord.Interaction):
        return self.shop_view.user == interaction.user

    async def callback(self, interaction: discord.Interaction):
        await self.shop_view.confirm_purchase(interaction, self.selected_item, self.quantity, self.confirmation_embed)