# calculations

import sqlite3
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

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
    #print('RESULT LIST')
    #print(result_list)
    for item in result_list:
        #print(item)
        total += item[0]
        count += 1
    total_average = total/count

    print(f"total avg {total_average}")
    return total_average

def find_country_death_avg(dbpath, txt_file, overall_avg):
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

    #WRITE CANADA_AVG AND US_AVG TO TXT

    with open(txt_file, "w") as file:
        file.write(f"Canada average deaths: {canada_avg}\n")
        file.write(f"US average deaths: {us_avg}\n")
        file.write(f"Combined average deaths (Canada + US): {overall_avg}\n")

    print(f"Canada avg: {canada_avg}")
    print(f"US avg: {us_avg}")

    return {
        'Canada Average COVID Deaths': canada_avg,
        'US Average COVID Deaths': us_avg
    }

def avg_vis(avg_dict, overall_avg):
    avg_list = [avg_dict['Canada Average COVID Deaths'], avg_dict['US Average COVID Deaths'], overall_avg]
    label_list = ['Canada', 'US', 'Combined']
    plt.bar(label_list, avg_list, color='purple')
    plt.xlabel('Countries')
    plt.ylabel('Average COVID Deaths')
    plt.title("Average COVID Deaths per Country")
    #USed ChatGPT because plot was using scientific notation for y-axis
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.ticklabel_format(style='plain', axis='y')

    plt.tight_layout()
    plt.savefig('avg_deaths.png')
    plt.show()


def death_over_time(dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute('SELECT deaths FROM CanadaStats')
    canada_list = cursor.fetchall()

    cursor.execute('SELECT death FROM DailyStats')
    us_list = cursor.fetchall()

    cursor.execute('SELECT date from CanadaStats')
    date_list = cursor.fetchall()

    plt.plot(date_list, us_list, label='US COVID Deaths', color='blue')
    plt.plot(date_list, canada_list, label='Canada COVID Deaths', color='green')
    plt.xlabel('Date')
    plt.ylabel('Total Deaths')
    plt.title('COVID Deaths Over Time in Canada and the US')
    plt.legend()
    #Used ChatGPT to not use scientific notation
    plt.gca().xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.ticklabel_format(style='plain', axis='x')
    plt.tight_layout()
    plt.savefig('deaths_over_time.png')
    plt.show()


    pass    

def cases_over_time(dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute('SELECT cases FROM CanadaStats')
    canada_cases = cursor.fetchall()

    cursor.execute('SELECT positive FROM DailyStats')
    us_cases = cursor.fetchall()

    cursor.execute('SELECT date FROM CanadaStats')
    dates = cursor.fetchall()

    plt.plot(dates, us_cases, label='US COVID Cases', color='blue')
    plt.plot(dates, canada_cases, label='Canada COVID Cases', color='green')
    plt.xlabel('Date')
    plt.ylabel('Total Cases')
    plt.title('COVID Cases Over Time in Canada and the US')
    plt.legend()
    #Used ChatGPT to not use scientific notation
    plt.gca().xaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.ticklabel_format(style='plain', axis='x')

    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
    plt.ticklabel_format(style='plain', axis='y')
    plt.tight_layout()
    plt.savefig('cases_over_time.png')
    plt.show()








overall_avg = find_total_death_avg('final_covid_db.db', 'calculations_output.txt')
avg_dict = find_country_death_avg('final_covid_db.db', 'calculations_output.txt', overall_avg)
avg_vis(avg_dict, overall_avg)
death_over_time('final_covid_db.db')
cases_over_time('final_covid_db.db')







