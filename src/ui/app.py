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

        bar = self.statusBar().addWidget(QLabel("Не подключено"))
        self.setStatusBar(bar)