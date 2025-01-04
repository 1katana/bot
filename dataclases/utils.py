
from wallet import Wallet
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class UseClases:
    wallet: Wallet
    _is_use: bool = field(default=True)

    def __post_init__(self):
        if not isinstance(self.wallet, Wallet): 
            raise TypeError("wallet должен быть экземпляром Wallet")
    
    @property
    def is_use(self) -> bool:
        """Свойство для получения значения isUse."""
        return self._is_use

    @is_use.setter
    def is_use(self, value: bool):
        """Свойство для изменения значения isUse."""
        if not isinstance(value, bool):
            raise ValueError("isUse должен быть булевым значением")
        self._is_use = value
