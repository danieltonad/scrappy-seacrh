from number import trx_private_key_to_address, eth_private_key_to_address, number_to_private_key
import os, random


for i in range(1, 300_000):
    j = i
    j = random.randint(int(1e70), int(1e77))
    private_key = number_to_private_key(j)
    eth_address = eth_private_key_to_address(private_key)
    trx_address = trx_private_key_to_address(private_key)

    with open('trx.csv', 'a') as f:
        f.write(f'{j},{trx_address}\n')

    with open('eth.csv', 'a') as f:
        f.write(f'{j},{eth_address}\n')

    print(f'{i:,}', end='\r')
    