from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = ROOT_DIR / "abi.json"

from api.tenders import TendersManager, CreateTenderDAO, TenderGetFullDTO
from api.users import UserManager, UserCreateDTO
from api import BlockchainService

service = BlockchainService(
    provider_url="http://127.0.0.1:7545",
    contract_address="0x4556c7dAF9FA0171bd21b47DE164Ac9d31094642",
    contract_abi_file=CONFIG_PATH
)

import datetime

time2 = datetime.datetime(2026,8,6,12,55,0)

tender = CreateTenderDAO(
    title="Rostov's roads project",
    description="Build some roads (#12, #10.1, #152) and fix other",
    budget=1_000_000,
    deadline=datetime.datetime(2027,8,6,12,59,0),
    bidding_deadline=datetime.datetime.now() + datetime.timedelta(minutes=1),
    parent_id=0
)

"""TendersManager.create_tender(
    service,
    "0xcbF67D7ee3823fe06CAaC60337C7c6d757351669",
    "0x622c5d96e79cc7ed7ae0c43dacdfb42bf7f97db678e3da0e26080ededd82ad84",
    tender
    )"""

user = UserCreateDTO(
    title="OOO OOA",
    description="Super cool company with no-good sreputation",
    cities=["Taganrog","Rostov-On-Don"],
    telephones=["89286235732","+7 (928) 623-57-32"],
    emails=["ooo@mail.ru","ooa@mail.ru"],
)

# UserManager.register(
#     service,
#     "0xfCDa431D7313a876A5D56E52D35C89093CF4cdE9",
#     "0xe6d51f1822c7887edc6c58afa679d2ba3e3b02a5b5be23b84a8e9eb92ac1c3fa",
#     user
# )

t: TenderGetFullDTO = TendersManager.get_tender_full(service, 1) 
print(t.model_dump_json().replace('{','{\n\t').replace(',"',',\n\t"').replace('}','\n}'))

TendersManager.revert_tender(
    service,
    "0xcbF67D7ee3823fe06CAaC60337C7c6d757351669",
    "0x622c5d96e79cc7ed7ae0c43dacdfb42bf7f97db678e3da0e26080ededd82ad84",
    [1]
    )
t = TendersManager.get_tender_full(service, 1) 
print(t.model_dump_json().replace('{','{\n\t').replace(',"',',\n\t"').replace('}','\n}'))