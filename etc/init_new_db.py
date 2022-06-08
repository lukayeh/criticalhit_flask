import csv, sqlite3

connection = sqlite3.connect('../new_database.db')

with open('schema_new.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# Import Roster
with open('../static/csv/roster.csv','rt') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['name'],i['real_name'],i['role'],i['association'],i['accolade'],i['active'],i['finisher'],i['attack'],i['defense'],i['health'],i['level'],i['wins'],i['losses'],i['img']) for i in dr]

cur.executemany("INSERT INTO roster (name, real_name, role, association, accolade, active, finisher, attack, defense, health, level, wins, losses, img) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)

# Import Titles
with open('../static/csv/titles.csv','rt') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['name'],i['type'],i['association'],i['img']) for i in dr]

cur.executemany("INSERT INTO titles (name,type,association,img) VALUES (?, ?, ?, ?);", to_db)


connection.commit()
connection.close()