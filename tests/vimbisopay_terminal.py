import json
import logging
import requests
import os
from pathlib import Path
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Import configuration
try:
    from avatar.app.config import VIMBISO_PAY_API_URL, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_ACCESS_TOKEN
    logging.info("Successfully imported configuration from avatar.app.config")
except ImportError as e:
    logging.error(f"Failed to import config: {e}")
    VIMBISO_PAY_API_URL = os.environ.get('VIMBISO_PAY_API_URL')
    WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
    WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN')
    logging.info(f"Using environment variables for configuration")

# Get GitHub token from environment
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    logging.warning("GITHUB_TOKEN not found in environment variables")

class WhatsAppSimulator:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.base_url = VIMBISO_PAY_API_URL.strip()
        self.endpoint = f"{self.base_url}whatsapp/webhook"
        self.auth_token = WHATSAPP_ACCESS_TOKEN

    def send_message(self, message):
        """Send a WhatsApp message to the Vimbiso-Pay endpoint"""
        timestamp = int(time.time())
        payload = {
            "object": "whatsapp_business_account",
            "entry": [{
                "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
                "changes": [{
                    "value": {
                        "messaging_product": "whatsapp",
                        "metadata": {
                            "display_phone_number": self.phone_number,
                            "phone_number_id": WHATSAPP_PHONE_NUMBER_ID
                        },
                        "contacts": [{
                            "profile": {
                                "name": "Test User"
                            },
                            "wa_id": self.phone_number
                        }],
                        "messages": [{
                            "from": self.phone_number,
                            "id": f"wamid.test{timestamp}",
                            "timestamp": str(timestamp),
                            "text": {
                                "body": message
                            },
                            "type": "text"
                        }]
                    },
                    "field": "messages"
                }]
            }]
        }
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Github-Token': GITHUB_TOKEN
        }
        logging.debug(f"Sending request to {self.endpoint}")
        logging.debug(f"Headers: {json.dumps(headers, indent=2)}")
        logging.debug(f"Payload: {json.dumps(payload, indent=2)}")
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers, timeout=10)
            logging.debug(f"Response status code: {response.status_code}")
            logging.debug(f"Response content: {response.text}")
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json() if response.text else {"message": "Empty response"}
        except requests.Timeout:
            logging.error("Request timed out")
            return {"error": "Request timed out"}
        except requests.ConnectionError:
            logging.error("Connection error occurred")
            return {"error": "Connection error"}
        except requests.RequestException as e:
            logging.error(f"Error sending message: {e}")
            return {"error": str(e)}

    def display_message(self, message):
        """Display the bot's response"""
        if isinstance(message, dict):
            if 'text' in message:
                print(f"Bot: {message['text']['body']}")
            elif 'error' in message:
                print(f"Error: {message['error']}")
            else:
                print(f"Bot: {json.dumps(message, indent=2)}")
        else:
            print(f"Bot: {message}")

    def run(self):
        print("Welcome to WhatsApp Vimbiso-Pay Simulator")
        print("Type 'exit' to quit the simulator")

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break

            response = self.send_message(user_input)
            self.display_message(response)

if __name__ == "__main__":
    simulator = WhatsAppSimulator(phone_number="1234567890")
    simulator.run()
