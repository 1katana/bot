
from wallet import Wallet
from dataclasses import dataclass, field
from typing import List, Optional
from PySide6.QtCore import Signal, QObject
from PySide6.QtCore import QObject, Property, Signal
from tokensData import useTokenInfo


@dataclass
class UseClasses:
    wallet: Wallet 
    is_use: bool = True
    usepriorityLevelWithMaxLamports: int = 4000000



class WalletWrapper(QObject):
    balanceChanged = Signal(int)
    nameChanged = Signal(str)
    isMasterChanged = Signal(bool)
    useTokenBalanceChanged = Signal(useTokenInfo)  # Используем object, так как тип useTokenInfo неизвестен

    def __init__(self, wallet: Wallet):
        super().__init__()
        self._wallet = wallet

    @Property(str, notify=nameChanged)
    def name(self):
        return self._wallet.name

    @name.setter
    def name(self, value):
        if self._wallet.name != value:
            self._wallet.name = value
            self.nameChanged.emit(value)

    @Property(int, notify=balanceChanged)
    def balance(self):
        return self._wallet.balance

    @balance.setter
    def balance(self, value):
        if self._wallet.balance != value:
            self._wallet.balance = value
            self.balanceChanged.emit(value)

    @Property(bool, notify=isMasterChanged)
    def is_master(self):
        return self._wallet.is_master

    @is_master.setter
    def is_master(self, value):
        if self._wallet.is_master != value:
            self._wallet.is_master = value
            self.isMasterChanged.emit(value)

    @Property(object, notify=useTokenBalanceChanged)
    def use_token_balance(self):
        return self._wallet.use_token_balance

    @use_token_balance.setter
    def use_token_balance(self, value):
        if self._wallet.use_token_balance != value:
            self._wallet.use_token_balance = value
            self.useTokenBalanceChanged.emit(value)





class UseClassesWrapper(QObject):
    is_use_changed = Signal(bool)
    usepriorityLevelWithMaxLamports_changed = Signal(int)
    wallet_changed = Signal(WalletWrapper)  

    def __init__(self, data: UseClasses):
        super().__init__()
        # Преобразуем Wallet в WalletWrapper, если это необходимо
        if not isinstance(data.wallet, WalletWrapper):
            data.wallet = WalletWrapper(data.wallet)
        self._data = data

    @property
    def usepriorityLevelWithMaxLamports(self) -> int:
        return self._data.usepriorityLevelWithMaxLamports

    @usepriorityLevelWithMaxLamports.setter
    def usepriorityLevelWithMaxLamports(self, value: int):
        if not isinstance(value, int):
            raise ValueError("usepriorityLevelWithMaxLamports должен быть int")
        if value < 0:
            raise ValueError("usepriorityLevelWithMaxLamports должен быть положительным")
        if self._data.usepriorityLevelWithMaxLamports != value:
            self._data.usepriorityLevelWithMaxLamports = value
            self.usepriorityLevelWithMaxLamports_changed.emit(value)

    @property
    def is_use(self) -> bool:
        return self._data.is_use

    @is_use.setter
    def is_use(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("is_use должен быть булевым значением")
        if self._data.is_use != value:
            self._data.is_use = value
            self.is_use_changed.emit(value)

    @property
    def wallet(self) -> WalletWrapper:
        return self._data.wallet

    @wallet.setter
    def wallet(self, value: WalletWrapper):
        if not isinstance(value, WalletWrapper):
            raise ValueError("wallet должен быть экземпляром WalletWrapper")
        if self._data.wallet != value:
            self._data.wallet = value
            self.wallet_changed.emit(value)
