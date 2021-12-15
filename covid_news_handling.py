from os import remove
from newsapi import NewsApiClient
from newsapi import NewsApiClient
from requests.api import delete
from covid_data_handler import covid_API_request, schedule_covid_updates
import requests
import json
import logging
from datetime import datetime
with open('config.json') as config_file: #import configuration file
    config_data = json.load(config_file)
newsapi = NewsApiClient(api_key=config_data["api_key"])

def news_API_request(covid_terms = config_data["covid_terms"]):
    """Access current news data from News API (https://newsapi.org/)"""
    url = ("https://newsapi.org/v2/top-headlines?q="+covid_terms+"&apiKey=f3d1af44de0c432eae28fd2e4a01800e")
    response = requests.get(url).json()
    with open(config_data["news_API_file"], 'r') as read:
        news = json.load(read)
    
    # compare if there is any same news. If there is remove the duplicate news
    for i in news["articles"]:
        index = 0
        for x in response["articles"]:
            if i["title"] == x["title"]:
                response["articles"].pop(index)
            index += 1
    # insert new articles
    for i in response["articles"]:
        news["articles"].insert(0, i) 
    
    # limits the news assined in config.json "number_of_news_stored". 
    del news["articles"][config_data["number_of_news_stored"]:]
    
    with open(config_data["news_API_file"], 'w') as write: 
        json.dump(news, write, indent=4)
    logging.info('news has been updated at ' + str(datetime.now()))
    return news


def update_news(update_time): 
    """updates news at a given time"""
    updated_news = schedule_covid_updates(update_time, news_API_request)
    return updated_news



