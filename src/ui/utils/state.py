from PyQt6.QtCore import (QObject,
                          pyqtSignal,
                          pyqtSlot)

from ui.operations import BlockchainUser
from services import BlockchainService

from eth_account import Account

class AppState(QObject):
    task_started = pyqtSignal(str)
    task_finished = pyqtSignal()
    user_changed = pyqtSignal(object)
    service_connected = pyqtSignal()
    tender_changed = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self._user: BlockchainUser | None = None
        self._service: BlockchainService | None = None
        self._can_create_tasks: bool = True

        self.tender_id: int | None = None

    def set_tender_id(self, _tender_id: int):
        self.tender_id = _tender_id

        self.tender_changed.emit(self.tender_id)

    @property
    def service(self) -> BlockchainService:
        return self._service
    
    def set_service(
        self,        
        url: str,
        contract: str,        
    ):
        self._service = BlockchainService(url, contract, 'src/abi.json')            

    def block(self, msg: str) -> bool:
        if self._can_create_tasks == True:
            self._can_create_tasks: bool = False
            self.task_started.emit(msg)
            return True
        return False

    def release(self):
        if self._can_create_tasks == False:
            self._can_create_tasks: bool = True
            self.task_finished.emit()
    
    @property
    def user(self) -> BlockchainUser:
        return self._user
    
    def set_user(self, key: str):
        ac = Account.from_key(key)

        self._user = BlockchainUser(ac.address, ac.key)

        self.user_changed.emit(self._user)