from solders.keypair import Keypair # type: ignore
from solders.system_program import TransferParams, transfer
from solders.message import MessageV0 # type: ignore
from solders.transaction import VersionedTransaction # type: ignore
from solders.pubkey import Pubkey # type: ignore
from solana.rpc.async_api import AsyncClient
from jupiter import Jupiter
import base64
from solders.pubkey import Pubkey # type: ignore
from solana.rpc.types import TxOpts
from solders.signature import Signature # type: ignore
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
        Инициализация кошелька с заданной парой ключей, именем и флагом,
        указывающим, является ли кошелек главным.
        
        :param keypair: Пара ключей для кошелька.
        :param name: Имя кошелька.
        :param is_master: Флаг, указывающий, является ли кошелек главным.
        """
        try:
            self.name = name
            self.keypair = keypair
            self.is_master = is_master
            self.balance: int = 0
            self.tokens: TokensData = None
            
        except Exception as e:
            print(f"Ошибка при инициализации кошелька: {e}")
            

    async def get_token_account_by_owner(self,client:AsyncClient) -> TokensData:
        """
        Получение токен-аккаунтов, принадлежащих владельцу этого кошелька.
        
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Список токен-аккаунтов.
        """

        # try:
        tokens_not_pars = await client.get_token_accounts_by_owner_json_parsed(
            self.keypair.pubkey(),
            TokenAccountOpts(program_id=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"))
        )
        
        



        self.tokens = parse_rpc_response(tokens_not_pars)
        # await asyncio.sleep(2)  # Задержка 100 мс
        
        return self.tokens
        # except Exception as e:
        #     print(f"Ошибка при получении токен-аккаунтов: {e}")
        

    async def get_token_account_balance(self,client:AsyncClient):
        """
        Получение баланса токен-аккаунта кошелька.
        
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Баланс токен-аккаунта.
        """
        try:
            return await client.get_token_account_balance(self.keypair.pubkey())
        except Exception as e:
            print(f"Ошибка при получении баланса токен-аккаунта: {e}")

    async def get_account_info(self,client:AsyncClient):
        """
        Получение информации об аккаунте кошелька.
        
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Информация об аккаунте.
        """
        try:
            return await client.get_account_info(self.keypair.pubkey())
        except Exception as e:
            print(f"Ошибка при получении информации об аккаунте: {e}")

    async def get_balance(self,client:AsyncClient) -> int:
        """
        Получение общего баланса SOL кошелька.
        
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Баланс в лампортах.
        """
        try:
            balance = await client.get_balance(self.keypair.pubkey())
            self.balance = balance.value
            return self.balance
        except Exception as e:
            print(f"Ошибка при получении баланса кошелька: {e}")

    async def get_latest_blockhash(self,client:AsyncClient):
        """
        Получение последнего блокхеша для выполнения транзакций.
        
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Последний блокхеш.
        """
        try:
            return await client.get_latest_blockhash()
        except Exception as e:
            print(f"Ошибка при получении последнего блокхеша: {e}")

    @measure_time
    async def transfer_token(self, quote_response,client:AsyncClient):
        """
        Осуществление обмена токенов по заданному котировочному ответу.
        
        :param quote_response: Ответ с котировкой для обмена токенов.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Результат выполнения транзакции.
        """
        try:
            transaction_data = await Jupiter.swap_tokens(self.keypair, quote_response)
            swap_transaction = transaction_data['swapTransaction']
            decoded_swap_transaction = base64.b64decode(swap_transaction)
            signed_txn = await self.sign_transaction_token(decoded_swap_transaction)
            opts = TxOpts(
                skip_preflight=False,
                preflight_commitment="confirmed",
                max_retries=3,
            )
            return await self.send_transaction_token(signed_txn,client, opts)
        except Exception as e:
            print(f"Ошибка при обмене токенов: {e}")

    
    @measure_time
    async def transfer_between_wallet(self, receiver: Pubkey, lamports: int,client:AsyncClient):
        """
        Перевод SOL на указанный адрес.
        
        :param receiver: Публичный ключ получателя.
        :param lamports: Сумма в лампортах для перевода.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Результат выполнения транзакции.
        """
        try:
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
        except Exception as e:
            print(f"Ошибка при переводе SOL: {e}")

    @measure_time
    async def send_transaction_between_wallet(self, txn: VersionedTransaction,client:AsyncClient):
        """
        Отправка указанной транзакции.
        
        :param txn: Транзакция для отправки.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Подпись транзакции.
        """
        try:
            return await client.send_transaction(txn)
        except Exception as e:
            print(f"Ошибка при отправке транзакции: {e}")

    @measure_time
    async def sign_transaction_token(self, transaction_data: dict):
        """
        Подписание транзакции токена.
        
        :param transaction_data: Сырые данные транзакции.
        :return: Подписанная транзакция.
        """
        try:
            swap_transaction = transaction_data['swapTransaction']
            decoded_swap_transaction = base64.b64decode(swap_transaction)
            raw_txn = VersionedTransaction.from_bytes(decoded_swap_transaction)
            signature = self.keypair.sign_message(message.to_bytes_versioned(raw_txn.message))
            signed_txn = VersionedTransaction.populate(raw_txn.message, [signature])
            return signed_txn
        except Exception as e:
            print(f"Ошибка при подписании транзакции токена: {e}")

    @measure_time
    async def send_transaction_token(self, signed_txn: VersionedTransaction,client:AsyncClient, opts: TxOpts = TxOpts(
        skip_preflight=False,
        preflight_commitment="confirmed",
        # max_retries=2,
    )) -> Signature:
        """
        Отправка транзакции токена с учетом приоритизации и дополнительных опций.
        
        :param signed_txn: Подписанная транзакция.
        :param opts: Опции выполнения транзакции.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Подпись транзакции.
        """
        try:
            result = await client.send_raw_transaction(bytes(signed_txn), opts)

            return result.value
        except Exception as e:
            print(f"Ошибка при отправке транзакции токена: {e}")

    async def test_transaction(self, txid: Signature,client:AsyncClient):
        """
        Тестирует транзакцию на подтверждение в сети.
        
        :param txid: Подпись транзакции.
        :param client: Асинхронный клиент для взаимодействия с блокчейном.
        :return: Подтверждение успешности транзакции.
        """
        print(f"Transaction: https://solscan.io/tx/{txid}")
        print("Ожидание подтверждения...")

        try:
            await asyncio.wait_for(client.confirm_transaction(txid, commitment="confirmed", sleep_seconds=1), timeout=10)
            print(f"Подтверждена: https://solscan.io/tx/{txid}")
            return True
        except asyncio.TimeoutError:
            print("Транзакция не подтверждена в течение 10 секунд.")
            return False

    async def find_transaction_error(self, txid: Signature,client:AsyncClient) -> dict:
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
