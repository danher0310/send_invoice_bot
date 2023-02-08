## ******BOT TO SEND INVOICE A ESPECIFIC CLIENT******

 ![header](https://raw.githubusercontent.com/danher0310/send_invoice_bot/blob/main/template/assets/img/pythonbot.jpg) 

**DESCRIPTION:**

This is a simple telegram bot to send invoices to a specific client, in this case, the invoice only has a service, and only changes in the date range, in that case, I created a database, for the invoice number. also, I use the PDFKIT library to convert HTML template into pdf file. Also, I work with the job_queue and run_montly of the python telegram bot library

**USAGE:**

First after all, you need create your bot in https://t.me/BotFather on telegram, after that you should be have your token to use the code.

To use the code you need run `*pip install -r requirements.txt*`.. 

after that you need configure your .env file:

1. Copy your token from botfather.
2. Create your database
3. run the code