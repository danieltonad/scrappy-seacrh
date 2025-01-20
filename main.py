from wallet_type_enum import WalletType
from exchange_enum import Exchange
from seedler import spawn_seed, is_valid_phrase
from wallets import generate_wallet_address
from utils import save_spot
import asyncio, json

feeder = json.load(open("feeder.json", "r"))
found = 0

async def scan_seed(seed: str):
    global found
    for exchange in feeder.keys():
        itr = Exchange.get_exchange_uid(Exchange[exchange])
        exchange_dict = feeder[exchange]
        for wallet in WalletType.get_wallet_types():
            seedler, coin = WalletType.coin_seedler(wallet)
            wallet_address: str = await generate_wallet_address(seed, coin, seedler, itr)
            if wallet_address.lower() == exchange_dict.get(wallet.value).lower():
                await save_spot(seed=seed, exchange=exchange)
                found += 1
            # print(f"{wallet.value}:", wallet_address.lower(), exchange_dict.get(wallet.value).lower(), exchange)

async def pull_seeds(_len: int = 12):
    while True:
        for i, seed in enumerate(await spawn_seed(_len)):
            seed = " ".join(seed)
            if is_valid_phrase(seed):
                await scan_seed(seed)
            if i % 1234 == 0:
                print(f"  {i:,}  |  [{found}]      ", end="\r")
                    


async def main():
    await pull_seeds(12)
asyncio.run(main())