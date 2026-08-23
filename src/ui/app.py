from PyQt6.QtWidgets import *

from ui.utils.state import AppState, BlockchainService, BlockchainUser
from ui.views.users_page import UserPage, UsersPresenter

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__(None)

        self.app_state = AppState()
        self.app_state.service = BlockchainService("http://127.0.0.1:7545", "0x5A2b41B9e49F7e79fA07dD2F75534a682830AD81", "src/abi.json")    

        self.setWindowTitle("First App")
        self.setGeometry(0,0,600,800)

        central = QTabWidget()
        users_presenter = UsersPresenter(self.app_state)
        users = UserPage(users_presenter, central)

        central.addTab(users, "Users")

        temp = QWidget()
        central.addTab(temp, "Temp")
        self.setCentralWidget(central)
        layout = QVBoxLayout(temp)

        self.main_label = QLabel("Hello world!")
        self.main_label.setText(self.app_state.service.web3.provider.make_request('evm_snapshot', [])['result'])

        self.button = QPushButton("save")
        self.button.clicked.connect(self.show_msg)

        self.line = QLineEdit()
        self.line.setPlaceholderText("Enter secret phrase")
        self.line.setEchoMode(QLineEdit.EchoMode.Password)

        self.id = QLineEdit()
        self.id.setPlaceholderText("reset blockchain on snapshot")
        self.obyt = QPushButton("reset")
        self.obyt.clicked.connect(self.oioi)

        self.button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.obyt.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.main_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.id.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout.addWidget(self.main_label, stretch=1)
        layout.addStretch(1)
        layout.addWidget(self.line, stretch=1)    
        layout.addStretch(1)
        layout.addWidget(self.button, stretch=1)
        layout.addStretch(1)
        layout.addWidget(self.obyt, stretch=1)
        layout.addStretch(1)
        layout.addWidget(self.id, stretch=1)
        

    def show_msg(self):
        txt: str = self.line.text()        
        self.app_state.user = BlockchainUser(address="0xFAD196800A9bBaa7bb05AA1226f45D1D5e0aCb8C", 
                                             key="0xbe4dcea404c36f180fa674dfdcdc2d110b91d6c279be2ba5049f9acf49afdc56")
        t = QMessageBox.information(self, "Some title", f"this is a button, your text id: {txt}")

    def oioi(self):        
        self.app_state.service.web3.provider.make_request('evm_revert', [1])
    