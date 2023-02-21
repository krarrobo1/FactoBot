import os

import telebot

from config.env_vars import ENV

from handlers.expense_receipt import MindeeReceiptHandler

bot = telebot.TeleBot(ENV['TELEGRAM_API_KEY'])

receipt_handler = MindeeReceiptHandler(bot)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi, do you have a receipt for me ? Send me a screenshot and I'll save it for you")


@bot.message_handler(content_types=['photo', 'document'])
def get_receipt(message):
    receipt = receipt_handler.handle_receipt(message)
    bot.reply_to(message, f'Received'
                          f'\n Date: {receipt["date"]}'
                          f'\n Supplier: {receipt["supplier"]}'
                          f'\n Expense Type: {receipt["expense_type"]}  '
                          f'\n Total Amount: {receipt["total_amount"]}')

bot.infinity_polling()
