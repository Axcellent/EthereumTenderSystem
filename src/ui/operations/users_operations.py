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
        data: addr
    ):
        super().__init__(service, user)
        self.data: addr = data

    def execute(self):
        return UsersService.get_user_full(
            self.service,
            self.address,
            self.key,
            self.data
        )
