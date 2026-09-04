from PyQt6.QtCore import (QObject,
                          pyqtSignal,
                          pyqtSlot,
                          QThread)
from PyQt6.QtWidgets import QMessageBox
from typing import Optional

from ui.utils.worker import BlockchainWorker
from ui.utils.state import AppState

from ui.operations.bids_operations import *
from ui.presenters import BasePresenter

from models.bids_dto import *

from models.common import addr, uid

class BidsPresenter(BasePresenter):
    submit_bid_finished = pyqtSignal()
    revert_bid_finished = pyqtSignal()
    get_bid_finished = pyqtSignal(object)
    get_tender_bids_finished = pyqtSignal(object)
    get_user_bids_finished = pyqtSignal(object)

    def __init__(
        self,
        app_state: AppState,
        parent=None
    ):
        super().__init__(app_state, parent)

    @BasePresenter.chain_operation
    def submit_bid(
        self,
        data: BidCreateDTO
    ):
        self._start_background_task(
            SubmitBidOperation(
                self.app_state.service,
                self.app_state.user,
                data
            ),
            self.submit_bid_finished
        )

    @BasePresenter.chain_operation
    def revert_bid(
        self,
        id: uid
    ):
        self._start_background_task(
            RevertBidOperation(
                self.app_state.service,
                self.app_state.user,
                id
            ),
            self.revert_bid_finished
        )

    @BasePresenter.chain_operation
    def get_bid(
        self,
        id: uid
    ):
        self._start_background_task(
            GetBidOperation(
                self.app_state.service,
                self.app_state.user,
                id
            ),
            self.get_bid_finished
        )

    @BasePresenter.chain_operation
    def get_tender_bids(
        self,
        tender_id: uid
    ):
        self._start_background_task(
            GetTenderBidsOperation(
                self.app_state.service,
                self.app_state.user,
                tender_id
            ),
            self.get_tender_bids_finished
        )

    @BasePresenter.chain_operation
    def get_user_bids(
        self,
        user: addr
    ):
        self._start_background_task(
            GetUserBidOperation(
                self.app_state.service,
                self.app_state.user,
                user
            ),
            self.get_user_bids_finished
        )