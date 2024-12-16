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

def get_api_data():
    data = requests.get(api_request)
    json_data = data.json()
    timeline = json_data.get('timeline')
    cases = timeline.get('cases')
    deaths = timeline.get('deaths')
    recovered = timeline.get('recovered')
    data_list = []
    for date, case_num in cases.items():
        #used chatgpt to fix date formatting to match the other api
        reformatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y%m%d")
        reformatted_date = int(reformatted_date)
        if reformatted_date >= START_DATE:
            data_list.append({
                'date': reformatted_date,
                'cases': case_num,
                'deaths': deaths.get(date),
                'recovered': recovered.get(date),
                'active': case_num - recovered.get(date) - deaths.get(date)    
            })
    return data_list