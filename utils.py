import jinja2
import pdfkit
from datetime import datetime, date
import calendar
import mysql.connector
import os 
from dotenv import load_dotenv, dotenv_values


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
  
def check_and_get_number():
  mydb = connectionDb()
  myCursor = mydb.cursor()
  myCursor.execute("SELECT invoicenumber from invoice_number order by invoicenumber DESC")
  result = myCursor.fetchone()
  mydb.close()
  return result[0]+1
  
  
def insert_invoice_number(invoiceNumber): 
  try:
    mydb = connectionDb()
    myCursor = mydb.cursor()
    scriptSQL = ("INSERT INTO invoice_number (invoicenumber) VALUES(%s)")
    value = invoiceNumber
    myCursor.execute(scriptSQL,(value,))
    mydb.commit()
    mydb.close()
    return True
  except OSError:
    return False
    
  
  
  
  


def create_invoice():
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
  
  invoiceN = check_and_get_number()
    
  context = {
  
    'dates':dates,
    'invoiceN': invoiceN,
    'firstDay': firstDay,
    'lastDay': lastDay
  }
  template_loader = jinja2.FileSystemLoader(r'./template')
  template_env = jinja2.Environment(loader=template_loader )
  path_saving = f"{os.getenv('path_saving')}{os.sep}Invoice_{invoice_date}.pdf"  
  if not os.path.exists(path_saving):
    template = template_env.get_template("invoice.html")
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" )
    if pdfkit.from_string(output_text, path_saving, configuration=config , css=r'./template/assets/css/index.css', options={"enable-local-file-access": ""} ):
      if insert_invoice_number(int(invoiceN)):
        return path_saving
      else:
        return "We have a error with the invoice"
  else:
    return "I created the invoice today"
    
    
  









