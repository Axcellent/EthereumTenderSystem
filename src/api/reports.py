from api import TxReceipt, BlockchainService

from models.common import addr, uint, pkey
from models.reports_dto import ReportCreateDTO, ReportGetDTO

from constants import CREATE_REPORT, REVIEW_REPORT, GET_REPORTS

class ReportsManager():
    def create_report(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        report_data: ReportCreateDTO
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = CREATE_REPORT,
            args = report_data.model_dump().values(),
        )

    def review_report(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        report_id: uint,
        accept: bool,
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = REVIEW_REPORT,
            args = [report_id, accept] 
        )
    

    def get_contract_reports(
        service: BlockchainService,
        contract_id: uint
    ) -> list[ReportGetDTO]:
        data = service.view(GET_REPORTS, contract_id)

        return [ReportGetDTO(
            contract_id=contract_id,
            description=d[1],
            status=d[2]
        ) for d in data]