from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from ui.presenters.tenders_presenter import TendersPresenter
from models.common import addr, pkey
from models.users_dto import *
from pydantic import ValidationError

class RegistrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Регистрация в GTS")
        self.setParent(parent)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_in = QLineEdit()
        self.title_in.setPlaceholderText("Название Вашей огранизации")
        form.addRow("Название", self.title_in)

        self.description_in = QTextEdit()
        self.description_in.setPlaceholderText("Описание Вашей организации")
        form.addRow("Описание", self.description_in)

        self.cities_in = QLineEdit()
        self.cities_in.setPlaceholderText("Города главных филиалов через запятую")
        form.addRow("Города", self.cities_in)

        self.telephones_in = QLineEdit()
        self.telephones_in.setPlaceholderText("Контактные телефоны через запятую")
        form.addRow("Телефоны", self.telephones_in)

        self.emails_in = QLineEdit()
        self.emails_in.setPlaceholderText("Корпоративные email через запятую")
        form.addRow("Почты", self.emails_in)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addLayout(form)
        layout.addWidget(self.buttons)

    def get_data(self) -> UserCreateDTO:
        return UserCreateDTO(
            title=self.title_in.text(),
            description=self.description_in.toPlainText(),
            cities=self.cities_in.text().split(', '),
            telephones=self.telephones_in.text().split(', '),
            emails=self.emails_in.text().split(', '),
        )


class AdminActionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Управление пользователями")
        self.setGeometry(150,150,600,400)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.address_in = QLineEdit()
        self.address_in.setPlaceholderText("Введите адрес пользователя GTS")
        form.addRow("Пользователь", self.address_in)

        self.reason_in = QLineEdit()
        self.reason_in.setPlaceholderText("Введите причину")
        form.addRow("Комментарий", self.reason_in)

        self.key_in = QLineEdit()
        self.key_in.setPlaceholderText("Введите модерационный ключ")
        form.addRow("Код подтверждения", self.key_in)

        layout.addLayout(form)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def get_data(self) -> addr:
        if self.key_in.text() == "12345":
            return (self.address_in.text(), self.reason_in.text())
        else:
            raise RuntimeError("Wrong passcode")



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
        self.page1 = QLabel("Это страница 1")
        self.stacked.addWidget(self.page1)
        self.page2 = QLabel("Это страница 2")    
        self.stacked.addWidget(self.page2)

        self.btn1 = QPushButton("Тендеры")
        btns_l.addWidget(self.btn1)
        self.btn1.clicked.connect(lambda: self.stacked.setCurrentIndex(0))
        self.btn2 = QPushButton("Показать страницу 2")
        btns_l.addWidget(self.btn2)
        self.btn2.clicked.connect(lambda: self.stacked.setCurrentIndex(1))


