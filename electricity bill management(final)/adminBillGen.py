import csv
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from os import path, system

import mysql.connector as c
from mysql.connector import Error

from billEmail import bilEmailHome
from billGen import bilGenHome
from clearscreen import clear
from logout import logout

connection = c.connect(host='localhost', database='electricity_bill', user='root', password='') 
db = connection.cursor()

# Load parameters from config.json file
with open('files/config_file/config.json', 'r') as config_file:
    params = json.load(config_file)["params"]

def adminHome(userid, logintime):
    clear()
    admin_message = open('files/messages/admin_message.txt', 'r').read()
    print(admin_message.format(params['company_name'], userid, logintime, datetime.now()))

    userinput = input()

    funcAdminTuple = ('01#01', '05#02', '06#03', '04#01', '00#01', '02#01', '07#44', '03#01')

    if userinput not in funcAdminTuple:
        clear()
        adminHome(userid, logintime)
    else:
        if userinput == '01#01':
            create_user(userid, logintime)
        elif userinput == '05#02':
            delete_user(userid, logintime)
        elif userinput == '06#03':
            dumpdata('customer', userid, logintime)
        elif userinput == '07#44':
            dumpdata('user', userid, logintime)
        elif userinput == '03#01':
            exportdatatoTable(userid, logintime)
        elif userinput == '02#01':
            bilGenHome(userid, logintime)
        elif userinput == '04#01':
            bilEmailHome(userid, logintime)
        elif userinput == '00#01':
            logout(userid)


def create_user(userid, logintime):
    clear()     #Clear the screen
    db.execute('SELECT dept_no, deptname from dept')
    dept = db.fetchall()

    
    #Print the department number
    print('     Department No       |             Department name')
    print('------------------------------------------------------------')
    for i, j in dept:
        print(f'      {i}                            {j}   ')
    print('Following are the department no')
    print()

    #ask user to enter the dept number
    while True:
        try:
            deptno1 = int(input('Enter the department no\n'))

            db.execute('SELECT dept_no FROM dept')
            deptnos = [row[0] for row in db.fetchall()]

            if deptno1 in deptnos:
                break
            else:
                print(f'{deptno1} Department No is not valid \n Please enter a valid department no !')
        except ValueError:
            print('Enter a number, not characters!')
    #enter name
    name1 = input('Please enter the name\n')
    name = ''.join(filter(str.isalpha, name1))

    while True:
        password1 = input('Please enter a password\n')      #enter password
        password2 = input('Please retype the password\n')
        if password1 == password2:
            break
        else:
            clear()
            print('Entered passwords do not match!')
    
    hashpass1 = hashlib.md5(password1.encode())
    db.execute(f'SELECT deptname FROM dept WHERE dept_no={deptno1}')
    branch = db.fetchall()[0][0]

    # generating the useradminid
    db.execute(f'select username from user where username="{name}"')
    occurence = len(db.fetchall())
    useradminid = f'{deptno1}{occurence+1}{name[:2]}#{branch}'

    db.execute(f'INSERT INTO user VALUES(NULL, "{name}", "{hashpass1.hexdigest()}", "{branch}", {deptno1}, "{useradminid}")')
    connection.commit()

    clear()
    created_message = open('files/messages/create_msg.txt', 'r').read()
    print(created_message.format(name, password1, branch, deptno1, useradminid))
    print()
    input('Press any key to continue')
    adminHome(userid, logintime)

def delete_user(userid, logintime):
    clear()
    db.execute('SELECT useradmin_id FROM user')
    useradmin_ids = [row[0] for row in db.fetchall()]

    while True:
        useradmin_id = input('Enter the UserAdminId\n')

        if useradmin_id in useradmin_ids:
            break
        else:
            print(f'{useradmin_id} UserAdminId is not valid\nPlease enter a valid UserAdminId!')

    # Delete the user from the database
    db.execute(f'DELETE FROM user WHERE useradmin_id = "{useradmin_id}"')
    connection.commit()

    # Confirmation message
    print('The user has been successfully deleted')
    time.sleep(1)
    adminHome(userid, logintime)
    
def dumpdata(tablename, userid, logintime):
    # Retrieve data from the specified table
    db.execute(f'SELECT * FROM {tablename}')
    result = db.fetchall()

    # Determine the filename based on the table name
    filename = 'employee_details' if tablename == 'user' else 'customer_details'
    filepath = os.path.join(os.getcwd(), 'files', 'details', f'{filename}.csv')

    # Write the data to a CSV file
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(result)

    print('The data has been successfully dumped')
    print('File path:', filepath)

    time.sleep(2)
    adminHome(userid, logintime)

def exportdatatoTable(userid, logintime):
    print()
    BASE_DIR = os.getcwd()

    print('Please write the data in a CSV file')
    print('and place it in the following directory:')
    print(os.path.join(BASE_DIR, 'files', 'export'))
    print()

    # Prompt the user for the filename of the CSV file
    filename = input('Enter the filename (without .csv extension):\n')
    filepath = os.path.join(BASE_DIR, 'files', 'export', f'{filename}.csv')

    # Read the data from the CSV file and insert it into the database
    with open(filepath, 'r') as file:
        csv_data = csv.reader(file)
        for row in csv_data:
            try:
                db.execute(f'INSERT INTO customer VALUES({row[0]},{row[1]},{row[2]},"{row[3]}","{row[4]}",{row[5]},"{row[6]}","{row[7]}","{row[8]}","{row[9]}",{row[10]})')
                connection.commit()
            except Error:
                pass

    print('Data imported successfully')

    time.sleep(2)
    adminHome(userid, logintime)

