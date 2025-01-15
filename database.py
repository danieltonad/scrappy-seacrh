import aiosqlite, asyncio
from settings import settings


async def connect():
    conn = await aiosqlite.connect(settings.DB_PATH)
    await conn.execute('CREATE TABLE IF NOT EXISTS seeds (id TEXT PRIMARY KEY)')
    await conn.commit()
    return conn

async def check_seed_exist(seed: list):
    seed = "-".join(seed)
    conn = await connect()
    cursor = await conn.execute('SELECT * FROM seeds')
    all = await cursor.fetchall()
    await conn.close()
    for _ in all:
        if _[0] == seed:
            return True
    return False

async def insert_seed(seed: list):
    seed_str = "-".join(seed)
    conn = await connect()
    await conn.execute('INSERT INTO seeds (id) VALUES (?)', (seed_str,))
    await conn.commit()
    await conn.close()
    
async def count_seeds():
    conn = await connect()
    async with conn.execute('SELECT COUNT(*) FROM seeds') as cursor:
        count = await cursor.fetchone()
    await conn.close()
    return count[0]


# asyncio.run(count_seeds())