from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana_manager import SolanaManager
import asyncio
from solana_manager import SolanaManager
from transaction import Transaction
import json
from solana.rpc.async_api import AsyncClient



async def main():
    

    receiver=Pubkey.from_string("7n2uZLLzLRQKHQE7X9cXU74oMdCwwAHQmBcm1gkGc1HK")


    
    
    manager= await SolanaManager.create(api_url="http://localhost:8899")

    manager.add_master_wallet_from_json("C:\\Users\\Katana\\Desktop\\bot\\wallet1.json")

    sender=manager.master_wallet

    blockHash= await manager.get_latest_blockhash()


        
    trans=Transaction(sender,receiver,1_000_000_000,blockHash.value.blockhash)

    print(trans)

    isTrue= await manager.send_transaction(txn=trans)

    print(isTrue)

    b= await manager.get_balance()

    print()


asyncio.run(main())

