import hashlib
from typing import Tuple, List

import ecdsa
import base58

# ---------- hex utils ----------
def hex_to_bytes(hexstr: str) -> bytes:
    return bytes.fromhex(hexstr)

def bytes_to_hex(b: bytes) -> str:
    return b.hex()

# ---------- hashing ----------
def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def ripemd160(data: bytes) -> bytes:
    h = hashlib.new('ripemd160')
    h.update(data)
    return h.digest()

def hash160(data: bytes) -> bytes:
    return ripemd160(sha256(data))

def double_sha256(data: bytes) -> bytes:
    return sha256(sha256(data))

# ---------- Bech32 ----------
BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"

def bech32_polymod(values: List[int]) -> int:
    GEN = [0x3b6a57b2,0x26508e6d,0x1ea119fa,0x3d4233dd,0x2a1462b3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = ((chk & 0x1ffffff) << 5) ^ v
        for i in range(5):
            if (b >> i) & 1:
                chk ^= GEN[i]
    return chk

def bech32_hrp_expand(hrp: str) -> List[int]:
    ret = [(ord(c) >> 5) & 7 for c in hrp]
    ret.append(0)
    ret.extend([ord(c) & 31 for c in hrp])
    return ret

def bech32_create_checksum(hrp: str, data: List[int]) -> List[int]:
    values = bech32_hrp_expand(hrp) + data + [0]*6
    polymod = bech32_polymod(values) ^ 1
    return [(polymod >> (5*(5-i))) & 31 for i in range(6)]

def bech32_encode(hrp: str, data5: List[int]) -> str:
    cs = bech32_create_checksum(hrp, data5)
    return hrp + '1' + ''.join(BECH32_CHARSET[d] for d in data5+cs)

def convertbits(data: bytes, frombits: int, tobits: int, pad: bool=True) -> List[int]:
    acc = 0
    bits = 0
    maxv = (1 << tobits) - 1
    ret = []
    for value in data:
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    else:
        if bits >= frombits or ((acc << (tobits - bits)) & maxv):
            return []
    return ret

# ---------- ECDSA public key ----------
def public_key_from_private_hex(priv_hex: str, compressed: bool=True) -> bytes:
    priv_bytes = hex_to_bytes(priv_hex)
    sk = ecdsa.SigningKey.from_string(priv_bytes, curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    if compressed:
        px = vk.pubkey.point.x()
        py = vk.pubkey.point.y()
        return bytes([2 + (py & 1)]) + px.to_bytes(32, 'big')
    else:
        return b'\x04' + vk.to_string()

# ---------- address generation ----------
def btc_addresses_from_private_key(priv_hex: str) -> Tuple[str,str,str]:
    compressed_pub = public_key_from_private_hex(priv_hex, compressed=True)
    h160 = hash160(compressed_pub)

    # P2PKH
    payload = b'\x00' + h160
    payload += double_sha256(payload)[:4]
    addr1 = base58.b58encode(payload).decode()

    # P2SH-P2WPKH
    redeem = b'\x00\x14' + h160
    h160_redeem = hash160(redeem)
    payload2 = b'\x05' + h160_redeem
    payload2 += double_sha256(payload2)[:4]
    addr3 = base58.b58encode(payload2).decode()

    # Bech32 native segwit
    conv = convertbits(h160, 8, 5, True)
    addrbc1 = bech32_encode('bc', [0]+conv)

    return addr1, addr3, addrbc1

def ltc_addresses_from_private_key(priv_hex: str) -> Tuple[str,str,str]:
    compressed_pub = public_key_from_private_hex(priv_hex, compressed=True)
    h160 = hash160(compressed_pub)

    # P2PKH prefix 0x30 -> L
    payload = b'\x30' + h160
    payload += double_sha256(payload)[:4]
    addr1 = base58.b58encode(payload).decode()

    # P2SH prefix 0x32 -> M
    redeem = b'\x00\x14' + h160
    h160_redeem = hash160(redeem)
    payload2 = b'\x32' + h160_redeem
    payload2 += double_sha256(payload2)[:4]
    addr3 = base58.b58encode(payload2).decode()

    # Bech32
    conv = convertbits(h160, 8, 5, True)
    addrbc1 = bech32_encode('ltc', [0]+conv)

    return addr1, addr3, addrbc1

def bch_cashaddr_from_private_key(priv_hex: str, addr_type: str) -> str:
    compressed_pub = public_key_from_private_hex(priv_hex, compressed=True)
    h_pub = hash160(compressed_pub)

    if addr_type == 'p2pkh':
        h160_ = h_pub
        version = 0
    elif addr_type == 'p2sh':
        redeem = b'\x00\x14' + h_pub
        h160_ = hash160(redeem)
        version = 8
    else:
        raise ValueError("addr_type must be 'p2pkh' or 'p2sh'")

    conv = convertbits(h160_, 8, 5, True)
    data5 = [version] + conv
    return bech32_encode('bitcoincash', data5)



if __name__ == "__main__":
    print(btc_addresses_from_private_key('0000000000000000000000000000000000000000000000000000000000000000'))