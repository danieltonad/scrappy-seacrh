import asyncio
from logger import Logger
from settings import settings
from httpx import AsyncClient


async def get_btc_balance(address, session: AsyncClient, retry: int = 1) -> bool:
    try:
        url = f"https://api.bitcore.io/api/BTC/mainnet/address/{address}/balance"
        async with settings.SEMAPHORE:
            response = await session.get(url)
            if response.status_code == 200:
                result = response.json()
                balance = float(result.get('confirmed')) / 1e8
                return balance
            if retry > 2:
                await asyncio.sleep(retry)
                await get_btc_balance(address, retry+1)
            else: 
                raise ValueError(f"Unable to get ({address}) balance")
    except Exception as err:
        Logger.app_log(title="BTC_BAL_ERR", message=str(err))
        return False


async def get_trx_balance(address, session: AsyncClient, retry: int = 1) -> bool:
    try:
        url = f"https://api.trongrid.io/v1/accounts/{address}"
        async with settings.SEMAPHORE:
            response = await session.get(url)
            if response.status_code == 200:
                result = response.json()
                data = result.get('data')
                if not data:
                    return 0.0
                balance = int(data[0].get("balance")) / 1e6
                return balance
            if retry > 2:
                await asyncio.sleep(retry)
                await get_trx_balance(address, retry+1)
            else: 
                raise ValueError(f"Unable to get ({address}) balance")
    except Exception as err:
        Logger.app_log(title="TRX_BAL_ERR", message=str(err))
        return False

async def get_usdt_trc20_balance(address, session: AsyncClient, retry: int = 1) -> bool:
    try:
        url = f"https://api.trongrid.io/v1/accounts/{address}"
        async with settings.SEMAPHORE:
            response = await session.get(url)
            if response.status_code == 200:
                result = response.json()
                data = result.get('data')
                if not data:
                    return 0.0
                trc20_dict = dict(data[0].get("trc20")[0])
                usdt_qty = int(list(trc20_dict.values())[0])
                balance = int(usdt_qty / 1e6)
                return balance
            if retry > 2:
                await asyncio.sleep(retry)
                await get_trx_balance(address, retry+1)
            else: 
                raise ValueError(f"Unable to get ({address}) balance")
    except Exception as err:
        Logger.app_log(title="USDT_BAL_ERR", message=str(err))
        return False


async def get_bnb_balance(address, session: AsyncClient, retry: int = 1) -> bool:
    try:
        url = f"https://bsc-dataseed.binance.org/"
        async with settings.SEMAPHORE:
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
        Logger.app_log(title="BNB_BAL_ERR", message=str(err))
        return False
    
    
    
    

async def get_coin_current_price(session: AsyncClient, coin:str = "bitcoin") -> int:
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coin,
            "vs_currencies": "usd"
        }
        async with settings.SEMAPHORE:
            response = await session.get(url, params=params)
            if response.status_code == 200:
                result = response.json()
                return float(result.get(coin, {}).get(params["vs_currencies"]))
            
    except Exception as err:
        Logger.app_log(title="COIN_PRICE_ERR", message=str(err))
        return False
    