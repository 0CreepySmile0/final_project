# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file

import csv, os, copy, datetime, random

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def read_csv(file_name):
    data = []
    with open(os.path.join(__location__, f'{file_name}.csv')) as f:
        rows = csv.DictReader(f)
        for r in rows:
            data.append(dict(r))
    return data


def write_csv(file_name, db, head):
    csv_file = open(f'{file_name}.csv', 'w', newline="")
    writer = csv.writer(csv_file)
    writer.writerow(head)
    for i in db.search(file_name).table:
        writer.writerow(i.values())
    csv_file.close()


def get_head(file_name):
    with open(os.path.join(__location__, f'{file_name}.csv')) as f:
        rows = csv.reader(f)
        head = [i for i in rows]
    return head[0]


def gen_project_id(lead_id):
    _1234 = "".join([random.choice(str(datetime.datetime.now()).split(".")[1]) for i in range(4)])
    _5 = random.randrange(9)
    _67 = "".join([random.choice(lead_id) for i in range(2)])
    return f"{_1234}{_5}{_67}"


# add in code for a Database class
class Database:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None
# add in code for a Table class


class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table

    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def __is_float(self, element):
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def insert(self, new_data):
        self.table.append(new_data)

    def get_row(self, condition):
        row = 0
        for i in self.table:
            if condition(i):
                return row
            else:
                row += 1

    def update(self, row, key, value):
        n = 0
        for i in self.table:
            if row == n:
                i[key] = value
                break
            else:
                n += 1

    def __str__(self):
        return self.table_name + ':' + str(self.table)

# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary

# modify the code in the Table class so that it supports the update operation where an entry's value associated with a key can be updated