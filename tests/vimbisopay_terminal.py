import json
import logging
import requests
import os
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Import configuration
try:
    from avatar.app.config import VIMBISO_PAY_API_URL
    logging.info("Successfully imported VIMBISO_PAY_API_URL from config")
except ImportError as e:
    logging.error(f"Failed to import config: {e}")
    VIMBISO_PAY_API_URL = os.environ.get('VIMBISO_PAY_API_URL', 'https://stunning-garbanzo-v766w6pwjw53p6q4-8080.app.github.dev/')
    logging.info(f"Using VIMBISO_PAY_API_URL from environment: {VIMBISO_PAY_API_URL}")

class WhatsAppSimulator:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.base_url = VIMBISO_PAY_API_URL.strip()
        self.endpoint = f"{self.base_url}whatsapp/webhook"
        
        # Add authentication token (you may need to adjust this based on your actual authentication method)
        self.auth_token = os.environ.get('VIMBISO_PAY_AUTH_TOKEN', 'default_token')

    def send_message(self, message):
        """Send a WhatsApp message to the Vimbiso-Pay endpoint"""
        payload = {
            "message": {"text": message},
            "from": self.phone_number,
            "type": "text"
        }
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
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
