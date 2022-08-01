import sqlalchemy as db

###############################################
#          Define db connection               #
###############################################
def get_connection():
    engine = db.create_engine("sqlite:///database.db")
    connection = engine.connect()

    return engine
