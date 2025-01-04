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
        self.init_wallets()
        
        self.main_token="So11111111111111111111111111111111111111112"
        self.use_token:str

    
    def init_wallets(self):
        if self.wallets is not None:
            # Получаем разницу между текущими и новыми кошельками
            diff = self.wallet_manager.wallets.symmetric_difference(self.wallets)
            # Добавляем недостающие элементы как объекты UseClases
            self.wallets.extend(UseClases(w) for w in diff)
        else:
            # Создаём новый список объектов UseClases
            self.wallets = [UseClases(w) for w in self.wallet_manager.wallets]
            
        self.use_wallets = [wallet for wallet in self.wallets if wallet.is_use]

    
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
  
  
    	
    async def buy_token(self,amount:int):
        
        list_sign_transactions:list[VersionedTransaction]=[]
        
        for wallet in self.use_wallets:
            
            balance= await wallet.wallet.get_balance(self.client)

            
            # НАДО УЧИТЫВАТЬ И ДРУГИЕ КОМИССИИ
            if balance<amount:
                print(f"кошелек {wallet.wallet.get_public_key()} НА СЧЕТУ {balance} lamports не хватает")
                buy_amount=balance-wallet.usepriorityLevelWithMaxLamports
            else:
                buy_amount=amount-wallet.usepriorityLevelWithMaxLamports
                
            print(f"кошелек {wallet.wallet.get_public_key()} покупка на {buy_amount} lamports")
        
        
            quote = await Jupiter.get_swap_quote(self.main_token,self.use_token,buy_amount)

            swap=await Jupiter.swap_tokens(wallet.wallet.keypair,
                                      quote,
                                      priorityLevelWithMaxLamports={"maxLamports": wallet.usepriorityLevelWithMaxLamports,
                                                                    "priorityLevel": "veryHigh"})
            
            sign_trans=await wallet.wallet.sign_transaction_token(swap)
            
            
            # НАДО СПРОСИТЬ ПРОДОЛЖАТЬ ИЛИ НЕТ
            if sign_trans is None:

                print(f"КОШЕЛЕК {wallet.wallet.name} НЕ СМОЖЕТ КУПИТЬ!!!")

            list_sign_transactions.append(sign_trans)
        
        # НАДО ВЫВЕСТИ В ОТДЕЛЬНУЮ ФУНКЦИЮ
        for wallet,transaction in zip(self.use_wallets,list_sign_transactions):
            if transaction is not None:
                signature = await wallet.wallet.send_transaction_token(transaction,self.client)
                wallet.wallet.test_transaction(signature,self.client)
                print(signature)
        
        
        
        
        
        
        
        
