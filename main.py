from dotenv import load_dotenv, dotenv_values
import os

dotenv_values()

config = dotenv_values('.env')
print(config)