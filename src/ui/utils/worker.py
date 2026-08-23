from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject

from ui.operations import Operation, BlockchainOperation

class BlockchainWorker(QObject):
    finished = pyqtSignal(object)
    error = pyqtSignal(Exception)

    def __init__(
        self,
        operation: Operation
    ):
        super().__init__()
        self.operation = operation
        

    @pyqtSlot()
    def run(self):
        try:        
            res = self.operation.execute()
            self.finished.emit(res)
        except Exception as e:
            self.error.emit(e)
            # GOV
            # 80000000000