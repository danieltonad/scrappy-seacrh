from tronpy.keys import PrivateKey
import random, secrets, hashlib, ecdsa
from typing import Tuple, Set

from math_shii import BITS

trx_path = "./data/trx_holders.txt"
eth_bnb_path = "./data/eth_bnb_holders.txt"

def last_count()-> int:
    with open("last_count.txt", "r") as f:
        return int(f.read().strip())

def save_last_count(count: int):
    with open("last_count.txt", "w") as f:
        f.write(str(count))

def fetch_holders() -> Tuple[Set[str], Set[str]]:
    with open(trx_path, "r") as f:
        trx_holders = f.read().splitlines()
    with open(eth_bnb_path, "r") as f:
        eth_bnb_holders = f.read().splitlines()
    return set(trx_holders), set(eth_bnb_holders)

TRX, BNB_ETH = fetch_holders() 
print(f"Lodaed {len(TRX):,} TRX holders and {len(BNB_ETH):,} BNB/ETH holders")


def int_to_hex_string(n: int) -> str:
    return hex(n)[2:]

def trx_private_key_to_address(private_key_hex: str) -> str:
    try:
        priv_key = PrivateKey(bytes.fromhex(private_key_hex))
        return priv_key.public_key.to_base58check_address()
    except Exception as e:
        return None

def save_rag(pkey, address):
    with open("pkey.rag", "a") as f:
        f.write(f"{pkey} -> {address}\n")

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


def play_in():
    from math_shii import OddStepReverse, LCGReverse, PRPCounterReverse
    BITS = 256
    START = (1 << BITS)  # == 2^256
    count = last_count()
    odd_gen = OddStepReverse(START, 3)
    lcg_gen = LCGReverse(START, 5, 1)
    prp_gen = PRPCounterReverse(START)

    if count:
        odd_gen.jump(count)
        lcg_gen.jump(count)
        prp_gen.jump(count)
        print(f"Last count: {count:,}", end="\r")
    
    while True:
        odd_key = int_to_hex_string(odd_gen.prev())
        lcg_key = int_to_hex_string(lcg_gen.prev())
        prp_key = int_to_hex_string(prp_gen.prev())

        odd_trx_address = trx_private_key_to_address(odd_key)
        lcg_trx_address = trx_private_key_to_address(lcg_key)
        prp_trx_address = trx_private_key_to_address(prp_key)

        odd_eth_bnb_addr = eth_private_key_to_address(odd_key)
        lcg_eth_bnb_addr = eth_private_key_to_address(lcg_key)
        prp_eth_bnb_addr = eth_private_key_to_address(prp_key)
        
        # TRX
        if odd_trx_address in TRX:
            print(f"Found TRX holder: {odd_trx_address} with key {odd_key}")
            save_rag(odd_key, odd_trx_address)

        if lcg_trx_address in TRX:
            print(f"Found TRX holder: {lcg_trx_address} with key {lcg_key}")
            save_rag(lcg_key, lcg_trx_address)

        if prp_trx_address in TRX:
            print(f"Found TRX holder: {prp_trx_address} with key {prp_key}")
            save_rag(prp_key, prp_trx_address)

        # BNB ETH
        if odd_eth_bnb_addr in BNB_ETH:
            print(f"Found ETH/BNB holder: {odd_eth_bnb_addr} with key {odd_key}")
            save_rag(odd_key, odd_eth_bnb_addr)

        if lcg_eth_bnb_addr in BNB_ETH:
            print(f"Found ETH/BNB holder: {lcg_eth_bnb_addr} with key {lcg_key}")
            save_rag(lcg_key, lcg_eth_bnb_addr)

        if prp_eth_bnb_addr in BNB_ETH:
            print(f"Found ETH/BNB holder: {prp_eth_bnb_addr} with key {prp_key}")
            save_rag(prp_key, prp_eth_bnb_addr)
        
        if count % 10_011 == 0:
            save_last_count(count)
            print(f"Last count: {count:,}", end="\r")
        
        count += 1

if __name__ == "__main__":
    play_in()

# print(trx_private_key_to_address(int_to_hex_string(96690521103684763241907041926562609780425301947070575270117074750536375318862)))
# print(eth_private_key_to_address(int_to_hex_string(96690521103684763241907041926562609780425301947070575270117074750536375318862)))