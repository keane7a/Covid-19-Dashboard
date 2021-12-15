import json
from covid_data_handler import covid_API_request, process_covid_csv_data, parse_csv_data
from covid_news_handling import news_API_request
from flask import Flask, render_template, request
import json
from datetime import datetime
from time_diffrence import time_difference_in_seconds
import logging
import sched
import time
with open('config.json') as config_file: #import configuration file
    config_data = json.load(config_file)
logging.basicConfig(filename='sys.log', level=logging.DEBUG)

schedule_update_data = [] # A list of pending updates to be displayed at schedule update section.
s = sched.scheduler(time.time, time.sleep)
def input_update(title, content):
    """This function create a list of updates for dashboard display."""
    schedule_update_data.append({"title": title, "content": content})
    logging.info('Input update dashboard display has been triggered at ' + str(datetime.now()))


def remove_update(title,content, update_time, data):
    """This function remove a list of update from dashboard display."""
    def remove_element(title, content, data):
        """Removes an update from the list."""
        data.remove({"title": title, "content": content})
        logging.info(f'{title} has been updated at ' + str(datetime.now()))
    s.enter(update_time,3,remove_element, kwargs={"title": title, "content": content, "data": data})


def formatted_news_API_data ():
    """The function removes unimportant keys in newsAPI_data.json file and returning 
    the necessary format for news_articles"""
    with open(config_data["news_API_file"], 'r') as read:
        data = json.load(read)
    keys_to_remove = ["source", "author", "url", "urlToImage", "publishedAt", "content"]
    for i in data['articles']:
        for key in keys_to_remove: 
            i.pop(key)
        i["content"] = i.pop("description")
    logging.info('News API data has successfully been formatted at '+ str(datetime.now()))
    return data['articles']
temporary_news_data = formatted_news_API_data()
    
def update_covid_data(update_time, covid_update, repeat_update, input_update_title):
    """This function updates the covid data on the dashboard"""
    if covid_update == 'covid-data':
        if len(update_time.split(':')) != 2:
            #if there is no time inputted it will return current time and update instantly
            update_time = str(datetime.now().strftime("%H:%M"))
            print(update_time)
        logging.info('covid is being updated at ' + str(datetime.now()))
        s.enter(time_difference_in_seconds(update_time),1, covid_API_request)
        input_update(input_update_title, "update schedule: "+str(update_time))
        remove_update(input_update_title, "update schedule: "+str(update_time), time_difference_in_seconds(update_time), schedule_update_data)
        
        
        if repeat_update == 'repeat':
            logging.info('covid data is being updated again at ' + str(datetime.now()))
            input_update(f"repeat {input_update_title}", "update schedule: "+str(update_time))
            s.enter(time_difference_in_seconds(update_time)+86400,1, covid_API_request)
            remove_update(f"repeat {input_update_title}", "update schedule: "+str(update_time), time_difference_in_seconds(update_time)+86400, schedule_update_data)
           
def update_news(update_time, news_article_update,repeat_update, input_update_title):
    """This function update news on the dashboard"""
    if news_article_update == 'news':
        if len(update_time.split(':')) != 2:
            #if there is no time inputted it will return current time and update instantly
            update_time = str(datetime.now().strftime("%H:%M"))
        logging.info('news is being updated at ' + str(datetime.now()))
        input_update(input_update_title, "update schedule: "+str(update_time))
        s.enter(time_difference_in_seconds(update_time),1,news_API_request) # get request from news API
        remove_update(input_update_title, "update schedule: "+str(update_time), time_difference_in_seconds(update_time), schedule_update_data)
        
        
        if repeat_update == 'repeat':
            input_update(f"repeat {input_update_title}", "update schedule: "+str(update_time))
            s.enter(time_difference_in_seconds(update_time)+86400,2, news_API_request)
            remove_update(f"repeat {input_update_title}", "update schedule: "+str(update_time), time_difference_in_seconds(update_time)+86400, schedule_update_data)


def remove_dashboard_news(notif):
    """removes news from dashboard. you can set to remove news permanently or temporarily through config.json"""
    if type(notif) == str:
        index = 0
        if config_data["remove_news"] == "permanent": # if remove news is assigned to be permanent in config.json
            with open(config_data["news_API_file"], 'r') as read:
                news = json.load(read)

            for i in news["articles"]:
                if notif == i["title"]:
                    news["articles"].pop(index)
                index += 1
            with open(config_data["news_API_file"], 'w') as write:
                data = json.dump(news, write, indent=4)
            logging.info('news has been removed permanently at ' + str(datetime.now()))   
        elif config_data["remove_news"] == "temporary": # if remove news is assigned to be temprary in config.json
            for i in temporary_news_data:
                if notif == i["title"]:
                    temporary_news_data.pop(index)
                index += 1
            logging.info('news has been removed temporarily at ' + str(datetime.now()))
        else: 
            logging.error('remove news has not been setup properly through config.json. Please check the spelling and comment. In the meantime news has been removed temporarily' + str(datetime.now()))
            for i in temporary_news_data:
                if notif == i["title"]:
                    temporary_news_data.pop(index)
                index += 1


def local_7day_infections(data="covid_data.json"):
    last7days_cases = 0
    with open(data) as read:
        covid_data = json.load(read)
    for i in range(0,7):  
        last7days_cases += int(covid_data["data"][i]["newCasesBySpecimenDate"])
    logging.info('local 7 day covid infections has been obtained through covid_data.json')
    return last7days_cases


app = Flask(__name__)
@app.route('/index')
def dashboard():
    s.run(blocking=False)
    if config_data["remove_news"] == "permanent":
        news_data = formatted_news_API_data()
    elif config_data["remove_news"] == "temporary":
        news_data = temporary_news_data
    else: 
        news_data = temporary_news_data
    covid_API_data = local_7day_infections()
    last7days_cases, current_hospital_cases, total_deaths = list(process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv')))
    update_time = request.args.get('update')
    input_update_title = request.args.get('two')
    repeat_update = request.args.get('repeat') 
    covid_data_update = request.args.get('covid-data')
    update_news_article = request.args.get('news')
    notif = request.args.get('notif')
    update_covid_data(update_time, covid_data_update, repeat_update, input_update_title)
    update_news(update_time, update_news_article, repeat_update, input_update_title)
    remove_dashboard_news(notif)
    return render_template('index.html', title=config_data["dashboard_title"], 
                           location=config_data["dashboard_location"],
                           local_7day_infections=covid_API_data,
                           nation_location = config_data["dashboard_nation_location"],
                           national_7day_infections= last7days_cases,
                           hospital_cases = current_hospital_cases,
                           deaths_total = total_deaths,
                           news_articles = news_data,
                           updates = schedule_update_data,
                           image = config_data["dashboard_image"]
                           )


if __name__ == '__main__':
    app.run(debug=True)