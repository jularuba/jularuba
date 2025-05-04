import requests
import time
from datetime import datetime

ETHERSCAN_API_KEY = "YourApiKeyHere"  # вставь свой API ключ

def get_internal_txs(address):
    url = f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&sort=asc&apikey={ETHERSCAN_API_KEY}"
    return requests.get(url).json().get("result", [])

def is_hot_wallet(address):
    txs = get_internal_txs(address)
    total_in = sum(int(tx["value"]) for tx in txs if tx["isError"] == "0")
    return total_in > 1e18  # больше 1 ETH входом

def scan_new_wallets(n=10):
    print(f"[{datetime.now()}] Scanning...")
    response = requests.get(f"https://api.etherscan.io/api?module=account&action=listaccounts&apikey={ETHERSCAN_API_KEY}")
    wallets = response.json().get("result", [])[:n]
    for wallet in wallets:
        if is_hot_wallet(wallet):
            print(f"🔥 Hot wallet found: {wallet}")
        else:
            print(f"- Cool wallet: {wallet}")
        time.sleep(0.2)

if __name__ == "__main__":
    scan_new_wallets()
