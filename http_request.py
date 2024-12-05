from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
import requests
import json
from solders.keypair import Keypair
import asyncio


class SolanaManager:
    def __init__(self,client):
        self.client:AsyncClient = client
        
        self.master_wallet:Keypair
        self.wallets:list[Keypair]=[]

    
    @classmethod
    async def create(cls,api_url="https://api.mainnet-beta.solana.com"):
        client= AsyncClient(api_url)
        await asyncio.sleep(1)
        return cls(client)
    
    async def add_master_wallet(self,secret_key:str):
        
        key = Keypair.from_bytes(bytes.fromhex(secret_key))

        self.master_wallet= key
    
    async def generate_wallet(self,count=1):
        
        for _ in enumerate(count):
            self.wallets.append(Keypair())
        
        
    async def add_wallet(self,secret_key:str):
        self.wallets.append(Keypair.from_bytes(bytes.fromhex(secret_key)))
        
    
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
    
    
    async def get_account_info(self):
        """
        Получает информацию об аккаунте по публичному ключу
        """
        
        return await self.client.get_account_info(pubkey=self.master_wallet.pubkey)
    
    async def get_balance(self):
        """
        Получает информацию об аккаунте по публичному ключу
        """
        return await self.client.get_balance(Pubkey.from_string("4gYYGqCCqYXuvG2gWgiCJtLxWkzujnxXeQaDZxrHNWWt"))


    async def close(self):
        """
        Закрывает соединение с Solana API
        """
        await self.client.close()
        print("Соединение с Solana API закрыто.")
 
