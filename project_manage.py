# import database module
from database import Database, Table, read_csv, write_csv, get_head
# define a function called initializing
db = Database()

def initializing():


# here are things to do in this function:

    # create an object to read all csv files that will serve as a persistent state for this program
    persons = read_csv("persons")
    log_in = read_csv("login")
    project = read_csv("Project_table")
    advisor_pen = read_csv("Advisor_pending_request")
    member_pen = read_csv("Member_pending_request")
    # create all the corresponding tables for those csv files
    persons_table = Table("persons", persons)
    login_table = Table("login", log_in)
    project_table = Table("Project_table", project)
    advisor_pen_table = Table("Advisor_pending_request", advisor_pen)
    member_pen_table = Table("Member_pending_request", member_pen)
    db.insert(persons_table)
    db.insert(login_table)
    db.insert(project_table)
    db.insert(advisor_pen_table)
    db.insert(member_pen_table)
    # see the guide how many tables are needed

    # add all these tables to the database


# define a function called login

def login():
    user = input("Username : ")
    password = input("Password : ")
    for i in db.search("login").table:
        if i["username"] == user and i["password"] == password:
            return [i["ID"], i["role"]]
        else:
            continue
    return None

# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [ID, role] if valid, otherwise returning None

# define a function called exit
def exit():
    write_csv("login", db, get_head("login"))
    write_csv("Project_table", db, get_head("Project_table"))
    write_csv("Advisor_pending_request", db, get_head("Advisor_pending_request"))
    write_csv("Member_pending_request", db, get_head("Member_pending_request"))

# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above

initializing()
val = login()
# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

# if val[1] = 'admin':
    # see and do admin related activities
# elif val[1] = 'student':
    # see and do student related activities
# elif val[1] = 'member':
    # see and do member related activities
# elif val[1] = 'lead':
    # see and do lead related activities
# elif val[1] = 'faculty':
    # see and do faculty related activities
# elif val[1] = 'advisor':
    # see and do advisor related activities

# once everything is done, make a call to the exit function
exit()
