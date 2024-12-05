wss_url="wss://api.mainnet-beta.solana.com"
http_url="https://api.mainnet-beta.solana.com"

manager = SolanaWebSocketManager(wss_url)

http_manager=SolanaHttpManager(http_url)


async def handler(messages):
    print(messages)
    res=await http_manager.get_account_info("GYMdqGcyJF8Knzxpr3J1v6LoJzxr2LeybPj7HyotGupH",messages[0].result.context.slot)
    print(res)
