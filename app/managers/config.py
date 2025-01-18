import os
import json


class Config:
    CONFIG_FILE = "config.json"

    def __init__(self):
        # Определяем начальные значения
        self.jupiter_url = "https://quote-api.jup.ag/v6"
        self.dynamic_slippage = {"dynamicSlippage": {"maxBps": 2000}}
        self.auto_slippage = "False"
        self.wallets_dir = "save_wallets"
        self.api_key = "https://api.mainnet-beta.solana.com/"
        self.primary_mint:str|None = None
        self.sol_mint = "So11111111111111111111111111111111111111112"

        # Указываем атрибуты, которые нужно сохранять и загружать
        self._tracked_attributes = [
            "jupiter_url",
            "dynamic_slippage",
            "auto_slippage",
            "wallets_dir",
            "api_key",
            "primary_mint",
            "sol_mint",
        ]

        self.load_config()

    def load_config(self):
        """Загружает конфигурацию из файла."""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as file:
                    data = json.load(file)
                    for key in self._tracked_attributes:
                        if key in data:
                            setattr(self, key, data[key])
            except Exception as e:
                print(f"Ошибка при загрузке конфигурации: {e}")

    def save_config(self):
        """Сохраняет текущую конфигурацию в файл."""
        try:
            data = {key: getattr(self, key) for key in self._tracked_attributes}
            with open(self.CONFIG_FILE, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении конфигурации: {e}")