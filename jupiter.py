import requests
from solders.keypair import Keypair # type: ignore
import json
import aiohttp
from typing import Optional


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
    async def get_swap_quote(cls, input_mint: str, output_mint: str, amount: int) -> Optional[dict]:
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

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Error fetching quote: {response.status} {await response.text()}")
                        return None
            except aiohttp.ClientError as e:
                print(f"Request failed: {e}")
                return None
        
    @classmethod
    async def swap_tokens(cls, sender_keypair: Keypair, quote_response: dict, prioritizationFeeLamports=0, 
                          priorityLevelWithMaxLamports=None) -> Optional[dict]:
        """
        Perform a token swap.

        :param sender_keypair: The sender's Keypair.
        :param quote_response: The response with quote details.
        :param prioritizationFeeLamports: Priority fee in lamports.
        :param priorityLevelWithMaxLamports: A dict specifying priority level and max lamports, e.g., 
                                            {maxLamports: 4000000, global: false, priorityLevel: "veryHigh"}.
        :return: The transaction response as a dictionary, or None if an error occurs.
        """

        url = f"{cls.BASE_URL}{cls.SWAP_ENDPOINT}"
        pubkey = sender_keypair.pubkey()

        # Base payload for the request
        payload = {
            "userPublicKey": str(pubkey),
            "quoteResponse": quote_response,
            "wrapAndUnwrapSol": True,
            "dynamicSlippage": {"maxBps": 1000},
            "dynamicComputeUnitLimit":True

        }

        # Add prioritization parameters based on input
        if priorityLevelWithMaxLamports:
            payload["prioritizationFeeLamports"] = {"priorityLevelWithMaxLamports": priorityLevelWithMaxLamports } 
        else:
            payload["prioritizationFeeLamports"] = prioritizationFeeLamports

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Error creating swap transaction: {response.status} {await response.text()}")
                        return None
            except aiohttp.ClientError as e:
                print(f"Request failed: {e}")
                return None


        

if __name__ == "__main__":
    result = Jupiter.get_swap_quote(
        input_mint="So11111111111111111111111111111111111111112",
        output_mint="AftybCzh88UzM1T435SDJPZ1vhYuJYfh9uJA8sTpump",
        amount=1000000000
    )
    print(result)