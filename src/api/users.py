from api import BlockchainService, TxReceipt
from models.users_dto import UserCreateDTO, UserGetFullDTO, UserGetShortDTO

from models.common import pkey, addr, uint

from constants import USER_REGISTER, GET_USER, GET_REPUTATION, DELETE_USER, BAN_USER

class UserManager:
    @staticmethod
    def register(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        user_data: UserCreateDTO
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name = USER_REGISTER,
            args = user_data.model_dump().values()
        )

    @staticmethod
    def get_user_full(
        service: BlockchainService,
        user_addr: addr
    ) -> UserGetFullDTO:
        data = service.view(
            function_name = GET_USER,
            args = [user_addr]
        )

        return UserGetFullDTO(
            title=data[0],
            description=data[1],
            cities=data[2],
            telephones=data[3],
            emails=data[4],
            status=data[5],
        )

    @staticmethod
    def get_user_short(
        service: BlockchainService,
        user_addr: addr
    ) -> UserGetShortDTO:
        data = service.view(
            function_name = GET_USER,
            args = [user_addr]
        )

        return UserGetShortDTO(
            title=data[0],
            status=data[5],
        )

    @staticmethod
    def getReputation(
        service: BlockchainService,
        user_addr: addr
    ) -> int:
        data = service.view(
            function_name = GET_REPUTATION,
            args = [user_addr]
        )

        return data

    @staticmethod
    def delete_user(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        user_addr: addr
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name = DELETE_USER,
            args = [user_addr]
        )

    @staticmethod
    def ban_user(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        user_addr: addr
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name = BAN_USER,
            args = [user_addr]
        )