from datetime import datetime
from os import system
from login import welcome_message  # Assuming the login module is imported from a separate file
from clearscreen import clear  # Assuming the clearscreen module is imported from a separate file
import mysql.connector as c

connection = c.connect(host='localhost', database='electricity_bill', user='root', password='')
db = connection.cursor()

clear()  # Clear the screen before proceeding

# Update the session_out field in the login table with the current timestamp
db.execute(f'UPDATE login SET session_out="{datetime.now()}" WHERE session_out="0000%"')
connection.commit()

welcome_message()  # Display the welcome message
