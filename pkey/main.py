from tronpy.keys import PrivateKey
import random, secrets, sha3, ecdsa


trx_path = "../data/trx_holders.txt"
eth_bnb_path = "../data/eth_bnb_holders.txt"

def fetch_holders() -> tuple:
    with open(trx_path, "r") as f:
        trx_holders = f.read().splitlines()
    with open(eth_bnb_path, "r") as f:
        eth_bnb_holders = f.read().splitlines()
    return trx_holders, eth_bnb_holders

def generate_trx_private_key() -> tuple:
    return secrets.token_hex(32), ''.join(random.choices('0123456789abcdef', k=64))

def trx_private_key_to_address(private_key_hex: str) -> str:
    priv_key = PrivateKey(bytes.fromhex(private_key_hex))
    return priv_key.public_key.to_base58check_address()

def eth_private_key_to_address(private_key_hex: str) -> str:
    private_key_bytes = bytes.fromhex(private_key_hex)
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()
    keccak = sha3.keccak_256()
    keccak.update(public_key[1:])
    eth_address = keccak.digest()[-20:]
    return '0x' + eth_address.hex()


def
TRX, BNB_ETH = fetch_holders()  

print(f"Lodaed {len(TRX):,} TRX holders and {len(BNB_ETH):,} BNB/ETH holders")

pk1, pk2 = generate_trx_private_key()





# pk1, pk2 = generate_trx_private_key()
# private_key_hex = "5aed2a12b51d621700f719c95115994cbc250347cab075e5e745d2eb0c33986a"
# print("Private Key:", pk1)
# print("TRX Address:", trx_private_key_to_address(pk1))
# print("ETH Address:", eth_private_key_to_address(pk1))

# print("Private Key:", pk2)
# print("TRX Address:", trx_private_key_to_address(pk2))
# print("ETH Address:", eth_private_key_to_address(pk2))
