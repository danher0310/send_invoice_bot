import jinja2
import pdfkit
from datetime import datetime, date, timedelta
import calendar
import mysql.connector
import os 
from dotenv import load_dotenv, dotenv_values
from dateutil.relativedelta import relativedelta


load_dotenv()
def connectionDb():
  try:
    mydb=mysql.connector.connect(
      host = os.getenv('dbhost'),
      user = os.getenv('userdb'),
      password = os.getenv('passdb'),
      database = os.getenv('dbname'),
      auth_plugin = "mysql_native_password"     
    )
    return mydb
  except OSError:
    return OSError
  
def check_and_get_number(table_name):
  mydb = connectionDb()
  myCursor = mydb.cursor()
  myCursor.execute(f"SELECT invoicenumber from {table_name} order by invoicenumber DESC")
  result = myCursor.fetchone()
  mydb.close()
  return int(result[0])+1
  
  
def insert_invoice_number(invoiceNumber, table_name ): 
  try:
    mydb = connectionDb()
    myCursor = mydb.cursor()
    scriptSQL = (f"INSERT INTO {table_name} (invoicenumber) VALUES(%s)")
    value = invoiceNumber
    myCursor.execute(scriptSQL,(value,))
    mydb.commit()
    mydb.close()
    return True
  except OSError:
    return False
    
  
  
  
  


def ccs_invoice():
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

  else: 
    firstDay = date(year, month, 1).strftime("%m/%d/%Y")
    lastDay = date(year,month, last_day).strftime("%m/%d/%Y")
  
  invoiceN = check_and_get_number('ccs_invoice')
    
  context = {
  
    'dates':dates,
    'to':os.getenv('to'),
    'invoiceN': invoiceN,
    'firstDay': firstDay,
    'lastDay': lastDay
  }
  template_loader = jinja2.FileSystemLoader(r'./template')
  template_env = jinja2.Environment(loader=template_loader )
  path_saving = f"{os.getenv('path_saving')}{os.sep}CCS{os.sep}Invoice_{invoice_date}.pdf"  
  if not os.path.exists(path_saving):
    template = template_env.get_template("invoice.html")
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" )
    if pdfkit.from_string(output_text, path_saving, configuration=config , css=r'./template/assets/css/index.css', options={"enable-local-file-access": ""} ):
      if insert_invoice_number(int(invoiceN), 'ccs_invoice'):
        return path_saving
      else:
        return "Sorry, but the invoice has some error, please contact to administrator"
  else:
    return "Sorry, but this invoice was already processed today. Try again tomorrow."
    
    
  #----------------------------Invoice CCS -------------------------#


def CC_invoice():
  now = datetime.now()
  actual_date = now.strftime("%d/%m/%Y")
  months = {1:"Enero", 2: "Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10: "Octubre", 11:"Noviembre", 12:"Diciembre"}
  actual_month = now.month
  actual_year =  now.year 
  amount = 500.00
  retroactive_date = now - relativedelta(months=27)
  
  
  if actual_month == 12:
    payment_day = date((actual_year+1), 1, 5).strftime("%d/%m/%y")
  else:
    payment_day = date(actual_year, (actual_month+1), 5).strftime("%d/%m/%y")
    
  if (retroactive_date.year <= 2022):
    first_date = datetime.strptime('01/1/2023', '%d/%m/%Y')
    end_date = datetime.strptime(f"1/{now.month}/{now.year}", '%d/%m/%Y')
    delta = relativedelta(end_date, first_date)
    if delta.years < 1:
      retroactive_number = delta.months + 1
    
    else:
      retroactive_number = (delta.years *12 ) + (delta.months + 1 )
    
    months = {1:"Enero", 2: "Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio", 7:"Julio", 8:"Agosto", 9:"Septiembre", 10: "Octubre", 11:"Noviembre", 12:"Diciembre"}
    retroactive_month = months[retroactive_date.month]
    retroctive_year = retroactive_date.year
    retroactive_line = f"Pago retroactivo {retroactive_month} de {retroctive_year}"
    amount_retro = "$"+'{:4,.2f}'.format(500)
    amount_subtotal = amount + 500
    amount_total = amount_subtotal
    tax_retro = '{:4,.2f}'.format(0)    
    retroactive_number_line = f"Pago de la espalda invoice No. {retroactive_number}/27"
    
    
    
    
  else: 
    retroactive_line =''
    retroactive_month = ''
    retroctive_year = ''
    amount_retro = ""
    amount_subtotal = amount
    amount_total = amount_subtotal
    tax_retro = ""
    retroactive_number_line=""
    
  invoiceN = check_and_get_number('cc_invoice')
    
  context = {
    
   
    'invoiceN': invoiceN,
    'dates':actual_date,
    'to':os.getenv('to'),    
    'monthNow': months[actual_month],
    'yearNow': actual_year,
    'amount': '{:4,.2f}'.format(amount), 
    'retroactive_line': retroactive_line,
    'amountRetro':  amount_retro,     
    'tax_retro': tax_retro,
    "ammountSubTotal" : '{:4,.2f}'.format(amount_subtotal),
    'ammountTotal': '{:4,.2f}'.format(amount_total),
    'dayMonth' : payment_day,
    'retroactive_number_line': retroactive_number_line    
    
  }
  
  template_loader = jinja2.FileSystemLoader(r'./template')
  template_env = jinja2.Environment(loader=template_loader )
  path_saving = f"{os.getenv('path_saving')}{os.sep}CCDR{os.sep}Invoice_{now.strftime('%d-%m-%Y')}.pdf"  
  print(path_saving)
  if not os.path.exists(path_saving):
    template = template_env.get_template("invoiceCC.html")
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" )
    if pdfkit.from_string(output_text, path_saving, configuration=config , css=r'./template/assets/css/index.css', options={"enable-local-file-access": ""} ):     
      if insert_invoice_number(int(invoiceN), 'cc_invoice'):
        return path_saving
      else:
        return "Sorry, but the invoice has some error, please contact to administrator"
  else:
    return "Sorry, but this invoice was already processed today. Try again tomorrow."
  
  
    
# now = datetime.now()
# print(now)

# start_date = datetime.strptime('01/1/2022', '%d/%m/%Y')
# end_date = datetime.strptime(f"1/{now.month}/{now.year}", '%d/%m/%Y')
# delta = relativedelta(end_date, start_date)
# print(delta.years, 'Years,', delta.months+1, 'months,', delta.days, 'days')
  
  



CC_invoice()


ccs_invoice()

