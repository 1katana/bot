
from wallet import Wallet
from dataclasses import dataclass, field
from typing import List, Optional
from PySide6.QtCore import Signal, QObject


@dataclass
class UseClases(QObject):
    

    is_use_changed = Signal(bool)
    usepriorityLevelWithMaxLamports_changed = Signal(int)
    wallet_changed = Signal(Wallet)

    def __init__(self,wallet:Wallet, is_use=True,usepriorityLevelWithMaxLamports=4000000):
        super().__init__()
        self._wallet=wallet
        self._is_use=is_use
        self._usepriorityLevelWithMaxLamports=usepriorityLevelWithMaxLamports
        

    @property
    def usepriorityLevelWithMaxLamports(self) -> int:
        return self._usepriorityLevelWithMaxLamports

    @usepriorityLevelWithMaxLamports.setter
    def usepriorityLevelWithMaxLamports(self, value: int):
        if not isinstance(value, int):
            raise ValueError("usepriorityLevelWithMaxLamports должен быть int")
        if value < 0:
            raise ValueError("usepriorityLevelWithMaxLamports должен быть положительным")
        self._usepriorityLevelWithMaxLamports = value
        self.usepriorityLevelWithMaxLamports_changed.emit(value)

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
        self.is_use_changed.emit(value)

    @property
    def wallet(self) -> Wallet:
        return self._wallet

    @wallet.setter
    def wallet(self, value: Wallet):
        if not isinstance(value, Wallet):
            raise ValueError("wallet должен быть экземпляром Wallet")
        self._wallet = value
        self.wallet_changed.emit(value)
