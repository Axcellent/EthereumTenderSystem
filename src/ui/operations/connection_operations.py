from ui.operations import Operation
from ui.utils.state import AppState

class ConnectOperation(Operation):
    def __init__(
        self,
        app_state: AppState,
        url: str,
        contract: str
    ):
        self.url = url
        self.contract = contract
        self.app_state = app_state

    def execute(self):        
        self.app_state.setService(self.url, self.contract)
