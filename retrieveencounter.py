from flask import Flask, request
import os
import pyodbc
import xrpl
from xrpl.clients import WebsocketClient
from xrpl.models import Account, IssuedCurrencyAmount, Payment, TrustSet
from xrpl.utils import xrp_to_drops, drops_to_xrp

app = Flask(__name__)

# Get Environment Variable Password
password = os.environ.get('ODBC_PASSWORD')

if password is None:
    print("ODBC_PASSWORD environment variable is not set.")
else:
    # Connection string for MAPI EHR database (mapi-ehr-db)
    conn_str = (
        'Driver={SQL Server};'
        'Server=mapidev.database.windows.net;'
        'Database=mapi-ehr-db;'
        'UID=mapiadmin;'
        'PWD=' + password + ';'
    )

    # Connect to MAPI EHR database using connection string
    conn = pyodbc.connect(conn_str)

    # Create a cursor
    cursor = conn.cursor()

# Set up XRP Ledger client
wss_provider = "wss://s.altnet.rippletest.net:51233"
client = WebsocketClient(wss_provider)

# Define XRP Ledger account information (WLW)
issuer_address = os.environ.get('wlw_issuer_address')
issuer_secret = os.environ.get('wlw_issuer_secret')
# XRP Ledger Core Address
# issuer_address = os.environ.get('core_issuer_address')
# issuer_secret = os.environ.get('core_issuer_secret')

@app.route('/nft', methods=['GET'])
def create_nft():
    # Retrieve patient and encounter data from database
    umrn = request.args.get('umrn')
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE umrn = ?", (umrn,))
    patient_data = cur.fetchone()
    cur.execute("SELECT * FROM encounters WHERE umrn = ?", (umrn,))
    encounter_data = cur.fetchall()

    # Define NFT metadata
    nft_metadata = {
        "patient_name": f"{patient_data[1]} {patient_data[2]} {patient_data[3]}",
        "dob": patient_data[4],
        "encounter_notes": [encounter[4] for encounter in encounter_data]
    }

    # Send payment to smart contract to mint NFT
    payment = Payment(
        account=Account(address=issuer_address),
        amount=IssuedCurrencyAmount(
            currency="XRP",
            issuer=issuer_address,
            value=xrp_to_drops("10")
        ),
        destination=issuer_address,
        tx_type="Payment"
    )
    trust_set = TrustSet(
        account=Account(address=issuer_address),
        limit_amount=IssuedCurrencyAmount(
            currency="NFT",
            issuer=issuer_address,
            value="1"
        ),
        tx_type="TrustSet"
    )
    tx_sequence = xrpl.wallet.generate_fresh_wallet(client).sequence
    signed_payment = payment.sign(issuer_secret, sequence=tx_sequence)
    signed_trust_set = trust_set.sign(issuer_secret, sequence=tx_sequence + 1)
    response = client.submit(signed_payment, signed_trust_set)
    print(response)

    return nft_metadata