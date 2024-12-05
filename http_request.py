from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
import requests
import json
from solders.keypair import Keypair
import asyncio
from solders.transaction import VersionedTransaction
from transaction import Transaction
from walletManager import WalletManager

class SolanaManager:
    def __init__(self,client, wallet_manager: WalletManager):
        self.client:AsyncClient = client
        
        self.master_wallet:Keypair
        self.wallet_manager = wallet_manager
        self.master_wallet: Keypair = None

    
    @classmethod
    async def create(cls, api_url="https://api.mainnet-beta.solana.com", wallets_dir="wallets"):
        client = AsyncClient(api_url)
        wallet_manager = WalletManager(wallets_dir)
        return cls(client, wallet_manager)

        
    async def send_transaction(self,txn:VersionedTransaction):
        
        return await self.client.send_transaction(txn)
    
    
        
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
 
