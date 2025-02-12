from tronpy.keys import PrivateKey

# Example Private Key (replace with your own)
private_key_hex = "ef8c3f61db859e035808fe037999c3554f4ae4ef5ba4ac9a095db6e0b6fe5cdf"

# Generate Public Key & Address
priv_key = PrivateKey(bytes.fromhex(private_key_hex))
trx_address = priv_key.public_key.to_base58check_address()

print("TRX Address:", trx_address)
