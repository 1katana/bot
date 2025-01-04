from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
import requests
import json
from solders.keypair import Keypair
import asyncio
from solders.transaction import VersionedTransaction
from walletManager import WalletManager
from dataclases.utils import UseClases




class SolanaManager:
    def __init__(self, client: AsyncClient, wallet_manager: WalletManager):
        self.client = client
        self.wallet_manager = wallet_manager
        self.init_wallets()

    
    def init_wallets(self):
        if self.wallets is not None:
            # Получаем разницу между текущими и новыми кошельками
            diff = self.wallet_manager.wallets.symmetric_difference(self.wallets)
            # Добавляем недостающие элементы как объекты UseClases
            self.wallets.extend(UseClases(w) for w in diff)
        else:
            # Создаём новый список объектов UseClases
            self.wallets = [UseClases(w) for w in self.wallet_manager.wallets]

    
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

    async def create_wallets(self, num_wallets: int):
        """
        Создает несколько кошельков.
        """
        for _ in range(num_wallets):
            self.wallet_manager.generate_wallet()

    async def distribute_funds(self, amount_per_wallet: int=-1):
        """
        Распределяет деньги с мастер-кошелька на другие кошельки.
        """
        if amount_per_wallet==-1:
            self.wallets
        
        master_wallet = self.wallet_manager.get_wallet(master_wallet_name)
        if not master_wallet or not master_wallet.is_master:
            print(f"Кошелек {master_wallet_name} не является мастер-кошельком.")
            return

        for wallet in self.wallet_manager.wallets:
            if wallet != master_wallet:
                await master_wallet.transfer_between_wallet(wallet.get_public_key(), amount_per_wallet, self.client)

    async def buy_tokens_in_cycle(self, input_mint: str, output_mint: str, amount: int):
        """
        Покупает токены по циклу с нескольких кошельков.
        """
        for wallet in self.wallet_manager.wallets:
            quote_response = await .get_quote_token(input_mint, output_mint, amount)
            await wallet.transfer_token(quote_response, self.client)
 
