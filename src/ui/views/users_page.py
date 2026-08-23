# views/user_page.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton,
                             QMessageBox, QDialog, QFormLayout, QLineEdit, QTextEdit,
                             QDialogButtonBox)
from PyQt6.QtCore import pyqtSignal
from ui.presenters.user_presenter import UsersPresenter
from models.users_dto import UserCreateDTO
from pydantic import ValidationError

class RegistrationDialog(QDialog):
    """Диалог для ввода данных нового пользователя."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация пользователя")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_edit = QLineEdit()
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.cities_edit = QLineEdit(placeholderText="Города через запятую")
        self.phones_edit = QLineEdit(placeholderText="Телефоны через запятую")
        self.emails_edit = QLineEdit(placeholderText="Email через запятую")

        form.addRow("Название организации:", self.title_edit)
        form.addRow("Описание:", self.description_edit)
        form.addRow("Города:", self.cities_edit)
        form.addRow("Телефоны:", self.phones_edit)
        form.addRow("Email:", self.emails_edit)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self) -> dict:
        """Возвращает словарь с данными формы."""
        return {
            'title': self.title_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'cities': [c.strip() for c in self.cities_edit.text().split(',') if c.strip()],
            'telephones': [t.strip() for t in self.phones_edit.text().split(',') if t.strip()],
            'emails': [e.strip() for e in self.emails_edit.text().split(',') if e.strip()],
        }

class UserPage(QWidget):
    def __init__(self, presenter: UsersPresenter, parent=None):
        super().__init__(parent)
        self.presenter = presenter
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        self.info_group = QGroupBox("Информация о пользователе")
        info_layout = QVBoxLayout(self.info_group)
        self.user_info_label = QLabel("Нет данных")
        info_layout.addWidget(self.user_info_label)

        buttons_layout = QVBoxLayout()
        self.load_profile_button = QPushButton("Загрузить профиль")
        self.reputation_button = QPushButton("Показать репутацию")
        self.register_button = QPushButton("Регистрация нового пользователя")
        buttons_layout.addWidget(self.load_profile_button)
        buttons_layout.addWidget(self.reputation_button)
        buttons_layout.addWidget(self.register_button)

        layout.addWidget(self.info_group)
        layout.addLayout(buttons_layout)

    def _connect_signals(self):
        self.register_button.clicked.connect(self._on_register_clicked)

        self.presenter.register_finished.connect(self._on_registration_finished)
        self.presenter.error.connect(self._on_error)

    def _on_register_clicked(self):
        dialog = RegistrationDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                user_dto = UserCreateDTO(**data)
            except ValidationError as e:
                QMessageBox.critical(self, "Ошибка данных", str(e))
                return
            self.presenter.register(user_dto)

    def _on_registration_finished(self, tx_receipt):
        QMessageBox.information(self, "Успех", f"Пользователь зарегистрирован. Tx: {tx_receipt.transactionHash.hex()}")

    def _on_error(self, error_msg: str):
        QMessageBox.critical(self, "Ошибка", error_msg)