import sqlite3


CREATE_SCORE_TABLE = "CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, name TEXT, score INTEGER);"

INSERT_SCORE = "INSERT INTO scores (name, score) VALUES (?, ?);"

SHOW_ALL_SCORES = "SELECT * FROM scores;"
SORT_BY_SCORES = """
SELECT * FROM scores
ORDER BY score DESC
LIMIT 10;"""


def connect():
    return sqlite3.connect("data.db")


def create_tables(connection):
    with connection:
        connection.execute(CREATE_SCORE_TABLE)


def add_score(connection, name, score):
    with connection:
        connection.execute(INSERT_SCORE, (name, score))

def show_all_scores(connection):
    with connection:
        return connection.execute(SHOW_ALL_SCORES).fetchall()

def sort_by_scores(connection):
    with connection:
        return connection.execute(SORT_BY_SCORES).fetchall()



