from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
import requests
import json
from solders.keypair import Keypair
import asyncio
from solders.transaction import VersionedTransaction
from wallet import Wallet
from walletManager import WalletManager
from dataclases.utils import UseClases
from typing import List, Tuple
from jupiter import Jupiter


class SolanaManager:
    def __init__(self, client: AsyncClient, wallet_manager: WalletManager):
        self.client = client
        self.wallet_manager = wallet_manager
        self.wallets:list[UseClases]=[]
        self.init_wallets()
        
        self.main_token="So11111111111111111111111111111111111111112"
        self.use_token:str

    
    def init_wallets(self):

        current_wallets = {w.wallet for w in self.wallets} 
        new_wallets = self.wallet_manager.wallets

        # Определяем, какие кошельки нужно добавить
        wallets_to_add = new_wallets - current_wallets
        # Определяем, какие кошельки нужно удалить
        wallets_to_remove = current_wallets - new_wallets

        if self.wallets is not None:
            # Удаляем лишние кошельки
            self.wallets = [wallet for wallet in self.wallets if wallet.wallet not in wallets_to_remove]
            # Добавляем новые кошельки
            self.wallets.extend(UseClases(w) for w in wallets_to_add)
        else:
            # Создаём новый список объектов UseClases
            self.wallets = [UseClases(w) for w in new_wallets]

        self.use_wallets = [wallet for wallet in self.wallets if wallet.is_use]


    
    @classmethod
    async def create(cls, api_url="https://api.mainnet-beta.solana.com", wallets_dir="wallets"):
        client = AsyncClient(api_url)
        wallet_manager =await WalletManager.create(wallets_dir)
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
            await self.wallet_manager.generate_wallet()
        self.init_wallets()
        
    async def add_wallet(self, secret_key:str):
       
        await self.wallet_manager.add_wallet(secret_key=secret_key) 
            
        self.init_wallets()
        
    async def set_master_wallet(self,wallet:Wallet,is_master: bool):
        await self.wallet_manager.set_master_wallet(str(wallet.get_public_key()),is_master)
        self.init_wallets()
        
    async def delete_wallet(self,wallet:Wallet):
        
        await self.wallet_manager.delete_wallet(str(wallet.get_public_key()))
        
        self.init_wallets()
        
    async def load_from_dir(self):
        
        await self.wallet_manager.load_wallets_from_dir()

        self.init_wallets()
        
    async def distribute_funds(self, amount_per_wallet: int = -1):
        """
        Равномерно распределяет средства между кошельками с минимальным количеством переводов
        или распределяет указанное количество средств из мастер-кошельков.

        :param amount_per_wallet: Количество средств для распределения. Если -1, распределяется равномерно.
        """
        try:
            
            # Выбираем активные кошельки
            
            balances = await asyncio.gather(*(wallet.wallet.get_balance(self.client) for wallet in self.use_wallets))
            if not self.use_wallets:
                raise ValueError("Нет активных кошельков для распределения средств.")

            # Если распределяем конкретное количество монет
            if amount_per_wallet > 0:
                master_wallets = [wallet.wallet for wallet in self.use_wallets if wallet.wallet.is_master]
                if not master_wallets:
                    raise ValueError("Нет мастер-кошельков для распределения средств.")

                total_needed = amount_per_wallet * (len(self.use_wallets) - len(master_wallets))
                total_available = sum(wallet.balance for wallet in master_wallets)

                if total_needed > total_available:
                    raise ValueError(f"Недостаточно средств. Необходимо: {total_needed}, доступно: {total_available}.")

                for wallet in self.use_wallets:
                    if wallet.wallet.is_master:
                        continue
                    for master_wallet in master_wallets:
                        if amount_per_wallet == 0:
                            break
                        transfer_amount = min(amount_per_wallet, master_wallet.balance)
                        await master_wallet.transfer_between_wallet(wallet.wallet.keypair.pubkey(), transfer_amount, self.client)
                        amount_per_wallet -= transfer_amount
                        if amount_per_wallet <= 0:
                            break

            # Если распределяем равномерно (-1)
            elif amount_per_wallet == -1:
                
                total_balance = sum(wallet.wallet.balance for wallet in self.use_wallets)
                avg_balance = total_balance // len(self.use_wallets)

                surplus_wallets: list[tuple[Wallet, int]] = []
                deficit_wallets: list[tuple[Wallet, int]] = []

                for wallet in self.use_wallets:
                    balance_diff = wallet.wallet.balance - avg_balance
                    if balance_diff > 0:
                        surplus_wallets.append((wallet, balance_diff))
                    elif balance_diff < 0:
                        deficit_wallets.append((wallet, -balance_diff))

                for surplus_wallet, surplus in surplus_wallets:
                    for deficit_wallet, deficit in deficit_wallets:
                        if surplus == 0:
                            break
                        transfer_amount = min(surplus, deficit)
                        await surplus_wallet.transfer_between_wallet(deficit_wallet.keypair.pubkey(), transfer_amount, self.client)
                        surplus -= transfer_amount
                        deficit -= transfer_amount

            else:
                raise ValueError("Недопустимое значение для 'amount_per_wallet'. Должно быть -1 или больше 0.")

        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")

    async def collect_funds_to_master(self):
        """
        Переводит все монеты с не-мастер-кошельков на мастер-кошельки.

        Исключения:
        - Если нет мастер-кошельков.
        - Если нет доступных кошельков для перевода.
        """
        try:
            # Выбираем активные кошельки
            if not self.use_wallets:
                raise ValueError("Нет активных кошельков для перевода.")

            # Отбираем мастер-кошельки
            master_wallets = [wallet for wallet in self.use_wallets if wallet.wallet.is_master]
            if not master_wallets:
                raise ValueError("Нет мастер-кошельков для получения средств.")

            # Список кошельков для перевода средств (не-мастер)
            non_master_wallets = [wallet for wallet in self.use_wallets if not wallet.wallet.is_master]
            if not non_master_wallets:
                raise ValueError("Нет кошельков с которых можно перевести средства.")

            # Получаем балансы всех не-мастер-кошельков
            balances = await asyncio.gather(
                *(wallet.wallet.get_balance(self.client) for wallet in non_master_wallets)
            )

            for wallet, balance in zip(non_master_wallets, balances):
                if balance > 0:
                    # Распределяем средства по мастер-кошелькам
                    for master_wallet in master_wallets:
                        transfer_amount = balance
                        await wallet.wallet.transfer_between_wallet(
                            master_wallet.wallet.keypair.pubkey(), transfer_amount, self.client
                        )
                        break

        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
    
    
    async def sell_token(self, confirmation_callback,amount:int=-1):
        list_sign_transactions = []

        for wallet in self.use_wallets:
            tokens = await wallet.wallet.get_token_account_by_owner(self.client)
            
            for token in tokens.tokens:
                if token.mint==self.use_token:
                    token_balance=token.token_amount.amount
            
            if token_balance is None:
                print(f"{wallet.wallet.name} Такого токена нет")
            

            print(f"Кошелек {wallet.wallet.get_public_key()} покупает токены на {token_balance} lamports.")

            try:
                quote = await Jupiter.get_swap_quote(              
                    self.use_token,
                    self.main_token,
                    token_balance
                )
                swap = await Jupiter.swap_tokens(
                    wallet.wallet.keypair,
                    quote,
                    priorityLevelWithMaxLamports={
                        "maxLamports": wallet.usepriorityLevelWithMaxLamports,
                        "priorityLevel": "veryHigh"
                    }
                )

                sign_trans = await wallet.wallet.sign_transaction_token(swap)

                if sign_trans is None:
                    print(f"Кошелек {wallet.wallet.name} не смог подписать транзакцию.")
                    if not await confirmation_callback(f"Кошелек {wallet.wallet.name} не смог подписать транзакцию.\n Пропустить кошелек {wallet.wallet.name}?"):
                        print("Прерывание выполнения по запросу пользователя.")
                        return
                    continue

                list_sign_transactions.append((wallet.wallet, sign_trans))
            except Exception as e:
                print(f"Ошибка при обработке кошелька {wallet.wallet.name}: {e}")
                if not await confirmation_callback(f"Ошибка при обработке кошелька {wallet.wallet.name}: {e}\n Пропустить кошелек {wallet.wallet.name} после ошибки?"):
                    print("Прерывание выполнения по запросу пользователя.")
                    return

        # Отправка транзакций
        await self._send_signed_transactions(list_sign_transactions, confirmation_callback)
  
    	
    async def buy_token(self, amount: int, confirmation_callback):
        """
        Метод покупки токенов с подтверждением.

        :param amount: Сумма, на которую нужно купить токены.
        :param confirmation_callback: Функция для подтверждения действия.
        """
        list_sign_transactions = []

        for wallet in self.use_wallets:
            balance = await wallet.wallet.get_balance(self.client)
            
            maximum_commission=wallet.usepriorityLevelWithMaxLamports*3
            
            

            # Учитываем дополнительные комиссии
            if balance < amount + maximum_commission:
                print(f"Кошелек {wallet.wallet.get_public_key()} имеет {balance} lamports, недостаточно средств.")
                buy_amount = balance - maximum_commission
                if buy_amount <= 0:
                    print(f"Кошелек {wallet.wallet.name} не может совершить покупку из-за нехватки SOL.")
                    if not await confirmation_callback(f"Кошелек {wallet.wallet.name} не может совершить покупку из-за нехватки SOL.\n Пропустить кошелек {wallet.wallet.name}?"):
                        print("Прерывание выполнения по запросу пользователя.")
                        return
                    continue
            else:
                buy_amount = amount - maximum_commission

            print(f"Кошелек {wallet.wallet.get_public_key()} покупает токены на {buy_amount} lamports.")

            try:
                quote = await Jupiter.get_swap_quote(
                    self.main_token,
                    self.use_token,
                    buy_amount
                )
                swap = await Jupiter.swap_tokens(
                    wallet.wallet.keypair,
                    quote,
                    priorityLevelWithMaxLamports={
                        "maxLamports": wallet.usepriorityLevelWithMaxLamports,
                        "priorityLevel": "veryHigh"
                    }
                )

                sign_trans = await wallet.wallet.sign_transaction_token(swap)

                if sign_trans is None:
                    print(f"Кошелек {wallet.wallet.name} не смог подписать транзакцию.")
                    if not await confirmation_callback(f"Кошелек {wallet.wallet.name} не смог подписать транзакцию.\n Пропустить кошелек {wallet.wallet.name}?"):
                        print("Прерывание выполнения по запросу пользователя.")
                        return
                    continue

                list_sign_transactions.append((wallet.wallet, sign_trans))
            except Exception as e:
                print(f"Ошибка при обработке кошелька {wallet.wallet.name}: {e}")
                if not await confirmation_callback(f"Ошибка при обработке кошелька {wallet.wallet.name}: {e}\n Пропустить кошелек {wallet.wallet.name} после ошибки?"):
                    print("Прерывание выполнения по запросу пользователя.")
                    return

        # Отправка транзакций
        await self._send_signed_transactions(list_sign_transactions, confirmation_callback)
        
        

    async def _send_signed_transactions(self, signed_transactions: list[tuple[Wallet,VersionedTransaction]], confirmation_callback):
        """
        Отправляет подписанные транзакции и проверяет их статус.

        :param signed_transactions: Список кортежей (кошелек, подписанная транзакция).
        :param confirmation_callback: Функция для подтверждения действия.
        """
        for wallet, transaction in signed_transactions:
            try:
                signature = await wallet.send_transaction_token(transaction, self.client)
                await wallet.test_transaction(signature, self.client)
                print(f"Транзакция для кошелька {wallet.name} успешно отправлена. Signature: {signature}")
            except Exception as e:
                print(f"Ошибка при отправке транзакции для кошелька {wallet.name}: {e}")
                if not await confirmation_callback(f"Ошибка при отправке транзакции для кошелька {wallet.name}: {e}\n Продолжить выполнение после ошибки?"):
                    print("Прерывание выполнения по запросу пользователя.")
                    return

        
        
        
        
async def main():        

    solana_manager = await SolanaManager.create()
    
    await solana_manager.create_wallets(2)
    print(solana_manager.wallets)
        
        
if __name__=="__main__":
    
    asyncio.run(main())