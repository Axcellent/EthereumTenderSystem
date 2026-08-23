from PyQt6.QtCore import (QObject,
                          pyqtSignal,
                          pyqtSlot,
                          QThread)
from PyQt6.QtWidgets import QMessageBox
from typing import Any

from ui.operations import (BlockchainOperation,
                                BlockchainService,
                                BlockchainUser)

from ui.utils.worker import BlockchainWorker
from ui.utils.state import AppState

from ui.operations.users_operations import RegisterUserOperation
from ui.presenters import BasePresenter

from models.users_dto import UserCreateDTO

class UsersPresenter(BasePresenter):
    register_finished = pyqtSignal(object)
    get_user_finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(
        self,
        app_state: AppState
    ):
        super().__init__()
        self._app_state = app_state
        self._tasks = []

    def register(
        self,        
        data: UserCreateDTO
    ):    
        self._start_background_task(
            RegisterUserOperation(
                self._app_state.service,
                self._app_state.user,
                data
            ),
            self.register_finished
        )