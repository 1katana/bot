from solders.keypair import Keypair
from solders.system_program import TransferParams, transfer
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from transaction import Transaction_between_wallets
from jupiter import Jupiter
from solders.message import MessageV0
import base64
from solders.pubkey import Pubkey
from solana.rpc.types import TxOpts
from solana.rpc.core import RPCException
from solders.transaction import VersionedTransaction
from solders.signature import Signature
from solders import message
import json
from solana.rpc.types import TokenAccountOpts


class Wallet:
    def __init__(self, keypair: Keypair, name: str, is_master=False):
        self.name = name
        self.keypair = keypair
        self.is_master = is_master

    
    async def get_token_account_by_owner(self,client: AsyncClient):
        tokens=await client.get_token_accounts_by_owner(self.keypair.pubkey(),
                                                        TokenAccountOpts(program_id=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")))
        return tokens
    
    async def get_token_account_balance(self,client: AsyncClient):
        balance = await client.get_token_account_balance(self.keypair.pubkey())
        return balance
    
    async def get_account_info(self,client: AsyncClient):
        info = await client.get_account_info(self.keypair.pubkey())
        return info

    async def get_balance(self, client: AsyncClient):
        """Получает баланс кошелька."""
        balance = await client.get_balance(self.keypair.pubkey())
        return balance



    async def get_latest_blockhash(self, client: AsyncClient):
        return await client.get_latest_blockhash()
    
    
    
    
    async def get_quote_token(self, input_mint: str, output_mint: str, amount: int):
        return Jupiter.get_swap_quote(input_mint, output_mint,amount)
    
    
    
    async def transfer_token(self, quote_response, client: AsyncClient):
        """Транзакция с токенами"""
        
        transaction_data=Jupiter.swap_tokens(self.keypair,quote_response)
        
        # print(transaction_data)
        # Извлечение данных
        swap_transaction = transaction_data['swapTransaction']
        last_valid_block_height = transaction_data['lastValidBlockHeight']
        prioritization_fee_lamports = transaction_data['prioritizationFeeLamports']
        compute_unit_limit = transaction_data['computeUnitLimit']
        prioritization_type = transaction_data['prioritizationType']

        # Декодирование swapTransaction
        decoded_swap_transaction = base64.b64decode(swap_transaction)

        # Вывод данных
        print(f"Swap Transaction: {decoded_swap_transaction}")
        print(f"Last Valid Block Height: {last_valid_block_height}")
        print(f"Prioritization Fee Lamports: {prioritization_fee_lamports}")
        print(f"Compute Unit Limit: {compute_unit_limit}")
        print(f"Prioritization Type: {prioritization_type}")
        
        tx_opts = TxOpts(
            # skip_confirmation=False,  # Ожидаем подтверждения
            skip_preflight=False,  # Не пропускаем предварительный полет
            preflight_commitment="confirmed",
            max_retries=3,  # Максимальное количество попыток
            # last_valid_block_height=last_valid_block_height
        )
        
        
        
        txn= await self.send_transaction_new(swap_transaction=decoded_swap_transaction,
                              opts=tx_opts,
                              client=client)
        
        ans = await self.find_transaction_error(txid=txn,client=client)
        
        print(ans)
            
            

    async def transfer_between_wallet(self, receiver: Pubkey, lamports: int, client: AsyncClient):
        """Отправляет SOL на указанный адрес."""
        blockhash = await self.get_latest_blockhash(client)
        txn = Transaction_between_wallets(sender=self.keypair, receiver=receiver, lamports=lamports, blockhash=blockhash.value.blockhash)
        return await self.send_transaction(txn, client)


    async def send_transaction(self, txn: VersionedTransaction, client: AsyncClient):
        return await client.send_transaction(txn)

    
    async def send_transaction_new(self,swap_transaction: str, opts: TxOpts,client: AsyncClient) -> Signature:
        raw_txn = VersionedTransaction.from_bytes(swap_transaction)
        

        
        signature = self.keypair.sign_message(message.to_bytes_versioned(raw_txn.message))
        
        signed_txn = VersionedTransaction.populate(raw_txn.message, [signature])

        result = await client.send_raw_transaction(bytes(signed_txn), opts)
        txid = result.value
        print(f"Transaction: https://explorer.solana.com/tx/{txid}")
        print("Ожидание подтверждения...")
        с=await client.confirm_transaction(txid, commitment="confirmed",sleep_seconds=1)
        print(f"Подвержден: https://explorer.solana.com/tx/{txid}")
        return txid
    
    async def find_transaction_error(self,txid: Signature,client: AsyncClient) -> dict:
        json_response =  await client.get_transaction(txid, max_supported_transaction_version=0)
        json_response=json_response.to_json()
        parsed_response = json.loads(json_response)["result"]["meta"]["err"]
        return parsed_response


    def get_public_key(self):
        """Возвращает публичный ключ кошелька."""
        return self.keypair.pubkey()


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