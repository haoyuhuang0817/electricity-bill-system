import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import time

import mysql.connector as c

from clearscreen import clear
from logout import logout

connection = c.connect(host='localhost', database='electricity_bill', user='root', password='') 
db = connection.cursor()

with open('files/config_file/config.json', 'r') as c:
    params = json.load(c)["params"]

def bilEmailHome(userid, logintime):
    # Clear the console screen
    clear()
    print(f"{params['company_name']} BILL EMAIL DEPARTMENT\n\n")
    print(f"Welcome {userid}! Logged in at {logintime}\n")
    print(f"Today's Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current Month: {datetime.now().strftime('%B')}\n\n")
    print("Choose an option:")
    print("1. Send bills to customers")
    print("0. Logout\n")

    userinput = input()

    if userinput == '1':
        sendmailtocustomers(userid, logintime)
    elif userinput == '0':
        logout(userid)
    else:
        bilEmailHome(userid, logintime)

def sendmailtocustomers(userid, logintime):
    # Establish SMTP connection
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(params['email'], params['password_email'])

    month = datetime.now().strftime('%B')

    # Retrieve customer data from the database
    db.execute(f'SELECT email, consumername, consumerno FROM customer WHERE month="{month}"')
    data = db.fetchall()

    success_count = 0
    error_count = 0

    for email, consumername, consumerno in data:
        subject = f"Your electricity bill has been generated for the month {month} ({consumername})"
        
        db.execute(f'SELECT unit_consumed FROM customer WHERE month="{month}" AND consumerno="{consumerno}"')
        unitsConsumed = db.fetchone()[0]

        try:
            # Read the bill content from file
            with open(f'files/customerBillFolder/{unitsConsumed}{consumerno}.txt', 'r') as bill_file:
                bill_content = bill_file.read()

                # Create the email message
                message = MIMEMultipart()
                message['From'] = params['email']
                message['To'] = email
                message['Subject'] = subject
                message.attach(MIMEText(bill_content, 'plain'))

                # Send the email
                server.send_message(message)

                success_count += 1
                print(f"Email (BILL) sent to {consumername}")
        except Exception as e:
            error_count += 1
            print(f"There was an error sending the email to {consumername}:", str(e))

    # Close the SMTP connection
    server.quit()

    print(f"\n{success_count} Email(s) sent!")
    print(f"With {error_count} error(s)!\n")

    time.sleep(2)
    bilEmailHome(userid, logintime)
