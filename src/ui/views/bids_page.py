from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from ui.presenters.bid_presenter import *
from models.common import addr, pkey
from models.bids_dto import *
from pydantic import ValidationError

class BidCreationDialog(QDialog):
    def __init__(
        self,
        presenter: BidsPresenter,
        parent=None
    ):
        super().__init__(parent)
        self.presenter = presenter

        self.setWindowTitle("Создание заявки")
        self.setParent(parent)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.budget_in = QSpinBox()
        self.budget_in.setRange(0, 2_000_000_000)
        self.budget_in.setSingleStep(1)
        self.budget_in.setSuffix(" wei")
        self.budget_in.setToolTip("Предлагаемый вами бюджет на интересующий тендер в wei")
        form.addRow("Ваш бюджет", self.budget_in)

        self.deadline_in = QDateEdit()
        self.deadline_in.setCalendarPopup(True)
        self.deadline_in.setDisplayFormat("dd.MM.yyyy")
        self.deadline_in.setDate(QDate.currentDate().addDays(14))
        form.addRow("Ваш дедлайн выполнения тендера", self.deadline_in)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(self.buttons)

    def get_data(self) -> BidCreateDTO:
        return BidCreateDTO(
            tender_id=self.presenter.app_state.tender_id,
            price=self.budget_in.value(),
            deadline=datetime.datetime.combine(self.deadline_in.date().toPyDate(), datetime.time.min),
        )

class BidRevertDialog(QDialog):
    def __init__(
        self,
        presenter: BidsPresenter,
        parent=None
    ):
        super().__init__(parent)
        self.presenter = presenter

        self.setWindowTitle("Отмена заявки")
        self.setParent(parent)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.lbl = QLabel(f"Отменить заявку #{1}")
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(self.buttons)



class BidsPage(QWidget):
    def __init__(
        self,
        presenter: BidsPresenter,        
        parent=None
    ):
        super().__init__(parent)
        self.presenter = presenter

        layout = QVBoxLayout(self)

        self.bids_gb = QGroupBox(f"Заявки на тендер #?")
        layout.addWidget(self.bids_gb)

        bids_l = QVBoxLayout(self.bids_gb)

        # bid menu
        bids_btns_l = QHBoxLayout()
        bids_l.addLayout(bids_btns_l)
        self._create_pagination_menu(bids_btns_l)

        # bid list
        bids_list_l = QVBoxLayout()
        bids_l.addLayout(bids_list_l)
        self._create_table(bids_list_l)
        self._create_bottom_menu(bids_list_l)

        self.presenter.error_occured.connect(self._on_error)    
        self.presenter.get_tender_bids_finished.connect(self._load_bids_finished)
        self.presenter.app_state.tender_changed.connect(self._refresh_tender_id)

    def _create_bottom_menu(self, layout: QLayout):
        # create btn: create
        bid_create_btn = QPushButton("Создать")    
        layout.addWidget(bid_create_btn)    

        # info label: create
        bids_status_lbl = QLabel("А тут доп инфа")
        layout.addWidget(bids_status_lbl)

        # signals
        bid_create_btn.clicked.connect(self._open_creation_dialog)

    def _create_pagination_menu(self, layout: QLayout):
        # load btn: create
        self.load_bids_btn = QPushButton("Загрузить")
        layout.addWidget(self.load_bids_btn)        

        # page inpt: create
        self.bids_page_in = QSpinBox()
        layout.addWidget(self.bids_page_in)
        # page inpt: setup
        self.bids_page_in.setRange(1, 1_000_000_000)
        self.bids_page_in.setPrefix("Страница №")    

        # count inpt: create
        self.bids_cnt_in = QSpinBox()
        layout.addWidget(self.bids_cnt_in)
        # count inpt: setup
        self.bids_cnt_in.setRange(0, 100)        
        self.bids_cnt_in.setSuffix(" штук")    

        # signals
        self.load_bids_btn.clicked.connect(self._load_bids)

    def _create_table(self, layout: QLayout):
        # table: create
        self.table = QTableWidget()
        layout.addWidget(self.table)
        # table: setup
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)

        # table header: setup
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Отправитель", "Бюджет", "Дедлайн", "Статус"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # signals
        self.table.itemDoubleClicked.connect(self._open_revert_dialog)


    def _open_revert_dialog(self, item: QModelIndex):        
        dialog = BidRevertDialog(self)
        res = dialog.exec()

        if res == QDialog.DialogCode.Accepted:
            try:                
                self.presenter.revert_bid(int(self.table.item(item.row(), 0).text()))
            except Exception as e:
                self._on_error(str(e))   

    def _open_creation_dialog(self):
        dialog = BidCreationDialog(self.presenter, self)
        res = dialog.exec()

        if res == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                self.presenter.submit_bid(data)
            except Exception as e:
                self._on_error(str(e))

    def _refresh_tender_id(self, new_id):
        self.bids_gb.setTitle(f"Заявки на тендер #{new_id}")

    def _load_bids(self):        
        self.presenter.get_tender_bids(self.presenter.app_state.tender_id)  

    def _load_bids_finished(self, bids_data: list[BidGetDTO]):
        self.table.setRowCount(len(bids_data))

        i,j=0,0    
        for t in bids_data:
            j = 0
            for f, v in t.model_dump().items():
                if f != "tender_id":
                    self.table.setItem(i, j, QTableWidgetItem(str(v)))
                    j += 1
            i += 1

    def _on_error(self, msg: str):
        QMessageBox.critical(self, "Ошибка", msg)