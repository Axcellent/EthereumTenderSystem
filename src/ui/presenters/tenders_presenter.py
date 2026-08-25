from PyQt6.QtCore import (QObject,
                          pyqtSignal,
                          pyqtSlot,
                          QThread)
from PyQt6.QtWidgets import QMessageBox
from typing import Optional

from ui.utils.worker import BlockchainWorker
from ui.utils.state import AppState

from ui.operations.tenders_operations import *
from ui.presenters import BasePresenter

from models.tenders_dto import *

from models.common import addr, uint

from models.tenders_dto import *


class TendersPresenter(BasePresenter):    
    create_tender_finished = pyqtSignal(object)      # TxReceipt
    close_tender_finished = pyqtSignal(bool)         # bool
    revert_tender_finished = pyqtSignal(object)      # TxReceipt
    get_tenders_finished = pyqtSignal(object)          # list[TenderGetShortDTO]
    get_user_tenders_finished = pyqtSignal(list)     # list[TenderGetShortDTO]
    get_tender_full_finished = pyqtSignal(object)    # TenderGetFullDTO

    def __init__(
        self,
        app_state: AppState,
        parent=None
    ):
        super().__init__(app_state, parent)


    @BasePresenter.chain_operation
    def create_tender(
        self,
        tender_data: TenderCreateDTO
    ):
        self._start_background_task(
            CreateTenderOperation(
                self.app_state.service,
                self.app_state.user,
                tender_data
            ),
            self.create_tender_finished
        )

    @BasePresenter.chain_operation
    def close_tender(
        self,
        tender_id: uint
    ):        
        self._start_background_task(
            CloseTenderOperation(
                self.app_state.service,
                self.app_state.user,
                tender_id
            ),
            self.close_tender_finished
        )

    @BasePresenter.chain_operation
    def revert_tender(
        self, 
        tender_id: uint
    ):
        self._start_background_task(
            RevertTenderOperation(
                self.app_state.service,
                self.app_state.user,
                tender_id
            ),
            self.revert_tender_finished
        )

    @BasePresenter.chain_operation
    def get_tenders(
        self,
        page: int,
        count: uint = 10
    ):
        print('get_tenders')
        self._start_background_task(
            LoadTendersOperation(
                self.app_state.service,
                self.app_state.user,
                page,
                count
            ),
            self.get_tenders_finished
        )

    @BasePresenter.chain_operation
    def get_user_tenders(
        self,
        user_address: Optional[addr] = None
    ):
        if user_address is None:
            user_address = self.app_state.user.address

        self._start_background_task(
            LoadUserTendersOperation(
                self.app_state.service,
                self.app_state.user,
                user_address
            ),
            self.get_user_tenders_finished
        )

    @BasePresenter.chain_operation
    def get_tender_full(
        self,
        tender: uint
    ):
        self._start_background_task(
            LoadFullTenderOperation(
                self.app_state.service,
                self.app_state.user,
                tender
            ),
            self.get_tender_full_finished
        )