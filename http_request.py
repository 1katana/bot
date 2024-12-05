from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
import requests
import json
from solders.keypair import Keypair
import asyncio
from solders.transaction import VersionedTransaction
from transaction import Transaction

class SolanaManager:
    def __init__(self,client):
        self.client:AsyncClient = client
        
        self.master_wallet:Keypair
        self.wallets:list[Keypair]=[]

    
    @classmethod
    async def create(cls,api_url="https://api.mainnet-beta.solana.com"):
        client= AsyncClient(api_url)
        return cls(client)
    
    async def add_master_wallet(self,secret_key:str):
        
        key = Keypair.from_bytes(bytes.fromhex(secret_key))

        self.master_wallet= key
    
    async def generate_wallet(self,count=1):
        
        for _ in enumerate(count):
            self.wallets.append(Keypair())
        
    async def send_transaction(self,txn:VersionedTransaction):
        
        return await self.client.send_transaction(txn)
    
    
    async def add_wallet(self,secret_key:str):
        self.wallets.append(Keypair.from_bytes(bytes.fromhex(secret_key)))
        
        
    def add_master_wallet_from_json(self,file_path:str):
        # Чтение JSON-файла
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Создание объекта Keypair из JSON-данных
        self.master_wallet = Keypair.from_bytes(data)
        
        
    # Метод для создания и отправки транзакции
    async def transfer_sol(self, receiver: Pubkey, lamports: int):
        blockhash = await self.get_latest_blockhash()
        tx = Transaction(self.master_wallet, receiver, lamports, blockhash)
        return await self.send_transaction(tx)
        
    
    async def get_signaturesfor_address_with_slot(self, pubkey,slot):
        """
        Получает информацию об аккаунте по публичному ключу
        """
        params = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                pubkey,
                {
                    "minContextSlot": slot,  # Минимальный слот
                }
            ]
        }
        
        response = requests.post(self.api_url, data=json.dumps(params), headers={"Content-Type": "application/json"})
        return response
    
    
    async def get_latest_blockhash(self):
        return await self.client.get_latest_blockhash()
    
    async def get_account_info(self):
        """
        Получает информацию об аккаунте по публичному ключу
        """
        
        return await self.client.get_account_info(pubkey=self.master_wallet.pubkey)
    
    async def get_balance(self):
        """
        Получает информацию об аккаунте по публичному ключу
        """
        return await self.client.get_balance(self.master_wallet.pubkey)


    async def close(self):
        """
        Закрывает соединение с Solana API
        """
        await self.client.close()
        print("Соединение с Solana API закрыто.")
 
