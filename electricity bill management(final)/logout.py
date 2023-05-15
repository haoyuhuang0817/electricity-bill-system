import sys
import time
from datetime import datetime
import mysql.connector as c
from clearscreen import clear

connection = c.connect(host='localhost', database='electricity_bill', user='root', password='')
db = connection.cursor()

def logout(userid):
    # Update the session_out field in the login table with the current timestamp for the given user
    db.execute(f'UPDATE login SET session_out="{datetime.now()}" WHERE userid="{userid}" AND session_out="0000%"')
    connection.commit()

    clear()  # Clear the screen

    print(f'You have been logged out!!! {userid}')
    print('The window is closing in 2 seconds')
    time.sleep(2)  # Wait for 2 seconds

    clear()  # Clear the screen again
    sys.exit()  # Exit the script
