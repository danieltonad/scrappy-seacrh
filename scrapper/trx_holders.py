from httpx import AsyncClient
import asyncio, os

def save_trx_holders(holders: list):
    trx_path = "../data/trx_holders.txt"
    prev_holders = []
    if os.path.exists(trx_path):
        with open(trx_path, "r") as f:
            prev_holders = f.read().splitlines()
    holders = list(set(holders + prev_holders))
    with open(trx_path, "w") as f:
        for holder in holders:
            f.write(f"{holder}\n")
            
async def fetch_trx_holders(start: int, limit: int = 50):
    url = f"https://apilist.tronscanapi.com/api/account/list?sort=&limit={limit}&start={start}"
    async with AsyncClient() as client:
        response = await client.get(url)
        data = response.json().get("data", [])    
        return [dt["address"] for dt in data] if len(data) > 0 else []

async def get_trx_holders():
    limit = 50
    all_data = []
    # url.format(20, 10)
    try:
        while True:
            start = len(all_data)
            all_data += await fetch_trx_holders(start, limit)
            
            if len(all_data) > 9_990:
                break
            
            print(f"Progress: {len(all_data)} ...", end="\r")
            await asyncio.sleep(1)
    except:
        pass
    
    return all_data

res = asyncio.run(get_trx_holders())
save_trx_holders(res)