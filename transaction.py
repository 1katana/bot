from solders.hash import Hash
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.message import MessageV0
from solders.system_program import TransferParams, transfer
from solders.transaction import VersionedTransaction



def Transaction(sender: Keypair,receiver:Pubkey,lamports: int,blockhash: Hash):

    ix = transfer(
        TransferParams(
            from_pubkey=sender.pubkey(), to_pubkey=receiver, lamports=lamports
        )
    )

    msg = MessageV0.try_compile(
        payer=sender.pubkey(),
        instructions=[ix],
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash,
    )
    tx = VersionedTransaction(msg, [sender])
    
    return tx