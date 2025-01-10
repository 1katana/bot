from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
import requests
import json
from solders.keypair import Keypair
import asyncio
from solders.transaction import VersionedTransaction
from wallet import Wallet
from walletManager import WalletManager
from dataclases.utils import UseClasses
from typing import List, Tuple
from jupiter import Jupiter
from solana.rpc.providers.async_http import AsyncHTTPProvider
from solders.rpc.requests import GetTokenAccountsByOwner
from solders.rpc.responses import GetTokenAccountsByOwnerJsonParsedResp
from solana.rpc.core import _ClientCore
from solana.rpc.types import TokenAccountOpts
from dataclases.tokensData import TokenInfo,useTokenInfo,TokenAmount
from converter import *


class SolanaManager:
    def __init__(self,api_url: str, client: AsyncClient, wallet_manager: WalletManager):
        

        self.AsyncHTTPProvider=AsyncHTTPProvider(endpoint=api_url)
        
        self.client:AsyncClient=client
        self.clientCore:_ClientCore=_ClientCore(self.client.commitment)
        self.wallet_manager = wallet_manager
        self.wallets:list[UseClasses]=[]
        
        
        self.main_token="So11111111111111111111111111111111111111112"
        
        self.use_token:str=""
        self.decimals:int=None
        
    async def set_use_token(self, use_token: str):
        self.use_token = use_token
        self.decimals=(await self.client.get_token_supply(Pubkey.from_string(use_token))).value.decimals
        print(self.decimals)
    
    async def init_wallets(self):

        current_wallets = {w.wallet for w in self.wallets} 
        new_wallets = self.wallet_manager.wallets

        # Определяем, какие кошельки нужно добавить
        wallets_to_add = new_wallets - current_wallets
        # Определяем, какие кошельки нужно удалить
        wallets_to_remove = current_wallets - new_wallets

        # Удаляем лишнее
        for wallet in self.wallets:
            if wallet.wallet in wallets_to_remove:
                # await wallet.wallet.close_client()
                self.wallets.remove(wallet)
                
        # Добавляем
        for wallet in wallets_to_add:
            # await wallet.init_client(self.api_url)
            self.wallets.append(UseClasses(wallet))



        self.use_wallets = [wallet for wallet in self.wallets if wallet.is_use==True]


    

    
    @classmethod
    async def create(cls, api_url="https://api.mainnet-beta.solana.com", wallets_dir="wallets"):
        
        client=AsyncClient(api_url)
        
        wallet_manager =await WalletManager.create(wallets_dir)
        
        sol_man=cls(api_url,client, wallet_manager)
        
        await sol_man.init_wallets()
        return sol_man

    async def close(self):
        """
        Закрывает соединение с Solana API
        """
        for wallet in self.wallets:
            await wallet.wallet.close_client()
        
        print("Соединение с Solana API закрыто.")

    async def create_wallets(self, num_wallets: int):
        """
        Создает несколько кошельков.
        """
        for _ in range(num_wallets):
            await self.wallet_manager.generate_wallet()
        await self.init_wallets()
        
    async def add_wallet(self, secret_key:str):
       
        await self.wallet_manager.add_wallet(secret_key=secret_key) 
            
        await self.init_wallets()
        
    async def set_master_wallet(self,wallet:Wallet,is_master: bool):
        await self.wallet_manager.set_master_wallet(str(wallet.get_public_key()),is_master)
        await self.init_wallets()
        
    async def delete_wallet(self,wallet:Wallet):
        
        if await self.wallet_manager.delete_wallet(str(wallet.get_public_key())):
            await self.init_wallets()
            return True
        else:
            return False
        

    async def update(self):
        print("\n Загрузка баланса\n ...")
        async def fetch_balance(wallet: UseClasses):
            """Обновляет баланс для одного кошелька."""
            await wallet.wallet.get_balance(self.client)

        async def fetch_token_accounts(wallet: UseClasses):
            """Обновляет токены для одного кошелька."""
            await wallet.wallet.get_token_account_by_owner(self.use_token, self.client)


        await asyncio.gather(*(fetch_balance(w) for w in self.wallets))



        

        for wallet in self.wallets:
            await fetch_token_accounts(wallet)
            await asyncio.sleep(5)  # Задержка между группами
        print("\n Загружено")
        # print([[w.wallet.balance,w.wallet.tokens] for w in self.wallets])
            
        
    async def load_from_dir(self):
        
        await self.wallet_manager.load_wallets_from_dir()

        await self.init_wallets()
        
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
                        await master_wallet.transfer_between_wallet(wallet.wallet.keypair.pubkey(), transfer_amount, )
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
                        surplus_wallets.append((wallet.wallet, balance_diff))
                    elif balance_diff < 0:
                        deficit_wallets.append((wallet.wallet, -balance_diff))

                for surplus_wallet, surplus in surplus_wallets:
                    for deficit_wallet, deficit in deficit_wallets:
                        if surplus == 0:
                            break
                        transfer_amount = min(surplus, deficit)
                        await surplus_wallet.transfer_between_wallet(deficit_wallet.keypair.pubkey(), transfer_amount ,self.client)
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
                        transfer_amount = balance-5000
                        await wallet.wallet.transfer_between_wallet(
                            master_wallet.wallet.keypair.pubkey(), transfer_amount, self.client
                        )
                        break

        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
    
    
    async def sell_token(self, amount,confirmation_callback):     
        # reqs=[]
        # pars=[]
        
        
        # for wallet in self.use_wallets:
            
        #     reqs.append(self.clientCore._get_token_accounts_by_owner_json_parsed_body(wallet.wallet.get_public_key(),
        #                                                                               TokenAccountOpts(mint=Pubkey.from_string("APBcWeYBwkBPMtyEj1QGy1AFzEqnYcQcVYCQofjwpump"),program_id=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")),None))
        #     pars.append(GetTokenAccountsByOwnerJsonParsedResp)
        
        # balances=await self.AsyncHTTPProvider.make_batch_request(tuple(reqs),tuple(pars))

        list_sign_transactions=[]
        
        for i,wallet in enumerate(self.use_wallets):
            
            if amount==-1:
                token = wallet.wallet.use_token_balance.tokenInfo
                
                token_balance=None

                if token.mint==self.use_token:
                    token_balance=token.token_amount.amount
                
                if token_balance is None:
                    print(f"{wallet.wallet.name} Такого токена нет")
                    status=await confirmation_callback(f"Кошелек {wallet.wallet.name} не имеет таких токенов!!!\n Пропустить кошелек {wallet.wallet.name}?")
                    if status:
                        print("Прерывание выполнения по запросу пользователя.")
                        return
                    continue
            else:
                token_balance=amount
            

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
                    status=await confirmation_callback(f"Кошелек {wallet.wallet.name} не смог подписать транзакцию.\n Пропустить кошелек {wallet.wallet.name}?")
                    if status:
                        print("Прерывание выполнения по запросу пользователя.")
                        return
                    continue

                list_sign_transactions.append((wallet.wallet, sign_trans))
            except Exception as e:
                print(f"Ошибка при обработке кошелька {wallet.wallet.name}: {e}")
                status=confirmation_callback(f"Ошибка при обработке кошелька {wallet.wallet.name}: {e}\n Пропустить кошелек {wallet.wallet.name} после ошибки?")
                if status:    
                    print("Прерывание выполнения по запросу пользователя.")
                    return

        # Отправка транзакций
        await self._send_signed_transactions(list_sign_transactions)
  
    	
    async def buy_token(self, amount: int, confirmation_callback):
        """
        Метод покупки токенов с подтверждением.

        :param amount: Сумма, на которую нужно купить токены.
        :param confirmation_callback: Функция для подтверждения действия.
        """
        list_sign_transactions = []

        for wallet in self.use_wallets:
            try:
                # Получение баланса кошелька
                balance = await wallet.wallet.get_balance(self.client)
            except Exception:
                print(Exception)
                return

            # Запрос первой и второй котировок для расчетов
            try:
                
                quote_to_reverse = await Jupiter.get_swap_quote(
                    self.use_token,
                    self.main_token,
                    amount
                )
                quote_to_buy = await Jupiter.get_swap_quote(
                    self.main_token,
                    self.use_token,
                    amount
                )

                print("outAmount: ",quote_to_buy["routePlan"][-1]["swapInfo"]["outAmount"])
            except Exception as e:
                print(f"Ошибка получения котировок для кошелька {wallet.wallet.name}: {e}")
                continue

            # Суммируем комиссии из обоих запросов
            route_commission_to_buy = sum(
                int(swap['swapInfo']['feeAmount']) for swap in quote_to_buy['routePlan']
            )
            route_commission_to_reverse = sum(
                int(swap['swapInfo']['feeAmount']) for swap in quote_to_reverse['routePlan']
            )

            # Расчет максимальной комиссии
            maximum_commission = (wallet.usepriorityLevelWithMaxLamports + 5000) * 2 + route_commission_to_buy + route_commission_to_reverse

            # Проверка наличия средств
            if balance < amount + maximum_commission:
                print(f"Кошелек {wallet.wallet.get_public_key()} имеет {balance} lamports, недостаточно средств.")
                buy_amount = balance - maximum_commission
                if buy_amount <= 0:
                    print(f"Кошелек {wallet.wallet.name} не может совершить покупку из-за нехватки SOL.")
                    status=await confirmation_callback(
                            f"Кошелек {wallet.wallet.name} не может совершить покупку из-за нехватки SOL.\n"
                            f"Пропустить кошелек {wallet.wallet.name}?")
                        
                    if status:
                        print("Прерывание выполнения по запросу пользователя.")
                        return
                    continue
            else:
                buy_amount = amount + maximum_commission

            print(f"Кошелек {wallet.wallet.get_public_key()} покупает токены на {buy_amount} lamports.")

            try:
                if amount!=buy_amount:

                    quote_to_buy = await Jupiter.get_swap_quote(
                        self.main_token,
                        self.use_token,
                        buy_amount
                    )

                # Использование первой котировки для операции
                swap = await Jupiter.swap_tokens(
                    wallet.wallet.keypair,
                    quote_to_buy,
                    priorityLevelWithMaxLamports={
                        "maxLamports": wallet.usepriorityLevelWithMaxLamports,
                        "priorityLevel": "veryHigh"
                    }
                )

                # Подписание транзакции
                sign_trans = await wallet.wallet.sign_transaction_token(swap)

                if sign_trans is None:
                    print(f"Кошелек {wallet.wallet.name} не смог подписать транзакцию.")
                    status =confirmation_callback(
                            f"Кошелек {wallet.wallet.name} не смог подписать транзакцию.\n"
                            f"Пропустить кошелек {wallet.wallet.name}?")
                        
                    if status:
                        print("Прерывание выполнения по запросу пользователя.")
                        return
                    continue

                list_sign_transactions.append((wallet.wallet, sign_trans))
            except Exception as e:
                print(f"Ошибка при обработке кошелька {wallet.wallet.name}: {e}")
                status = await confirmation_callback(
                        f"Ошибка при обработке кошелька {wallet.wallet.name}: {e}\n"
                        f"Пропустить кошелек {wallet.wallet.name} после ошибки?")
                if status:
                    print("Прерывание выполнения по запросу пользователя.")
                    return

        # Отправка подписанных транзакций
        await self._send_signed_transactions(list_sign_transactions,quote_to_buy=quote_to_buy)

        
        

    async def _send_signed_transactions(self,signed_transactions: list[tuple[Wallet, VersionedTransaction]],quote_to_buy: dict=None):
        """
        Отправляет подписанные транзакции и проверяет их статус.

        :param signed_transactions: Список кортежей (кошелек, подписанная транзакция).
        :param confirmation_callback: Функция для подтверждения действия.
        """
        async def process_transaction(wallet:Wallet, transaction:VersionedTransaction):
            try:
                signature = await wallet.send_transaction_token(transaction,self.client)
                if signature is not None:
                    print(f"Транзакция для кошелька {wallet.name} отправлена. Signature: {signature}")
                # Проверка транзакции
                if await wallet.test_transaction(signature,self.client) and quote_to_buy is not None:
                    amount=int(quote_to_buy["routePlan"][-1]["swapInfo"]["outAmount"])
                    ui_amount=token_units_to_amount(amount,self.decimals)
                    wallet.use_token_balance=useTokenInfo(False,
                                                          tokenInfo=TokenInfo(self.use_token,
                                                                              TokenAmount(amount,
                                                                                          self.decimals,
                                                                                          ui_amount,str(ui_amount))))

                    
            except Exception as e:
                print(f"Ошибка при обработке транзакции для кошелька {wallet.name}: {e}")


        print("\n ОТПРАВКА")
        # Создание задач для всех транзакций
        tasks = [asyncio.create_task(process_transaction(wallet, transaction)) for wallet, transaction in signed_transactions]

        # Ожидание выполнения всех задач
        await asyncio.gather(*tasks)

        
        
async def console_confirmation(message: str) -> bool:
    user_input = input(f"{message} (y/n): ").strip().lower()
    return user_input in {"y", "yes"}       
        
async def main():        

    solana_manager = await SolanaManager.create()
    
    # await solana_manager.create_wallets(3)
    print(solana_manager.wallets)
    solana_manager.use_token="7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr"
    
    for w in solana_manager.use_wallets:
        print(w.wallet.name)
        print(w.wallet.get_public_key())
        print(await w.wallet.get_balance(solana_manager.client))
        # if w.wallet.name=="wallet1":
        #     if w.wallet.name=="wallet1":
        #         w.wallet.is_master=True
        #     continue
        # w.is_use=False
        
    # await solana_manager.init_wallets()
    
    # await solana_manager.collect_funds_to_master()
    # await solana_manager.distribute_funds()
    # await solana_manager.buy_token(15_000_000,console_confirmation)
    await solana_manager.sell_token(console_confirmation)
    
        
    print()
        
        
if __name__=="__main__":
    
    asyncio.run(main())