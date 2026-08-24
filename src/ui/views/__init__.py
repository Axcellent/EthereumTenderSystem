from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton,
                             QMessageBox, QDialog, QFormLayout, QLineEdit, QTextEdit,
                             QDialogButtonBox)
from PyQt6.QtCore import pyqtSignal
from ui.presenters.user_presenter import UsersPresenter
from models.users_dto import UserCreateDTO
from pydantic import ValidationError

from abc import ABC, abstractmethod

class BasePage(QWidget):
    error = pyqtSignal(str)
    warn = pyqtSignal(str)

    @abstractmethod
    def _init_ui():
        pass

    @abstractmethod
    def _connect_signals():
        pass

    @abstractmethod
    def _on_error():
        pass

    @abstractmethod
    def _on_warn():
        pass