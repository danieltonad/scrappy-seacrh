import aiofiles

async def save_spot(exchange: str, seed: str):
    async with aiofiles.open(f"scrappies.txt", mode="a") as file:
        await file.write(f"{seed} -> [{exchange}]\n")