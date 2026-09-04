from PyQt6.QtWidgets import *

from ui.utils.state import AppState, BlockchainService, BlockchainUser
from ui.views.users_page import UserPage, UsersPresenter
from ui.views.connection_page import ConnectionPage, ConnectionPresenter
from ui.views.main_page import MainPage, TendersPresenter, BidsPresenter
from ui.views.my_page import MyPage, UsersPresenter

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.app_state = AppState()
        users_presenter = UsersPresenter(self.app_state)
        connection_presenter = ConnectionPresenter(self.app_state)
        tenders_presenter = TendersPresenter(self.app_state)
        bids_presenter = BidsPresenter(self.app_state)

        ### Настраиваем главное окно
        self.setWindowTitle("GTS App")
        self.setGeometry(200,100,600,800)
        ### Настраиваем главное окно

        ### Настраиваем контент
        central = QTabWidget()
        self.setCentralWidget(central)
            # Создаем страницы
        users_page = UserPage(users_presenter, central)
        connection_page = ConnectionPage(connection_presenter, central)
        main_page = MainPage(tenders_presenter, bids_presenter, central)
        my_page = MyPage(users_presenter, central)
            # Добавляем страницы
        central.addTab(connection_page, "Подключение")
        central.addTab(users_page, "Профиль")
        central.addTab(main_page, "Главная")
        central.addTab(my_page, "Мое")
        ### Настраиваем контент

        ### Creating statusbar
        self.connection_bar = QLabel("Не подключено")
        self.task_bar = QLabel("Нет задач")
        self.statusBar().addWidget(self.connection_bar)
        self.statusBar().addWidget(self.task_bar)
        ### Creating statusbar

        ### Connecting signals
        self.app_state.service_connected.connect(self._change_connection_bar)
        self.app_state.task_started.connect(self._change_task_bar)
        self.app_state.task_finished.connect(self._clear_task_bar)
        ### Connecting signals

    def _change_connection_bar(self):
        self.connection_bar.setText(str(self.app_state.service.chain_id))

    def _change_task_bar(self, msg: str):
        self.task_bar.setText(msg)

    def _clear_task_bar(self):
        self.task_bar.setText("Нет задач")