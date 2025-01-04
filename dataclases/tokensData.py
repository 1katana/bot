from solders.rpc.responses import GetTokenAccountsByOwnerJsonParsedResp
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TokenAmount:
    amount: int
    decimals: int
    uiAmount: float
    uiAmountString: str

@dataclass
class TokenInfo:
    mint: str
    token_amount: TokenAmount

@dataclass
class TokensData:
    slot: int
    tokens: List[TokenInfo]

def parse_rpc_response(data: GetTokenAccountsByOwnerJsonParsedResp) -> TokensData:
    # Извлекаем слот
    slot = data.context.slot
    
    # Извлекаем список токенов
    tokens = []
    for account in data.value:
        account_data = account.account.data.parsed["info"]
        
        # Парсим токеновые данные
        token_amount_data = account_data["tokenAmount"]
        token_amount = TokenAmount(
            amount=int(token_amount_data["amount"]),
            decimals=int(token_amount_data["decimals"]),
            uiAmount=float(token_amount_data["uiAmount"]),
            uiAmountString=token_amount_data["uiAmountString"]
        )
        
        mint = account_data["mint"]
        tokens.append(TokenInfo(mint=mint, token_amount=token_amount))
    
    return TokensData(slot=slot, tokens=tokens)