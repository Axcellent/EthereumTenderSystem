from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from ui.presenters.user_presenter import UsersPresenter
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
        self.admin_cb = QCheckBox("Показывать функции модераторов")
        self.admin_cb.checkStateChanged.connect(self._show_admin_funcs)
        key_gb_l.addWidget(self.admin_cb)
        admin_l = QHBoxLayout()
        key_gb_l.addLayout(admin_l)
        self.ban_btn = QPushButton("× Заблокировать")
        self.ban_btn.clicked.connect(self._ban_user)
        self.ban_btn.setToolTip("Заблокировать пользователя по адресу (только админ)")
        admin_l.addWidget(self.ban_btn)
        self.delete_btn = QPushButton("※ Удаление")
        self.delete_btn.clicked.connect(self._delete_user)
        self.delete_btn.setToolTip("Удалить пользователя по адресу (только админ)")
        admin_l.addWidget(self.delete_btn)
        self.unban_btn = QPushButton("⁙ Разблокировать")
        self.unban_btn.clicked.connect(self._unban_user)
        self.unban_btn.setToolTip("Разблокировать пользователя по адресу (только админ)")
        admin_l.addWidget(self.unban_btn)
        self._show_admin_funcs()
        

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

        backup_l = QHBoxLayout()
        key_gb_l.addLayout(backup_l)
        self._backup_btn = QPushButton("CREATE BACKUP")
        self._backup_btn.clicked.connect(self._CREATE_BACKUP)
        self._goto_btn = QPushButton("GOTO BACKUP")
        self._goto_btn.clicked.connect(self._GOTO_BACKUP)
        backup_l.addWidget(self._goto_btn)
        backup_l.addWidget(self._backup_btn)

        self.user_gb = QGroupBox("Профиль")
        user_l = QGridLayout(self.user_gb)

        self.title_lbl = QLabel("не указано")
        self.title_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.description_lbl = QLabel("не указано")
        self.description_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.description_lbl.setWordWrap(True)
        self.cities_lbl = QLabel("не указано")
        self.cities_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.telephones_lbl = QLabel("не указано")
        self.telephones_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.emails_lbl = QLabel("не указано")
        self.emails_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        user_l.addWidget(QLabel("НАЗВАНИЕ"), 0, 0)
        user_l.addWidget(self.title_lbl, 0, 1)
        user_l.addWidget(QLabel("ОПИСАНИЕ"), 1, 0)
        user_l.addWidget(self.description_lbl, 1, 1)
        user_l.addWidget(QLabel("ФИЛИАЛЫ"), 2, 0)
        user_l.addWidget(self.cities_lbl, 2, 1)
        user_l.addWidget(QLabel("ТЕЛЕФОНЫ"), 3, 0)
        user_l.addWidget(self.telephones_lbl, 3, 1)
        user_l.addWidget(QLabel("ПОЧТЫ"), 4, 0)
        user_l.addWidget(self.emails_lbl, 4, 1)

        user_l.setColumnStretch(0, 1)
        user_l.setColumnStretch(1, 3)

        layout.addWidget(key_gb, stretch=1)
        layout.addWidget(self.user_gb, stretch=2)

        self.presenter.get_user_finished.connect(self._load_user_finished)
        self.presenter.register_finished.connect(self._register_finished)
        self.presenter.error_occured.connect(self._on_error)
        self.presenter.app_state.user_changed.connect(self._key_save_finished)
        self.presenter.admin_action_finished.connect(self._admin_op_finished)

    def _CREATE_BACKUP(self):        
        print(self.presenter.app_state.service.web3.provider.make_request('evm_snapshot', [])['result'])

    def _GOTO_BACKUP(self):
        self.presenter.app_state.service.web3.provider.make_request('evm_revert', [1])
        print('backuped to 0x1')


    def _save_key(self):
        try:
            self.presenter.app_state.setUser(self.key_in.text())
        except Exception as e:
            self._on_error(str(e))

    def _key_save_finished(self):
        QMessageBox.information(self, "Аккаунт сети", "Ваш приватный ключ был успешно сохранен в оперативной памяти устройства")

    def _load_user(self):
        self.presenter.get_user_data()

    def _load_user_finished(self, data: UserGetFullDTO):        
        print(data)

        self.title_lbl.setText(f"{data.title}")
        self.description_lbl.setText(f"{data.description}")
        self.cities_lbl.setText(f"{', '.join(data.cities)}")
        self.telephones_lbl.setText(f"{', '.join(data.telephones)}")
        self.emails_lbl.setText(f"{', '.join(data.emails)}")
        self.user_loaded = True

    def _register(self):
        dialog = RegistrationDialog()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_data()
                self.presenter.register(data)
            except Exception as e:
                self._on_error(str(e))       

    def _register_finished(self) :
        QMessageBox.information(self, "Успешная регистрация", "Вы успешно зарегистирировали свою организацию в GTS!")

    def _on_error(self, msg: str):
        QMessageBox.critical(self, "Ошибка профилей", msg)

    def _show_admin_funcs(self):
        cur = self.admin_cb.isChecked()
        if cur:
            self.ban_btn.show()
            self.unban_btn.show()
            self.delete_btn.show()
        else:
            self.ban_btn.hide()
            self.unban_btn.hide()
            self.delete_btn.hide()

    def _ban_user(self):
        dialog = AdminActionDialog()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            try:
                address, reason = dialog.get_data()
                self.presenter.ban_user(address, reason)
            except Exception as e:
                self._on_error(str(e))

    def _delete_user(self):
        dialog = AdminActionDialog()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            try:
                address, reason = dialog.get_data()
                self.presenter.delete_user(address, reason)
            except Exception as e:
                self._on_error(str(e))

    def _unban_user(self):
        dialog = AdminActionDialog()
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            try:
                address, reason = dialog.get_data()
                self.presenter.unban_user(address, reason)
            except Exception as e:
                self._on_error(str(e))

    def _admin_op_finished(self):
        QMessageBox.information(self, "Успешное действие", "Изменение в GTS внесено")