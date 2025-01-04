class SolanaManager:
    def __init__(self, client: AsyncClient, wallet_manager: WalletManager, main_token: str):
        """
        Инициализирует менеджер для управления кошельками и взаимодействия с Solana.
        
        :param client: Асинхронный клиент для работы с Solana API.
        :param wallet_manager: Менеджер для управления кошельками.
        :param main_token: Основной токен (SOL) для операций.
        """
        self.client = client
        self.wallet_manager = wallet_manager
        self.main_token = main_token

    @classmethod
    async def create(cls, main_token: str, api_url="https://api.mainnet-beta.solana.com", wallets_dir="wallets"):
        """
        Создает экземпляр SolanaManager.
        
        :param main_token: Основной токен (SOL).
        :param api_url: URL Solana API.
        :param wallets_dir: Директория для хранения кошельков.
        :return: Экземпляр SolanaManager.
        """
        client = AsyncClient(api_url)
        wallet_manager = WalletManager(wallets_dir)
        return cls(client, wallet_manager, main_token)

    async def close(self):
        """
        Закрывает соединение с Solana API.
        """
        await self.client.close()
        print("Соединение с Solana API закрыто.")

    async def distribute_funds(self, master_wallet_name: str, total_amount: int, add_noise: bool = False, noise_range: tuple = (0, 0)):
        """
        Распределяет монеты равномерно между кошельками с возможностью добавления шума.
        
        :param master_wallet_name: Имя мастер-кошелька.
        :param total_amount: Общая сумма, которую нужно распределить.
        :param add_noise: Флаг добавления шума.
        :param noise_range: Диапазон шума (минимум, максимум).
        """
        master_wallet = self.wallet_manager.get_wallet(master_wallet_name)
        if not master_wallet or not master_wallet.is_master:
            print(f"Кошелек {master_wallet_name} не является мастер-кошельком.")
            return

        wallets = [wallet for wallet in self.wallet_manager.wallets if wallet != master_wallet]
        num_wallets = len(wallets)
        if num_wallets == 0:
            print("Нет кошельков для распределения.")
            return

        base_amount = total_amount // num_wallets

        for wallet in wallets:
            amount = base_amount
            if add_noise:
                noise = random.randint(*noise_range)
                amount += noise

            # Создание и отправка транзакции
            transaction = await master_wallet.transfer_between_wallet(wallet.get_public_key(), amount, self.client)
            await master_wallet.send_transaction_between_wallet(transaction, self.client)

    async def perform_parallel_token_action(self, input_mint: str, output_mint: str, amount: int, action: str):
        """
        Одновременная покупка или продажа токенов со всех кошельков.
        
        :param input_mint: Адрес токена ввода.
        :param output_mint: Адрес токена вывода.
        :param amount: Количество токенов для покупки/продажи.
        :param action: Действие ("buy" или "sell").
        """
        async def handle_wallet(wallet):
            quote_response = await Jupiter.get_quote_token(input_mint, output_mint, amount)
            if action == "buy":
                await wallet.transfer_token(quote_response, self.client)
            elif action == "sell":
                await wallet.transfer_token(quote_response, self.client)

        await asyncio.gather(*[handle_wallet(wallet) for wallet in self.wallet_manager.wallets])

    async def buy_tokens_in_cycle(self, input_mint: str, output_mint: str, amount: int):
        """
        Одновременная покупка токенов с нескольких кошельков.
        
        :param input_mint: Адрес токена ввода.
        :param output_mint: Адрес токена вывода.
        :param amount: Количество токенов для покупки.
        """
        await self.perform_parallel_token_action(input_mint, output_mint, amount, action="buy")

    async def sell_tokens_in_cycle(self, input_mint: str, output_mint: str, amount: int):
        """
        Одновременная продажа токенов с нескольких кошельков.
        
        :param input_mint: Адрес токена ввода.
        :param output_mint: Адрес токена вывода.
        :param amount: Количество токенов для продажи.
        """
        await self.perform_parallel_token_action(input_mint, output_mint, amount, action="sell")
