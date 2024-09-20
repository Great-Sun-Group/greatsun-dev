import os
from dotenv import load_dotenv

load_dotenv()

class SharedSecrets:
    JWT_SECRET = os.getenv('JWT_SECRET')
    WHATSAPP_BOT_API_KEY = os.getenv('WHATSAPP_BOT_API_KEY')

    @staticmethod
    def check_shared_secrets():
        required_secrets = ['JWT_SECRET', 'WHATSAPP_BOT_API_KEY']
        
        missing_secrets = [secret for secret in required_secrets if not getattr(SharedSecrets, secret)]
        
        if missing_secrets:
            print("Error: The following required shared secrets are missing:")
            for secret in missing_secrets:
                print(f"- {secret}")
            return False
        
        return True