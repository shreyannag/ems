import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import pwinput
from tabulate import tabulate

try:
    conn = mysql.connector.connect(user='root',password='',host='127.0.0.1',database='ems')
    print("Database connected")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something wrong with username and password")
    elif err.errno ==  errorcode.ER_BAD_DB_ERROR:
        print("Database does not exists")
        print("Press 1 to generate employee database and tables\nPress 2 to exit")
        
    else:
        print(err)

#get cursor

cur = conn.cursor()
#store credentials
storepassword=''
storename=''


def login_admin(userid,password):
    try:
        select_stmt = "SELECT admin_name,admin_passwd FROM adminstrator WHERE admin_id = %(admin_id)s"
        cur.execute(select_stmt,{'admin_id':userid})
        for (admin_name,admin_passwd) in cur:
            storename=admin_name
            storepassword=admin_passwd
            
        
        if(password==storepassword):
            print("Welcome to Employee Management System\nWelcome %s " %storename)
            while True:            
                print("""
+--------------------------------------------------+
|                                                  |
| Press 1 to add employees to the system           |
|                                                  |
|                                                  |
| Press 2 to remove employees from the system      |
|                                                  |
|                                                  |
| Press 3 to update details of the employee        |
|                                                  |
|                                                  |
| Press 4 to show list of the employees            |
|                                                  |
|                                                  |
| Press 5 to exit                                  |
|                                                  |
+--------------------------------------------------+ 
                """)
                choice = int(input("Enter your choice: "))
                if(choice==1):
                    name = input("Enter employee's full name: ")
                    sal = input("Enter employee's salary: ")
                    dob = input("Enter date of birth of the employee in YYYY-MM-DD format: ")
                    doj = input("Enter date of joining of the employee in YYYY-MM-DD format: ")
                    dol = input("Enter date of contract expiry of the employee in YYYY-MM-DD format: ")
                    pos = input("Enter employee's position: ")
                    addEmployee(name,sal,dob,doj,dol,pos)
                elif(choice==2):
                    removeEmployee()
                elif(choice==3):
                    updateEmployeeDetails()
                elif(choice==4):
                    showEmployeeList()
                elif(choice==5):
                    exitEMS()
                    break

        else:
            print("Wrong Password. Access Denied\nEmployee Management System ")
            exitEMS()
                    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_EMPTY_QUERY:
            print("Wrong username and password")
            exitEMS()



def showEmployeeList():
    data = [] #blank list
    try:
        AddStmt = 'select * from employee'
        cur.execute(AddStmt)
        result = cur.fetchall()
        for x in result:
            data.append([x[0],x[1],x[2],x[3],x[4],x[5],x[6]])
        
        #using tabulate function print nested list in table format
        print("\t\t\t\t\t\t\tEmployee List")
        print(tabulate(data,headers=["ID","Name","Salary","Date of birth","Date of joining","Date of contract expiry","Position"],tablefmt="grid"))

    except mysql.connector.Error as err:
        print("Error: ",err)    


def addEmployee(name,sal,dob,doj,dol,pos):
    try:
        AddStmt = 'insert into employee(emp_name,emp_salary,emp_dob,emp_doj,emp_dol,emp_position) values (%s,%s,%s,%s,%s,%s)'
        empInfo = (name,sal,dob,doj,dol,pos)
        cur.execute(AddStmt,empInfo)
        conn.commit()
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_EMPTY_QUERY:
            print("One or more non empty fields were not filled")


def  removeEmployee():
    id = input("Enter employee id you want remove: ")
    try:
        AddStmt = "delete from employee where emp_id= {}".format(id)
        cur.execute(AddStmt)
        conn.commit()
        showEmployeeList()
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_EMPTY_QUERY:
            print("One or more non empty fields were not filled")


def updateEmployeeDetails():
    id = int(input("Enter Employee ID: "))
    print(""" 
┌────────────────────────────────────────────────┐
│                                                │
│   Press 1 to change Employee's Name            │
│                                                │
│   Press 2 to change date of birth              │
│                                                │
│   Press 3 to update salary of the Employee     │
│                                                │
│   Press 4 to update position of the Employee   │
│                                                │
└────────────────────────────────────────────────┘
    """)
    option = int(input("Enter your choice: "))
    if option == 1:
        name = input("Enter the new name of the employee: ")
        AddStmt = 'update employee set emp_name=(%s) where emp_id=(%s)'
        empinfo = (name,id)
        cur.execute(AddStmt,empinfo)
        conn.commit()
        showEmployeeList()

    if option == 2:
        dob = input("Enter date of birth of the employee in YYYY-MM-DD format you want to change: ")
        AddStmt = 'update employee set emp_dob=(%s) where emp_id=(%s)'
        empinfo=(dob,id)
        cur.execute(AddStmt,empinfo)
        conn.commit()
        showEmployeeList()

    if option == 3:
        salary = input("Enter the new salary of the employee: ")
        AddStmt = 'update employee set emp_salary=(%s) where emp_id=(%s)'
        emp = (salary,id)
        cur.execute(AddStmt,emp)
        conn.commit()
        showEmployeeList()

    if option==4:
        postion = input("Enter new position of the employee: ")
        AddStmt = 'update employee set emp_position=(%s) where emp_id=(%s)'
        emp=(postion,id)
        cur.execute(AddStmt,emp)
        conn.commit()
        showEmployeeList()

        
    
def exitEMS():
    print("Exiting Employee Management System.")
    conn.close()


print("""
╔═╗┌┬┐┌─┐┬  ┌─┐┬ ┬┌─┐┌─┐  ╔╦╗┌─┐┌┐┌┌─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┌┬┐  ╔═╗┬ ┬┌─┐┌┬┐┌─┐┌┬┐
║╣ │││├─┘│  │ │└┬┘├┤ ├┤   ║║║├─┤│││├─┤│ ┬├┤ │││├┤ │││ │   ╚═╗└┬┘└─┐ │ ├┤ │││
╚═╝┴ ┴┴  ┴─┘└─┘ ┴ └─┘└─┘  ╩ ╩┴ ┴┘└┘┴ ┴└─┘└─┘┴ ┴└─┘┘└┘ ┴   ╚═╝ ┴ └─┘ ┴ └─┘┴ ┴
""")
now = datetime.now()
print("Date is ",now.strftime('%m/%d/%Y'))
uid = int(input("User id: "))
passw = pwinput.pwinput(prompt='Password: ')

#calling login_admin() function
login_admin(uid,passw)
