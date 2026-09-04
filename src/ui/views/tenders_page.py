from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from pydantic import ValidationError

from models.common import addr, pkey
from models.tenders_dto import *

from ui.presenters.tenders_presenter import *

class TenderCreatingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Создание тендера")
        self.setParent(parent)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_in = QLineEdit()
        self.title_in.setPlaceholderText("Название тендера")
        form.addRow("Название", self.title_in)

        self.description_in = QTextEdit()
        self.description_in.setPlaceholderText("Полное описание тендера со ссылками на необходимые материалы")
        form.addRow("Описание", self.description_in)

        self.budget_in = QSpinBox()
        self.budget_in.setRange(0, 2_000_000_000)
        self.budget_in.setSingleStep(1)
        self.budget_in.setSuffix(" wei")
        self.budget_in.setToolTip("Бюджет на ваш заказ в wei")
        form.addRow("Бюджет", self.budget_in)

        self.deadline_in = QDateEdit()
        self.deadline_in.setCalendarPopup(True)
        self.deadline_in.setDisplayFormat("dd.MM.yyyy")
        self.deadline_in.setDate(QDate.currentDate().addDays(14))
        form.addRow("Дедлайн выполнения тендера", self.deadline_in)

        self.bidding_deadline_in = QDateEdit()
        self.bidding_deadline_in.setCalendarPopup(True)
        self.bidding_deadline_in.setDisplayFormat("dd.MM.yyyy")
        self.bidding_deadline_in.setDate(QDate.currentDate().addDays(1))
        form.addRow("Дедлайн подачи заявок на тендер", self.bidding_deadline_in)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(self.buttons)
        

    def get_data(self):        
        return TenderCreateDTO(
            title=self.title_in.text(),
            description=self.description_in.toPlainText(),
            budget=self.budget_in.value(),
            deadline=datetime.datetime.combine(self.deadline_in.date().toPyDate(), datetime.time.min),
            bidding_deadline=datetime.datetime.combine(self.bidding_deadline_in.date().toPyDate(), datetime.time.min),
            parent_id=0
        )

class TendersPage(QWidget):
    def __init__(
        self,
        presenter: TendersPresenter,
        parent
    ):
        super().__init__(parent)
        self.presenter = presenter

        layout = QVBoxLayout(self)

        tenders_gb = QGroupBox("Тендеры")
        layout.addWidget(tenders_gb)

        tenders_l = QVBoxLayout(tenders_gb)

        # tender menu
        tenders_btns_l = QHBoxLayout()
        tenders_l.addLayout(tenders_btns_l)
        self._create_pagination_menu(tenders_btns_l)

        # tender list
        tenders_list_l = QVBoxLayout()
        tenders_l.addLayout(tenders_list_l)
        self._create_table(tenders_list_l)
        self._create_bottom_menu(tenders_list_l)

        # signals
        self.presenter.error_occured.connect(self._on_error)    
        self.presenter.get_tenders_finished.connect(self._load_tenders_finished)

    def _create_bottom_menu(self, layout: QLayout):
        # create btn: create
        create_tender_btn = QPushButton("Создать")    
        layout.addWidget(create_tender_btn)    

        # info label: create
        tenders_status_lbl = QLabel("А тут доп инфа")
        layout.addWidget(tenders_status_lbl)

        # signals
        create_tender_btn.clicked.connect(self._open_creation_dialog)

    def _create_pagination_menu(self, layout: QLayout):
        # load btn: create
        self.load_tenders_btn = QPushButton("Загрузить")
        layout.addWidget(self.load_tenders_btn)        

        # page inpt: create
        self.tenders_page_in = QSpinBox()
        layout.addWidget(self.tenders_page_in)
        # page inpt: setup
        self.tenders_page_in.setRange(1,1_000_000_000)
        self.tenders_page_in.setPrefix("Страница №")    

        # count inpt: create
        self.tenders_cnt_in = QSpinBox()
        layout.addWidget(self.tenders_cnt_in)
        # count inpt: setup
        self.tenders_cnt_in.setRange(0,100)        
        self.tenders_cnt_in.setSuffix(" штук")    

        # signals
        self.load_tenders_btn.clicked.connect(self._load_tenders)

    def _create_table(self, layout: QLayout):
        # table: create
        self.table = QTableWidget()
        layout.addWidget(self.table)
        # table: setup
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)

        # table header: setup
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Заказчик", "Название", "Бюджет", "Дедлайн", "Статус"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # signals
        self.table.itemDoubleClicked.connect(self._go_to_tender)


    def _go_to_tender(self, item: QModelIndex):        
        self.presenter.app_state.set_tender_id(int(self.table.item(item.row(), 0).text()))        

    def _open_creation_dialog(self):
        dialog = TenderCreatingDialog(self)
        res = dialog.exec()

        if res == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                self.presenter.create_tender(data)
            except Exception as e:
                self._on_error(str(e))

    def _load_tenders(self):        
        self.presenter.get_tenders(self.tenders_page_in.value(),self.tenders_cnt_in.value())  

    def _load_tenders_finished(self, tender_data: list[TenderGetFullDTO]):
        self.table.setRowCount(len(tender_data))

        i,j=0,0    
        for t in tender_data:
            j = 0
            for f, v in t.model_dump().items():                
                self.table.setItem(i, j, QTableWidgetItem(str(v)))
                j += 1
            i += 1

    def _on_error(self, msg: str):
        QMessageBox.critical(self, "Ошибка", msg)
    

class TenderView(QWidget):
    def __init__(
        self,
        presenter: TendersPresenter,
        parent=None
    ):
        super().__init__(parent)
        self.presenter = presenter        

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

    def _change_id(self, new_id: uid):
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