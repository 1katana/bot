import asyncio
from solana.rpc.websocket_api import connect


class SolanaWebSocketManager:
    def __init__(self, websocket_url):
        """
        Инициализация с URL WebSocket и функцией-обработчиком сообщений.
        
        :param websocket_url: URL для подключения WebSocket.
        :param message_handler: Функция для обработки сообщений.
        """
        self.websocket_url = websocket_url
        self.websocket = None
        self.subscriptions = {}

    async def connect(self):
        """Устанавливаем WebSocket-соединение"""
        self.websocket = await connect(self.websocket_url)

    async def subscribe_to_account(self, pubkey,callback):
        """Подписка на события аккаунта"""
        await self.websocket.account_subscribe(pubkey)
        
        first_resp = await self.websocket.recv()
        subscription_id = first_resp[0].result
        
        self.subscriptions[subscription_id] = {
            'type': 'account',
            'pubkey': pubkey,
            'handler': callback
        }
        print(f"Подписка на аккаунт {pubkey} активна, ID: {subscription_id}")
        return subscription_id



    async def unsubscribe(self, subscription_id):
        """Отписка от подписки"""
        subscription = self.subscriptions.get(subscription_id)
        if subscription:
            if subscription['type'] == 'account':
                await self.websocket.account_unsubscribe(subscription_id)

            print(f"Отписка от подписки {subscription_id} выполнена.")
            del self.subscriptions[subscription_id]
        else:
            print(f"Подписка с ID {subscription_id} не найдена.")

    async def listen(self):
        """Прослушивание сообщений через WebSocket"""
        try:
            while True:
                message = await self.websocket.recv()
                # Определяем тип подписки по ID
                for subscription_id, subscription in self.subscriptions.items():
                    if subscription['type'] == 'account' and message[0].subscription == subscription_id:
                        await subscription['handler'](message)
                    
        except asyncio.CancelledError:
            print("Отслеживание завершено.")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            await self.close()

    async def close(self):
        """Закрытие WebSocket-соединения"""
        if self.websocket:
            await self.websocket.close()
            print("WebSocket-соединение закрыто.")





