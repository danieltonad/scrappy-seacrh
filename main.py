from wallet_type_enum import WalletType
from seedler import spawn_seed, is_valid_phrase
from wallets import generate_wallet_address, generate_public_key
import asyncio


async def main():
    for i,seed in enumerate(await spawn_seed()):
        if is_valid_phrase(" ".join(seed)):
            print(f"{i:,}", end="\r")
            
            
asyncio.run(main())