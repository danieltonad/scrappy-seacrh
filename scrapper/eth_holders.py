import requests_html
import asyncio, os


def save_eth_bnb_holders(holders: list):
    eth_bnb_path = "../data/eth_bnb_holders.txt"
    prev_holders = []
    if os.path.exists(eth_bnb_path):
        with open(eth_bnb_path, "r") as f:
            prev_holders = f.read().splitlines()
    holders = list(set(holders + prev_holders))
    with open(eth_bnb_path, "w") as f:
        for holder in holders:
            f.write(f"{holder}\n")
            
            
async def fetch_eth_holders(page: int):
    all = []
    url = f"https://etherscan.io/accounts/{page}?ps=100"
    session = requests_html.AsyncHTMLSession()
    response = await session.get(url)
    data = response.html.find("td.d-flex.align-items-center")
    for dt in data:
        address = str(dt.find("a.me-1", first=True).attrs.get("href")).split("/")[-1]
        if address:
            all.append(address)
    save_eth_bnb_holders(all)
            
            
async def fetch_bnb_holders(page: int):
    all = []
    url = f"https://bscscan.com/accounts/{page}?ps=100"
    session = requests_html.AsyncHTMLSession()
    response = await session.get(url)
    data = response.html.find("td.d-flex.align-items-center")
    for dt in data:
        address = str(dt.find("a.me-1", first=True).attrs.get("href")).split("/")[-1]
        if address:
            all.append(address)
    save_eth_bnb_holders(all)
        
        
for i in range(101):        
    asyncio.run(fetch_eth_holders(i))
    asyncio.run(fetch_eth_holders(i))
    print(f"Progress: {i} ...", end="\r")
    