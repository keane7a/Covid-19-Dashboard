from csv import reader
import sched
import time
import json
from requests import get
import logging
from datetime import datetime
with open('config.json') as config_file: 
    config_data = json.load(config_file)


def parse_csv_data (csv_filename):
    """Takes an argument called csv filename and returns
    a list of strings for the rows in the file. """
    
    with open (csv_filename, 'r' ) as r:
        csv_data = list(reader(r))
    return csv_data

def process_covid_csv_data(list_data):
    """The function takes a list of data and returns three variables, the number of cases in the last 7 days, the current number
    of hospital cases and the cumulative number of deaths"""
    #7 days cases
    a = 1
    last7days_cases = 0
    while list_data[a][6] =='':
        a+=1
    for i in range(1,8):  
        last7days_cases += int(list_data[a+i][6])
    
    # current hospital cases
    current_hospital_cases = int(list_data[1][5])

    #total deaths
    b=1
    total_deaths = 0
    while list_data[b][4] == '':
        b+=1
    total_deaths = int(list_data[b][4])
    
    return last7days_cases, current_hospital_cases, total_deaths

def covid_API_request(location = "Exeter", location_type = "ltla"): 
    """The function returns up-to-date Covid data as a dictionary."""
    def get_data(filters):
        endpoint = (
        'https://api.coronavirus.data.gov.uk/v1/data?'
        f'filters={filters}'
        'structure={"date":"date","areaName":"areaName","newCasesBySpecimenDate":"newCasesBySpecimenDate"}'
    )
        response = get(endpoint, timeout=10)
        if response.status_code >= 400:
            raise RuntimeError(f'Request failed: { response.text }')
        up_to_date_covid_data = response.json()
        with open ("covid_data.json", 'w') as write: 
            json.dump(up_to_date_covid_data, write, indent=4)
        return response.json()
    
    filters =f"areaType={location_type};areaName={location}&"
    logging.info('covid data has been updated at ' + str(datetime.now()))
    return get_data(filters)


def schedule_covid_updates(update_interval, update_name):
    """schedule updates to the covid data at the given time interval.
    update_interval = time in seconds
    update_name = a function name
    """
    s = sched.scheduler(time.time, time.sleep)
    s.enter(update_interval,1,update_name)
    s.run()
