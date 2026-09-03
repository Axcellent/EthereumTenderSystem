from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from ui.presenters.tenders_presenter import *
from models.common import addr, pkey
from models.users_dto import *
from pydantic import ValidationError
from ui.views.tenders_page import TenderPage

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
        print("Data got successfuly")
        return TenderCreateDTO(
            title=self.title_in.text(),
            description=self.description_in.toPlainText(),
            budget=self.budget_in.value(),
            deadline=datetime.datetime.combine(self.deadline_in.date().toPyDate(), datetime.time.min),
            bidding_deadline=datetime.datetime.combine(self.bidding_deadline_in.date().toPyDate(), datetime.time.min),
            parent_id=0
        )


class MainPage(QWidget):
    def __init__(
        self,
        presenter: TendersPresenter,
        parent=None
    ):
        super().__init__(parent)
        self.presenter = presenter

        layout = QVBoxLayout(self)
        btns_l = QHBoxLayout()
        layout.addLayout(btns_l)

        self.stacked = QStackedWidget()
        layout.addWidget(self.stacked)

        tenders_gb = QGroupBox("Тендеры")
        self.stacked.addWidget(tenders_gb)

        tenders_l = QVBoxLayout(tenders_gb)
        tenders_btns_l = QHBoxLayout()
        tenders_l.addLayout(tenders_btns_l)
        tenders_list_l = QVBoxLayout()
        tenders_l.addLayout(tenders_list_l)

        self.load_tenders_btn = QPushButton("Загрузить")
        tenders_btns_l.addWidget(self.load_tenders_btn)
        self.tenders_page_in = QSpinBox()
        self.tenders_page_in.setRange(1,1_000_000_000)
        self.tenders_page_in.setPrefix("Страница №")
        tenders_btns_l.addWidget(self.tenders_page_in)
        self.tenders_cnt_in = QSpinBox()
        self.tenders_cnt_in.setRange(0,100)        
        self.tenders_cnt_in.setSuffix(" штук")
        tenders_btns_l.addWidget(self.tenders_cnt_in)


        self.table = QTableWidget()
        self.table.setColumnCount(5)
        
        self.table.setHorizontalHeaderLabels(["Заказчик", "Название", "Бюджет", "Дедлайн", "Статус"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.doubleClicked.connect(self._go_to_tender)

        tenders_list_l.addWidget(self.table)
        create_tender_btn = QPushButton("Создать")
        create_tender_btn.clicked.connect(self._open_creation_dialog)
        tenders_list_l.addWidget(create_tender_btn)    
        tenders_status_lbl = QLabel("А тут доп инфа")
        tenders_list_l.addWidget(tenders_status_lbl)

        self.page1 = TenderPage(self.presenter, 1, self)
        self.stacked.addWidget(self.page1)
        self.page2 = QLabel("Это страница 2")    
        self.stacked.addWidget(self.page2)

        self.btn1 = QPushButton(" < ")
        btns_l.addWidget(self.btn1)
        self.btn1.clicked.connect(lambda: self.stacked.setCurrentIndex(max(0,self.stacked.currentIndex() - 1)))
        self.btn2 = QPushButton(" > ")
        btns_l.addWidget(self.btn2)
        self.btn2.clicked.connect(lambda: self.stacked.setCurrentIndex(min(self.stacked.currentIndex() + 1, 2)))

        self.presenter.error_occured.connect(self._on_error)
        self.load_tenders_btn.clicked.connect(self._load_tender)
        self.presenter.get_tenders_finished.connect(self._load_tender_finished)

    def _go_to_tender(self, item: QModelIndex):        
        self.presenter.app_state.set_tender_id(int(self.table.item(item.row(), 0).text()))
        self.stacked.setCurrentIndex(1)

    def _open_creation_dialog(self):
        dialog = TenderCreatingDialog(self)
        res = dialog.exec()

        if res == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                self.presenter.create_tender(data)
            except Exception as e:
                self._on_error(str(e))

    def _load_tender(self):        
        self.presenter.get_tenders(self.tenders_page_in.value(),self.tenders_cnt_in.value())  

    def _load_tender_finished(self, tender_data: list[TenderGetFullDTO]):
        print(tender_data)
        i,j=0,0
        self.table.setRowCount(len(tender_data))
        for t in tender_data:
            j = 0
            for f, v in t.model_dump().items():
                try:
                    self.table.setItem(i,j,QTableWidgetItem(str(v)))
                except:
                    self.table.setItem(i,j,QTableWidgetItem("as"))
                j += 1
            i += 1

    def _on_error(self, msg: str):
        QMessageBox.critical(self, "Ошибка", msg)


