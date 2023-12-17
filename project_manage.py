from database import Database, Table, read_csv, write_csv, get_head, gen_project_id, get_info_dict
from datetime import date
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
            print(i.table_name)
            n = 1
            for j in i.table:
                print(f"{n}. {j}")
                n += 1

    def create_table(self, table_name):
        self.__database.insert(Table(table_name, []))

    def insert_data(self, table_name, info):
        data = {}
        head = get_head(table_name)
        for i in range(len(head)):
            data[head[i]] = info[i]
        self.__database.search(table_name).insert(data)

    def update_table(self, table_name, row, key, value):
        self.__database.search(table_name).update(row, key, value)

    def remove_table(self, table_name):
        self.__database.remove(table_name)

    def remove_row(self, table_name, row):
        self.__database.search(table_name).remove(row)

    def operation(self, choice):
        if choice == "1":
            """See Database"""
            self.see_database()
        elif choice == "2":
            """Create Table"""
            table_name = input("Input name for this table (leave it blank to cancel): ")
            if table_name.strip() == "":
                return None
            else:
                self.create_table(table_name)
        elif choice == "3":
            """Insert Data"""
            txt1 = "Which table you would like to insert data? " \
                   "(input only number or leave it blank to cancel): "
            txt2 = "Input number of table again (leave it blank to cancel): "
            table_name_list = [i.table_name for i in self.__database.database]
            table_name = get_value(txt1, txt2, table_name_list)
            if table_name is None:
                return None
            head = get_head(table_name)
            data = [input(f"{i}: ") for i in head]
            self.insert_data(table_name, data)
        elif choice == "4":
            """Update Table"""
            txt1_name = "Which table you would like to update? " \
                        "(input only number or leave it blank to cancel): "
            txt2_name = "Input number of table again (leave it blank to cancel): "
            txt1_key = "Which key you would like to update? " \
                       "(input only number or leave it blank to cancel): "
            txt2_key = "Input number of key again (leave it blank to cancel): "
            table_name_list = [i.table_name for i in self.__database.database]
            table_name = get_value(txt1_name, txt2_name, table_name_list)
            if table_name is None:
                return None
            key_list = get_head(table_name)
            key = get_value(txt1_key, txt2_key, key_list)
            if key is None:
                return None
            txt1_row = "Which row you want to update? " \
                       "(input only number or leave it blank to cancel): "
            txt2_row = "Input number of row again (leave it blank to cancel): "
            row_list = self.__database.search(table_name).table
            row_dict = get_value(txt1_row, txt2_row, row_list)
            if row_dict is None:
                return None
            row = self.__database.search(table_name).get_row(lambda x: x[key] == row_dict[key])
            new_value = input("Input the new value to update: ")
            self.__database.update(row, key, new_value)
        elif choice == "5":
            """Remove Table"""
            txt1 = "Which table you want to remove? " \
                   "(input only number or leave it blank to cancel): "
            txt2 = "Input number of table again (leave it blank to cancel): "
            table_name_list = [i.table_name for i in self.__database.database]
            table_name = get_value(txt1, txt2, table_name_list)
            if table_name is None:
                return None
            self.remove_table(table_name)
        elif choice == "6":
            """Remove Row"""
            txt1 = "Which table you want to remove row? " \
                   "(input only number or leave it blank to cancel): "
            txt2 = "Input number of table again (leave it blank to cancel): "
            table_name_list = [i.table_name for i in self.__database.database]
            table_name = get_value(txt1, txt2, table_name_list)
            if table_name is None:
                return None
            txt1_row = "Which row you want to remove? " \
                       "(input only number or leave it blank to cancel): "
            txt2_row = "Input number of row again (leave it blank to cancel): "
            row_list = self.__database.search(table_name).table
            row_dict = get_value(txt1_row, txt2_row, row_list)
            if row_dict is None:
                return None
            row = self.__database.search(table_name).get_row(lambda x: x == row_dict)
            self.remove_row(table_name, row)


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
            return Member(get_info_dict(db, self.__id), self.__database)
        elif response == "D":
            member_pending.update(mem_pen_row, "Response", "Deny")
            return None

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
        return Lead(get_info_dict(db, self.__id), self.__database)


class Lead:

    def __init__(self, info_dict, database):
        self.__id = info_dict["ID"]
        self.__first = info_dict["first"]
        self.__last = info_dict["last"]
        self.__user = info_dict["user"]
        self.__role = info_dict["role"]
        self.__database = database
        my_project = self.__database.search("Project_table").\
            filter(lambda x: x["Lead"] == self.__id)
        self.__project_id = my_project.table[0]["ProjectID"]

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

    def modify_project_info(self, key, value):
        my_project = self.__database.search("Project_table")
        row = my_project.get_row(lambda x: x["Lead"] == self.__id)
        my_project.update(row, key, value)

    def see_pending_request(self):
        pending_member = self.__database.search("Member_pending_request").\
            filter(lambda x: x["ProjectID"] == self.__project_id and x["Response"] == "Pending").\
            table
        pending_advisor = self.__database.search("Advisor_pending_request").\
            filter(lambda x: x["ProjectID"] == self.__project_id and x["Response"] == "Pending").\
            table
        if len(pending_member) + len(pending_advisor) == 0:
            print("No pending request now, you can send request to student to be member and "
                  "faculty to be advisor")
        else:
            print("Pending request in my project")
            if len(pending_member) != 0:
                print("Pending Member")
                for i in range(len(pending_member)):
                    temp_dict = get_info_dict(self.__database, pending_member[i]["PersonID"])
                    print(f'{i+1}. {temp_dict["first"]} {temp_dict["last"]}')
            if len(pending_advisor) != 0:
                print("Pending Advisor")
                temp_dict = get_info_dict(self.__database, pending_advisor[0]["PersonID"])
                print(f'{temp_dict["first"]} {temp_dict["last"]}')

    def send_request(self, person_id):
        person_info = get_info_dict(self.__database, person_id)
        my_project = self.__database.search("Project_table")
        row = my_project.get_row(lambda x: x["Lead"] == self.__id)
        if person_info["role"] == "student":
            data = {
                "ProjectID": self.__project_id,
                "PersonID": person_id,
                "to_be_member": person_info["username"],
                "Response": "Pending",
                "Response_Date": "Pending"
            }
            self.__database.search("Member_pending_request").insert(data)
            if my_project[row]["Member1"] == "-":
                my_project.update(row, "Member1", f"{person_id} (Pending)")
            else:
                my_project.update(row, "Member2", f"{person_id} (Pending)")
        elif person_info["role"] == "faculty":
            data = {
                "ProjectID": self.__project_id,
                "PersonID": person_id,
                "to_be_advisor": person_info["username"],
                "Response": "Pending",
                "Response_Date": "Pending"
            }
            self.__database.search("Advisor_pending_request").insert(data)
            my_project.update(row, "Advisor", f"{person_id} (Pending)")
        else:
            print("You can only send request to student or faculty")


class Member:

    def __init__(self, info_dict, database):
        self.__id = info_dict["ID"]
        self.__first = info_dict["first"]
        self.__last = info_dict["last"]
        self.__user = info_dict["user"]
        self.__role = info_dict["role"]
        self.__database = database
        my_project = self.__database.search("Project_table"). \
            filter(lambda x: (x["Member1"] or x["Member2"]) == self.__id)
        self.__project_id = my_project.table[0]["ProjectID"]

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

    def modify_project_info(self, key, value):
        my_project = self.__database.search("Project_table")
        row = my_project.get_row(lambda x: x["Lead"] == self.__id)
        my_project.update(row, key, value)

    def see_pending_request(self):
        pending_member = self.__database.search("Member_pending_request").\
            filter(lambda x: x["ProjectID"] == self.__project_id and x["Response"] == "Pending").\
            table
        pending_advisor = self.__database.search("Advisor_pending_request").\
            filter(lambda x: x["ProjectID"] == self.__project_id and x["Response"] == "Pending").\
            table
        if len(pending_member) + len(pending_advisor) == 0:
            print("No pending request now")
        else:
            print("Pending request in my project")
            if len(pending_member) != 0:
                print("Pending Member")
                for i in range(len(pending_member)):
                    temp_dict = get_info_dict(self.__database, pending_member[i]["PersonID"])
                    print(f'{i+1}. {temp_dict["first"]} {temp_dict["last"]}')
            if len(pending_advisor) != 0:
                print("Pending Advisor")
                temp_dict = get_info_dict(self.__database, pending_advisor[0]["PersonID"])
                print(f'{temp_dict["first"]} {temp_dict["last"]}')


class Faculty:

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
        print(self.__database.search("Advisor_pending_request").
              filter(lambda x: self.__id == x["PersonID"]).table)

    def response_request(self, project_id, response):
        advisor_pending = self.__database.search("Advisor_pending_request")
        ad_pen_row = advisor_pending.get_row(lambda x: x["ProjectID"] == project_id
                                             and x["PersonID"] == self.__id)
        project = self.__database.search("Project_table")
        project_row = project.get_row(lambda x: x["ProjectID"] == project_id)
        login_table = self.__database.search("login")
        login_row = login_table.get_row(lambda x: x["ID"] == self.__id)
        advisor_pending.update(ad_pen_row, "Response_date", date.today())
        if response == "A":
            advisor_pending.update(ad_pen_row, "Response", "Accept")
            login_table.update(login_row, "role", "advisor")
            project.update(project_row, "Advisor", self.__id)
            return Advisor(get_info_dict(db, self.__id), self.__database)
        elif response == "D":
            advisor_pending.update(ad_pen_row, "Response", "Deny")
            return None

    def see_project_table(self):
        project_table = self.__database.search("Project_table")
        for i in project_table.table:
            print(i)

    def eval_project(self, project_id, result):
        project_table = self.__database.search("Project_table")
        row = project_table.get_row(lambda x: x["ProjectID"] == project_id)
        project_table.update(row, "Status", result)


class Advisor:

    def __init__(self, info_dict, database):
        self.__id = info_dict["ID"]
        self.__first = info_dict["first"]
        self.__last = info_dict["last"]
        self.__user = info_dict["user"]
        self.__role = info_dict["role"]
        self.__database = database
        my_project = self.__database.search("Project_table"). \
            filter(lambda x: x["Advisor"] == self.__id)
        self.__project_id = my_project.table[0]["ProjectID"]

    def __str__(self):
        return f"""Hello {self.__user}, you logged in as {self.__role}
First name: {self.__first}
Last name: {self.__last}
ID: {self.__id}"""

    def see_project_table(self):
        project_table = self.__database.search("Project_table")
        for i in project_table.table:
            print(i)

    def approve_project(self):
        project_table = self.__database.search("Project_table")
        row = project_table.get_row(lambda x: x["ProjectID"] == self.__project_id)
        project_table.update(row, "Status", "Approved")

    def approve_final_report(self):
        project_table = self.__database.search("Project_table")
        row = project_table.get_row(lambda x: x["ProjectID"] == self.__project_id)
        project_table.update(row, "Status", "Final report approved")


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
def get_value(txt1, txt2, list_of_something):
    for i in range(len(list_of_something)):
        print(f"{i + 1}. {list_of_something[i]}")
    user_input = input(txt1)
    if user_input.strip() == "":
        return None
    while user_input not in [str(i + 1) for i in range(len(list_of_something))]:
        user_input = input(txt2)
        if user_input.strip() == "":
            return None
    return list_of_something[int(user_input)-1]


def perform(list_of_login):
    if list_of_login is None:
        return None
    if list_of_login[1] == "admin":
        user = Admin(get_info_dict(db, list_of_login[0]), db)
        txt = f"""{user}
1. See Database
2. Create Table
3. Insert Data
4. Update Table
5. Remove Table
6. Remove Row
What to do? (leave it blank to exit): """
        choice = input(txt)
        while choice.strip() != "":
            while choice not in [str(i + 1) for i in range(7)]:
                choice = input("Input only number of index: ")
                if choice.strip() == "":
                    return None
            user.operation(choice)
            print()
            choice = input(txt)
        return None


# make calls to the initializing and login functions defined above

initializing()
val = login()
perform(val)
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
