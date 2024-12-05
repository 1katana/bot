import json
import os
import uuid
from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solders.message import MessageV0
from solders.hash import Hash
from solders.transaction import VersionedTransaction
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
import requests
import json
import asyncio
from transaction import Transaction
from walletManager import WalletManager

class Wallet():
    
    def __init__(self,keypair: Keypair,name: str,file_path: str,is_master=False):
        
        self.name:str
        self.wallet:Keypair
        self.is_master=False
        self.file_path=file_path
        
        
    async def get_balance(self,client:AsyncClient):
        """Получает баланс кошелька."""
        balance = await client.get_balance(self.wallet.pubkey)
        return balance

    async def get_latest_blockhash(self,client:AsyncClient):
        return await client.get_latest_blockhash()
    
    async def transfer(self, receiver: Pubkey, lamports: int,client:AsyncClient):
        """Отправляет SOL на указанный адрес."""
        blockhash = await self.get_latest_blockhash(client)
        
        txn=Transaction(sender=self.wallet,receiver=receiver,lamports=lamports,blockhash=blockhash.value.blockhash)
        
        return await client.send_transaction(txn)
    
    

    def get_public_key(self):
        """Возвращает публичный ключ кошелька."""
        return self.wallet.pubkey