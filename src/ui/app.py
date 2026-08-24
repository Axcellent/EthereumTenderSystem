from PyQt6.QtWidgets import *

from ui.utils.state import AppState, BlockchainService, BlockchainUser
from ui.views.users_page import UserPage, UsersPresenter
from ui.views.connection_page import ConnectionPage, ConnectionPresenter

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.app_state = AppState()

        self.setWindowTitle("First App")
        self.setGeometry(0,0,600,800)

        central = QTabWidget()
        self.setCentralWidget(central)

        users_presenter = UsersPresenter(self.app_state)
        connection_presenter = ConnectionPresenter(self.app_state)

        users_page = UserPage(users_presenter, central)
        connection_page = ConnectionPage(connection_presenter, central)

        central.addTab(connection_page, "Подключение")
        central.addTab(users_page, "Профиль")

        self.connection_bar = QLabel("Не подключено")
        self.task_bar = QLabel("Нет задач")
        self.app_state.service_connected.connect(self._change_connection_bar)
        self.app_state.task_started.connect(self._change_task_bar)
        self.app_state.task_finished.connect(self._clear_task_bar)

        self.statusBar().addWidget(self.connection_bar)
        self.statusBar().addWidget(self.task_bar)

    def _change_connection_bar(self):
        self.connection_bar.setText(self.app_state.service.chain_id)

    def _change_task_bar(self, msg: str):
        self.task_bar.setText(msg)

    def _clear_task_bar(self):
        self.task_bar.setText("Нет задач")