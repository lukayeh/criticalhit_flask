import csv, sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Fields
# name,real_name,role,association,accolade,active,attack,defense,health,level


# Import Roster
with open('static/csv/roster.csv','rt') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['name'],i['real_name'],i['role'],i['association'],i['accolade'],i['active'],i['finisher'],i['attack'],i['defense'],i['health'],i['level'],i['wins'],i['losses'],i['img']) for i in dr]

cur.executemany("INSERT INTO roster (name, real_name, role, association, accolade, active, finisher, attack, defense, health, level, wins, losses, img) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)

# Import Titles
with open('static/csv/titles.csv','rt') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['name'],i['type'],i['association'],i['img']) for i in dr]

cur.executemany("INSERT INTO titles (name,type,association,img) VALUES (?, ?, ?, ?);", to_db)

# Import Companies
with open('static/csv/companies.csv','rt') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['name'],i['img']) for i in dr]

cur.executemany("INSERT INTO companies (name,img) VALUES (?, ?);", to_db)


# Import fueds
with open('static/csv/fueds.csv','rt') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['participant_1'],i['participant_2'],i['popularity'],i['status'],i['company']) for i in dr]

cur.executemany("INSERT INTO fueds (participant_1,participant_2,popularity,status,company) VALUES (?, ?, ?, ?, ?);", to_db)


# Import Match types
# with open('static/csv/matchtypes.csv','rt') as fin: # `with` statement available in 2.5+
#     # csv.DictReader uses first line in file for column headings by default
#     dr = csv.DictReader(fin) # comma is default delimiter
#     to_db = [(i['name']) for i in dr]

# cur.executemany("INSERT INTO match_types (name) VALUES (?);", to_db)

connection.commit()
connection.close()