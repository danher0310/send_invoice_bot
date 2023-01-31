import jinja2
import pdfkit
from datetime import datetime, date
import calendar
import os 

now = datetime.now()
dates = now.strftime("%m/%d/%Y")

month = now.month
year =  now.year
day = now.day 
last_day = calendar.monthrange (year,month) [1] 

if day == 10:
  firstDay = date(year, month, 1).strftime("%m/%d/%Y")
  lastDay = date(year,month, 16).strftime("%m/%d/%Y")

elif day == 25:
  firstDay = date(year, month, 16).strftime("%m/%d/%Y")
  lastDay = date(year,month, last_day).strftime("%m/%d/%Y")

else: 
  firstDay = date(year, month, 1).strftime("%m/%d/%Y")
  lastDay = date(year,month, last_day).strftime("%m/%d/%Y")
  
  
context = {
  'date':dates,
  'invoiceN': '4040Test',
  'firstDay': firstDay,
  'lastDay': lastDay
}
template_loader = jinja2.FileSystemLoader(r'./template')
template_env = jinja2.Environment(loader=template_loader )

template = template_env.get_template("invoice.html")
output_text = template.render(context)

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" )
pdfkit.from_string(output_text, r'./pdf_test4.pdf', configuration=config , css=r'./template/assets/css/index.css', options={"enable-local-file-access": ""} )


# list = os.listdir(r"C:\Program Files\wkhtmltopdf\bin")
# print(list)





