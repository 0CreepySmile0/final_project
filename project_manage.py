# import database module
from database import Database, Table, read_csv, write_csv, get_head, gen_project_id
from datetime import date
# define a function called initializing
db = Database()


class Admin:
    def __init__(self, info_dict, database):
        self.__id = info_dict["ID"]
        self.__first = info_dict["first"]
        self.__last = info_dict["last"]
        self.__user = info_dict["user"]
        self.__role = info_dict["role"]
        self.__database = database

    @property
    def db(self):
        return self.__database

    def create(self, table_name):
        self.db.insert(Table(table_name, []))

    def update(self, table_name, person_id, key, value):
        self.db.search(table_name).update(person_id, key, value)

    def remove(self, table_name):
        n = 0
        for i in self.db.database:
            if i.table_name == table_name:
                self.db.database.pop(n)
            else:
                n += 1


class Student:
    def __init__(self, info_dict, database):
        self.__id = info_dict["ID"]
        self.__first = info_dict["first"]
        self.__last = info_dict["last"]
        self.__user = info_dict["user"]
        self.__role = info_dict["role"]
        self.__database = database

    def see_request(self):
        print(self.__database.search("Member_pending_request").table)

    def response_request(self, project_id, response):
        member_pending = self.__database.search("Member_pending_request")
        mem_pen_row = member_pending.get_row(lambda x: x["ProjectID"] == project_id
                                             and x["PersonID"] == self.__id)
        project = self.__database.search("Project_table")
        project_row = project.get_row(lambda x: x["ProjectID"] == project_id)
        login_table = self.__database.search("login")
        login_row = login_table.get_row(lambda x: x["ID"] == self.__id)
        member_pending.update(mem_pen_row, "Response_date", date.today())
        if response == "A":
            member_pending.update(mem_pen_row, "Response", "Accept")
            login_table.update(login_row, "role", "member")
            if project.table[project_row]["Member1"] == "-":
                project.update(project_row, "Member1", self.__id)
            else:
                project.update(project_row, "Member2", self.__id)
        elif response == "D":
            member_pending.update(mem_pen_row, "Response", "Deny")

    def create_project(self, title):
        temp_data = {
            "ProjectID": gen_project_id(self.__id),
            "Title": title,
            "Lead": self.__id,
            "Member1": "-",
            "Member2": "-",
            "Advisor": "-",
            "Status": "Processing"
        }
        self.__database.search("Project_table").insert(temp_data)
        login_table = self.__database.search("login")
        login_row = login_table.get_row(lambda x: x["ID"] == self.__id)
        login_table.update(login_row, "role", "lead")


def get_info_dict(db, person_id):
    temp = db.search("persons")
    temp1 = temp.join(db.search("login"), "ID")
    for i in temp1.table:
        if i["ID"] == person_id:
            return {"ID": i["ID"], "first": i["fist"], "last": i["last"], "user": i["username"],
                    "role": i["role"]}
        else:
            continue


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
# val = login()
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
# exit()
