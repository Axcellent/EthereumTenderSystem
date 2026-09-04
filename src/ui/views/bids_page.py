from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
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


class BidsPage(QWidget):
    def __init__(
        self,
        presenter: BidsPresenter,        
        parent=None
    ):
        super().__init__(parent)
        self.presenter = presenter

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID","Отправитель","Цена","Дедлайн", "Активна"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        
        
    def _register_finished(self) :
        QMessageBox.information(self, "Успешная регистрация", "Вы успешно зарегистирировали свою организацию в GTS!")

    def _on_error(self, msg: str):
        QMessageBox.critical(self, "Ошибка действия с заявкой", msg)