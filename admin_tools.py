import aiosqlite
import asyncio
import battles.cards as cards

async def update_cards():
    async with aiosqlite.connect('gacha.sqlite') as db:
        async with db.cursor() as cursor:
            await cursor.execute('PRAGMA table_info(cards)')
            columns = await cursor.fetchall()
            columns = [column[1] for column in columns[1:]]
    
    card_list = [card.name.lower() for card in cards.Cards]
    missing = [card for card in card_list if card not in columns]
    excess = [column for column in columns if column not in card_list]

    async with aiosqlite.connect('gacha.sqlite') as db:
        async with db.cursor() as cursor:
            for card in missing:
                await cursor.execute(f'ALTER TABLE cards ADD COLUMN {card} INTEGER DEFAULT 0')
            for column in excess:
                await cursor.execute(f'ALTER TABLE cards DROP COLUMN {column}')
        await db.commit()

            

if __name__ == "__main__":
    asyncio.run(update_cards())