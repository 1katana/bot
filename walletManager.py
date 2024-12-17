import json
import os
from solders.keypair import Keypair
from wallet import Wallet
import asyncio
from solana.rpc.async_api import AsyncClient

class WalletManager:
    def __init__(self, wallets_dir="wallets"):
        os.makedirs(wallets_dir, exist_ok=True)
        self.wallets_dir = os.path.join(wallets_dir, "keypairs")
        self.db_file = os.path.join(wallets_dir, "wallet_db.json")
        self.wallets: set[Wallet] = set()
        self.load_wallets_from_db()

    def add_wallet(self, secret_key: str):
        secret_key = secret_key.replace(" ", "")
        key = Keypair.from_base58_string(secret_key)
        wallet_name = f"wallet{self.get_wallet_counter()}"
        wallet = Wallet(key, wallet_name, is_master=True)
        self.save_wallet(wallet)

    def load_wallets_from_dir(self):
        if not os.path.exists(self.wallets_dir):
            print(f"Директория {self.wallets_dir} не существует.")
            return

        for file_name in os.listdir(self.wallets_dir):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.wallets_dir, file_name)
                try:
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        keypair = Keypair.from_bytes(data)
                        wallet = Wallet(keypair, file_name, False)
                        self.wallets.add(wallet)
                except (json.JSONDecodeError, KeyError, ValueError) as e:
                    print(f"Ошибка при загрузке кошелька из файла {file_name}: {e}")

        self.save_wallets_to_db()

    def load_wallets_from_db(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as file:
                data = json.load(file)
                for wallet_info in data:
                    byte_list = list(map(int, wallet_info['keypair'].strip("[]").split(",")))
                    keypair = Keypair.from_bytes(bytes(byte_list))
                    wallet = Wallet(keypair, wallet_info['name'], wallet_info['is_master'])
                    self.wallets.add(wallet)

    def save_wallets_to_db(self):
        wallets_data = [
            {
                'name': wallet.name,
                'keypair': wallet.keypair.to_json(),
                'is_master': wallet.is_master
            }
            for wallet in self.wallets
        ]
        with open(self.db_file, 'w') as file:
            json.dump(wallets_data, file, indent=4)

    def save_wallet(self, wallet: Wallet):
        file_path = os.path.join(self.wallets_dir, f"{wallet.name}.json")
        with open(file_path, 'w') as file:
            file.write(wallet.keypair.to_json())
        self.wallets.add(wallet)
        self.save_wallets_to_db()

    def generate_wallet(self):
        wallet_name = f"wallet{self.get_wallet_counter()}"
        keypair = Keypair()
        print(keypair.pubkey())
        wallet = Wallet(keypair, wallet_name)
        self.save_wallet(wallet)
        return wallet

    def get_wallet(self, name: str):
        for wallet in self.wallets:
            if wallet.name == name:
                return wallet
        return None

    def set_master_wallet(self, name: str):
        wallet = self.get_wallet(name)
        if wallet:
            wallet.is_master = True
            self.save_wallets_to_db()

    def get_wallet_counter(self) -> int:
        counter = 0
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as file:
                data = json.load(file)
                for wallet_info in data:
                    try:
                        num = int(wallet_info['name'][6:])
                        counter = max(counter, num + 1)
                    except (ValueError, IndexError):
                        continue
        return counter

    
async def main():
    wallets=WalletManager()
    
    
    
 
    wal0=wallets.get_wallet("wallet0")

    print(wal0.keypair.pubkey())
    
    
    sol= AsyncClient("https://api.mainnet-beta.solana.com")
    
    
    ans=await wal0.get_balance(sol)
    print( ans)

    path= await wal0.get_quote_token("fisyo27uouYhxNKY51zDVxLTLhrrHxDx5hBk9EZddzL","So11111111111111111111111111111111111111112",10_000_000) 
   
    a=await wal0.transfer_token(path,sol)
    
    print()


    
    
        
if __name__=="__main__":
    
    
    asyncio.run(main())
    