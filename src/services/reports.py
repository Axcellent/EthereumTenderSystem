from services import TxReceipt, BlockchainService

from models.common import (addr,
                           uid,
                           pkey)
from models.reports_dto import ReportCreateDTO, ReportGetDTO

from constants import (CREATE_REPORT,
                       REVIEW_REPORT,
                       GET_REPORTS,
                       GET_REPORT)

class ReportsService():
    @staticmethod
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

    @staticmethod
    def review_report(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        report_id: uid,
        accept: bool,
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = REVIEW_REPORT,
            args = [report_id, accept] 
        )

    @staticmethod
    def get_report(
        service: BlockchainService,
        report_id: uid,
    ) -> ReportGetDTO:
        data = service.view(GET_REPORT, [report_id])

        return ReportGetDTO(
            contract_id=data[0],
            reporter=data[1],
            description=data[2],
            status=data[3]
        )
    
    @staticmethod
    def get_contract_reports(
        service: BlockchainService,
        contract_id: uid
    ) -> list[ReportGetDTO]:
        reports = service.view(GET_REPORTS, [contract_id])

        data = []
        for report_id in reports:
            data.append(ReportsService.get_report(
                service,
                report_id
            ))

        return data