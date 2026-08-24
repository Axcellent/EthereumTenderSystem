from ui.operations import (BlockchainOperation,
                                BlockchainUser,
                                BlockchainService)

from models.common import (uint,
                           addr,
                           pkey)

from services.users import (UsersService,
                            UserCreateDTO)

class RegisterUserOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        data: UserCreateDTO
    ):
        super().__init__(service, user)
        self.data: UserCreateDTO = data

    def execute(self):
        return UsersService.register(
            self.service,
            self.address,
            self.key,
            self.data
        )


class GetUserOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        address=None
    ):
        super().__init__(service, user)   
        self.other_address = address   

    def execute(self):
        return UsersService.get_user_full(
            self.service,
            self.other_address if self.other_address is not None else self.address
        )

class BanUserOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        address: addr,
        comment: str
    ):
        super().__init__(service, user)
        self.address: addr = address
        self.comment: str = comment

    def execute(self):
        return UsersService.ban_user(
            self.service,
            self.address,
            self.key,
            self.address,
            self.comment
        )

class UnbanUserOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        address: addr,
        comment: str
    ):
        super().__init__(service, user)
        self.address: addr = address
        self.comment: str = comment

    def execute(self):
        return UsersService.unban_user(
            self.service,
            self.address,
            self.key,
            self.address,
            self.comment
        )

class DeleteUserOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        address: addr,
        comment: str
    ):
        super().__init__(service, user)
        self.address: addr = address
        self.comment: str = comment

    def execute(self):
        return UsersService.delete_user(
            self.service,
            self.address,
            self.key,
            self.address,
            self.comment
        )
