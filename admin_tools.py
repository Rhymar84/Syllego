import aiosqlite
import asyncio
import battles.cards as cards


async def update_cards():
    async with aiosqlite.connect('databases/gacha.sqlite') as db:
        async with db.cursor() as cursor:
            await cursor.execute('PRAGMA table_info(cards)')
            columns = await cursor.fetchall()
            columns = [column[1] for column in columns[1:]]
    
    card_list = [card.name.lower() for card in cards.Cards]
    missing = [card for card in card_list if card not in columns]
    excess = [column for column in columns if column not in card_list]

    async with aiosqlite.connect('databases/gacha.sqlite') as db:
        async with db.cursor() as cursor:
            for card in missing:
                await cursor.execute(f'ALTER TABLE cards ADD COLUMN {card} INTEGER DEFAULT 0')
            for column in excess:
                await cursor.execute(f'ALTER TABLE cards DROP COLUMN {column}')
        await db.commit()

async def update_inventory():
    import system.items as items

    async with aiosqlite.connect('databases/eco.sqlite') as db:
        async with db.cursor() as cursor:
            await cursor.execute('PRAGMA table_info(inventory)')
            columns = await cursor.fetchall()
            columns = [column[1] for column in columns[1:]]
    
    item_list = [item for item in items.ITEMS.keys()]
    missing = [item for item in item_list if item not in columns]
    excess = [column for column in columns if column not in item_list]

    async with aiosqlite.connect('databases/eco.sqlite') as db:
        async with db.cursor() as cursor:
            for item in missing:
                await cursor.execute(f'ALTER TABLE inventory ADD COLUMN {item} INTEGER DEFAULT 0')
            for column in excess:
                await cursor.execute(f'ALTER TABLE inventory DROP COLUMN {column}')
        await db.commit()

    if missing:
        print("Added " + ", ".join(missing))
    if excess:
        print("Removed " + ", ".join(excess))


if __name__ == "__main__":
    asyncio.run(update_cards())
    asyncio.run(update_inventory())