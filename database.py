import sqlite3


CREATE_TEAMS_TABLE = "CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY, city TEXT, name TEXT, record INTEGER, rings INTEGER, history INTEGER, player TEXT);"

INSERT_TEAM = "INSERT INTO teams (city, name, record, rings, history, player) VALUES (?, ?, ?, ?, ?, ?);"

GET_ALL_TEAMS = "SELECT * FROM teams;"
GET_TEAMS_BY_NAME = "SELECT * FROM teams WHERE name = ?;"
DELETE_TEAM = """
DELETE FROM teams
WHERE name = ?;"""
SORT_BY_RINGS = """
SELECT * FROM teams
ORDER BY rings DESC;"""
SORT_BY_RECORD = """
SELECT * FROM teams
ORDER BY record DESC;"""


def connect():
    return sqlite3.connect("data.db")


def create_tables(connection):
    with connection:
        connection.execute(CREATE_TEAMS_TABLE)


def add_team(connection, city, name, record, rings, history, player):
    with connection:
        connection.execute(INSERT_TEAM, (city, name, record, rings, history, player))


def get_all_teams(connection):
    with connection:
        return connection.execute(GET_ALL_TEAMS).fetchall()


def get_teams_by_name(connection, name):
    with connection:
        return connection.execute(GET_TEAMS_BY_NAME, (name,)).fetchall()


def delete_team(connection, name):
    with connection:
        return connection.execute(DELETE_TEAM, (name, )).fetchone()


def sort_by_rings(connection):
    with connection:
        return connection.execute(SORT_BY_RINGS).fetchall()


def sort_by_record(connection):
    with connection:
        return connection.execute(SORT_BY_RECORD).fetchall()

