
from tronpy.keys import PrivateKey
import random, secrets, hashlib, ecdsa, base58, asyncio, os, multiprocessing
from bitcoinlib.keys import Key
from web3 import Web3
from datetime import datetime
from requests_html import AsyncHTMLSession
import sympy
import math

def save_rag(pkey, address):
    with open("pkey.rag", "a") as f:
        f.write(f"{pkey} -> {address}\n")

def is_prime(n, k=15):
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randint(2, min(n - 2, 1 << 20))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def number_properties(n):
    properties = {}
    if isinstance(n, complex):
        properties['type'] = 'complex'
        return properties

    # Check if the number is even or odd
    if n % 2 == 0:
        properties['even'] = True
        properties['odd'] = False
    else:
        properties['even'] = False
        properties['odd'] = True

    # Check if the number is prime or composite
    if n > 1:
        if is_prime(n):
            properties['prime'] = True
            properties['composite'] = False
        else:
            properties['prime'] = False
            properties['composite'] = True
    else:
        properties['prime'] = False
        properties['composite'] = False

    # Check if the number is a perfect square
    sqrt = math.isqrt(n)
    if sqrt * sqrt == n:
        properties['perfect_square'] = True
    else:
        properties['perfect_square'] = False

    return properties

properties = {'even': 0, 'odd': 0, 'prime': 0, 'composite': 0, 'perfect_square': 0}

# while True:
#     # no = secrets.randbelow(2**256 - 1)
#     no = random.randint(1, 2**256 - 1)
#     stat = number_properties(no)
#     for key in stat:
#         if stat[key]:
#             properties[key] += 1
    
#     print(f"  Even: {properties['even']:,}, Odd: {properties['odd']:,}, Prime: {properties['prime']:,}, Composite: {properties['composite']:,}, Perfect Square: {properties['perfect_square']:,}", end="\r")


def next_prime(n):
    return sympy.nextprime(n)

def prev_prime(n):
    sympy.prevprime(n)



def date_to_timestamp(date_str):
    dt_object = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    timestamp = int(dt_object.timestamp())
    return timestamp


def fetch_holders() -> tuple:
    trx_path = "../data/trx_holders.txt"
    eth_bnb_path = "../data/eth_bnb_holders.txt"
    with open(trx_path, "r") as f:
        trx_holders = f.read().splitlines()
    with open(eth_bnb_path, "r") as f:
        eth_bnb_holders = f.read().splitlines()
    return trx_holders, eth_bnb_holders


def private_key_to_bch_address(private_key_hex):
    from ecdsa import SigningKey, SECP256k1
    sk = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    sha256 = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160', sha256).digest()
    payload = b'\x00' + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    address = base58.b58encode(payload + checksum)
    return address.decode()

def private_key_to_polygon_address(private_key_hex):
    w3 = Web3()
    account = w3.eth.account.from_key(private_key_hex)
    return account.address

def private_key_to_solana_address(private_key_hex):
    private_key_bytes = bytes.fromhex(private_key_hex)
    signing_key = ed25519.SigningKey(private_key_bytes)
    public_key_bytes = signing_key.get_verifying_key().to_bytes()
    # Encode the public key in base58
    solana_address = base58.b58encode(public_key_bytes).decode()
    return solana_address

def private_key_to_btc_address(private_key_hex):
    key = Key(private_key_hex)
    segwit_address = key.address(script_type='p2wpkh')
    return segwit_address

def trx_private_key_to_address(private_key_hex: str) -> str:
    priv_key = PrivateKey(bytes.fromhex(private_key_hex))
    return priv_key.public_key.to_base58check_address()

def eth_private_key_to_address(private_key_hex: str) -> str:
    private_key_bytes = bytes.fromhex(private_key_hex)
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    keccak = hashlib.sha3_256()
    keccak.update(public_key[1:])
    eth_address = keccak.digest()[-20:]
    return '0x' + eth_address.hex()

def number_to_private_key(number):
    min_key = 1
    max_key = 2**256 - 1
    if number < min_key or number > max_key:
        return "Error: The number must be between 1 and 2^256 - 1."
    private_key_hex = hex(number)[2:]  # Remove the '0x' prefix
    private_key_hex = private_key_hex.zfill(64)  # Pad with leading zeros to ensure 64 characters

    return private_key_hex

def private_key_to_number(private_key_hex):
    return int(private_key_hex, 16)

def genetic_stupid_search():
    from rand import genetic_algorithm
    TRX, ETH = fetch_holders()
    i = 400_000_000
    while True:
        i += 1
        p_int = genetic_algorithm(population_size=9_999_999, generations=1, min=1, max=2**256 - 1)
        for p in p_int:
            private_key = number_to_private_key(p)
            trx_address = trx_private_key_to_address(private_key)
            eth_address = eth_private_key_to_address(private_key)
            if trx_address in TRX:
                print("=========================================")
                print("Private Key:", private_key)
                print("TRX Address:", trx_address)
                print("=========================================")

            if eth_address in ETH:
                print("=========================================")
                print("Private Key:", private_key)
                print("ETH Address:", eth_address)
                print("=========================================")
        print(f"  Prog: {i:,}  ", end="\r")


def impossible_search():
    TRX, ETH = fetch_holders()
    i = 400_000_000
    while True:
        i += 1
        private_key = number_to_private_key(i)
        trx_address = trx_private_key_to_address(private_key)
        eth_address = eth_private_key_to_address(private_key)
        if trx_address in TRX:
            print("=========================================")
            print("Private Key:", private_key)
            print("TRX Address:", trx_address)
            print("=========================================")

        if eth_address in ETH:
            print("=========================================")
            print("Private Key:", private_key)
            print("ETH Address:", eth_address)
            print("=========================================")
        if i % 12345 == 0:
            print(f"  Prog: {i:,}  ", end="\r")



def perm_impossible_search():
    from rand import generate_combinations_chunked
    TRX, ETH = fetch_holders()
    no = random.randint(10000000000000000000000000000000000000000000000000000000000000000000000000000, 20000000000000000000000000000000000000000000000000000000000000000000000000000)
    for j in generate_combinations_chunked(str(no)):
        j = int(j)
        private_key = number_to_private_key(j)
        trx_address = trx_private_key_to_address(private_key)
        eth_address = eth_private_key_to_address(private_key)
        
        if trx_address in TRX:
            print("=========================================")
            print("No:", j)
            print("Private Key:", private_key)
            print("TRX Address:", trx_address)
            print("=========================================")
        
        if eth_address in ETH:
            print("=========================================")
            print("No:", j)
            print("Private Key:", private_key)
            print("ETH Address:", eth_address)
            print("=========================================")
            
        print(f"  Prog: {j:,}  ", end="\r")




def custom_perm_impossible_search():
    from rand import generate_combinations_custom
    TRX, ETH = fetch_holders()
    no = random.randint(1, 2**256 - 1)
    for j in generate_combinations_custom(str(no)):
        j = int(j)
        private_key = number_to_private_key(j)
        trx_address = trx_private_key_to_address(private_key)
        eth_address = eth_private_key_to_address(private_key)
        
        if trx_address in TRX:
            print("=========================================")
            print("No:", j)
            print("Private Key:", private_key)
            print("TRX Address:", trx_address)
            print("=========================================")
        
        if eth_address in ETH:
            print("=========================================")
            print("No:", j)
            print("Private Key:", private_key)
            print("ETH Address:", eth_address)
            print("=========================================")
            
        print(f"  Prog: {j:,}  ", end="\r")




def fac_seq_play():
    from rand import factorial_sequence
    TRX, ETH = fetch_holders()
    while True:
        no = random.randint(1, 2**256 - 1)
        for j in factorial_sequence(str(no)):
            j = int(j)
            private_key = number_to_private_key(j)
            trx_address = trx_private_key_to_address(private_key)
            eth_address = eth_private_key_to_address(private_key)
            
            if trx_address in TRX:
                print("=========================================")
                print("No:", j)
                print("Private Key:", private_key)
                print("TRX Address:", trx_address)
                print("=========================================")
            
            if eth_address in ETH:
                print("=========================================")
                print("No:", j)
                print("Private Key:", private_key)
                print("ETH Address:", eth_address)
                print("=========================================")
                
            print(f"  Prog: {j:,}  ", end="\r")
            # reverse
            j = int(str(j)[:-1])
            private_key = number_to_private_key(j)
            trx_address = trx_private_key_to_address(private_key)
            eth_address = eth_private_key_to_address(private_key)
            
            if trx_address in TRX:
                print("=========================================")
                print("No:", j)
                print("Private Key:", private_key)
                print("TRX Address:", trx_address)
                print("=========================================")
            
            if eth_address in ETH:
                print("=========================================")
                print("No:", j)
                print("Private Key:", private_key)
                print("ETH Address:", eth_address)
                print("=========================================")
                
def rand_itr(start: int = 1):
    TRX, ETH = fetch_holders()
    stop = int(1e78)
    i = start
    while i < stop:
        private_key = number_to_private_key(i)
        trx_address = trx_private_key_to_address(private_key)
        eth_address = eth_private_key_to_address(private_key)
        
        if trx_address in TRX:
            print("=========================================")
            print("No:", i)
            print("Private Key:", private_key)
            print("TRX Address:", trx_address)
            print("=========================================")
            save_rag(private_key, trx_address)
        
        if eth_address in ETH:
            print("=========================================")
            print("No:", i)
            print("Private Key:", private_key)
            print("ETH Address:", eth_address)
            print("=========================================")
            save_rag(private_key, trx_address)
            
        print(f"  Prog: {i:,}  ", end="\r")
        i+= int(random.uniform(1e10, 1e20))



def rand_itr_multi_core(start: int = 1, process_id: int = 0):
    TRX, ETH = fetch_holders()
    stop = int(1e78)
    i = start
    while i < stop:
        private_key = number_to_private_key(i)
        trx_address = trx_private_key_to_address(private_key)
        eth_address = eth_private_key_to_address(private_key)
        
        if trx_address in TRX:
            print(f"Process {process_id} found match:")
            print("=========================================")
            print("No:", i)
            print("Private Key:", private_key)
            print("TRX Address:", trx_address)
            print("=========================================")
            save_rag(private_key, trx_address)
        
        if eth_address in ETH:
            print(f"Process {process_id} found match:")
            print("=========================================")
            print("No:", i)
            print("Private Key:", private_key)
            print("ETH Address:", eth_address)
            print("=========================================")
            save_rag(private_key, eth_address)
            
        print(f"Process {process_id} - Prog: {i}  ", end="\r")
        i += int(random.uniform(1e10, 1e20))

def start_multi_core():
    num_cores = 5  # Using your 5 free cores
    base_increment = int(1e69)  # A reasonable large step to avoid overlap
    
    # Create starting points for each process
    starting_points = [1 + i * base_increment for i in range(num_cores)]
    
    # Create a pool of processes
    with multiprocessing.Pool(processes=num_cores) as pool:
        # Map the rand_itr function to each starting point
        pool.starmap(rand_itr_multi_core, [(start, pid) for pid, start in enumerate(starting_points)])

# print(private_key_to_number(""))
# loop = asyncio.get_event_loop()
# loop.run_until_complete(trx_play())


# date_str = "2018-07-25 00:00:00"
# input_number = date_to_timestamp(date_str)
# input_number = next_prime(27)  #27
# input_number = 58545652  #27
# private_key = number_to_private_key(input_number)
# print("Private Key (Hex):", private_key, input_number)
# print("TRX Address:", trx_private_key_to_address(private_key))
# print("ETH Address:", eth_private_key_to_address(private_key))
# print("BTC Address:", private_key_to_btc_address(private_key))
# print("Polygon Address:", private_key_to_polygon_address(private_key))
# # print("Solana Address:", private_key_to_solana_address(private_key))
# print("BCH Address:", private_key_to_bch_address(private_key))

if __name__ == "__main__":
    start_multi_core()
    # rand_itr(start=int(1e70))
    # impossible_search()
    # perm_impossible_search()
    # custom_perm_impossible_search()
    # fac_seq_play()