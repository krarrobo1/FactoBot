from abc import ABC, abstractmethod

from mindee import Client, documents
from telebot import TeleBot, types

from models.receipt import Receipt


from config.env_vars import ENV


mindee_client = Client(api_key=ENV['MINDEE_API_KEY'])


class ExpenseReceiptHandler(ABC):
    def __init__(self, bot):
        self.bot: TeleBot = bot

    def get_file_path(self, message: types.Message) -> str:
        file_id = message.photo[-1].file_id
        file = self.bot.get_file(file_id)
        return file.file_path

    def download_file(self, message: types.Message) -> str:
        file_path = self.get_file_path(message)
        downloaded_file = self.bot.download_file(file_path)
        src = 'store/' + file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        return src

    @abstractmethod
    def handle_receipt(self, message) -> Receipt:
        pass


class MindeeReceiptHandler(ExpenseReceiptHandler):
    def handle_receipt(self, message) -> Receipt:
        path = self.download_file(message)
        input_doc = mindee_client.doc_from_path(path)

        api_response = input_doc.parse(documents.TypeReceiptV4)
        doc = api_response.document

        return {
            'supplier': doc.supplier,
            'expense_type': doc.category,
            'date': doc.date,
            'total_amount': doc.total_amount,
        }
