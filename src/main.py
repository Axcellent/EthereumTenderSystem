from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = ROOT_DIR / "abi.json"

from api.tenders import TendersManager, CreateTenderDTO, TenderGetFullDTO
from api.users import UserManager, UserCreateDTO
from api.bids import BidManager, BidCreateDTO
from api import BlockchainService

service = BlockchainService(
    provider_url="http://127.0.0.1:7545",
    contract_address="0x4556c7dAF9FA0171bd21b47DE164Ac9d31094642",
    contract_abi_file=CONFIG_PATH
)

import datetime

time2 = datetime.datetime(2026,8,6,12,55,0)

tender = CreateTenderDTO(
    title="Moscow's roads project",
    description="Build some roads (#121, #710.1, #156) and fix other",
    budget=1_000_000_000,
    deadline=datetime.datetime(2027,8,6,12,59,0),
    bidding_deadline=datetime.datetime.now() + datetime.timedelta(seconds=10),
    parent_id=0
)

bid1 = BidCreateDTO(
    tender_id=12   , 
    price=1_000_000,
    deadline=datetime.datetime(2027,8,6,12,50,0),
)

bid2 = BidCreateDTO(
    tender_id=12    ,
    price=5_000_000,
    deadline=datetime.datetime(2027,6,6,12,50,0),
)

bid3 = BidCreateDTO(
    tender_id=12    ,
    price=2_000_000,
    deadline=datetime.datetime(2028,8,6,12,50,0),
)

try:
    TendersManager.create_tender(
        service,
        "0xcbF67D7ee3823fe06CAaC60337C7c6d757351669",
        "0x622c5d96e79cc7ed7ae0c43dacdfb42bf7f97db678e3da0e26080ededd82ad84",
        tender
        )

    t = TendersManager.get_tender_full(service, 12)
    print(t.model_dump_json().replace('{','{\n\t').replace(',"',',\n\t"').replace('}','\n}'))

    
except Exception as e:
    print(str(e))

