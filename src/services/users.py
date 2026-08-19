from services import BlockchainService, TxReceipt
from models.users_dto import UserCreateDTO, UserGetFullDTO, UserGetShortDTO

from models.common import (pkey,
                           addr,                           
                           string)

from constants import (USER_REGISTER, 
                        GET_USER, 
                        GET_REPUTATION, 
                        DELETE_USER, 
                        BAN_USER, 
                        UNBAN_USER)

class UsersService:
    @staticmethod
    def register(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        user_data: UserCreateDTO
    ) -> TxReceipt:
        data = [
            user_data.title,
            user_data.description,
            user_data.cities,
            user_data.telephones,
            user_data.emails
        ]
        
        return service.send_tx(
            address_from,
            key,
            function_name = USER_REGISTER,
            args = data
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
    def get_reputation(
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
        user_addr: addr,
        reason: string
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name = DELETE_USER,
            args = [user_addr, reason]
        )

    @staticmethod
    def ban_user(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        user_addr: addr,
        reason: string
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name = BAN_USER,
            args = [user_addr, reason]
        )

    @staticmethod
    def unban_user(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        user_addr: addr,
        reason: string
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name = UNBAN_USER,
            args = [user_addr, reason]
        )