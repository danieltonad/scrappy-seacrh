import hashlib, base58
import ecdsa

# helper: hash160 = RIPEMD160(SHA256(data))
def hash160(data: bytes) -> bytes:
    sha = hashlib.sha256(data).digest()
    rip = hashlib.new('ripemd160', sha).digest()
    return rip

# helper: checksum for base58
def checksum(data: bytes) -> bytes:
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]

# helper: Bech32 encoding
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
def bech32_polymod(values):
    gen = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = (chk >> 25)
        chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5):
            chk ^= gen[i] if ((b >> i) & 1) else 0
    return chk

def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]

def bech32_create_checksum(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0,0,0,0,0,0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]

def bech32_encode(hrp, data):
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + '1' + ''.join([CHARSET[d] for d in combined])

def cashaddr_encode(hrp: str, data: list[int]) -> str:
    """Encode in Bitcoin Cash CashAddr format (uses ':' separator)."""
    combined = data + bech32_create_checksum(hrp, data)
    return hrp + ':' + ''.join([CHARSET[d] for d in combined])


def convertbits(data, frombits, tobits, pad=True):
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << tobits) - 1
    for value in data:
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret

def btc_addresses_from_private_key(private_key_hex: str) -> tuple:
    try:
        # derive public key
        private_key_bytes = bytes.fromhex(private_key_hex)
        sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        public_key = b'\x04' + vk.to_string()   # uncompressed pubkey

        # compressed pubkey
        pk_bytes = vk.to_string()
        if pk_bytes[-1] % 2 == 0:
            compressed_pubkey = b'\x02' + pk_bytes[:32]
        else:
            compressed_pubkey = b'\x03' + pk_bytes[:32]

        # --- Address 1 (P2PKH, starts with "1") ---
        h160 = hash160(compressed_pubkey)
        prefix = b'\x00' + h160
        addr1 = base58.b58encode(prefix + checksum(prefix)).decode()

        # --- Address 3 (P2SH-P2WPKH, starts with "3") ---
        redeem_script = b'\x00\x14' + h160  # 0x00 PUSH(20) <hash160>
        h160_redeem = hash160(redeem_script)
        prefix = b'\x05' + h160_redeem
        addr3 = base58.b58encode(prefix + checksum(prefix)).decode()

        # --- Address bc1 (Bech32, native SegWit) ---
        converted = convertbits(h160, 8, 5)
        bech32_data = [0] + converted
        addrbc1 = bech32_encode("bc", bech32_data)
        return addr1, addr3, addrbc1

        # return {"p2pkh": addr1, "p2sh_p2wpkh": addr3, "bech32": addrbc1}

    except Exception as e:
        return "","",""
    



def ltc_addresses_from_private_key(private_key_hex: str) -> tuple:
    try:
        private_key_bytes = bytes.fromhex(private_key_hex)
        sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        pk_bytes = vk.to_string()
        if pk_bytes[-1] % 2 == 0:
            compressed_pubkey = b'\x02' + pk_bytes[:32]
        else:
            compressed_pubkey = b'\x03' + pk_bytes[:32]

        # --- P2PKH (starts with L) ---
        h160 = hash160(compressed_pubkey)
        prefix = b'\x30' + h160  # 0x30 = 48 = L
        addr1 = base58.b58encode(prefix + checksum(prefix)).decode()

        # --- P2SH (starts with M) ---
        redeem_script = b'\x00\x14' + h160
        h160_redeem = hash160(redeem_script)
        prefix = b'\x32' + h160_redeem  # 0x32 = 50 = M
        addr3 = base58.b58encode(prefix + checksum(prefix)).decode()

        # --- Bech32 (starts with ltc1) ---
        converted = convertbits(h160, 8, 5)
        bech32_data = [0] + converted
        addrbc1 = bech32_encode("ltc", bech32_data)

        return addr1, addr3, addrbc1
    except Exception as e:
        return "", "", ""


def bch_cashaddr_from_private_key(private_key_hex: str, addr_type: str = "p2pkh") -> str:
    """
    Generate a Bitcoin Cash CashAddr address from a private key.
    addr_type = "p2pkh" (bitcoincash:q...) or "p2sh" (bitcoincash:p...)
    """
    try:
        # derive compressed public key
        private_key_bytes = bytes.fromhex(private_key_hex)
        sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        pk_bytes = vk.to_string()
        if pk_bytes[-1] % 2 == 0:
            compressed_pubkey = b'\x02' + pk_bytes[:32]
        else:
            compressed_pubkey = b'\x03' + pk_bytes[:32]

        if addr_type == "p2pkh":
            # hash160(pubkey)
            h160 = hash160(compressed_pubkey)
            version = 0  # P2PKH
        elif addr_type == "p2sh":
            # hash160(redeem_script)
            redeem_script = b'\x00\x14' + hash160(compressed_pubkey)
            h160 = hash160(redeem_script)
            version = 8  # P2SH
        else:
            raise ValueError("addr_type must be 'p2pkh' or 'p2sh'")

        # convert 8-bit bytes → 5-bit groups for bech32
        converted = convertbits(h160, 8, 5)

        # prepend version + data
        bech32_data = [version] + converted

        # encode with CashAddr prefix
        return cashaddr_encode("bitcoincash", bech32_data)

    except Exception as e:
        return ""





def int_to_hex_string(n: int) -> str:
    return hex(n)[2:]

# shit = bch_cashaddr_from_private_key(int_to_hex_string(96690521103684763241907041926562609780425301947070575270117074750536375318862))
# print(shit)
# for i in shit:
#     print(i)