import os

from dotenv import load_dotenv

load_dotenv()

ENV = {
    'TELEGRAM_API_KEY': os.getenv('TELEGRAM_API_KEY'),
    'MINDEE_API_KEY': os.getenv('MINDEE_API_KEY')
}