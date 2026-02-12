from btc_gen_shit import btc_addresses_from_private_key, ltc_addresses_from_private_key, bch_cashaddr_from_private_key
from tronpy.keys import PrivateKey
import random, secrets, hashlib, ecdsa



def eth_private_key_to_address(private_key_hex: str) -> str:
    try:
        private_key_bytes = bytes.fromhex(private_key_hex)
        sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        public_key = b'\x04' + vk.to_string()
        keccak = hashlib.sha3_256()
        keccak.update(public_key[1:])
        eth_address = keccak.digest()[-20:]
        return '0x' + eth_address.hex()
    except Exception as e:
        return None

def int_to_hex_string(n: int) -> str:
    return hex(n)[2:]

def trx_private_key_to_address(private_key_hex: str) -> str:
    try:
        priv_key = PrivateKey(bytes.fromhex(private_key_hex))
        return priv_key.public_key.to_base58check_address()
    except Exception as e:
        return None

def play_in(big_int: int = None):

    new_int = int(big_int)
    hex = int_to_hex_string(new_int)

    trx_address = trx_private_key_to_address(hex)
    eth_bnb_addr = eth_private_key_to_address(hex)
    btc_addresses = btc_addresses_from_private_key(hex)
    ltc_addresses = ltc_addresses_from_private_key(hex)
    bch_address = bch_cashaddr_from_private_key(hex)

    # TRX
    print(f"TRX address: {trx_address}")

    # ETH/BNB
    print(f"ETH/BNB address: {eth_bnb_addr}")
    
    # BCH
    print(f"BCH address: {bch_address}")

    # BTC
    for i, addr in enumerate(btc_addresses):
        print(f"BTC address ({i}): {addr}")


    # LTC
    for i, addr in enumerate(ltc_addresses):
        print(f"LTC address ({i}): {addr}")



def pull_big_int_from_seed(_seed: str) -> int:
    random.seed(_seed)
    return random.getrandbits(256)



if __name__ == "__main__":
    big_int = pull_big_int_from_seed("Nakamoto")
    # print(f"Big int from seed: {big_int}")
    play_in(big_int)