import requests
from solders.keypair import Keypair
import json


class Jupiter:
    BASE_URL = "https://quote-api.jup.ag/v6"
    QUOTE_ENDPOINT = "/quote"
    SWAP_ENDPOINT="/swap"

    @classmethod
    def set_url(cls, url: str):
        """
        Устанавливает новый базовый URL для класса.

        :param url: Новый базовый URL.
        """
        cls.BASE_URL = url

    @classmethod
    def get_swap_quote(cls, input_mint: str, output_mint: str, amount: int) -> dict | None: 
        """
        Получает котировку для обмена между двумя токенами.

        :param input_mint: Адрес входного токена.
        :param output_mint: Адрес выходного токена.
        :param amount: Количество входного токена для обмена.
        :return: JSON-ответ с котировкой или None в случае ошибки.
        """
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount,
            "autoSlippage": "true",
            
        }

        url = f"{cls.BASE_URL}{cls.QUOTE_ENDPOINT}"


        response = requests.get(url=url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching quote: {response.text}")
            return None
        
    @classmethod
    def swap_tokens(cls,sender_keypair: Keypair, quote_response: dict):

        url = f"{cls.BASE_URL}{cls.SWAP_ENDPOINT}"
        
        pubkey=sender_keypair.pubkey()
        # Параметры для запроса
        payload = json.dumps({
            "userPublicKey": str(pubkey),
            "quoteResponse": quote_response,
            "wrapUnwrapSOL": True,
            "computeUnitPriceMicroLamports": 20 * 14000  # fee of roughly $.04  :shrug:

        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Отправка POST-запроса
        response = requests.request("POST", url, headers=headers, data=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error creating swap transaction: {response.text}")
            return None
        

if __name__ == "__main__":
    result = Jupiter.get_swap_quote(
        input_mint="So11111111111111111111111111111111111111112",
        output_mint="AftybCzh88UzM1T435SDJPZ1vhYuJYfh9uJA8sTpump",
        amount=1000000000
    )
    print(result)