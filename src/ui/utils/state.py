from PyQt6.QtCore import (QObject,
                          pyqtSignal,
                          pyqtSlot)

from ui.operations import BlockchainUser
from services import BlockchainService

from eth_account import Account

class AppState(QObject):
    user_changed = pyqtSignal(object)
    service_connected = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._user: BlockchainUser | None = None
        self._service: BlockchainService | None = None

    @property
    def service(self) -> BlockchainService:
        return self._service
    
    def setService(
        self,        
        url: str,
        contract: str,        
    ):
        self._service = BlockchainService(url, contract, 'src/abi.json')    
        self.service_connected.emit()     

    @property
    def user(self) -> BlockchainUser:
        return self._user
    
    def setUser(self, key: str):
        ac = Account.from_key(key)

        self._user = BlockchainUser(ac.address, ac.key)

        self.user_changed.emit(self._user)