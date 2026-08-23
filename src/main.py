import sys

from PyQt6.QtWidgets import QApplication
from ui.app import MainApp

from services import BlockchainService

def main():
    app = QApplication(sys.argv)

    window = MainApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()