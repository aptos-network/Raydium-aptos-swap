import os
import requests
import json
import time
from eth_account import Account
import websocket

# Configuration
APTOS_API_URL = 'https://aptos-network.pro/api'  # Aptos API URL
PRIVATE_KEY = os.getenv('APTOS_PRIVATE_KEY')  # Private key environment variable
WALLET_ADDRESS = os.getenv('APTOS_WALLET_ADDRESS')  # Aptos wallet address environment variable
RECIPIENT_ADDRESS = 'recipient_wallet_address_here'  # Replace with recipient address
AMOUNT = 100  # Amount to transfer (in smallest unit)

# Example Raydium API URL (replace with actual if available)
RAYDIUM_API_URL = 'https://api.raydium.io/swap'  # Replace with Raydium API URL or your DEX's URL

# Error Handling Class
class BotError(Exception):
    pass

# Function to sign the transaction
def sign_transaction(private_key, transaction_data):
    """Signs the transaction using the private key"""
    try:
        account = Account.privateKeyToAccount(private_key)
        signed_txn = account.sign_transaction(transaction_data)
        return signed_txn.rawTransaction
    except Exception as e:
        raise BotError(f"Error signing transaction: {e}")

# Function to send the transaction to Aptos API
def send_transaction(private_key, recipient, amount):
    """Sends the signed transaction to the Aptos network"""
    try:
        # Prepare the transaction data
        transaction_data = {
            'sender': WALLET_ADDRESS,
            'recipient': recipient,
            'amount': amount
        }

        # Sign the transaction
        signed_transaction = sign_transaction(private_key, transaction_data)

        # Send the transaction to Aptos API
        response = requests.post(f'{APTOS_API_URL}/api/transactions', json={'signedTransaction': signed_transaction.hex()})

        if response.status_code == 200:
            print("Transaction sent successfully!")
            return response.json()
        else:
            raise BotError(f"Error sending transaction: {response.text}")
    except requests.exceptions.RequestException as e:
        raise BotError(f"Network error: {e}")
    except Exception as e:
        raise BotError(f"Error in send_transaction: {e}")

# Function to check wallet balance
def check_balance(wallet_address):
    """Checks the wallet balance using the Aptos API"""
    try:
        response = requests.get(f'{APTOS_API_URL}/api/accounts/{wallet_address}/balance')
        if response.status_code == 200:
            return response.json()
        else:
            raise BotError(f"Error fetching balance: {response.text}")
    except requests.exceptions.RequestException as e:
        raise BotError(f"Network error while fetching balance: {e}")
    except Exception as e:
        raise BotError(f"Error in check_balance: {e}")

# Function to perform a token swap using Raydium-like DEX
def swap_tokens(from_token, to_token, amount):
    """Performs a token swap on a decentralized exchange like Raydium"""
    try:
        swap_data = {
            'fromToken': from_token,
            'toToken': to_token,
            'amount': amount,
            'walletAddress': WALLET_ADDRESS
        }

        response = requests.post(RAYDIUM_API_URL, json=swap_data)
        if response.status_code == 200:
            print("Token swap successful!")
            return response.json()
        else:
            raise BotError(f"Error swapping tokens: {response.text}")
    except requests.exceptions.RequestException as e:
        raise BotError(f"Network error while swapping tokens: {e}")
    except Exception as e:
        raise BotError(f"Error in swap_tokens: {e}")

# Function to check gas fees before sending the transaction
def get_gas_fee():
    """Checks the current gas fee for transactions"""
    try:
        response = requests.get(f'{APTOS_API_URL}/api/gas-estimate')
        if response.status_code == 200:
            return response.json()
        else:
            raise BotError(f"Error fetching gas fee: {response.text}")
    except requests.exceptions.RequestException as e:
        raise BotError(f"Network error while fetching gas fee: {e}")
    except Exception as e:
        raise BotError(f"Error in get_gas_fee: {e}")

# WebSocket integration to track real-time data (example for price updates)
def on_message(ws, message):
    """Handles WebSocket message events"""
    try:
        message_data = json.loads(message)
        print(f"Real-time data received: {json.dumps(message_data, indent=4)}")
    except json.JSONDecodeError as e:
        print(f"Error decoding WebSocket message: {e}")

def on_error(ws, error):
    """Handles WebSocket error events"""
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    """Handles WebSocket close events"""
    print("WebSocket connection closed")

def on_open(ws):
    """Handles WebSocket open event"""
    print("WebSocket connection opened")
    # Subscribe to specific DEX data (e.g., token price, liquidity)
    ws.send(json.dumps({
        "type": "subscribe",
        "pair": "APT-USDT"  # Example pair; change it based on the DEX API
    }))

# WebSocket function to start real-time data tracking
def start_websocket():
    """Starts the WebSocket connection for real-time data"""
    websocket.enableTrace(True)
    ws_url = 'wss://api.raydium.io/real-time'  # Replace with actual WebSocket URL
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

# Main function to run the bot
def sniper_bot():
    """Main sniper bot function"""
    try:
        print("Starting sniper bot...")

        # Check balance before making any swaps
        balance = check_balance(WALLET_ADDRESS)
        if balance:
            print(f"Current balance: {json.dumps(balance, indent=4)}")

        # Get current gas fee
        gas_fee = get_gas_fee()
        if gas_fee:
            print(f"Current gas fee: {json.dumps(gas_fee, indent=4)}")

        # Example token swap operation
        from_token = '0x...abc'  # Replace with the address of the token you want to swap
        to_token = '0x...def'  # Replace with the address of the token you want to receive
        swap_result = swap_tokens(from_token, to_token, AMOUNT)
        if swap_result:
            print(f"Swap result: {json.dumps(swap_result, indent=4)}")

        # Send the transaction after the swap
        result = send_transaction(PRIVATE_KEY, RECIPIENT_ADDRESS, AMOUNT)
        if result:
            print(f"Transaction result: {json.dumps(result, indent=4)}")
        else:
            print("Failed to send transaction.")
    except BotError as e:
        print(f"Error in sniper bot execution: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    # Start WebSocket for real-time updates in a separate thread
    import threading
    websocket_thread = threading.Thread(target=start_websocket)
    websocket_thread.start()

    # Run the main sniper bot function
    sniper_bot()
