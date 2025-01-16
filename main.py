from wallet_type_enum import WalletType
from seedler import spawn_seed, is_valid_phrase
from wallets import generate_wallet_address, generate_public_key
import asyncio




async def main():
    # for i,seed in enumerate(await spawn_seed()):
    #     if is_valid_phrase(" ".join(seed)):
    #         print(f"{i:,}", end="\r")
    
    seed = "fatigue purpose cable sniff tool lock roast risk pipe hunt buyer illness"
    for wallet in WalletType.get_wallet_types():
        wallet_address = await generate_wallet_address(seed, WalletType.coin_seedler(wallet)[1], WalletType.coin_seedler(wallet)[0])
        print(f"{wallet}:", wallet_address)
            
            
asyncio.run(main())