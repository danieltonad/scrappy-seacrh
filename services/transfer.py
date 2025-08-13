from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.keys import PrivateKey
from settings import settings
# from bitcoin import privkey_to_pubkey, privkey_to_address, mk_tx, ecdsa_sign, serialize
from web3 import Web3
from eth_account import Account

def send_bnb(priv_key_hex, to_address, amount, rpc_url="https://bsc-dataseed.binance.org/"):
    """
    Send BNB to another wallet address.
    - priv_key_hex: Private key in hex format.
    - to_address: Recipient wallet address.
    - amount: Amount to send (in BNB).
    - rpc_url: Binance Smart Chain RPC endpoint.
    """
    # Initialize Web3
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to Binance Smart Chain RPC")
    
    # Get sender's account and balance
    account = Account.from_key(priv_key_hex)
    from_address = account.address
    balance = web3.eth.get_balance(from_address)

    # Convert amount to wei
    amount_in_wei = web3.to_wei(amount, "ether")

    # Get transaction parameters
    nonce = web3.eth.get_transaction_count(from_address)
    gas_limit = 21000  # Standard for BNB transfers
    gas_price = web3.eth.gas_price  # Current gas price from the network
    gas_fee = gas_limit * gas_price

    total_cost = amount_in_wei + gas_fee
    if balance < total_cost:
        raise ValueError(
            f"Insufficient funds: Available={web3.from_wei(balance, 'ether')} BNB, Required={web3.from_wei(total_cost, 'ether')} BNB"
        )
    
    amount_in_wei = balance - gas_fee

    # Create the transaction
    tx = {
        "nonce": nonce,
        "to": to_address,
        "value": web3.to_wei(amount, "ether"),
        "gas": 21000,
        "gasPrice": web3.eth.gas_price,
        "chainId": 56
    }

    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=priv_key_hex)

    # Broadcast the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Return the transaction hash
    return web3.to_hex(tx_hash)


def sweep_bnb(priv_key_hex, to_address, rpc_url="https://bsc-dataseed.binance.org/"):
    """
    Sends all available BNB (minus gas fees) to the target address.
    :param priv_key_hex: Sender's private key in hex format.
    :param to_address: Receiver's wallet address.
    :param rpc_url: RPC URL for Binance Smart Chain.
    :return: Transaction hash as a string.
    """
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to Binance Smart Chain RPC")

    # Get sender's account and balance
    account = Account.from_key(priv_key_hex)
    from_address = account.address
    balance = web3.eth.get_balance(from_address)

    # Transaction parameters
    nonce = web3.eth.get_transaction_count(from_address)
    gas_limit = 21000  # Standard gas for BNB transfers
    gas_price = web3.eth.gas_price
    gas_fee = gas_limit * gas_price

    # Check if balance can cover at least the gas fee
    if balance <= gas_fee:
        raise ValueError("Insufficient funds to cover gas fee")

    # Calculate exact amount to send (balance - gas_fee)
    amount_in_wei = balance - gas_fee

    # Create and sign the transaction
    tx = {
        "nonce": nonce,
        "to": to_address,
        "value": amount_in_wei,
        "gas": gas_limit,
        "gasPrice": gas_price,
        "chainId": 56,  # BSC mainnet chain ID
    }
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=priv_key_hex)

    # Send transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return web3.to_hex(tx_hash)



def send_trx(priv_key_hex, to_address, amount):
    client = Tron(provider=HTTPProvider(api_key=settings.TRON_GRID_API))
    private_key = PrivateKey(bytes.fromhex(priv_key_hex))
    from_address = private_key.public_key.to_base58check_address()
    tx = (
        client.trx.transfer(from_address, to_address, int(amount * 1e6))
        .build()
        .sign(private_key)
    )
    tx_hash = tx.broadcast()
    return tx_hash


def sweep_trx(priv_key_hex, to_address):
    client = Tron(provider=HTTPProvider(api_key=settings.TRON_GRID_API))
    private_key = PrivateKey(bytes.fromhex(priv_key_hex))
    from_address = private_key.public_key.to_base58check_address()
    balance = int(client.get_account_balance(from_address) * int(1e6))
    # Build a dummy transaction to estimate fee
    tx = client.trx.transfer(from_address, to_address, balance).build()
    # tx_info = tx.inspect()
    DEFAULT_TRX_TRANSFER_FEE = 100000  # in SUN (0.1 TRX)
    # Ensure sufficient balance for transaction and fee
    if balance <= DEFAULT_TRX_TRANSFER_FEE:
        raise ValueError("Insufficient balance to cover transaction fees.")
    # Calculate the maximum amount to send
    max_amount_to_send = balance - DEFAULT_TRX_TRANSFER_FEE
    # Build, sign, and broadcast the transaction
    final_tx = (
        client.trx.transfer(from_address, to_address, max_amount_to_send)
        .build()
        .sign(private_key)
    )
    tx_hash = final_tx.broadcast()
    return tx_hash


def send_usdt(client, priv_key_hex, to_address, amount):
    """
    Transfer USDT from one address to another.

    :param client: Tronpy client instance.
    :param priv_key_hex: Sender's private key in hex format.
    :param to_address: Recipient's wallet address.
    :param amount: Amount of USDT to send (float).
    :return: Transaction hash.
    """
    client = Tron(provider=HTTPProvider(api_key=settings.TRON_GRID_API))
    # USDT contract address on TRON mainnet
    usdt_contract_address = "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj"
    
    # Private key
    private_key = PrivateKey(bytes.fromhex(priv_key_hex))
    from_address = private_key.public_key.to_base58check_address()

    # Get the contract instance
    contract = client.get_contract(usdt_contract_address)
    
    # Build a transaction to call the transfer method
    amount_in_sun = int(amount * 1e6)  # Convert USDT to SUN
    txn = contract.functions.transfer(to_address, amount_in_sun).with_owner(from_address).build()

    # Sign and broadcast the transaction
    signed_tx = txn.sign(private_key)
    tx_hash = signed_tx.broadcast()
    
    return tx_hash