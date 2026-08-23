from PyQt6.QtCore import (QObject,
                          pyqtSignal,
                          pyqtSlot,
                          QThread)
from PyQt6.QtWidgets import QMessageBox
from typing import Any

from ui.operations import (BlockchainOperation,
                            BlockchainService,
                            BlockchainUser,
                            Operation)

from ui.utils.worker import BlockchainWorker

from ui.operations.users_operations import RegisterUserOperation

from ui.utils.state import AppState

from models.users_dto import UserCreateDTO

class BasePresenter(QObject):
    def __init__(
        self, 
        parent=None
    ):
        super().__init__(parent)
        self.tasks: list[QThread] = []
        self.workers: list[BlockchainWorker] = []

    def _start_background_task(
        self,
        operation: Operation,
        success_signal
    ):
        thread = QThread()
        task = BlockchainWorker(operation)
        task.moveToThread(thread)

        thread.started.connect(task.run)
        task.finished.connect(thread.quit)
        task.finished.connect(success_signal)
        task.error.connect(thread.quit)
        task.error.connect(self._on_error)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(task.deleteLater)        

        self.tasks.append(thread)
        self.workers.append(task)
        thread.start()

    def _on_error(self):
        pass