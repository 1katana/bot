from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from jupiter import Jupiter
import base64
from solders.pubkey import Pubkey
from solana.rpc.types import TxOpts
from solders.signature import Signature
from solders import message
import json
from solana.rpc.types import TokenAccountOpts
from dataclases.tokensData import TokensData,parse_rpc_response
import asyncio
import time
import functools


def measure_time(func):
    @functools.wraps(func)
    def wrapper_measure_time(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function {func.__name__} took {elapsed_time:.4f} seconds to execute")
        return result
    return wrapper_measure_time

class Wallet:
    def __init__(self, keypair: Keypair, name: str, is_master=False):
        """
        Инициализирует кошелек с заданной парой ключей, именем и флагом,
        указывающим, является ли кошелек главным.
        
        :param keypair: Пара ключей для кошелька.
        :param name: Имя кошелька.
        :param is_master: Флаг, указывающий, является ли кошелек главным.
        """
        self.name = name
        self.keypair = keypair
        self.is_master = is_master
        
        self.balance:int
        self.tokens:TokensData

    async def get_token_account_by_owner(self, client: AsyncClient) -> TokensData:
        """
        Получает токен-аккаунты, принадлежащие владельцу этого кошелька.
        
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Список токен-аккаунтов.
        """
        tokens = await client.get_token_accounts_by_owner_json_parsed(
            self.keypair.pubkey(),
            TokenAccountOpts(program_id=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"))
        )
        
        self.tokens=parse_rpc_response(tokens)
        
        return self.tokens

    async def get_token_account_balance(self, client: AsyncClient):
        """
        Получает баланс токен-аккаунта кошелька.
        
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Баланс токен-аккаунта.
        """
        return await client.get_token_account_balance(self.keypair.pubkey())

    async def get_account_info(self, client: AsyncClient):
        """
        Получает информацию об аккаунте кошелька.
        
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Информация об аккаунте.
        """
        return await client.get_account_info(self.keypair.pubkey())

    async def get_balance(self, client: AsyncClient) -> int:
        """
        Получает общий баланс SOL кошелька.
        
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Баланс в лампортах.
        """
        balance=await client.get_balance(self.keypair.pubkey())
        
        self.balance=balance.value
        
        return balance

    async def get_latest_blockhash(self, client: AsyncClient):
        """
        Получает последний блокхеш для выполнения транзакций.
        
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Последний блокхеш.
        """
        return await client.get_latest_blockhash()

    async def transfer_token(self, quote_response, client: AsyncClient):
        """
        Осуществляет обмен токенов по заданному котировочному ответу.
        
        :param quote_response: Ответ с котировкой для обмена токенов.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Результат выполнения транзакции.
        """
        transaction_data = await Jupiter.swap_tokens(self.keypair, quote_response)
        swap_transaction = transaction_data['swapTransaction']
        decoded_swap_transaction = base64.b64decode(swap_transaction)
        signed_txn = await self.sign_transaction_token(decoded_swap_transaction)
        opts = TxOpts(
            skip_preflight=False,
            preflight_commitment="confirmed",
            max_retries=3,
        )
        return await self.send_transaction_token(signed_txn, opts, client)

    @measure_time
    async def transfer_between_wallet(self, receiver: Pubkey, lamports: int, client: AsyncClient):
        """
        Переводит SOL на указанный адрес.
        
        :param receiver: Публичный ключ получателя.
        :param lamports: Сумма в лампортах для перевода.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Результат выполнения транзакции.
        """
        blockhash = await self.get_latest_blockhash(client)
        ix = transfer(
            TransferParams(
                from_pubkey=self.keypair.pubkey(), to_pubkey=receiver, lamports=lamports
            )
        )
        msg = MessageV0.try_compile(
            payer=self.keypair.pubkey(),
            instructions=[ix],
            address_lookup_table_accounts=[],
            recent_blockhash=blockhash.value.blockhash,
        )
        txn = VersionedTransaction(msg, [self.keypair])
        return await self.send_transaction_between_wallet(txn, client)


    async def send_transaction_between_wallet(self, txn: VersionedTransaction, client: AsyncClient):
        """
        Отправляет указанную транзакцию.
        
        :param txn: Транзакция для отправки.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Подпись транзакции.
        """
        return await client.send_transaction(txn)


    @measure_time
    async def sign_transaction_token(self, transaction_data: dict):
        """
        Подписывает транзакцию токена.
        
        :param swap_transaction: Сырые данные транзакции.
        :return: Подписанная транзакция.
        """
        swap_transaction = transaction_data['swapTransaction']
        decoded_swap_transaction = base64.b64decode(swap_transaction)

        raw_txn = VersionedTransaction.from_bytes(decoded_swap_transaction)
        signature = self.keypair.sign_message(message.to_bytes_versioned(raw_txn.message))
        signed_txn = VersionedTransaction.populate(raw_txn.message, [signature])
        return signed_txn

    @measure_time
    async def send_transaction_token(self, signed_txn: VersionedTransaction, client: AsyncClient, opts: TxOpts=TxOpts(
            skip_preflight=False,
            preflight_commitment="confirmed",
            max_retries=3,
        )) -> Signature:
        """
        Отправляет транзакцию токена с учетом приоритизации и дополнительных опций.
        
        :param signed_txn: Подписанная транзакция.
        :param opts: Опции выполнения транзакции.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Подпись транзакции.
        """
        result = await client.send_raw_transaction(bytes(signed_txn), opts)
        return result.value

    async def test_transaction(self, txid: Signature, client: AsyncClient):
        """
        Тестирует транзакцию на подтверждение в сети.
        
        :param txid: Подпись транзакции.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Подтверждение успешности транзакции.
        """
        print(f"Transaction: https://explorer.solana.com/tx/{txid}")
        print("Ожидание подтверждения...")

        try:
            await asyncio.wait_for(client.confirm_transaction(txid, commitment="confirmed", sleep_seconds=1), timeout=3)
            print(f"Подтверждена: https://explorer.solana.com/tx/{txid}")
            return True
        except asyncio.TimeoutError:
            print("Транзакция не подтверждена в течение 3 секунд.")
            return False

    async def find_transaction_error(self, txid: Signature, client: AsyncClient) -> dict:
        """
        Ищет ошибку в транзакции.
        
        :param txid: Подпись транзакции.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Сведения об ошибке.
        """
        json_response = await client.get_transaction(txid, max_supported_transaction_version=0)
        parsed_response = json.loads(json_response.to_json())["result"]["meta"]["err"]
        return parsed_response

    def get_public_key(self):
        """Возвращает публичный ключ кошелька."""
        return self.keypair.pubkey()

    def __hash__(self):
        """Генерирует хэш на основе публичного ключа кошелька."""
        return hash(self.keypair)

    def __eq__(self, other):
        """Сравнивает кошельки на основе публичного ключа."""
        if not isinstance(other, Wallet):
            return False
        return self.keypair == other.keypair
