# calculations

import sqlite3
import requests
from datetime import datetime
import matplotlib.pyplot as plt

def find_total_death_avg(dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT CanadaStats.deaths + DailyStats.death FROM CanadaStats JOIN DailyStats
                   ON CanadaStats.date = DailyStats.date
    ''')
    result_list = cursor.fetchall()
    conn.close()
    
    total = 0
    count = 0
    print('RESULT LIST')
    print(result_list)
    for item in result_list:
        #print(item)
        total += item[0]
        count += 1
    total_average = total/count
    return total_average

def find_country_death_avg(dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    cursor.execute('SELECT deaths FROM CanadaStats')
    canada_list = cursor.fetchall()
    canada_total = 0
    canada_count = 0
    for item in canada_list:
        canada_total += item[0]
        canada_count += 1
    canada_avg = canada_total/canada_count

    cursor.execute('SELECT death FROM DailyStats')
    us_list = cursor.fetchall()
    us_total = 0
    us_count = 0
    for item in us_list:
        us_total += item[0]
        us_count += 1
    us_avg = us_total/us_count

    conn.close()

    return {
        'Canada Average Deaths': canada_avg,
        'US Average Deaths': us_avg
    }

def avg_vis(avg_dict, overall_avg):
    avg_list = [avg_dict['Canada Average Deaths'], avg_dict['US Average Deaths'], overall_avg]
    label_list = ['Canada', 'US', 'Combined']
    plt.bar(label_list, avg_list, color='green')
    plt.xlabel('Countries')
    plt.ylabel('Average Deaths')
    plt.title("Average COVID Deaths per Country")
    #Used ChatGPT to help get plot to fully show in the image
    plt.tight_layout()
    plt.savefig('avg_deaths.png')
    plt.show()

overall_avg = find_total_death_avg('final_covid_db.db')
avg_dict = find_country_death_avg('final_covid_db.db')
avg_vis(avg_dict, overall_avg)






