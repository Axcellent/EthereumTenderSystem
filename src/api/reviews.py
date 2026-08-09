from api import TxReceipt, BlockchainService

from models.common import (addr,
                           pkey)
from models.reviews_dto import ReviewGetDTO, ReviewCreateDTO

from constants import (CREATE_REVIEW,
                       EXAMINE_REVIEW,
                       GET_REVIEW)

class ReviewsManager():
    @staticmethod
    def submit_review(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        review_data: ReviewCreateDTO
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = CREATE_REVIEW,
            args = review_data.model_dump().values(),
        )

    @staticmethod
    def examine_review(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        review_id: int,
        accept: bool
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = EXAMINE_REVIEW,
            args = [review_id, accept] 
        )
    
    @staticmethod
    def get_review(
        service: BlockchainService,
        review_id: int
    ) -> ReviewGetDTO:
        data = service.view(GET_REVIEW, review_id)

        return ReviewGetDTO(
            contractId=data[0],
            review_from=data[1],
            review_to=data[2],
            rating=data[3],
            comment=data[4],
            status=data[5]
        )