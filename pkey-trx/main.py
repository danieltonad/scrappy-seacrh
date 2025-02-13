from tronpy.keys import PrivateKey
import random, secrets, sha3, ecdsa

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

# private_key_hex = "5aed2a12b51d621700f719c95115994cbc250347cab075e5e745d2eb0c33986a"
pk1, pk2 = generate_trx_private_key()

print("Private Key:", pk1)
print("TRX Address:", trx_private_key_to_address(pk1))
print("ETH Address:", eth_private_key_to_address(pk1))

print("Private Key:", pk2)
print("TRX Address:", trx_private_key_to_address(pk2))
print("ETH Address:", eth_private_key_to_address(pk2))
