import sqlite3
import requests
from datetime import datetime
api_request = "https://disease.sh/v3/covid-19/historical/USA?lastdays=all"
START_DATE = 20210211

def make_table(dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apistats (
                   date INTEGER PRIMARY KEY,
                   cases INTEGER,
                   deaths INTEGER,
                   recovered INTEGER,
                   active INTEGER
                   )
        CREATE TABLE IF NOT EXISTS CanadaStats (
            date INTEGER PRIMARY KEY,
            cases INTEGER,
            deaths INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CanadaCases (
            date INTEGER PRIMARY KEY,
            recovered INTEGER,
            active INTEGER
        )
    ''')

    conn.commit()
    conn.close()

    