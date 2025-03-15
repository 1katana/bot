import aiohttp
import asyncio
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal
from aiohttp import FormData
import requests
from PIL import Image
import io
from app.dataclases.utils import UseClasses
from typing import List
import base58
from solders.signature import Signature

@dataclass
class TokenCreator:
    def __init__(self, mint:Keypair, sign:List[Signature],dev_wallet:UseClasses,transactions: List[str]):
        self.mint = mint
        self.transactions=transactions
        self.dev_wallet = dev_wallet
        self.sign=sign

class PumpFunTokenCreator(QObject):
    tokenDataChanged = Signal(dict)  
    validMetadataChanged = Signal(dict)

    def __init__(self, api_url: str):
        """
        Инициализирует объект TokenCreator с API URL.

        :param api_url: URL API для взаимодействия с сервисом.
        """
        super().__init__()
        self.api_url = api_url
        self.tokenCreator: TokenCreator = None
        self._token_data = {
            "name": "",
            "symbol": "",
            "description": "",
            "social_links": {
                "twitter": "",
                "telegram": "",
                "website": ""
            },
            "image_path": None
        }
        
        self._valid_metadata: dict | None = None

    @property
    def valid_metadata(self):
        """Возвращает метаданные токена."""
        return self._valid_metadata

    @valid_metadata.setter
    def valid_metadata(self, value: dict | None):
        """Устанавливает метаданные и эмитирует сигнал об изменении."""
        if self._valid_metadata != value:
            self._valid_metadata = value
            # Эмитируем сигнал, что метаданные изменились
            self.validMetadataChanged.emit(self._valid_metadata)
        

    async def validate_token_metadata(self, name: str, symbol: str, description: str, image_path: str, social_links: dict) -> dict | None:
        """
        Проверяет возможность использования изображения и метаданных токена.

        :param name: Название токена.
        :param symbol: Символ токена.
        :param description: Описание токена.
        :param image_path: Путь к изображению.
        :param social_links: Ссылки на социальные сети.
        :return: Словарь с метаданными (включая ссылку на IPFS) или None при ошибке.
        """
        metadata = {
            'name': name,
            'symbol': symbol,
            'description': description,
            'twitter': social_links.get('twitter', ''),
            'telegram': social_links.get('telegram', ''),
            'website': social_links.get('website', ''),
            'showName': 'true'
        }

        metadata_response_json = await self._upload_image_to_ipfs(image_path, metadata)
        if metadata_response_json is None:
            return None

        self.valid_metadata={
            'name': name,
            'symbol': symbol,
            'uri': metadata_response_json['metadataUri']
        }
        
        return self.valid_metadata

    async def _upload_image_to_ipfs(self, image_path: str, metadata: dict):
        """
        Асинхронно загружает изображение на IPFS.

        :param image_path: Путь к файлу изображения.
        :param metadata: Метаданные, которые передаются с изображением.
        :return: JSON-ответ с данными об изображении или None при ошибке.
        """
        # Уменьшаем размер изображения
        image = Image.open(image_path)
        image.thumbnail((800, 800))  
        output = io.BytesIO()
        image.save(output, format='PNG')
        file_content = output.getvalue()

        name = image_path.split('/')[-1]

        # Формируем multipart данные
        data = aiohttp.FormData()
        data.add_field('file', file_content, filename=name, content_type='image/png')

        for key, value in metadata.items():
            data.add_field(key, value)

        # Асинхронный запрос
        async with aiohttp.ClientSession() as session:
            async with session.post("https://pump.fun/api/ipfs", data=data) as response:
                if response.status != 200:
                    print(f"Ошибка загрузки изображения на IPFS: {response.status}")
                    req=await response.text()
                    if "The owner of this website (pump.fun) has banned the country or region your IP address is in (RU) from accessing this website." in req:
                        print("The owner of this website (pump.fun) has banned the country or region your IP address is in (RU) from accessing this website.")
                    else:
                        print(req)
                    return None
                return await response.json()

    def _generate_token_keypair(self):
        """
        Генерирует новую пару ключей для токена.
        :return: Объект Keypair.
        """
        return Keypair()

    async def create_token_transaction(self, signer_keypairs:List[UseClasses], create_amount=1000000,buy_amount=1000000, priority_fee=0.0005) -> TokenCreator | None:
        """
        Создает `VersionedTransaction` для выпуска токена.

        :param signer_keypair: Ключ подписывающего.
        :param token_metadata: Проверенные метаданные токена.
        :param amount: Количество токенов.
        :param priority_fee: Приоритетная комиссия.
        :return: Объект TokenCreator или None при ошибке.
        """
        if not self.valid_metadata:
            print("Ошибка: переданы некорректные метаданные.")
            return None

        mint_keypair = self._generate_token_keypair()
        
        
        
        dev_wallet:UseClasses = None
        
        for wal in signer_keypairs:
            if wal.wallet.is_master:
                dev_wallet=wal
                
        if dev_wallet==None:
            print("Нету Master кошелька")
            return None
        else:
            print("dev wallet: ",dev_wallet.wallet.keypair.pubkey())
            
        

        bundled_transaction_args = [
            {
                'publicKey': str(dev_wallet.wallet.keypair.pubkey()),
                'action': 'create',
                'tokenMetadata': self.valid_metadata,
                'mint': str(mint_keypair.pubkey()),
                'denominatedInSol': 'false',
                'amount': create_amount,
                'slippage': 10,
                'priorityFee': priority_fee,
                'pool': 'pump'
            }
        ]
        
        for wal in signer_keypairs:
            if wal!=dev_wallet:
                
                bundled_transaction_args.append({
                    'publicKey': str(wal.wallet.keypair.pubkey()),
                    'action': "buy",
                    'mint': str(mint_keypair.pubkey()),
                    'denominatedInSol': 'false',
                    'amount': buy_amount,
                    'slippage': 50,
                    'pool': 'pump'
                })

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_url}/api/trade-local",
                json=bundled_transaction_args
            ) as response:
                if response.status != 200:
                    print("Ошибка при генерации транзакции.")
                    return None

                encodedTransactions = await response.json()
                encodedSignedTransactions = []
                txSignatures = []

                try:
                    for index, encodedTransaction in enumerate(encodedTransactions):
                        if bundled_transaction_args[index]["action"] == "create":
                            signedTx = VersionedTransaction(VersionedTransaction.from_bytes(base58.b58decode(encodedTransaction)).message, [mint_keypair, signer_keypairs[index].wallet.keypair])
                        else:
                            signedTx = VersionedTransaction(VersionedTransaction.from_bytes(base58.b58decode(encodedTransaction)).message, [signer_keypairs[index].wallet.keypair])
                        
                        encodedSignedTransactions.append(base58.b58encode(bytes(signedTx)).decode('ascii'))
                        txSignatures.append(signedTx.signatures[0])


                    self.tokenCreator = TokenCreator(mint_keypair, 
                                                     txSignatures,
                                                     dev_wallet=dev_wallet,
                                                     transactions=encodedSignedTransactions)
                    print("TOKEN: ",mint_keypair.pubkey())
                    
                    return self.tokenCreator
                except Exception as e:
                    print(f"Ошибка при создании объекта VersionedTransaction: {e}")
                    return None
                
    @property
    def token_data(self) -> dict:
        """Возвращает сохраненные данные токена."""
        return self._token_data

    @token_data.setter
    def token_data(self, value: dict):
        """Устанавливает новые данные токена и уведомляет об изменении."""
        if self._token_data != value:
            self._token_data = value
            
            self.valid_metadata=None
            
            self.tokenDataChanged.emit(value)  # Уведомляем об изменении