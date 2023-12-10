# import database module
from database import Database, Table, read_csv, write_csv, get_head, gen_project_id, get_info_dict
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

    def __str__(self):
        return f"""Hello {self.__user}, you logged in as {self.__role}
First name: {self.__first}
Last name: {self.__last}
ID: {self.__id}"""

    def see_database(self):
        for i in self.__database.database:
            print(i)

    def create_table(self, table_name):
        self.__database.insert(Table(table_name, []))

    def insert_table(self, table):
        self.__database.insert(table)

    def insert_row(self, table_name, data):
        self.__database.search(table_name).insert(data)

    def update_table(self, table_name, row, key, value):
        self.__database.search(table_name).update(row, key, value)

    def remove_table(self, table_name):
        self.__database.remove(table_name)

    def remove_row(self, table_name, row):
        self.__database.search(table_name).remove(row)


class Student:
    def __init__(self, info_dict, database):
        self.__id = info_dict["ID"]
        self.__first = info_dict["first"]
        self.__last = info_dict["last"]
        self.__user = info_dict["user"]
        self.__role = info_dict["role"]
        self.__database = database

    def __str__(self):
        return f"""Hello {self.__user}, you logged in as {self.__role}
First name: {self.__first}
Last name: {self.__last}
ID: {self.__id}"""

    def see_request(self):
        print(self.__database.search("Member_pending_request").
              filter(lambda x: self.__id == x["PersonID"]).table)

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
            if project.table[project_row]["Member1"] == f"{self.__id} (Pending)":
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


class Lead:

    def __init__(self, info_dict, database):
        self.__id = info_dict["ID"]
        self.__first = info_dict["first"]
        self.__last = info_dict["last"]
        self.__user = info_dict["user"]
        self.__role = info_dict["role"]
        self.__database = database

    def __str__(self):
        return f"""Hello {self.__user}, you logged in as {self.__role}
First name: {self.__first}
Last name: {self.__last}
ID: {self.__id}"""

    def project_status(self):
        temp = self.__database.search("Project_table").filter(lambda x: x["Lead"] == self.__id)
        if temp["Member1"] == "-":
            member1 = "-"
        elif "Pending" in temp["Member1"]:
            member1_id = temp["Member1"].split(" ")[0]
            member1_info = get_info_dict(self.__database, member1_id)
            member1 = f'{member1_info["first"]} {member1_info["last"]} (Pending)'
        else:
            member1_info = get_info_dict(self.__database, temp["Member1"])
            member1 = f'{member1_info["first"]} {member1_info["last"]}'
        if temp["Member2"] == "-":
            member2 = "-"
        elif "Pending" in temp["Member2"]:
            member2_id = temp["Member2"].split(" ")[0]
            member2_info = get_info_dict(self.__database, member2_id)
            member2 = f'{member2_info["first"]} {member2_info["last"]} (Pending)'
        else:
            member2_info = get_info_dict(self.__database, temp["Member2"])
            member2 = f'{member2_info["first"]} {member2_info["last"]}'
        if temp["Advisor"] == "-":
            advisor = "-"
        else:
            advisor_info = get_info_dict(self.__database, temp["Advisor"])
            advisor = f'{advisor_info["first"]} {advisor_info["last"]}'
        print(f"""Project Title: {temp["Title"]}
Project ID: {temp["ProjectID"]}
Lead: {self.__first} {self.__last}
Member1: {member1}
Member2: {member2}
Advisor: {advisor}
Status: {temp["Status"]}""")


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
    for i in db.database:
        write_csv(i.table_name, db, get_head(i.table_name))

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
