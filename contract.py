from xrpl.clients import JsonRpcClient
from xrpl.transaction import (
    safe_sign_and_autofill_transaction,
    send_reliable_submission,
    AccountSet,
    TrustSet,
    Payment,
    TokenCreate,
    Memo,
)
from xrpl.utils import xrp_to_drops

def contract(inputs):
    # Extract input values
    issuer = inputs['issuer']
    token_name = inputs['token_name']
    token_symbol = inputs['token_symbol']
    total_supply = inputs['total_supply']

    # Connect to the XRPL testnet
    client = JsonRpcClient('https://s.altnet.rippletest.net:51234')

    # Create a new token
    token_create_tx = TokenCreate(
        account=issuer,
        token_name=token_name,
        token_symbol=token_symbol,
        total_supply=total_supply,
        flags=0
    )
    token_create_tx.set_sequence(client.get_account_info(issuer)['sequence'])
    signed_tx = safe_sign_and_autofill_transaction(token_create_tx, issuer, client)
    tx_result = send_reliable_submission(signed_tx, client)

    # Disconnect from the XRPL
    client.close()

    # Return the transaction hash
    return tx_result['tx_json']['hash']