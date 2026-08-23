from PyQt6.QtCore import (QObject,
                          pyqtSignal,
                          pyqtSlot,
                          QThread)
from PyQt6.QtWidgets import QMessageBox
from typing import Any

from ui.operations.base import (BlockchainOperation,
                                BlockchainService,
                                BlockchainUser)

from ui.utils.worker import BlockchainWorker

from ui.operations.users_operations import RegisterUserOperation

from ui.utils.state import AppState

from models.users_dto import UserCreateDTO

class UsersPresenter(QObject):
    register_finished = pyqtSignal()
    get_user_finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(
        self,
        app_state: AppState
    ):
        super().__init__()
        self._app_state = app_state
        self._tasks = []

    def _start_operation(
        self,
        operation: BlockchainOperation,
        success_signal
    ):
        thread = QThread()
        task = BlockchainWorker(
            operation
        )
        task.moveToThread(thread)

        thread.started.connect(task.run)

        task.finished.connect(success_signal)
        task.error.connect(self._on_error)

        task.finished.connect(thread.quit)
        task.error.connect(thread.quit)

        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(task.deleteLater)

        self._tasks.append(thread)
        thread.start()

    def register(
        self,        
        data: UserCreateDTO
    ):    
        self._start_operation(
            RegisterUserOperation(
                self._app_state.service,
                self._app_state.user,
                data
            ),
            self.register_finished
        )

    def _on_error(self, msg: str):
        self.error.emit(msg)
    