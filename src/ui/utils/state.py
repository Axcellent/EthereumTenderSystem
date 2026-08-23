from PyQt6.QtCore import (QObject,
                          pyqtSignal,
                          pyqtSlot)

from ui.operations.base import BlockchainUser
from services import BlockchainService

class AppState(QObject):
    user_changed = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        
        self._user: BlockchainUser | None = None
        self.service: BlockchainService | None = None

    @property
    def user(self) -> BlockchainUser:
        return self._user

    @user.setter
    def user(self, value: BlockchainUser | None):
        self._user = value
        self.user_changed.emit(value)