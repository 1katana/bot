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


class Wallet:
    def __init__(self, keypair: Keypair, name: str, is_master=False):
        self.name = name
        self.keypair = keypair
        self.is_master = is_master

    async def get_balance(self, client: AsyncClient):
        """Получает баланс кошелька."""
        balance = await client.get_balance(self.keypair.pubkey)
        return balance

    async def get_latest_blockhash(self, client: AsyncClient):
        return await client.get_latest_blockhash()

    async def transfer(self, receiver: Pubkey, lamports: int, client: AsyncClient):
        """Отправляет SOL на указанный адрес."""
        blockhash = await self.get_latest_blockhash(client)
        txn = Transaction(sender=self.keypair, receiver=receiver, lamports=lamports, blockhash=blockhash.value.blockhash)
        return await self.send_transaction(txn, client)

    async def send_transaction(self, txn: VersionedTransaction, client: AsyncClient):
        return await client.send_transaction(txn)

    def get_public_key(self):
        """Возвращает публичный ключ кошелька."""
        return self.keypair.pubkey

    def __hash__(self):
        """
        Генерирует хэш на основе публичного ключа, который является уникальным для каждого кошелька.
        """
        
        return hash(self.keypair)

    def __eq__(self, other):
        """
        Сравнивает кошельки на основе публичного ключа.
        """
        if not isinstance(other, Wallet):
            return False
        

        return self.keypair == other.keypair