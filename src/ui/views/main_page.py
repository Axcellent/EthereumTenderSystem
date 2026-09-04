from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from pydantic import ValidationError

from models.common import addr, pkey
from models.users_dto import *

from ui.presenters.tenders_presenter import *
from ui.presenters.bid_presenter import *

from ui.views.tenders_page import TendersPage, TenderView
from ui.views.bids_page import BidsPage

class MainPage(QWidget):
    def __init__(
        self,
        tenders_presenter: TendersPresenter,
        bids_presenter: BidsPresenter,
        parent=None
    ):
        super().__init__(parent)        
        layout = QVBoxLayout(self)
        self.app_state = tenders_presenter.app_state

        # arrows and f5
        menu_buttons_l = QHBoxLayout()
        layout.addLayout(menu_buttons_l)
        self._create_menu(menu_buttons_l)

        # central view
        self.stacked = QStackedWidget()
        layout.addWidget(self.stacked)

        # p0 = all tenders
        self.all_tenders_page = TendersPage(tenders_presenter, self)
        self.stacked.addWidget(self.all_tenders_page)
        # p1 = current tender
        self.tender_page = TenderView(tenders_presenter, self)
        self.stacked.addWidget(self.tender_page)
        # p2 = all bids for tender
        self.bids_page = BidsPage(bids_presenter, self)    
        self.stacked.addWidget(self.bids_page)
        # p3 = contract for tender
        self.contract_page = BidsPage(bids_presenter, self)
        self.stacked.addWidget(self.contract_page)

        # signals
        self.app_state.tender_changed.connect(lambda: self.stacked.setCurrentIndex(1))

    def _create_menu(self, layout: QLayout):
        # <
        self.back_btn = QPushButton(" < Назад ")
        layout.addWidget(self.back_btn)    

        # f5
        self.refresh_btn = QPushButton(" o Обновить o ")
        layout.addWidget(self.refresh_btn)   

        # >
        self.forward_btn = QPushButton(" Вперед > ")
        layout.addWidget(self.forward_btn)

        # signals
        self.back_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(max(0,self.stacked.currentIndex() - 1)))
        self.forward_btn.clicked.connect(lambda: self.stacked.setCurrentIndex(min(self.stacked.currentIndex() + 1, 2)))
