from mnemonic import Mnemonic
from bip_utils import Bip44Changes, Bip84, Bip84Coins, Bip49, Bip49Coins, Bip44
from httpx import AsyncClient
from utilities.wallets import WalletType


mnemonic = Mnemonic("english")

async def generate_bip44_master(seed: str, coin: Bip84Coins, seedler: Bip44|Bip49|Bip84, itr: int = 0):
    try:
        if not is_valid_phrase(seed):
            print("SEED_ERR: Invalid seed phrase")
            return False
        seed = mnemonic.to_seed(seed)
        bip44_mst = seedler.FromSeed(seed, coin)
        return bip44_mst.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(itr)
    except Exception as err:
        print(f"SEED_ERR: {err}")

async def generate_wallet_address(seed: str, coin: Bip84Coins, seedler: Bip44|Bip49|Bip84, itr: int = 0):
    master = await generate_bip44_master(seed, coin, seedler, itr)
    return master.PublicKey().ToAddress()

async def generate_public_key(seed: str, coin: Bip84Coins, seedler: Bip44|Bip49|Bip84, itr: int = 0):
    master = await generate_bip44_master(seed, coin, seedler, itr)
    return master.PublicKey().RawCompressed().ToHex()

async def generate_private_key(seed: str, coin: Bip84Coins, seedler: Bip44|Bip49|Bip84, itr: int = 0):
    master = await generate_bip44_master(seed, coin, seedler, itr)
    return master.PrivateKey().Raw().ToHex()

def is_valid_phrase(phrase: str) -> bool:
    return mnemonic.check(phrase)

