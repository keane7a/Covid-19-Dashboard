Release notes Covid-19 Dashboard version 1.0

Table of contents: 
1) INSTALLATION AND RUNNING COVID-19 DASHBOARD
2) DEVELOPERS GUIDE
3) USER GUIDE
4) HELP AND SUPPORT


1) INSTALLATION AND RUNNING COVID-19 DASHBOARD

Installing necessary framework and libraries:
• flask 
• datetime
• newsapi-python
To install the framework and libraries open command prompt and type "pip install 'framework'"
To run the Covid-19 Dashboard, open terminal and run python file main_dashboard_handling.py. 


2) DEVELOPERS GUIDE

General description:
Covid-19 Dashboard is an automated system that help visualise input data streams. 
Covid-19 Dashboard provides information about the COVID infection rates from the Public Health England API and news stories about Covid from a given news API.

File description: 
A comment has been added to each function in the Covid-19 Dashboard for better understanding.
 • config.json
   Stores sensitive information such as API keys and dashboard configurations.
 • covid_data.json
   Stores up-to-date covid data from https://api.coronavirus.data.gov.uk/v1/data? (This file only provides the date, area name, and new cases by specimen date)
 • covid_data_handler.py
   A library of functions for covid data handling functionality such as read data from a file, data processing, and live data access. 
 • covid_news_handling.py
   A library to get information from a news API and updating headlines on the dashboard.
 • Main_dashboard_handling.py
   The main file to run covid-19 dashboard.
 • Nation_2021-10-28.csv
   Stores covid-19 data. (This file only contains areaCode,areaName,areaType,date,cumDailyNsoDeathsByDeathDate,hospitalCases,and newCasesBySpecimenDate)
 • newsAPI_data.json
   Stores up-to-date news provided from the news API
 • READ_ME_COVID19_DASHBOARD.txt
   Defined in the file name
 • sys.log
   logs most events happening in the Covid-19 Dashboard.
 • test_covid_data_handling.py
   Test most of the functions present in covid_data_handling.py
 • test_main_dashboard_handling.py
   Test most of the functions present in main_dashboard_handling.py
 • time_difference.py
   Test most of the functions present in time_difference.py


3) USER GUIDE

General description:
Since the outbreak of COVID-19 the day-to-day routine for many people has been disrupted and keeping up-to-date with the local and national infection rates and news on government guidelines has become a daily challenge.
Covid-19 Dashboard is an automated system that provides information about the COVID infection rates from the Public Health England API and news stories about Covid from a given news API.

Features:
 • Provide up-to-date data about local 7-day infection rate in Exeter, national 7-day infection rate in England, national hospital cases in England, total deaths in England
 • Displays recent news that mentions about 'Covid', 'COVID-19' or 'coronavirus'
 • Schedule updates for covid data and news articles (Note: Update label is the title for the schedule data updates).
 • Displays scheduled updates on top left if the user decided to schedule an update
 • Remove news by double click

4) HELP AND SUPPORT 

For help and support email me at nkn203@exeter.ac.uk





