
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import base58
import requests
import random
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message
from solders.instruction import Instruction
from solders.hash import Hash
from typing import List
from solders.transaction import VersionedTransaction
from solders.pubkey import Pubkey
from solders.keypair import Keypair 

@dataclass
class BundleStatus:
    bundle_id: str
    transactions: List[str]
    slot: int
    confirmation_status: str
    err: Dict[str, Any]


@dataclass
class BundleStatusesResponse:
    context_slot: int
    statuses: List[BundleStatus] = field(default_factory=list)


class Searcher:
    def __init__(self, block_engine_url: str):
        self.block_engine_url = block_engine_url

    @staticmethod
    def _extract_result(response: Dict[str, Any], method: str) -> Any:
        if 'result' in response:
            return response['result']
        else:
            raise Exception(f"Error in {method} response: {response}")

    def _send_rpc_request(self, endpoint: str, method: str, params: Optional[List] = None) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or []
            
        }
        try:
            # url = f"{self.block_engine_url}/{endpoint}"
            url = f"{self.block_engine_url.rstrip('/')}/{endpoint.lstrip('/')}"
            
            response = requests.post(url=url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"HTTP request failed: {e}")
        except ValueError as e:
            raise Exception(f"Invalid JSON response: {e}")

    def get_bundle_statuses(self, bundle_ids: List[str]) -> BundleStatusesResponse:
        """
        Returns the status of submitted bundle(s).

        :param bundle_ids: An array of bundle ids to confirm, as base-58 encoded strings (up to a maximum of 5).
        :return: A BundleStatusesResponse object containing the context slot and a list of BundleStatus objects.
        """
        response = self._send_rpc_request("/api/v1/bundles", "getBundleStatuses", [bundle_ids])
        result = self._extract_result(response, "getBundleStatuses")
        context_slot = result['context']['slot']
        statuses = [
            BundleStatus(
                bundle_id=status['bundle_id'],
                transactions=status['transactions'],
                slot=status['slot'],
                confirmation_status=status['confirmation_status'],
                err=status['err']
            )
            for status in result['value']
        ]
        return BundleStatusesResponse(context_slot=context_slot, statuses=statuses)

    def get_tip_accounts(self) -> List[str]:
        """
        Retrieves the tip accounts designated for tip payments for bundles.

        :return: Tip accounts as a list of strings.
        """
        response = self._send_rpc_request("/api/v1/bundles", "getTipAccounts")
        return self._extract_result(response, "getTipAccounts")

    def send_bundle(self, transactions: List[str]) -> str:
        """
        Submits a bundled list of signed transactions (base-58 encoded strings) to the cluster for processing.

        :param transactions: Fully-signed transactions, as base-58 encoded strings (up to a maximum of 5).
                             Base-64 encoded transactions are not supported at this time.
        :return: A bundle ID, used to identify the bundle. This is the SHA-256 hash of the bundle's transaction signatures.
        """
        response = self._send_rpc_request("/api/v1/bundles", "sendBundle", [transactions])
        return self._extract_result(response, "sendBundle")

    def send_transaction(self, transaction: str) -> str:
        """
        This method serves as a proxy to the Solana sendTransaction RPC method. It forwards the received transaction as a
        regular Solana transaction via the Solana RPC method and submits it as a bundle. Jito sponsors the bundling and
        provides a minimum tip for the bundle. However, please note that this minimum tip might not be sufficient to get
        the bundle through the auction, especially during high-demand periods. If you set the query parameter bundleOnly=true,
        the transaction will only be sent out as a bundle and not as a regular transaction via RPC.

        :param transaction: First Transaction Signature embedded in the transaction, as base-58 encoded string.
        :return: The result will be the same as described in the Solana RPC documentation. If sending as a bundle was
                 successful, you can get the bundle_id for further querying from the custom header in the response x-bundle-id.
        """
        response = self._send_rpc_request("/api/v1/transactions", "sendTransaction", [transaction])
        return self._extract_result(response, "sendTransaction")


class BlockEngine:
    MAINNET_ADDRESS = {
        "Amsterdam": {
            "block_engine_url": "https://amsterdam.mainnet.block-engine.jito.wtf",
            "shred_receiver_addr": "74.118.140.240:1002",
            "relayer_url": "http://amsterdam.mainnet.relayer.jito.wtf:8100",
        },
        "Frankfurt": {
            "block_engine_url": "https://frankfurt.mainnet.block-engine.jito.wtf",
            "shred_receiver_addr": "145.40.93.84:1002",
            "relayer_url": "http://frankfurt.mainnet.relayer.jito.wtf:8100",
        },
        "York": {
            "block_engine_url": "https://ny.mainnet.block-engine.jito.wtf",
            "shred_receiver_addr": "141.98.216.96:1002",
            "relayer_url": "http://ny.mainnet.relayer.jito.wtf:8100",
        },
        "Tokyo": {
            "block_engine_url": "https://tokyo.mainnet.block-engine.jito.wtf",
            "shred_receiver_addr": "202.8.9.160:1002",
            "relayer_url": "http://tokyo.mainnet.relayer.jito.wtf:8100",
        }

    }
    TESTNET_ADDRESS = {
        "Dallas": {
            "block_engine_url": "https://dallas.testnet.block-engine.jito.wtf",
            "shred_receiver_addr": "147.28.154.132:1002",
            "relayer_url": "http://dallas.testnet.relayer.jito.wtf:8100",
        },

        "York": {
            "block_engine_url": "https://ny.testnet.block-engine.jito.wtf",
            "shred_receiver_addr": "141.98.216.97:1002",
            "relayer_url": "http://nyc.testnet.relayer.jito.wtf:8100",
        },

    }

    # noinspection HttpUrlsUsage
    @staticmethod
    def get_block_engines(network="mainnet") -> dict | None:
        if network == "mainnet":
            return BlockEngine.MAINNET_ADDRESS
        if network == "testnet":
            return BlockEngine.TESTNET_ADDRESS
        return None



class JitoManager:
    
    def __init__(self):
        self.searcher = Searcher("https://mainnet.block-engine.jito.wtf")
        
    async def get_tip_account(self) -> List[Pubkey]:
        return self.searcher.get_tip_accounts()
        
    async def send_bundle(self, transactions: List[VersionedTransaction]): 
        # Конвертируем транзакции в base58
        encoded_transactions = [base58.b58encode(bytes(tr)).decode('ascii') for tr in transactions]

        # Отправляем бандл
        bundle_id = self.searcher.send_bundle(encoded_transactions)
        print("Sent Bundle ID:", bundle_id)
        
        return bundle_id  # Теперь метод возвращает ID бандла
    
    async def get_bundle_statuses(self, bundle_ids: List[str]):
        bundle_statuses = self.searcher.get_bundle_statuses(bundle_ids)
        print("Bundle Statuses:", bundle_statuses)
        return bundle_statuses
    
    async def create_jito_instr(self, sender:Pubkey, jito_tip_amount=1000)->Instruction:
        tip_accounts = await self.get_tip_account()
        jito_tip_account = Pubkey.from_string(random.choice(tip_accounts))

        tip_ix = transfer(TransferParams(
            from_pubkey=sender,
            to_pubkey=jito_tip_account,
            lamports=jito_tip_amount
        ))
        return tip_ix
    
