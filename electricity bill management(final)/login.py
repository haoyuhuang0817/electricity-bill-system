import hashlib
import json
import time
from datetime import datetime
from os import path
import mysql.connector as c

# Database connection
connection = c.connect(host='localhost', database='electricity_bill', user='root', password='')
db = connection.cursor()

# Read configuration parameters
with open('files/config_file/config.json', 'r') as c:
    params = json.load(c)["params"]

# Welcome message
def welcome_message():
    clear()
    print(open('files/messages/welcome.txt', 'r').read().format(params['company_name']))
    login_deptno()

# Login system
def login_deptno():
    while True:
        try:
            deptno_in = int(input('Please enter the department no.\n'))
            if deptno_in == 15675812:
                consumerDetails()
            else:
                logincheck(deptno_in)
            break
        except ValueError:
            print('\nPlease recheck department no (Tip: Enter all numbers not alphabets!)')

def logincheck(deptno):
    # Check if the department number exists in the database
    db.execute('SELECT dept_no FROM dept')
    deptno_dict = {i[0] for i in db.fetchall()}
    newline = '\n'
    if deptno not in deptno_dict:
        login_deptno(f'{deptno} Department No is invalid{newline}Please enter a valid department no!!')
    else:
        login_user(deptno)

def login_user(deptno):
    clear()
    print('\nNow please enter your login credentials')
    print('---------------------------------------')
    userid = input('Please enter your USERID\n')
    print('---------------------------------------')
    password = input('Please enter your password\n')
    hashpass = hashlib.md5(password.encode()).hexdigest()
    
    # Check if the entered credentials exist in the database
    db.execute(f'SELECT * FROM user WHERE password="{hashpass}" AND dept_no="{deptno}" AND useradmin_id="{userid}"')
    query = db.fetchall()
    if query is None or query == []:
        print('The given credentials were wrong')
        print('Please wait for 2 sec!')
        time.sleep(2)
        welcome_message()
    else:
        login_user_in(userid, hashpass, deptno)

def login_user_in(userid, hashpass, deptno, work=None):
    logintime = datetime.now()
    db.execute(f'SELECT branch FROM user WHERE useradmin_id="{userid}"')
    branch = db.fetchall()[0][0]
    
    if work is None:
        # Insert the login details into the login table
        db.execute(f'INSERT INTO login(userid, branch, session_in, dept_no) VALUES("{userid}", "{branch}", "{logintime}", "{deptno}")')
        connection.commit()
    else:
        # Update the session time for an existing login
        db.execute(f'UPDATE login SET session={datetime.now()} WHERE userid="{userid}" AND session_out="0000%"')
    
    branchget = userid.split("#")
    print('Please wait, you are being redirected there! in 5 sec.....')
    time.sleep(5)
    
    # Redirect to the appropriate branch based on the user's branch
    if branch == 'ADMIN':
        adminHome(userid, logintime)
    elif branch == 'BILL GENERATION':
        bilGenHome(userid, logintime)
    elif branch == 'BILL DELIVERY':
        bilEmailHome(userid, logintime)

welcome_message()
