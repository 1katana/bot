
from wallet import Wallet
from dataclasses import dataclass, field
from typing import List, Optional
from PySide6.QtCore import Signal, QObject
from PySide6.QtCore import QObject, Property, Signal
from dataclases.tokensData import useTokenInfo
from dataclasses import dataclass
from PySide6.QtCore import QObject, Signal, Property

class UseClasses(QObject):
    is_use_changed = Signal(bool)
    usepriorityLevelWithMaxLamports_changed = Signal(int)
    # walletChanged = Signal(Wallet)  # Signal for the Wallet object

    def __init__(self, wallet:Wallet, is_use=True, usepriorityLevelWithMaxLamports=4000000):
        super().__init__()
        self.wallet = wallet
        self._is_use = is_use
        self._usepriorityLevelWithMaxLamports = usepriorityLevelWithMaxLamports

    def __hash__(self):
        return hash(self.wallet)

    def __eq__(self, other):
        if isinstance(other, UseClasses):
            return self.wallet == other.wallet
        return False

    @Property(bool, notify=is_use_changed)
    def is_use(self) -> bool:
        return self._is_use

    @is_use.setter
    def is_use(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_use должно быть булевым значением")
        if self._is_use != value:
            self._is_use = value
            self.is_use_changed.emit(value)

    @Property(int, notify=usepriorityLevelWithMaxLamports_changed)
    def usepriorityLevelWithMaxLamports(self) -> int:
        return self._usepriorityLevelWithMaxLamports

    @usepriorityLevelWithMaxLamports.setter
    def usepriorityLevelWithMaxLamports(self, value: int):
        if not isinstance(value, int):
            raise ValueError("usepriorityLevelWithMaxLamports должен быть целым числом")
        if value < 0:
            raise ValueError("usepriorityLevelWithMaxLamports должен быть положительным")
        if self._usepriorityLevelWithMaxLamports != value:
            self._usepriorityLevelWithMaxLamports = value
            self.usepriorityLevelWithMaxLamports_changed.emit(value)

    # @Property(object, notify=walletChanged)
    # def wallet(self)->Wallet:
    #     return self._wallet

    # @wallet.setter
    # def wallet(self, value:Wallet):
    #     if not isinstance(value, Wallet):
    #         raise ValueError("wallet должен быть экземпляром Wallet")
    #     if self._wallet != value:
    #         self._wallet = value
    #         self.walletChanged.emit(value)