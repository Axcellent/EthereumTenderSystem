from PyQt6.QtCore import (QObject,
                          pyqtSlot,
                          pyqtSignal)

from ui.utils.state import BlockchainService, AppState
from ui.presenters import BasePresenter
from ui.operations.connection_operations import ConnectOperation

class ConnectionPresenter(BasePresenter):
    error_occured = pyqtSignal(str)

    def __init__(
        self,
        app_state: AppState,
        parent=None
    ):
        super().__init__(parent)
        self.app_state = app_state

    def connect(
        self,
        url: str,
        contract: str,        
    ):
        try:
            self._start_background_task(
                ConnectOperation(
                    self.app_state,
                    url,
                    contract,
                ), 
                self.app_state.service_connected
            )
        except Exception as e:
            self.error_occured.emit(str(e))
