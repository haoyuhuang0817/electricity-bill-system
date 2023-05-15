import mysql.connector as c
import datetime
from os import path
import json
import sys
import time
from clearscreen import clear

# Database connection
connection = c.connect(host='localhost', database='electricity_bill', user='root', password='')
db = connection.cursor()

# Get the file path for the config.json file
THIS_FOLDER = path.dirname(path.abspath(__file__))
my_file = path.join(THIS_FOLDER, 'files', 'config_file', 'config.json')

# Read configuration parameters
with open(my_file, 'r') as c:
    params = json.load(c)["params"]

def consumerDetails():
    clear()  # Clear the screen

    # Retrieve the existing consumer numbers from the database
    db.execute('SELECT consumerno FROM customer')
    detailsconsumerno = {i[0] for i in db.fetchall()}

    mydate = datetime.datetime.now()

    while True:
        try:
            consumerno = int(input('Please enter your consumer no.\n'))
        except ValueError:
            print("\nPlease enter a valid consumer no")

        if consumerno not in detailsconsumerno:
            print('\nThe consumer no does not exist!! \nPlease enter a valid consumer no')
        else:
            break

    # Retrieve customer details for the given consumer number and current month
    db.execute(f'SELECT * FROM customer WHERE consumerno={consumerno} AND month="{mydate.strftime("%B")}"')
    custdetails = db.fetchone()

    if custdetails[-1] == 0:
        print('No bill has been generated for this month!')
    else:
        my_file1 = path.join(THIS_FOLDER, 'files', 'messages', 'custdetails.txt')
        with open(my_file1, 'r') as c1:
            fileread = c1.read()
            # Format the template with customer details and print it
            print(fileread.format(params['company_name'], custdetails[3], custdetails[1], custdetails[2],
                                  custdetails[4], custdetails[5], custdetails[-1], custdetails[8], custdetails[9]))

    print('\nPress any key to exit!!!')
    input()
    print(f"Thank you for using the {params['company_name']} ELECTRICITY CUSTOMER DEPARTMENT SERVICES")
    time.sleep(2)
    sys.exit()
