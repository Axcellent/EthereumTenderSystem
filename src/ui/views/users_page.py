from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from ui.presenters.user_presenter import UsersPresenter
from models.common import addr, pkey
from models.users_dto import UserCreateDTO
from pydantic import ValidationError

class RegistrationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Регистрация в GTS")

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

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.address_in = QLineEdit()
        self.address_in.setPlaceholderText("Введите адрес пользователя GTS")
        form.addRow("Пользователь", self.address_in)

        self.key_in = QLineEdit()
        self.key_in.setPlaceholderText("Введите модерационный ключ")
        form.addRow("Код подтверждения", self.key_in)

        layout.addWidget(form)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(button_box)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)


class UserPage(QWidget):
    def __init__(
        self,
        presenter: UsersPresenter,
        parent=None
    ):
        super().__init__(parent)
        self.presenter = presenter
        self.user_loaded = False

        layout = QVBoxLayout(self)

        key_gb = QGroupBox("Идентификатор в сети")
        key_gb_l = QVBoxLayout(key_gb)
        key_field_l = QFormLayout()
        key_actions_l = QHBoxLayout()
        key_gb_l.addLayout(key_field_l)
        key_gb_l.addLayout(key_actions_l)

        self.key_in = QLineEdit()
        self.key_in.setPlaceholderText("Введите ваш приватный ключ")
        key_field_l.addRow("Приватный ключ", self.key_in)

        self.save_key_btn = QPushButton("↑ Сохранить")
        self.save_key_btn.clicked.connect(self._save_key)
        self.save_key_btn.setToolTip("Сохранить ключ в оперативной памяти")
        self.register_btn = QPushButton("⁜ Регистрация")
        self.register_btn.setToolTip("Зарегитстрироваться в системе по адресу из ключа")
        self.register_btn.clicked.connect(self._register)
        self.load_user_btn = QPushButton("↓ Авторизация")
        self.load_user_btn.setToolTip("Получить из GTS данные о пользователе по адресу из ключа")
        self.load_user_btn.clicked.connect(self._load_user)
        key_actions_l.addWidget(self.save_key_btn)
        key_actions_l.addWidget(self.register_btn)
        key_actions_l.addWidget(self.load_user_btn)

        user_gb = QGroupBox("Профиль")
        key_gb_l = QVBoxLayout(user_gb)

        self.user_info_field = QWidget()
        if self.user_loaded:
            pass
        else:
            self.user_info_field = QLabel("Нет данных")

        layout.addWidget(key_gb, stretch=1)
        layout.addWidget(user_gb, stretch=2)

    def _save_key(self):
        pass

    def _load_user(self):
        self.user_loaded = True

    def _register(self):
        dialog = RegistrationDialog()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            print(dialog.get_data().model_dump_json())            
        else:
            print("Пользователь отменил")