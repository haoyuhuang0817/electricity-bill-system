from datetime import datetime
from os import system
from login import welcome_message
from clearscreen import clear
import mysql.connector as c

connection = c.connect(host='localhost', database='electricity_bill', user='root', password='')
db = connection.cursor()

clear()

db.execute(f'UPDATE login SET session_out="{datetime.now()}" WHERE session_out="0000%"')
connection.commit()
welcome_message()
