import sqlite3

###############################################
#          Define dict factory                #
###############################################
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
###############################################
#          Define db connection               #
###############################################
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    return conn
