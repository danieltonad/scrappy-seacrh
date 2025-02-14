from tronpy.keys import PrivateKey
import random, secrets, hashlib, ecdsa


trx_path = "../data/trx_holders.txt"
eth_bnb_path = "../data/eth_bnb_holders.txt"

def fetch_holders() -> tuple:
    with open(trx_path, "r") as f:
        trx_holders = f.read().splitlines()
    with open(eth_bnb_path, "r") as f:
        eth_bnb_holders = f.read().splitlines()
    return trx_holders, eth_bnb_holders

TRX, BNB_ETH = fetch_holders() 
print(f"Lodaed {len(TRX):,} TRX holders and {len(BNB_ETH):,} BNB/ETH holders")

def save_rag(pkey, address):
    with open("pkey.rag", "a") as f:
        f.write(f"{pkey} -> {address}\n")

def generate_private_key() -> tuple:
    return secrets.token_hex(32), ''.join(random.choices('0123456789abcdef', k=64))

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


def spin_shii(): 
    pk1, pk2 = generate_private_key()
    
    pk1_trx_addr = trx_private_key_to_address(pk1)
    pk1_bnb_eth_addr = eth_private_key_to_address(pk1)
    
    if pk1_trx_addr in TRX:
        save_rag(pk1, pk1_trx_addr)
        print(f"Saved {pk1} -> {pk1_trx_addr}")
     
    if pk1_bnb_eth_addr in BNB_ETH:
        save_rag(pk1, pk1_bnb_eth_addr)
        print(f"Saved {pk1} -> {pk1_bnb_eth_addr}")   
    
    pk2_trx_addr = trx_private_key_to_address(pk2)
    pk2_bnb_eth_addr = eth_private_key_to_address(pk2)
    
    if pk2_trx_addr in TRX:
        save_rag(pk2, pk2_trx_addr)
        print(f"Saved {pk2} -> {pk2_trx_addr}")
     
    if pk2_bnb_eth_addr in BNB_ETH:
        save_rag(pk2, pk2_bnb_eth_addr)
        print(f"Saved {pk2} -> {pk2_bnb_eth_addr}")   
    


def main():
    while True:
        spin_shii()
        
        
        
main()

# pk1, pk2 = generate_private_key()
# print("Private Key:", pk1)
# print("TRX Address:", trx_private_key_to_address(pk1))
# print("ETH Address:", eth_private_key_to_address(pk1))

# print("Private Key:", pk2)
# print("TRX Address:", trx_private_key_to_address(pk2))
# print("ETH Address:", eth_private_key_to_address(pk2))