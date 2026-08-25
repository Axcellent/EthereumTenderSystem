from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from ui.presenters.user_presenter import UsersPresenter
from models.common import addr, pkey
from models.users_dto import *
from pydantic import ValidationError


class MyPage(QWidget):
    def __init__(
        self,
        presenter: UsersPresenter,
        parent=None
    ):
        super().__init__(parent)
        self.presenter = presenter
        self.user_loaded = False

        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        