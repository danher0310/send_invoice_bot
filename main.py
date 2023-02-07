from telegram.ext import Application, CommandHandler, MessageHandler, filters
import logging
from datetime import datetime, date, time
import calendar
import pytz
from dotenv import load_dotenv
import os 
import utils

load_dotenv()

now = datetime.now()
dates = now.strftime("%m/%d/%Y")
invoice_date = now.strftime("%m-%d-%Y")
month = now.month
year =  now.year
day = now.day 
last_day = calendar.monthrange (year,month) [1]  
  

if day <= 10:
  firstDay = date(year, month, 1).strftime("%m/%d/%Y")
  lastDay = date(year,month, 15).strftime("%m/%d/%Y")

elif day >= 11:
  firstDay = date(year, month, 16).strftime("%m/%d/%Y")
  lastDay = date(year,month, last_day).strftime("%m/%d/%Y")

async def start(update, context):
  user = update.effective_user
  await update.message.reply_text(f"Greetings {user.username} !")

async def chatId(update,context):
    """Returns the chat id where the bot responds to"""
    chatId = update.message.chat.id
    await update.message.reply_text(chatId)
    
async def send_invoice(update,context):
  chatId = os.getenv('chat_id')
  document = utils.create_invoice()
  if os.path.isfile(document):
    await context.bot.send_document(
      chat_id = chatId,
      document = document,
      caption = f"Consulting services from {firstDay} to {lastDay}"
    )
  else:
    await context.bot.send_message(
      chat_id = chatId,
      text = document
    )
    

def main():
  token = os.getenv('tlgtoken')
  application = Application.builder().token(token).build()
  logging.basicConfig(format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  application.add_handler(CommandHandler('start', start))
  application.add_handler(CommandHandler('chat_id', chatId))
  application.add_handler(CommandHandler('send_invoice', send_invoice))
  application.job_queue.run_monthly(send_invoice, time(hour=6, minute=50, second=0, tzinfo=pytz.timezone('US/Eastern')), 10)
  print("-----Bot Started-----")
  application.run_polling()
    
if __name__ == "__main__":
  main()

  
  