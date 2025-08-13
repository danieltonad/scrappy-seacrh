from number import trx_private_key_to_address, number_to_private_key,eth_private_key_to_address
from httpx import AsyncClient
import asyncio, socket, requests

def has_internet_connection(timeout=5):
    try:
        # Option 1: Ping Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=timeout)
        return True
    except OSError:
        pass

    try:
        # Option 2: Make an HTTP request to a reliable website
        requests.get("https://www.google.com", timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        pass

    return False

async def get_bnb_balance(address, session: AsyncClient, retry: int = 1) -> bool:
    try:
        url = f"https://bsc-dataseed.binance.org/"
        payload = { "jsonrpc": "2.0","method": "eth_getBalance","params": [address,"latest"],"id": 1}
        response = await session.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            balance = int(result.get('result', "0x0"), 16) / 10**18
            return balance
        if retry > 2:
            await asyncio.sleep(retry)
            await get_bnb_balance(address, retry+1)
        else: 
            raise ValueError(f"Unable to get ({address}) balance")
    except Exception as err:
        return 0
    
async def get_trx_balance(address, session: AsyncClient, retry: int = 1) -> bool:
    try:
        url = f"https://api.trongrid.io/v1/accounts/{address}"
        response = await session.get(url)
        if response.status_code == 200:
            result = response.json()
            data = result.get('data')
            if not data:
                return 0.0
            balance = int(data[0].get("balance", 0)) / 1e6
            return balance
        if retry > 2:
            await asyncio.sleep(retry)
            await get_trx_balance(address, retry+1)
        else: 
            raise ValueError(f"Unable to get ({address}) balance")
    except Exception as err:
        # print("TRX_BAL_ERR: ", str(err))
        return 0

    
def save_info(itr, address: str, bal: str):
    with open(f"info.csv", "a") as f:
        f.write(f"{itr},{address},{bal}\n")

async def stale_itr(resume: int = 1):
    async with AsyncClient() as client:
        found = 0
        for i in range(int(resume), int(1e78)):
            repeat = True
            pkey = number_to_private_key(i)
            address = trx_private_key_to_address(pkey)
            eth_address = eth_private_key_to_address(pkey)
            # print(address)
            while repeat:
                if has_internet_connection():
                    repeat = False
                    trx_balance = await get_trx_balance(address, client)
                    eth_balance = await get_bnb_balance(eth_address, client)
                    if trx_balance > 0:
                        found += 1
                        save_info(i, address, trx_balance)
                    
                    if eth_balance > 0:
                        found += 1
                        save_info(i, eth_address, eth_address)
                else:
                    print("No Internet ...", end="\r")
                    await asyncio.sleep(10)
            
            print(f"[{found:,}] | Prog {i}              ", end="\r")

            # await asyncio.sleep(1)
        # print(await get_trx_balance("TYa8m37KgwBX7CnozYA2JxzDuQjZfNUaZv", client))



if __name__ == "__main__":
    asyncio.run(stale_itr(300_000))
    # print(has_internet_connection())