from api import BlockchainService
from models.users_dto import UserCreateDTO

class UserManager:
    def register(
        service: BlockchainService,
        address_from: str,
        key: str,
        user_data: UserCreateDTO
    ):
        return service.send_tx(
            address_from,
            key,
            function_name = "register",
            args = user_data.model_dump().values()
        )

    def get_user_short(
        service: BlockchainService,
        address_from: str,
        key: str,
        user_data: UserCreateDTO
    ):
        return service.send_tx(
            address_from,
            key,
            function_name = "register",
            args = user_data.model_dump().values()
        )

    def get_user_full(
        service: BlockchainService,
        address_from: str,
        key: str,
        user_data: UserCreateDTO
    ):
        return service.send_tx(
            address_from,
            key,
            function_name = "register",
            args = user_data.model_dump().values()
        )
    def delete_user(
        service: BlockchainService,
        address_from: str,
        key: str,
        user_data: UserCreateDTO
    ):
        return service.send_tx(
            address_from,
            key,
            function_ыname = "register",
            args = user_data.model_dump().values()
        )

    def ban_user(
        service: BlockchainService,
        address_from: str,
        key: str,
        user_data: UserCreateDTO
    ):
        return service.send_tx(
            address_from,
            key,
            function_name = "register",
            args = user_data.model_dump().values()
        )