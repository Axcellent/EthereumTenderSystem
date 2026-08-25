from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

from ui.presenters.connection_presenter import ConnectionPresenter

class ConnectionPage(QWidget):
    def __init__(
            self,
            connection_presenter: ConnectionPresenter,
            parent=None
        ):
        super().__init__(parent)
        self.presenter = connection_presenter

        layout = QVBoxLayout(self)
        self.connection_box = QGroupBox("Подключение")
        self.connection_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.connection_box)

        gb_layout = QVBoxLayout(self.connection_box)

        self.url_lbl = QLabel("Адрес удаленной ноды", parent=self.connection_box)
        self.url_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.url_lbl.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.url_in = QLineEdit(parent=self.connection_box)
        self.url_in.setText("http://127.0.0.1:7545")        
        self.url_in.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.contract_lbl = QLabel("Адрес контракта", parent=self.connection_box)    
        self.contract_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.contract_lbl.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.contract_in = QLineEdit(parent=self.connection_box)
        self.contract_in.setText("0x5d330455cb467dbFCe177F2C2b79F6940187901C")
        self.contract_in.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.connect_btn = QPushButton("Подключиться",parent=self.connection_box)
        self.connect_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        gb_layout.addWidget(self.url_lbl, stretch=0)    
        gb_layout.addWidget(self.url_in, stretch=1)
        gb_layout.addStretch(1)
        gb_layout.addWidget(self.contract_lbl, stretch=0)
        gb_layout.addWidget(self.contract_in, stretch=1)        
        gb_layout.addStretch(1)
        gb_layout.addWidget(self.connect_btn, stretch=1)        

        # con signals
        self.connect_btn.clicked.connect(self._connect)
        self.presenter.error_occured.connect(self._error)
        self.presenter.app_state.service_connected.connect(self._show_successful_conn)        

    def _connect(self):    
        self.presenter.connect(self.url_in.text(), self.contract_in.text())

    def _error(self, msg):
        QMessageBox.critical(self, "Ошибка подключения", msg)

    def _show_successful_conn(self):
        QMessageBox.information(self, "Успешное подключение", "Вы успешно подключились к GTS!")
