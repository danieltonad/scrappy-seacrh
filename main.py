from wallet_type_enum import WalletType
from seedler import spawn_seed, is_valid_phrase
from wallets import generate_wallet_address, generate_public_key
import asyncio, json

feeder = json.load(open("feeder.json", "r"))

print(feeder)




async def main():
    # for i,seed in enumerate(await spawn_seed()):
    #     if is_valid_phrase(" ".join(seed)):
    #         print(f"{i:,}", end="\r")
    
    seed = "fatigue purpose cable sniff tool lock roast risk pipe hunt buyer illness"
    for wallet in WalletType.get_wallet_types():
        seedler, coin = WalletType.coin_seedler(wallet)
        wallet_address = await generate_wallet_address(seed, coin, seedler)
        print(f"{wallet}:", wallet_address)
            
            
asyncio.run(main())