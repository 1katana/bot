import os
import json

import os
import json
from app.utils.converter import *

class Config:
    CONFIG_FILE = "config.json"

    def __init__(self):
        # urls
        self._jupiter_url = "https://api.jup.ag/swap/v1"
        self._jito_url = "https://mainnet.block-engine.jit"
        self._pump_fun_url = "https://pumpportal.fun"
        self._api_key = "https://api.mainnet-beta.solana.com/"
        
        self._jitoTipLamports = 1000000
        self._usepriorityLevelWithMaxLamports = 4000000
        self.use_jito=True
        
        self._dynamic_slippage = True
        self._wrapUnwrapSOL = True
        self._dynamicComputeUnitLimit = True
        
        self._wallets_dir = "save_wallets"
        self._primary_mint = None
        self._sol_mint = "So11111111111111111111111111111111111111112"

        # Указываем атрибуты, которые нужно сохранять и загружать
        self._tracked_attributes = [
            "jupiter_url",
            "jito_url",
            "pump_fun_url",
            "dynamic_slippage",
            "wrapUnwrapSOL",
            "dynamicComputeUnitLimit",
            "usepriorityLevelWithMaxLamports",
            "use_jito",
            "jitoTipLamports",
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
                            setattr(self, f"_{key}", data[key])
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

    def reset_to_defaults(self):
        """Сбрасывает все значения к дефолтным."""

        for key, value in self.get_default_values().items():
            setattr(self, f"_{key}", value)
        self.save_config()


    def get_default_values(self):
        """Генерирует словарь с дефолтными значениями из конструктора."""
        return {
            "jupiter_url": "https://api.jup.ag/swap/v1",
            "jito_url": "https://mainnet.block-engine.jit",
            "pump_fun_url":"https://pumpportal.fun",
            "dynamic_slippage": True,
            "wrapUnwrapSOL": True,
            "dynamicComputeUnitLimit": True,
            "usepriorityLevelWithMaxLamports": 4000000,
            "use_jito":True,
            "jitoTipLamports": 1000000,
            "wallets_dir": "save_wallets",
            "api_key": "https://api.mainnet-beta.solana.com/",
            "primary_mint": None,
            "sol_mint": "So11111111111111111111111111111111111111112",
        }

    
    
    @property
    def pump_fun_url(self):
        return self._pump_fun_url
    
    @pump_fun_url.setter
    def pump_fun_url(self, value):
        self._pump_fun_url = value
        
    
    @property
    def jito_url(self):
        return self._jito_url
    
    @jito_url.setter
    def jito_url(self, value):
        self._jito_url = value
    
    @property
    def primary_mint(self):
        return self._primary_mint

    @primary_mint.setter
    def primary_mint(self, value):
        self._primary_mint = value
        self.save_config()
        
    @property
    def sol_mint(self):
        return self._sol_mint

    @sol_mint.setter
    def sol_mint(self, value):
        self._sol_mint = value



    # Свойства с автоматическим сохранением
    @property
    def dynamic_slippage(self):
        return self._dynamic_slippage

    @dynamic_slippage.setter
    def dynamic_slippage(self, value):
        self._dynamic_slippage = value
     
            
    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key=value

    @property
    def wrapUnwrapSOL(self):
        return self._wrapUnwrapSOL

    @wrapUnwrapSOL.setter
    def wrapUnwrapSOL(self, value):
        self._wrapUnwrapSOL = value


    @property
    def dynamicComputeUnitLimit(self):
        return self._dynamicComputeUnitLimit

    @dynamicComputeUnitLimit.setter
    def dynamicComputeUnitLimit(self, value):
        self._dynamicComputeUnitLimit = value


    @property
    def usepriorityLevelWithMaxLamports(self):
        return self._usepriorityLevelWithMaxLamports

    @usepriorityLevelWithMaxLamports.setter
    def usepriorityLevelWithMaxLamports(self, value):
        self._usepriorityLevelWithMaxLamports = sol_to_lamports(value)
        
        
    @property
    def jitoTipLamports(self):
        return self._jitoTipLamports

    @jitoTipLamports.setter
    def jitoTipLamports(self, value):
        self._jitoTipLamports= sol_to_lamports(value)

    @property
    def jupiter_url(self):
        return self._jupiter_url

    @jupiter_url.setter
    def jupiter_url(self, value):
        self._jupiter_url = value

        
    @property
    def wallets_dir(self):
        return self._wallets_dir

    @wallets_dir.setter
    def wallets_dir(self, value):
        self._wallets_dir = value



