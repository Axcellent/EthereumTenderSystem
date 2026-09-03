from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from ui.presenters.tenders_presenter import *
from models.common import addr, pkey
from models.users_dto import *
from pydantic import ValidationError

class TenderPage(QWidget):
    def __init__(
        self,
        presenter: TendersPresenter,
        tender_id: uint,
        parent=None
    ):
        super().__init__(parent)
        self.presenter = presenter
        self.tender_id = tender_id

        self.open_bid_menu_btn = QPushButton("Заявка")
        self.open_bid_menu_btn.clicked.connect(lambda: self.presenter.close_tender())
        self.close_tender_btn =  QPushButton("Закрыть")
        self.close_tender_btn.clicked.connect(lambda: self.presenter.close_tender())
        self.revert_tender_btn = QPushButton("Отменить")
        self.revert_tender_btn.clicked.connect(lambda: self.presenter.revert_tender())
        btns_l = QHBoxLayout()
        btns_l.addWidget(self.open_bid_menu_btn)
        btns_l.addWidget(self.close_tender_btn)
        btns_l.addWidget(self.revert_tender_btn)


        layout = QVBoxLayout(self)
        layout.addLayout(btns_l)

        self.tender_gb = QGroupBox("Тендер")
        tender_l = QGridLayout(self.tender_gb)

        self.title_lbl = QLabel("не указано")
        self.title_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.description_lbl = QLabel("не указано")
        self.description_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.description_lbl.setWordWrap(True)
        self.budget_lbl = QLabel("не указано")
        self.budget_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.deadline_lbl = QLabel("не указано")
        self.deadline_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


        tender_l.addWidget(QLabel("НАЗВАНИЕ"), 0, 0)
        tender_l.addWidget(self.title_lbl, 0, 1)
        tender_l.addWidget(QLabel("ОПИСАНИЕ"), 1, 0)
        tender_l.addWidget(self.description_lbl, 1, 1)
        tender_l.addWidget(QLabel("Бюджет"), 2, 0)
        tender_l.addWidget(self.budget_lbl, 2, 1)
        tender_l.addWidget(QLabel("Дедлайн на выполнение"), 3, 0)
        tender_l.addWidget(self.deadline_lbl, 3, 1)

        tender_l.setColumnStretch(0, 1)
        tender_l.setColumnStretch(1, 3) 




        self.status_gb = QGroupBox("Статус")
        status_l = QGridLayout(self.status_gb)

        self.bidding_deadline_lbl = QLabel("не указано")
        self.bidding_deadline_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)        
        self.status_lbl = QLabel("не указано")
        self.status_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        status_l.addWidget(QLabel("Дедлайн подачи заявок"), 1, 0)
        status_l.addWidget(self.bidding_deadline_lbl, 1, 1)
        status_l.addWidget(QLabel("Статус"), 2, 0)
        status_l.addWidget(self.status_lbl, 2, 1)

        status_l.setColumnStretch(0, 1)
        status_l.setColumnStretch(1, 3) 

        layout.addLayout(status_l)
        layout.addWidget(self.tender_gb)
        layout.addWidget(self.status_gb)
    
        self.presenter.get_tender_full_finished.connect(self._show_tender)
        self.presenter.app_state.tender_changed.connect(self._change_id)

        self.presenter.error_occured.connect(self._on_error)

    def _change_id(self, new_id: uint):
        self.presenter.get_tender_full(new_id)

    def _show_tender(self, data: TenderGetFullDTO):
        print(data)
        self.title_lbl.setText(data.title)
        self.description_lbl.setText(data.description)
        self.budget_lbl.setText(str(data.budget) + " wei")
        self.deadline_lbl.setText(str(data.deadline.date()))
        self.bidding_deadline_lbl.setText(str(data.bidding_deadline.date()))
        self.status_lbl.setText(str(data.status))
        
    def _register_finished(self) :
        QMessageBox.information(self, "Успешная регистрация", "Вы успешно зарегистирировали свою организацию в GTS!")

    def _on_error(self, msg: str):
        QMessageBox.critical(self, "Ошибка действия с тендером", msg)