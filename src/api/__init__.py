from web3 import Web3
from web3.types import TxParams, TxReceipt
from web3.exceptions import Web3RPCError
from web3.contract.contract import ContractFunction, Contract
from eth_typing import ChecksumAddress
from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from typing import Any
import json

class BlockchainService:
    def __init__(
        self,
        provider_url: str,
        contract_address: str,
        contract_abi_file: str
    ):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.web3 or not self.web3.is_connected():
            raise ConnectionError("Unable to connect to provider")

        self.chain_id: int = self.web3.eth.chain_id

        self.contract_address: ChecksumAddress = self.web3.to_checksum_address(contract_address)

        with open(contract_abi_file, "r") as f:
            contract_abi: list[dict] = json.load(f)

        self.contract: Contract = self.web3.eth.contract(
            address=self.contract_address,
            abi=contract_abi
        )

        if not self.contract:
            raise ConnectionError("Unable to find contract")

    def send_tx(
        self,
        address_from: str,
        key: str,
        function_name: str,
        args: list,
        value: int = 0,
        gas: int = 600000,
        gas_price_gwei: int = 1
    ) -> TxReceipt:
        address_from: ChecksumAddress = self.web3.to_checksum_address(address_from)
        func: ContractFunction = getattr(self.contract.functions, function_name)

        if not func:
            raise NameError(f"Function {function_name} does not exist")

        if value:
            tx: TxParams = func(*args).build_transaction({
                'chainId': self.chain_id,
                'gas': gas,
                'gasPrice': self.web3.to_wei(gas_price_gwei, 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(address_from),
                'value': value
            })
        else:
            tx: TxParams = func(*args).build_transaction({
                'chainId': self.chain_id,
                'gas': gas,
                'gasPrice': self.web3.to_wei(gas_price_gwei, 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(address_from)
            })

        signed_tx: SignedTransaction = self.web3.eth.account.sign_transaction(tx, key)    

        try:
            tx_hash: HexBytes = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            rx: TxReceipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

            if rx["status"] == 0:
                try:
                    self.web3.eth.call({
                        'from': address_from,
                        'to': self.contract_address,
                        'data': tx["data"]
                    })
                except Exception as e:
                    raise RuntimeError(f"Transaction reverted: {str(e)}")
        except Web3RPCError as we:
            st = we.message.find("revert") + 7
            end = we.message.find("', '")
            raise RuntimeError(we.message[st:end])
        except Exception as e:
            raise RuntimeError(str(e))


        return rx

    def view(
        self,
        function_name,
        *args
    ) -> Any:        
        func: ContractFunction = getattr(self.contract.functions, function_name)
        return func(*args).call()

