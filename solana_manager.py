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

        

    async def close(self):
        """
        Закрывает соединение с Solana API
        """
        await self.client.close()
        print("Соединение с Solana API закрыто.")
 
