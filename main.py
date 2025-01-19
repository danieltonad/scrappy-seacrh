from wallet_type_enum import WalletType
from exchange_enum import Exchange
from seedler import spawn_seed, is_valid_phrase
from wallets import generate_wallet_address, generate_public_key
import asyncio, json

feeder = json.load(open("feeder.json", "r"))

async def scan_seed(seed: str):
    for exchange in feeder.keys():
        itr = Exchange.get_exchange_uid(Exchange[exchange])
        exchange_dict = feeder[exchange]
        for wallet in WalletType.get_wallet_types():
            seedler, coin = WalletType.coin_seedler(wallet)
            wallet_address: str = await generate_wallet_address(seed, coin, seedler, itr)
            if wallet_address.lower() == exchange_dict.get(wallet.value).lower():
                print(f"{wallet.value}:", wallet_address.lower(), exchange_dict.get(wallet.value).lower(), exchange)
            
            print(f"{wallet.value}:", wallet_address.lower(), exchange_dict.get(wallet.value).lower(), exchange)




async def main():
    # for i,seed in enumerate(await spawn_seed()):
    #     if is_valid_phrase(" ".join(seed)):
    #         print(f"{i:,}", end="\r")
    
    seed = "fatigue purpose cable sniff tool lock roast risk pipe hunt buyer illness"
    await scan_seed(seed)
    # for wallet in WalletType.get_wallet_types():
    #     seedler, coin = WalletType.coin_seedler(wallet)
    #     wallet_address = await generate_wallet_address(seed, coin, seedler)
    #     print(f"{wallet}:", wallet_address)
            
            
asyncio.run(main())