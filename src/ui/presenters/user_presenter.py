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

from ui.operations.users_operations import *
from ui.presenters import BasePresenter

from models.users_dto import *

class UsersPresenter(BasePresenter):
    register_finished = pyqtSignal(object)
    get_user_finished = pyqtSignal(object)
    admin_action_finished = pyqtSignal()

    def __init__(
        self,
        app_state: AppState,
        parent=None
    ):
        super().__init__(app_state, parent)

    @BasePresenter.chain_operation
    def register(
        self,        
        data: UserCreateDTO
    ):    
        self._start_background_task(
            RegisterUserOperation(
                self.app_state.service,
                self.app_state.user,
                data
            ),
            self.register_finished
        )

    @BasePresenter.chain_operation
    def get_user_data(
        self,        
        address=None
    ):    
        self._start_background_task(
            GetUserOperation(
                self.app_state.service,
                self.app_state.user,
                address
            ),
            self.get_user_finished
        )

    @BasePresenter.chain_operation
    def ban_user(
        self,        
        address: addr,
        reason: str
    ):    
        self._start_background_task(
            BanUserOperation(
                self.app_state.service,
                self.app_state.user,
                address,
                reason
            ),
            self.admin_action_finished
        )

    @BasePresenter.chain_operation
    def delete_user(
        self,        
        address: addr,
        reason: str
    ):    
        self._start_background_task(
            DeleteUserOperation(
                self.app_state.service,
                self.app_state.user,
                address,
                reason
            ),
            self.admin_action_finished
        )

    @BasePresenter.chain_operation
    def unban_user(
        self,        
        address: addr,
        reason: str
    ):        
        self._start_background_task(
            UnbanUserOperation(
                self.app_state.service,
                self.app_state.user,
                address,
                reason
            ),
            self.admin_action_finished
        )