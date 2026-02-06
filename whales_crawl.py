from tronpy.keys import PrivateKey
import random, secrets, hashlib, ecdsa
from typing import Tuple, Set
from math_shii import BITS
from typing import Callable, Optional
from btc_gen_shit import btc_addresses_from_private_key, ltc_addresses_from_private_key, bch_cashaddr_from_private_key

trx_path = "./data/trx_holders.txt"
eth_bnb_path = r"C:\Users\msiso\Downloads\eth_dump.txt"
btc_path = r"C:\Users\msiso\Downloads\btc_dump.txt"
ltc_path = r"C:\Users\msiso\Downloads\ltc_dump.txt"
bch_path = r"C:\Users\msiso\Downloads\bch_dump.txt"

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
    with open(btc_path, "r") as f:
        btc_holders = f.read().splitlines()
    with open(ltc_path, "r") as f:
        ltc_holders = f.read().splitlines()
    with open(bch_path, "r") as f:
        bch_holders = f.read().splitlines()
    with open(ltc_path, "r") as f:
        ltc_holders = f.read().splitlines()
    return set(trx_holders), set(eth_bnb_holders), set(btc_holders), set(ltc_holders), set(bch_holders)


TRX, BNB_ETH, BTC, LTC, BCH = fetch_holders() 
print(f"Loaded: {len(TRX):,} TRX holders | {len(BNB_ETH):,}  BNB/ETH holders | {len(BTC):,} BTC holders | {len(LTC):,} LTC holders | {len(BCH):,} BCH holders")


def int_to_hex_string(n: int) -> str:
    return hex(n)[2:]

def trx_private_key_to_address(private_key_hex: str) -> str:
    try:
        priv_key = PrivateKey(bytes.fromhex(private_key_hex))
        return priv_key.public_key.to_base58check_address()
    except Exception as e:
        return None
    
def _default_entropy(nbytes: int) -> bytes:
    return secrets.token_bytes(nbytes)
    
def generate_secure_bigint(
    bit_length: int = 256,
    *,
    allow_zero: bool = True,
    entropy_fn: Optional[Callable[[int], bytes]] = None
) -> int:

    if entropy_fn is None:
        entropy_fn = _default_entropy

    nbytes = (bit_length + 7) // 8  # number of full bytes needed
    top_bits = nbytes * 8 - bit_length  # number of unused high bits in the top byte

    # Rejection loop only used for allow_zero == False. For allow_zero==True there is
    # no bias because we are generating exactly bit_length bits and mapping to 0..2**bit_length-1.
    while True:
        raw = entropy_fn(nbytes)  # cryptographic randomness

        # mask away extra top bits so we produce exactly `bit_length` bits
        if top_bits:
            mask = (1 << (8 - top_bits)) - 1
            raw = bytes([raw[0] & mask]) + raw[1:]

        value = int.from_bytes(raw, "big")

        if 0 <= value < (1 << bit_length):
            if not allow_zero and value == 0:
                # very rare; re-sample
                continue
            return value
        continue
    
def heaps_permutations(seq, jump=None):
    """
    Yield permutations of seq using Heap's algorithm.
    If jump is None, yield all permutations.
    If jump is an integer k > 0, yield every (k+1)th permutation.
    """
    seq = list(seq)
    n = len(seq)
    c = [0] * n
    count = 0
    step = jump + 1 if jump is not None else 1

    # always yield the first permutation
    if count % step == 0:
        yield ''.join(seq)
    count += 1

    i = 0
    while i < n:
        if c[i] < i:
            if i % 2 == 0:
                seq[0], seq[i] = seq[i], seq[0]
            else:
                seq[c[i]], seq[i] = seq[i], seq[c[i]]
            if count % step == 0:
                yield ''.join(seq)
            count += 1
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1


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


def play_in(big_int: int = None):
    if big_int is None:
        big_int = generate_secure_bigint(256, allow_zero=False)

    # print(f"Digging... [{len(str(big_int))}] -> {big_int:,}")

    new_int = int(big_int)
    hex = int_to_hex_string(new_int)

    trx_address = trx_private_key_to_address(hex)
    eth_bnb_addr = eth_private_key_to_address(hex)
    btc_addresses = btc_addresses_from_private_key(hex)
    ltc_addresses = ltc_addresses_from_private_key(hex)
    bch_address = bch_cashaddr_from_private_key(hex)

    # TRX
    if trx_address in TRX:
        print(f"Found TRX holder: {trx_address} with key {hex}")
        save_rag(hex, trx_address)

    # ETH/BNB
    if eth_bnb_addr in BNB_ETH:
        print(f"Found ETH/BNB holder: {eth_bnb_addr} with key {hex}")
        save_rag(hex, eth_bnb_addr)

    
    # BCH
    if bch_address in BCH:
        print(f"Found BCH holder: {bch_address} with key {hex}")
        save_rag(hex, bch_address)

    # BTC
    for addr in btc_addresses:
        if addr in BTC:
            print(f"Found BTC holder: {addr} with key {hex}")
            save_rag(hex, addr)


    # LTC
    for addr in ltc_addresses:
        if addr in LTC:
            print(f"Found LTC holder: {addr} with key {hex}")
            save_rag(hex, addr)
    
    # print(f"Digging... {new_int:,}", end="\r")


if __name__ == "__main__":
    play_in()
